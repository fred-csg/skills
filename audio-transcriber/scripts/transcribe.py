import sys
import os
import torch
from faster_whisper import WhisperModel

def formatar_tempo(segundos: float) -> str:
    """Formata um valor de segundos em string no padrao SRT (HH:MM:SS,mmm)."""
    horas = int(segundos // 3600)
    minutos = int((segundos % 3600) // 60)
    segs = int(segundos % 60)
    milisegundos = int((segundos - int(segundos)) * 1000)
    return f"{horas:02d}:{minutos:02d}:{segs:02d},{milisegundos:03d}"

def principal() -> None:
    """Funcao principal para executar a transcricao a partir da linha de comando."""
    if len(sys.argv) < 3:
        print("Erro: Argumentos insuficientes. Uso: python transcribe.py <caminho_audio> <caminho_srt_saida>")
        sys.exit(1)
        
    caminho_audio = sys.argv[1]
    caminho_srt = sys.argv[2]
    
    if not os.path.exists(caminho_audio):
        print(f"Erro: Arquivo de audio nao encontrado: {caminho_audio}")
        sys.exit(1)
        
    # Configuracao do modelo e dispositivo
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    print(f"Carregando modelo Whisper (dispositivo: {device}, compute_type: {compute_type})...")
    try:
        model = WhisperModel("base", device=device, compute_type=compute_type)
    except Exception as e:
        if device == "cuda":
            print(f"Aviso: Falha ao carregar com CUDA ({e}). Tentando CPU...")
            device = "cpu"
            compute_type = "int8"
            model = WhisperModel("base", device=device, compute_type=compute_type)
        else:
            raise e
            
    print("Iniciando transcricao...")
    segments, info = model.transcribe(caminho_audio, beam_size=5)
    
    print(f"Idioma detectado: {info.language} (probabilidade: {info.language_probability:.2f})")
    
    # Gravacao do arquivo SRT
    with open(caminho_srt, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            inicio = formatar_tempo(segment.start)
            fim = formatar_tempo(segment.end)
            texto = segment.text.strip()
            
            f.write(f"{i}\n")
            f.write(f"{inicio} --> {fim}\n")
            f.write(f"{texto}\n\n")
            
    print(f"Transcricao concluida com sucesso! SRT salvo em: {caminho_srt}")

if __name__ == "__main__":
    principal()
