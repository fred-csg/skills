import argparse
import os
import sys
import time
from faster_whisper import WhisperModel

def format_timestamp(seconds: float) -> str:
    """Formata os segundos num timestamp no formato do SRT (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def transcribe_audio(input_file: str, output_file: str, device: str, model_size: str):
    print(f"[INFO] Iniciando carregamento do modelo Whisper ({model_size}) no dispositivo '{device}'...")
    
    # Parâmetros de otimização dependendo do hardware
    compute_type = "float16" if device == "cuda" else "int8"
    
    try:
        model = WhisperModel(model_size, device=device, compute_type=compute_type)
        print("[INFO] Modelo carregado com sucesso.")
    except Exception as e:
        print(f"[ERRO] Falha ao carregar o modelo. Detalhes: {e}")
        sys.exit(1)
        
    print(f"[INFO] Transcrevendo o arquivo: {input_file}")
    
    # vad_filter=True é essencial para áudios longos: remove os silêncios primeiro, acelerando absurdamente.
    try:
        segments, info = model.transcribe(input_file, beam_size=5, vad_filter=True)
    except Exception as e:
        print(f"[ERRO] Falha ao iniciar a transcrição. (ffmpeg instalado e acessível?). Detalhes: {e}")
        sys.exit(1)

    print(f"[INFO] Áudio detectado no idioma '{info.language}' com probabilidade de {info.language_probability:.2f}")
    print(f"[INFO] Duração estimada do áudio: {info.duration:.2f} segundos.")
    print(f"[INFO] O arquivo .srt será gravado de forma incremental em: {output_file}\n")
    
    start_time = time.time()
    
    # Abrir arquivo de saída para escrita contínua (incremental)
    with open(output_file, "w", encoding="utf-8") as f:
        for idx, segment in enumerate(segments, start=1):
            start_fmt = format_timestamp(segment.start)
            end_fmt = format_timestamp(segment.end)
            text = segment.text.strip()
            
            # Formato do SRT
            srt_block = f"{idx}\n{start_fmt} --> {end_fmt}\n{text}\n\n"
            
            # Escreve e força flush (salvamento no disco)
            f.write(srt_block)
            f.flush()
            
            print(f"[{start_fmt} -> {end_fmt}] {text}")

    end_time = time.time()
    elapsed = end_time - start_time
    
    print("\n[SUCESSO] Transcrição concluída!")
    print(f"[INFO] Tempo de processamento: {elapsed:.2f} segundos.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Long Audio Transcriber via Faster-Whisper")
    parser.add_argument("--input", required=True, help="Caminho do arquivo de áudio ou vídeo de entrada.")
    parser.add_argument("--output", required=True, help="Caminho do arquivo SRT de saída.")
    parser.add_argument("--device", choices=["cuda", "cpu"], default="cpu", help="Dispositivo de execução (cuda ou cpu).")
    parser.add_argument("--model", default="medium", help="Tamanho do modelo (tiny, base, small, medium, large-v3). Default: medium.")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input):
        print(f"[ERRO] O arquivo de entrada '{args.input}' não existe.")
        sys.exit(1)
        
    transcribe_audio(args.input, args.output, args.device, args.model)
