"""
Exemplo de uso da skill text-to-speech (ElevenLabs)
ref: .agent/skills/text-to-speech/SKILL.md
"""

import os
import re
from elevenlabs import ElevenLabs, VoiceSettings

# Le a API key diretamente do .env (compativel com nomes de variavel com hifen)
def _ler_api_key(env_path: str = ".env") -> str:
    with open(env_path) as f:
        for linha in f:
            match = re.match(r'^\s*[\w\-]+\s*=\s*["\']?([^"\'#\n]+)["\']?\s*$', linha)
            if match:
                return match.group(1).strip()
    raise ValueError("API key nao encontrada no arquivo .env")

api_key = _ler_api_key()
client = ElevenLabs(api_key=api_key)


texto = (
    "Olá! Eu sou uma demonstração da skill de conversão de texto em fala. "
    "Posso gerar áudio natural em mais de 70 idiomas usando inteligência artificial."
)

audio = client.text_to_speech.convert(
    text=texto,
    voice_id="pieg5i1qSp1QH3RuGeEp",       # FACCI
    model_id="eleven_multilingual_v2",
    language_code="pt",
    voice_settings=VoiceSettings(
        stability=0.5,
        similarity_boost=0.75,
        style=0.4,
        speed=1.0,
        use_speaker_boost=True,
    ),
)

output_path = "output_demo.mp3"
with open(output_path, "wb") as f:
    for chunk in audio:
        f.write(chunk)

print(f"Audio gerado: {output_path}")
print(f"Texto: {texto}")
