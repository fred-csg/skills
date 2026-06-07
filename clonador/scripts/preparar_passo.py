# Requisito Originário: g:\projeto_python\clonador\etapas
"""
Módulo de preparação e consolidação de insumos para as etapas de clonagem de expert.
Este script consolida de forma coesa arquivos de conhecimento e análises intermediárias.
"""

import os
import glob
import argparse
from typing import List, Optional

class KnowledgeConsolidator:
    """
    Classe responsável por consolidar múltiplos arquivos de texto e markdown em um único arquivo temporário.
    A consolidação é feita adicionando marcadores claros de início e fim para cada arquivo.
    """

    def __init__(self, project_dir: str) -> None:
        """
        Inicializa o consolidador de conhecimento.

        Args:
            project_dir (str): Caminho absoluto da raiz do projeto.
        """
        self._project_dir = os.path.abspath(project_dir)
        self._knowledge_dir = os.path.join(self._project_dir, "base-de-conhecimento")
        self._markdown_dir = os.path.join(self._project_dir, "markdown")

    def _obter_arquivos_conhecimento(self) -> List[str]:
        """
        Retorna a lista de caminhos absolutos de arquivos válidos na pasta base-de-conhecimento.

        Returns:
            List[str]: Caminhos dos arquivos de texto e markdown da base de conhecimento.
        """
        arquivos = []
        if not os.path.exists(self._knowledge_dir):
            return arquivos
        
        # Busca por .md e .txt
        padroes = [
            os.path.join(self._knowledge_dir, "*.md"),
            os.path.join(self._knowledge_dir, "*.txt")
        ]
        for padrao in padroes:
            arquivos.extend(glob.glob(padrao))
        
        return sorted(arquivos)

    def _obter_arquivos_markdown_intermediarios(self, passo: int) -> List[str]:
        """
        Retorna a lista de relatórios markdown gerados em etapas anteriores.

        Args:
            passo (int): O passo atual de execução.

        Returns:
            List[str]: Caminhos dos arquivos markdown válidos anteriores.
        """
        arquivos = []
        if passo <= 1 or not os.path.exists(self._markdown_dir):
            return arquivos

        # Mapeamento de quais relatórios intermediários são necessários em cada passo
        mapeamento = {
            2: ["extracao.md"],
            3: ["extracao.md", "padrao-linguistico.md"],
            4: ["extracao.md", "padrao-linguistico.md", "clone-digital.md"]
        }

        nomes_arquivos = mapeamento.get(passo, [])
        for nome in nomes_arquivos:
            caminho = os.path.join(self._markdown_dir, nome)
            if os.path.exists(caminho):
                arquivos.append(caminho)
            
        return arquivos

    def consolidar_para_passo(self, passo: int) -> str:
        """
        Consolida todos os insumos requeridos para o passo indicado em um único arquivo temporário.

        Args:
            passo (int): O passo atual de 1 a 4.

        Returns:
            str: Caminho absoluto do arquivo consolidado temporário gerado.

        Raises:
            ValueError: Se o passo informado for inválido.
            FileNotFoundError: Se arquivos requeridos de etapas anteriores não forem encontrados.
        """
        if passo < 1 or passo > 4:
            raise ValueError(f"Passo inválido: {passo}. Deve ser um valor entre 1 e 4.")

        # Verificar se as pastas básicas do projeto existem
        if not os.path.exists(self._knowledge_dir):
            raise FileNotFoundError(f"Diretório de base de conhecimento não encontrado: {self._knowledge_dir}")
        
        os.makedirs(self._markdown_dir, exist_ok=True)

        # Buscar arquivos que devem compor o insumo
        arquivos_conhecimento = self._obter_arquivos_conhecimento()
        arquivos_markdown = self._obter_arquivos_markdown_intermediarios(passo)

        # No passo > 1, validar se os arquivos anteriores existem de fato
        if passo > 1:
            esperados = {
                2: ["extracao.md"],
                3: ["extracao.md", "padrao-linguistico.md"],
                4: ["extracao.md", "padrao-linguistico.md", "clone-digital.md"]
            }[passo]
            for esp in esperados:
                caminho_esp = os.path.join(self._markdown_dir, esp)
                if not os.path.exists(caminho_esp):
                    raise FileNotFoundError(
                        f"Erro: O arquivo '{esp}' da etapa anterior é obrigatório para o passo {passo} e não foi encontrado."
                    )

        # Nome do arquivo de saída temporário
        temp_file_path = os.path.join(self._markdown_dir, f"insumos_passo_{passo}.txt.tmp")

        with open(temp_file_path, "w", encoding="utf-8") as outfile:
            # Escrever sumário inicial
            outfile.write("=========================================================================\n")
            outfile.write(f" ARQUIVO CONSOLIDADO DE INSUMOS - PASSO {passo}\n")
            outfile.write("=========================================================================\n\n")
            outfile.write("Fontes de Base de Conhecimento incluídas:\n")
            for f in arquivos_conhecimento:
                outfile.write(f" - {os.path.basename(f)}\n")
            
            if arquivos_markdown:
                outfile.write("\nAnálises de etapas anteriores incluídas:\n")
                for f in arquivos_markdown:
                    outfile.write(f" - {os.path.basename(f)}\n")
            
            outfile.write("\n" + "=" * 73 + "\n\n")

            # Escrever conteúdo dos arquivos de base de conhecimento
            for caminho in arquivos_conhecimento:
                nome_base = os.path.basename(caminho)
                outfile.write(f"--- INÍCIO DO ARQUIVO DE CONHECIMENTO: {nome_base} ---\n")
                try:
                    with open(caminho, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Erro ao ler arquivo {nome_base}: {str(e)}]\n")
                outfile.write(f"\n--- FIM DO ARQUIVO DE CONHECIMENTO: {nome_base} ---\n\n")

            # Escrever conteúdo dos markdowns intermediários
            for caminho in arquivos_markdown:
                nome_base = os.path.basename(caminho)
                outfile.write(f"--- INÍCIO DO MARKDOWN INTERMEDIÁRIO: {nome_base} ---\n")
                try:
                    with open(caminho, "r", encoding="utf-8") as infile:
                        outfile.write(infile.read())
                except Exception as e:
                    outfile.write(f"[Erro ao ler arquivo {nome_base}: {str(e)}]\n")
                outfile.write(f"\n--- FIM DO MARKDOWN INTERMEDIÁRIO: {nome_base} ---\n\n")

        return temp_file_path

    def limpar_arquivos_temporarios(self) -> List[str]:
        """
        Remove todos os arquivos temporários (.tmp) criados pelo consolidador na pasta markdown.

        Returns:
            List[str]: Lista de arquivos temporários que foram removidos.
        """
        removidos = []
        if not os.path.exists(self._markdown_dir):
            return removidos

        arquivos_tmp = glob.glob(os.path.join(self._markdown_dir, "*.tmp"))
        for caminho in arquivos_tmp:
            try:
                os.remove(caminho)
                removidos.append(caminho)
            except Exception:
                pass
        return removidos


