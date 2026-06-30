"""
projeto: analista-freudiano
autor: carlos.gluck
modulo: scripts/registrar_sessao.py
spec: SKILL.md
status: rascunho
versao: 1.0.0
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Forçar UTF-8 no stdout/stderr (Windows usa cp1252 por padrão)
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


# Caminho da raiz da skill (pasta pai de scripts/)
_SKILL_ROOT = Path(__file__).resolve().parent.parent
_PRONTUARIO_DIR = _SKILL_ROOT / "prontuario"
PRONTUARIO_FILE = "prontuario.md"
ESTADO_FILE = ".sessao_estado.json"


def _caminho_prontuario_dir() -> Path:
    """Retorna o caminho da pasta de prontuário, criando se necessário."""
    _PRONTUARIO_DIR.mkdir(parents=True, exist_ok=True)
    return _PRONTUARIO_DIR


def _caminho_prontuario() -> Path:
    """Retorna o caminho do arquivo de prontuário."""
    return _caminho_prontuario_dir() / PRONTUARIO_FILE


def _caminho_estado() -> Path:
    """Retorna o caminho do arquivo de estado da sessão ativa."""
    return _caminho_prontuario_dir() / ESTADO_FILE


def _agora() -> datetime:
    """Retorna data/hora atual."""
    return datetime.now()


def _formatar_data(dt: datetime) -> str:
    """Formata data no padrão DD/MM/AAAA."""
    return dt.strftime("%d/%m/%Y")


def _formatar_hora(dt: datetime) -> str:
    """Formata hora no padrão HH:MM."""
    return dt.strftime("%H:%M")


def _contar_sessoes() -> int:
    """Conta quantas sessões existem no prontuário."""
    prontuario = _caminho_prontuario()
    if not prontuario.exists():
        return 0
    conteudo = prontuario.read_text(encoding="utf-8")
    return conteudo.count("## Sessão #")


def _carregar_estado() -> dict | None:
    """Carrega o estado da sessão ativa, se existir."""
    estado = _caminho_estado()
    if not estado.exists():
        return None
    return json.loads(estado.read_text(encoding="utf-8"))


def _salvar_estado(dados: dict) -> None:
    """Salva o estado da sessão ativa."""
    estado = _caminho_estado()
    estado.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")


def _remover_estado() -> None:
    """Remove o arquivo de estado da sessão."""
    estado = _caminho_estado()
    if estado.exists():
        estado.unlink()


def iniciar() -> None:
    """Inicia uma nova sessão: registra data/hora e cria cabeçalho no prontuário."""
    estado_atual = _carregar_estado()
    if estado_atual:
        print(
            f"⚠️  Já existe uma sessão ativa (Sessão #{estado_atual['numero']}, "
            f"iniciada em {estado_atual['inicio']}). "
            f"Encerre-a antes de iniciar uma nova.",
            file=sys.stderr,
        )
        sys.exit(1)

    agora = _agora()
    numero = _contar_sessoes() + 1
    prontuario = _caminho_prontuario()

    # Criar cabeçalho do prontuário se for a primeira sessão
    if not prontuario.exists() or prontuario.stat().st_size == 0:
        prontuario.write_text(
            "# Prontuário de Atendimento Psicanalítico\n\n",
            encoding="utf-8",
        )

    # Adicionar cabeçalho da sessão
    with open(prontuario, "a", encoding="utf-8") as f:
        f.write(f"---\n\n")
        f.write(f"## Sessão #{numero} — {_formatar_data(agora)}\n\n")
        f.write(f"**Início:** {_formatar_hora(agora)}\n\n")
        f.write(f"### Transcrição\n\n")

    # Salvar estado
    _salvar_estado({
        "numero": numero,
        "inicio": agora.isoformat(),
        "inicio_formatado": _formatar_hora(agora),
        "data": _formatar_data(agora),
    })

    print(f"✅ Sessão #{numero} iniciada em {_formatar_data(agora)} às {_formatar_hora(agora)}")
    print(f"📄 Prontuário: {prontuario}")


def registrar(papel: str, texto: str) -> None:
    """Registra uma troca no prontuário da sessão ativa."""
    estado = _carregar_estado()
    if not estado:
        print("⚠️  Nenhuma sessão ativa. Execute com --acao iniciar primeiro.", file=sys.stderr)
        sys.exit(1)

    prontuario = _caminho_prontuario()
    agora = _agora()

    rotulo = "Analisando" if papel == "analisando" else "Analista"

    with open(prontuario, "a", encoding="utf-8") as f:
        f.write(f"**{rotulo}** ({_formatar_hora(agora)}): {texto}\n\n")

    print(f"📝 Registrado: {rotulo} às {_formatar_hora(agora)}")


def verificar_tempo() -> None:
    """Verifica o tempo decorrido desde o início da sessão."""
    estado = _carregar_estado()
    if not estado:
        print("⚠️  Nenhuma sessão ativa.", file=sys.stderr)
        sys.exit(1)

    inicio = datetime.fromisoformat(estado["inicio"])
    agora = _agora()
    decorrido = agora - inicio
    minutos = int(decorrido.total_seconds() / 60)

    print(f"⏱️  Tempo decorrido: {minutos} minutos")

    if minutos >= 50:
        print("🔴 TEMPO ESGOTADO — Encerre a sessão agora.")
    elif minutos >= 40:
        print("🟡 JANELA DE ENCERRAMENTO — Comece a encaminhar o fechamento.")
    elif minutos >= 30:
        print("🟢 Sessão em andamento — Últimos 10-20 minutos.")
    else:
        print(f"🟢 Sessão em andamento — Restam aproximadamente {40 - minutos} minutos.")


def encerrar(sintese: str = "") -> None:
    """Encerra a sessão ativa, registra término e duração."""
    estado = _carregar_estado()
    if not estado:
        print("⚠️  Nenhuma sessão ativa para encerrar.", file=sys.stderr)
        sys.exit(1)

    inicio = datetime.fromisoformat(estado["inicio"])
    agora = _agora()
    duracao = agora - inicio
    minutos = int(duracao.total_seconds() / 60)

    prontuario = _caminho_prontuario()

    with open(prontuario, "a", encoding="utf-8") as f:
        f.write(f"**Término:** {_formatar_hora(agora)}\n")
        f.write(f"**Duração:** {minutos}min\n\n")
        if sintese:
            f.write(f"### Síntese Clínica\n\n{sintese}\n\n")

    _remover_estado()

    print(f"✅ Sessão #{estado['numero']} encerrada às {_formatar_hora(agora)}")
    print(f"⏱️  Duração total: {minutos} minutos")
    print(f"📄 Prontuário atualizado: {prontuario}")


def main() -> None:
    """Ponto de entrada do script de registro de sessão."""
    parser = argparse.ArgumentParser(
        description="Gerenciador de sessões psicanalíticas — registro em prontuário"
    )
    parser.add_argument(
        "--acao",
        required=True,
        choices=["iniciar", "registrar", "verificar_tempo", "encerrar"],
        help="Ação a executar",
    )
    parser.add_argument(
        "--papel",
        choices=["analisando", "analista"],
        help="Quem está falando (para ação 'registrar')",
    )
    parser.add_argument(
        "--texto",
        help="Conteúdo da fala (para ação 'registrar') ou síntese (para 'encerrar')",
    )

    args = parser.parse_args()

    if args.acao == "iniciar":
        iniciar()
    elif args.acao == "registrar":
        if not args.papel or not args.texto:
            parser.error("--papel e --texto são obrigatórios para a ação 'registrar'")
        registrar(args.papel, args.texto)
    elif args.acao == "verificar_tempo":
        verificar_tempo()
    elif args.acao == "encerrar":
        encerrar(args.texto or "")


if __name__ == "__main__":
    main()
