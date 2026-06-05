import os
import yt_dlp

class BaixadorDeAudio:
    """Responsavel por realizar o download da trilha de audio de um video do YouTube."""

    def baixar(self, url: str, pasta_destino: str) -> str:
        """Efetua o download do audio e retorna o caminho do arquivo gerado.
        
        Pre-condicao: A URL deve ser uma string de video valida do YouTube. A pasta de destino deve existir.
        Pos-condicao: O arquivo de audio correspondente e salvo em disco e seu caminho absoluto e retornado.
        """
        opcoes = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(pasta_destino, '%(id)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'm4a',
                'preferredquality': '192',
            }],
            'quiet': True,
        }
        
        with yt_dlp.YoutubeDL(opcoes) as ytdl:
            info = ytdl.extract_info(url, download=True)
            caminho_arquivo = ytdl.prepare_filename(info)
            caminho_sem_ext, _ = os.path.splitext(caminho_arquivo)
            caminho_final = caminho_sem_ext + ".m4a"
            return os.path.abspath(caminho_final)
