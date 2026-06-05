import os
import re
from baixador import BaixadorDeAudio
from transcritor import TranscritorDeAudio
from escritor import EscritorDeArquivo

class ProcessadorVideoAulas:
    """Orquestra o download e a transcricao das videoaulas informadas."""

    def __init__(self, baixador: BaixadorDeAudio, transcritor: TranscritorDeAudio, escritor: EscritorDeArquivo) -> None:
        """Inicializa o processador injetando as dependencias necessarias."""
        self.baixador = baixador
        self.transcritor = transcritor
        self.escritor = escritor

    def _sanitizar_nome_arquivo(self, nome: str) -> str:
        """Sanitiza o nome para ser usado como nome de arquivo."""
        nome_sanitizado = nome.lower()
        nome_sanitizado = re.sub(r'[^a-z0-9_]', '_', nome_sanitizado)
        nome_sanitizado = re.sub(r'_+', '_', nome_sanitizado)
        return nome_sanitizado.strip('_')

    def processar(self, entrada: str, nome_aula: str, pasta_destino: str) -> str:
        """Executa o download (se for URL) ou transcricao direta (se for arquivo local), salvando a saida final em Markdown.
        
        Pre-condicao: A entrada (URL ou caminho de arquivo local existente) e o nome da aula devem ser validos. A pasta de destino deve existir.
        Pos-condicao: Os arquivos finais .srt e .md sao gerados, e arquivos de audio temporarios sao limpos se aplicavel.
        """
        nome_sanitizado = self._sanitizar_nome_arquivo(nome_aula)
        caminho_srt_final = os.path.join(pasta_destino, f"{nome_sanitizado}.srt")
        caminho_markdown_final = os.path.join(pasta_destino, f"{nome_sanitizado}.md")
        
        # Caso ambos os arquivos ja existam, reaproveita os resultados (idempotencia)
        if os.path.exists(caminho_srt_final) and os.path.exists(caminho_markdown_final):
            return caminho_markdown_final
            
        # Caso apenas o arquivo .srt exista, gera o markdown a partir dele
        if os.path.exists(caminho_srt_final) and not os.path.exists(caminho_markdown_final):
            conteudo_markdown = self._converter_srt_para_markdown(caminho_srt_final, nome_aula)
            self.escritor.salvar(conteudo_markdown, caminho_markdown_final)
            return caminho_markdown_final
            
        # Caso precise transcrever do zero
        deve_remover_audio = False
        if os.path.exists(entrada):
            # Se for um caminho de arquivo local existente, usamos diretamente
            caminho_audio = os.path.abspath(entrada)
        else:
            # Caso contrario, assume-se que e uma URL e faz o download
            caminho_audio = self.baixador.baixar(entrada, pasta_destino)
            deve_remover_audio = True
        
        try:
            self.transcritor.transcrever(caminho_audio, caminho_srt_final)
            conteudo_markdown = self._converter_srt_para_markdown(caminho_srt_final, nome_aula)
            self.escritor.salvar(conteudo_markdown, caminho_markdown_final)
            return caminho_markdown_final
            
        finally:
            if deve_remover_audio and os.path.exists(caminho_audio):
                os.remove(caminho_audio)

    def _converter_srt_para_markdown(self, caminho_srt: str, nome_aula: str) -> str:
        """Converte o formato SRT em texto Markdown corrido sem marcas de tempo."""
        linhas_texto = []
        
        with open(caminho_srt, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            
        i = 0
        while i < len(linhas):
            linha = linhas[i].strip()
            if not linha:
                i += 1
                continue
                
            if linha.isdigit():
                i += 1
                continue
                
            if "-->" in linha:
                i += 1
                continue
                
            linhas_texto.append(linha + " ")
            i += 1
            
        texto_corrido = "".join(linhas_texto).strip()
        texto_corrido = re.sub(r'\s+', ' ', texto_corrido)
        conteudo_final = f"# {nome_aula}\n\n{texto_corrido}\n"
        return conteudo_final