class StepRunner:
    """
    Classe responsável por orquestrar a execução e exibição de instruções para o agente.
    """

    def __init__(self, consolidator: KnowledgeConsolidator, skill_dir: str) -> None:
        """
        Inicializa o orquestrador do passo.

        Args:
            consolidator (KnowledgeConsolidator): Instância do consolidador de conhecimento.
            skill_dir (str): Diretório da skill para localizar as referências de passos.
        """
        self._consolidator = consolidator
        self._skill_dir = os.path.abspath(skill_dir)

    def executar_passo(self, passo: int) -> None:
        """
        Executa a preparação do passo e exibe instruções operacionais para o agente.

        Args:
            passo (int): O passo a executar (1 a 4).
        """
        try:
            temp_file = self._consolidator.consolidar_para_passo(passo)
            print(f"SUCESSO: Insumos consolidados com sucesso em: {temp_file}")
            print("\nDiretrizes de análise e processamento:\n")
            print("1. Leia o arquivo consolidado de insumos indicado acima.")
            print(f"2. Siga rigorosamente as instruções da especificação no arquivo correspondente ao passo {passo}.")
            
            # Mostrar nome do arquivo final esperado
            arquivos_finais = {
                1: "markdown/extracao.md",
                2: "markdown/padrao-linguistico.md",
                3: "markdown/clone-digital.md",
                4: "markdown/prompt-gpt.txt"
            }
            print(f"3. O resultado final deve ser salvo no arquivo de destino: {arquivos_finais[passo]}")
            print("\nPara iniciar a análise, você pode visualizar as regras originais do passo em:")
            
            refs = {
                1: "references/passo1-extracao.md",
                2: "references/passo2-padrao-linguistico.md",
                3: "references/passo3-clonagem.md",
                4: "references/passo4-prompt-gpt.md"
            }
            caminho_ref = os.path.join(self._skill_dir, refs[passo])
            print(f" -> {caminho_ref}\n")
        except Exception as e:
            print(f"ERRO ao preparar o passo {passo}: {str(e)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Orquestrador e preparador de insumos para a skill clonador.")
    parser.add_argument("--passo", "-p", type=int, choices=[1, 2, 3, 4], help="Número da etapa a ser preparada (1 a 4).")
    parser.add_argument("--limpar", "-l", action="store_true", help="Remove arquivos temporários da pasta markdown.")
    parser.add_argument("--projeto", "-d", type=str, default=".", help="Diretório da raiz do projeto (padrão: pasta atual).")
    
    args = parser.parse_args()

    # Identificar diretório da skill (que contém este script em scripts/preparar_passo.py)
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    consolidator = KnowledgeConsolidator(args.projeto)
    runner = StepRunner(consolidator, skill_dir)

    if args.limpar:
        removidos = consolidator.limpar_arquivos_temporarios()
        if removidos:
            print("Arquivos temporários removidos:")
            for r in removidos:
                print(f" - {r}")
        else:
            print("Nenhum arquivo temporário encontrado para limpeza.")
    elif args.passo:
        runner.executar_passo(args.passo)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
