import os

class EscritorDeArquivo:
    """Responsavel por gravar as transcricoes formatadas no disco."""

    def salvar(self, conteudo: str, caminho_destino: str) -> None:
        """Salva o conteudo de texto no caminho de destino.
        
        Pre-condicao: O conteudo nao pode ser vazio ou nulo.
        Pos-condicao: A pasta pai e criada se necessario, e o arquivo e escrito com sucesso.
        """
        if not conteudo:
            raise ValueError("O conteudo a ser salvo nao pode ser vazio ou nulo.")
            
        pasta_pai = os.path.dirname(caminho_destino)
        if pasta_pai and not os.path.exists(pasta_pai):
            os.makedirs(pasta_pai, exist_ok=True)
            
        with open(caminho_destino, "w", encoding="utf-8") as f:
            f.write(conteudo)
