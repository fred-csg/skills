# Esquema do projeto

## Projeto

Campos mínimos:

- `name`, `launch_type`, `owner`, `target_date`, `timezone`, `status`;
- `product`, `audience`, `scope`, `constraints`;
- `created_at`, `updated_at`, `version`.

## Tarefas

Cada tarefa contém:

- `id`: estável e único;
- `name`, `track`, `required`;
- `status`: `not_started`, `ready`, `in_progress`, `review`, `approved`, `blocked`, `paused`, `cancelled` ou `not_applicable`;
- `priority`: 1 crítica, 2 alta, 3 normal, 4 baixa;
- `depends_on`: IDs;
- `skill`: skill, `manual` ou `external`;
- `owner`, `approver`, `due_date`;
- `inputs`, `outputs`;
- `checkpoint`: `pending`, `approved`, `changes_requested`, `paused` ou `not_applicable`;
- `blockers`, `risks`, `next_action`, `notes`.

Dependências são satisfeitas por `approved` ou `not_applicable`. Uma tarefa cancelada não satisfaz dependência sem decisão explícita de replanejamento.

## Decisões

Registrar `id`, data, título, contexto, decisão, alternativas, impacto, autor e tarefas afetadas. Não sobrescrever decisão antiga; criar uma nova que a substitua.

## Riscos

Registrar probabilidade e impacto de 1 a 5, exposição, gatilho, mitigação, contingência, dono, status e tarefas afetadas.

## Alegações

Registrar texto, fonte, status (`verified`, `pending`, `rejected`), canais, limites e responsável. Nenhuma aprovação de copy torna uma alegação verdadeira sem fonte.

## Métricas

Registrar nome, definição, numerador, denominador, fonte, frequência, owner, baseline e meta quando aprovada. Não misturar definições entre ferramentas.

## Marcos

Registrar data, critério de conclusão, tarefas associadas, owner e status. Um marco não é concluído por calendário; exige critério atendido.
