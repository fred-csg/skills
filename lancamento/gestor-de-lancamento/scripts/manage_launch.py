#!/usr/bin/env python3
"""Validate a launch project manifest and report actionable status."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import date
from pathlib import Path


STATUSES = {"not_started", "ready", "in_progress", "review", "approved", "blocked", "paused", "cancelled", "not_applicable"}
CHECKPOINTS = {"pending", "approved", "changes_requested", "paused", "not_applicable"}
DONE = {"approved", "not_applicable"}
PROJECT_REQUIRED = {"name", "launch_type", "owner", "target_date", "timezone", "status", "version"}
TASK_REQUIRED = {"id", "name", "track", "required", "status", "priority", "depends_on", "skill", "owner", "approver", "due_date", "inputs", "outputs", "checkpoint", "blockers", "risks", "next_action"}


def parse_date(raw: str, label: str, errors: list[str]) -> date | None:
    try:
        return date.fromisoformat(raw)
    except (TypeError, ValueError):
        errors.append(f"{label}: expected YYYY-MM-DD, got {raw!r}")
        return None


def find_cycle(tasks: dict[str, dict]) -> list[str] | None:
    visiting: set[str] = set()
    visited: set[str] = set()
    trail: list[str] = []

    def visit(task_id: str) -> list[str] | None:
        if task_id in visiting:
            start = trail.index(task_id)
            return trail[start:] + [task_id]
        if task_id in visited:
            return None
        visiting.add(task_id)
        trail.append(task_id)
        for dep in tasks[task_id].get("depends_on", []):
            if dep in tasks:
                cycle = visit(dep)
                if cycle:
                    return cycle
        trail.pop()
        visiting.remove(task_id)
        visited.add(task_id)
        return None

    for task_id in tasks:
        cycle = visit(task_id)
        if cycle:
            return cycle
    return None


def validate(data: dict) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if not isinstance(data, dict):
        return ["root must be an object"], warnings
    project = data.get("project")
    if not isinstance(project, dict):
        errors.append("project must be an object")
    else:
        for field in sorted(PROJECT_REQUIRED - set(project)):
            errors.append(f"project missing field: {field}")
        if "target_date" in project:
            parse_date(project["target_date"], "project.target_date", errors)
    raw_tasks = data.get("tasks")
    if not isinstance(raw_tasks, list) or not raw_tasks:
        errors.append("tasks must be a non-empty array")
        return errors, warnings
    ids = [task.get("id") for task in raw_tasks if isinstance(task, dict)]
    for task_id, count in Counter(ids).items():
        if task_id is not None and count > 1:
            errors.append(f"duplicate task id: {task_id}")
    tasks = {task["id"]: task for task in raw_tasks if isinstance(task, dict) and isinstance(task.get("id"), str)}
    for index, task in enumerate(raw_tasks):
        label = task.get("id", f"tasks[{index}]") if isinstance(task, dict) else f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label}: task must be an object")
            continue
        for field in sorted(TASK_REQUIRED - set(task)):
            errors.append(f"{label}: missing field {field}")
        status = task.get("status")
        checkpoint = task.get("checkpoint")
        if status not in STATUSES:
            errors.append(f"{label}: invalid status {status!r}")
        if checkpoint not in CHECKPOINTS:
            errors.append(f"{label}: invalid checkpoint {checkpoint!r}")
        if not isinstance(task.get("required"), bool):
            errors.append(f"{label}: required must be boolean")
        priority = task.get("priority")
        if not isinstance(priority, int) or not 1 <= priority <= 4:
            errors.append(f"{label}: priority must be an integer from 1 to 4")
        deps = task.get("depends_on", [])
        if not isinstance(deps, list):
            errors.append(f"{label}: depends_on must be an array")
            deps = []
        for dep in deps:
            if dep == task.get("id"):
                errors.append(f"{label}: cannot depend on itself")
            elif dep not in tasks:
                errors.append(f"{label}: unknown dependency {dep!r}")
        if "due_date" in task:
            parse_date(task["due_date"], f"{label}.due_date", errors)
        unresolved = [dep for dep in deps if dep in tasks and tasks[dep].get("status") not in DONE]
        if status in {"ready", "in_progress", "review", "approved"} and unresolved:
            errors.append(f"{label}: status {status} with unresolved dependencies: {', '.join(unresolved)}")
        if status == "approved":
            if checkpoint != "approved":
                errors.append(f"{label}: approved task requires approved checkpoint")
            if not task.get("outputs"):
                errors.append(f"{label}: approved task requires at least one output")
            if not str(task.get("approver", "")).strip() or task.get("approver") == "a definir":
                errors.append(f"{label}: approved task requires a named approver")
        if status == "blocked" and not task.get("blockers"):
            errors.append(f"{label}: blocked task requires blockers")
        if status == "not_applicable" and checkpoint not in {"not_applicable", "approved"}:
            warnings.append(f"{label}: not_applicable task should use not_applicable checkpoint")
        if task.get("required") and status == "cancelled":
            warnings.append(f"{label}: required task is cancelled; replan its dependents")
        if status in {"ready", "in_progress"} and (not str(task.get("owner", "")).strip() or task.get("owner") == "a definir"):
            warnings.append(f"{label}: active task has no named owner")
    cycle = find_cycle(tasks)
    if cycle:
        errors.append("dependency cycle: " + " -> ".join(cycle))
    return errors, warnings


def status_report(data: dict) -> str:
    tasks = {task["id"]: task for task in data["tasks"]}
    today = date.today()
    counts = Counter(task["status"] for task in tasks.values())
    ready = []
    blocked = []
    overdue = []
    for task in tasks.values():
        deps_done = all(tasks[dep]["status"] in DONE for dep in task["depends_on"])
        if task["status"] in {"ready"} or (task["status"] == "not_started" and deps_done):
            if task.get("required", True):
                ready.append(task)
        if task["status"] == "blocked":
            blocked.append(task)
        due = date.fromisoformat(task["due_date"])
        if due < today and task["status"] not in DONE | {"cancelled"}:
            overdue.append(task)
    ready.sort(key=lambda task: (task["priority"], task["due_date"], task["id"]))
    lines = [
        f"Project: {data['project']['name']}",
        f"Target: {data['project']['target_date']} ({data['project']['timezone']})",
        "Status counts: " + ", ".join(f"{key}={counts[key]}" for key in sorted(counts)),
        f"Ready candidates: {len(ready)}",
    ]
    for task in ready[:3]:
        lines.append(f"  - {task['id']} [{task['skill']}]: {task['name']} — {task['next_action']}")
    lines.append(f"Blocked: {len(blocked)}")
    for task in blocked:
        lines.append(f"  - {task['id']}: {'; '.join(task['blockers'])}")
    lines.append(f"Overdue: {len(overdue)}")
    for task in sorted(overdue, key=lambda item: item["due_date"]):
        lines.append(f"  - {task['id']}: due {task['due_date']} ({task['status']})")
    return "\n".join(lines)


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and inspect a launch project manifest.")
    parser.add_argument("command", choices=("validate", "status"))
    parser.add_argument("project_file", type=Path)
    args = parser.parse_args()
    try:
        data = load(args.project_file)
    except (OSError, json.JSONDecodeError) as exc:
        parser.error(str(exc))
    errors, warnings = validate(data)
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}", file=sys.stderr)
    if errors:
        return 1
    if args.command == "validate":
        print("Project manifest is valid.")
    else:
        print(status_report(data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
