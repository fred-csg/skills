import os
import sys
import subprocess
import argparse
import site

def fix_nvidia_dll_path():
    """Adiciona as DLLs do NVIDIA CUDA (instaladas via pip) ao path do Windows."""
    if os.name == 'nt':
        paths = site.getsitepackages()
        user_site = site.getusersitepackages()
        if isinstance(user_site, str):
            paths.append(user_site)
            
        for path in paths:
            for lib in ["cublas", "cudnn", "cuda_nvrtc"]:
                bin_path = os.path.join(path, "nvidia", lib, "bin")
                if os.path.exists(bin_path):
                    os.environ["PATH"] += os.pathsep + bin_path
                    try:
                        if hasattr(os, "add_dll_directory"):
                            os.add_dll_directory(bin_path)
                    except Exception:
                        pass

# Applica correção de DLLs do CUDA antes de qualquer carregamento de modelo
fix_nvidia_dll_path()

def check_gpu():
    """Detecta se uma GPU NVIDIA está disponível no sistema."""
    try:
        subprocess.check_output(['nvidia-smi'], stderr=subprocess.STDOUT)
        return True
    except Exception:
        return False

def install_package(package):
    """Instala uma dependência dinamicamente."""
    print(f"Instalando dependência necessária: {package}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def format_timestamp(seconds: float):
    """Formata segundos em timestamp padrão SRT (HH:MM:SS,mmm)."""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def transcribe_faster_whisper(audio_file, srt_file):
    """Usa faster-whisper para transcrever incrementalmente com GPU."""
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        install_package("faster-whisper")
        from faster_whisper import WhisperModel

    print("[GPU Detectada] Utilizando faster-whisper otimizado com CUDA.")
    # Utilizando modelo base ou distil-large-v3 dependendo da necessidade de VRAM, 
    # por padrão vamos de turbo ou large-v3. Optando por "turbo" por balancear velocidade e VRAM.
    try:
        model = WhisperModel("turbo", device="cuda", compute_type="float16")
    except ValueError:
        print("[GPU] Float16 não suportado. Realizando fallback para int8...")
        model = WhisperModel("turbo", device="cuda", compute_type="int8")
    
    print(f"Iniciando transcrição de: {audio_file}")
    print("Ativando VAD Filter para otimização de chunks longos...")
    
    # O gerador segments retorna os dados conforme são processados
    segments, info = model.transcribe(audio_file, vad_filter=True)
    
    print(f"Idioma detectado: '{info.language}' (probabilidade: {info.language_probability:.2f})")
    
    with open(srt_file, "w", encoding="utf-8") as f:
        for i, segment in enumerate(segments, start=1):
            start_time = format_timestamp(segment.start)
            end_time = format_timestamp(segment.end)
            text = segment.text.strip()
            
            srt_entry = f"{i}\n{start_time} --> {end_time}\n{text}\n\n"
            f.write(srt_entry)
            f.flush() # Força a escrita no disco garantindo salvamento incremental
            print(f"[{start_time} --> {end_time}] {text}")
            
    print(f"\nTranscrição concluída com sucesso! Salvo em: {srt_file}")

def transcribe_standard_whisper(audio_file, srt_file):
    """Usa openai-whisper para fallback na CPU."""
    try:
        import whisper
    except ImportError:
        install_package("openai-whisper")
        import whisper

    print("[GPU Não Detectada] Utilizando whisper padrão na CPU.")
    
    # Para salvar incrementalmente com openai-whisper e garantir que não trave em memória,
    # invocamos o whisper pela linha de comando e repassamos o streaming.
    print(f"Iniciando transcrição de: {audio_file} (Isso pode demorar consideravelmente em CPU)")
    
    try:
        out_dir = os.path.dirname(os.path.abspath(srt_file))
        if not out_dir:
            out_dir = "."
            
        cmd = [
            sys.executable, "-m", "whisper", 
            audio_file, 
            "--model", "base", # Base é mais seguro para CPU
            "--output_format", "srt", 
            "--output_dir", out_dir
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
        
        for line in process.stdout:
            print(line, end="")
        process.wait()
        
        # O openai-whisper salvará o arquivo SRT como <nome-do-audio>.srt na pasta out_dir
        base_name = os.path.splitext(os.path.basename(audio_file))[0]
        expected_srt = os.path.join(out_dir, f"{base_name}.srt")
        
        if os.path.exists(expected_srt) and os.path.abspath(expected_srt) != os.path.abspath(srt_file):
            import shutil
            shutil.move(expected_srt, srt_file)
            
        print(f"\nTranscrição concluída! Salvo em: {srt_file}")
    except Exception as e:
        print(f"Erro ao transcrever com whisper padrão: {e}")

def main():
    parser = argparse.ArgumentParser(description="Transcreve arquivo de áudio e gera SRT incremental.")
    parser.add_argument("audio_file", help="Caminho do arquivo de áudio de entrada")
    parser.add_argument("srt_file", help="Caminho do arquivo SRT de saída")
    args = parser.parse_args()

    if not os.path.exists(args.audio_file):
        print(f"Erro: O arquivo de áudio '{args.audio_file}' não foi encontrado.")
        sys.exit(1)

    if check_gpu():
        try:
            transcribe_faster_whisper(args.audio_file, args.srt_file)
        except Exception as e:
            print(f"Erro ao usar GPU ({e}). Realizando fallback para CPU com whisper padrão...")
            transcribe_standard_whisper(args.audio_file, args.srt_file)
    else:
        transcribe_standard_whisper(args.audio_file, args.srt_file)

if __name__ == "__main__":
    main()
