import subprocess
import sys

class TranscritorDeAudio:
    """Responsavel por invocar a skill de transcricao sobre um arquivo de audio local."""

    def __init__(self, caminho_script_skill: str) -> None:
        """Inicializa o transcritor com o caminho do script da skill.
        
        Pre-condicao: O caminho do script deve apontar para o transcribe.py valido.
        """
        self.caminho_script_skill = caminho_script_skill

    def transcrever(self, caminho_audio: str, caminho_srt_saida: str) -> None:
        """Invoca a skill externa para gerar o arquivo SRT.
        
        Pre-condicao: O arquivo de audio deve existir no local especificado.
        Pos-condicao: O arquivo SRT deve ser gerado no caminho de saida.
        """
        comando = [
            sys.executable,
            self.caminho_script_skill,
            caminho_audio,
            caminho_srt_saida
        ]
        
        subprocess.run(comando, check=True)
