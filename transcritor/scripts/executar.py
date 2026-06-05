import os
import sys
from baixador import BaixadorDeAudio
from transcritor import TranscritorDeAudio
from escritor import EscritorDeArquivo
from processador import ProcessadorVideoAulas

def principal() -> None:
    """Funcao principal para coordenar a transcricao de videos ou audios."""
    if len(sys.argv) < 2:
        print("Erro: Argumento ausente. Uso correto:")
        print("python executar.py <URL_do_YouTube_ou_caminho_de_arquivo_local> [nome_da_transcricao_opcional]")
        sys.exit(1)
        
    argumento = sys.argv[1]
    
    # Caminhos de configuracao
    # A pasta de destino das transcricoes e resolvida a partir do diretorio atual de trabalho
    diretorio_trabalho = os.getcwd()
    pasta_destino_transcricoes = os.path.join(diretorio_trabalho, "transcricoes")
    caminho_script_skill = "G:\\SKILLS\\audio-transcriber\\scripts\\transcribe.py"
    
    if not os.path.exists(pasta_destino_transcricoes):
        os.makedirs(pasta_destino_transcricoes, exist_ok=True)
        
    # Inicializacao das classes
    baixador = BaixadorDeAudio()
    transcritor = TranscritorDeAudio(caminho_script_skill)
    escritor = EscritorDeArquivo()
    processador = ProcessadorVideoAulas(baixador, transcritor, escritor)
    
    # Define o nome amigavel da transcricao
    if len(sys.argv) > 2:
        nome_aula = sys.argv[2]
    else:
        if os.path.exists(argumento):
            nome_aula = os.path.splitext(os.path.basename(argumento))[0]
        else:
            nome_aula = "videoaula_transcrita"
            
    # Processa o argumento de entrada
    if os.path.exists(argumento):
        print(f"Configurado para processar o arquivo local: {argumento}")
        print(f"Destino das transcricoes: {pasta_destino_transcricoes}\n")
        print(f"Processando arquivo local: {nome_aula}")
        print(f"Caminho: {argumento}")
    else:
        print(f"Configurado para processar a URL: {argumento}")
        print(f"Destino das transcricoes: {pasta_destino_transcricoes}\n")
        print(f"Processando videoaula remota...")
        print(f"URL: {argumento}")
        
    try:
        caminho_final = processador.processar(argumento, nome_aula, pasta_destino_transcricoes)
        print(f"\nSucesso! Arquivo gerado em: {caminho_final}\n")
    except Exception as erro:
        print(f"\nErro ao processar a transcricao: {erro}\n", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    principal()
