Inteligência Artificial Visual

2

A Etiene, Rafael, Pedro e Mafalda (nossa poodle)
Todas minhas razões são vocês.

Publisher:
Canal Sandeco
First edition, published in 2024.

Copyright © 2023–
This work is licensed under a Creative Commons "Attribution-NonCommercial-ShareAlike 3.
Unported"license.

ISBN:
978-0-2021-

CAPA:
Tema: Espectro de Dados: A Arte do Orange Canvas
Autora: Rosimere Marinho
E-mail: rosicmarinho@gmail.com
Instagram: @marinho.rosi
Qualificação: Graduada em Letras pela PUC RJ
Interesses: Apaixonada por IA, ChatGPT e imagens geradas por IA

Prefácio
A inteligência artificial (IA) é um tema de debate constante e objeto de várias interpretações que
podem ser resumidas em se é útil ou prejudicial. Quando nos deparamos com um conceito novo,
frequentemente o receamos, ele nos incute temor, sentimos isso como uma ameaça. Entretanto,
isso não vale apenas para a inteligência artificial.

A IA é uma ferramenta que complementa e potencializa as oportunidades geradas pela chegada
da internet e da economia digital. Estou absolutamente tranquilo ao afirmar que a IA é uma grande
oportunidade e não uma ameaça. Os meios de comunicação de massa empregam a intimidação
para despertar a atenção, desconsiderando os prejuízos que possam provocar. É verdade que
os responsáveis pela inteligência artificial, para conseguirem investimentos, às vezes exageram
nos resultados que podem atingir e lançam produtos prematuramente que apresentam defeitos
operacionais.

O trabalho do meu amigo e professor Sandeco serve para esclarecer essa questão e disponibiliza
uma ferramenta, como o uso da inteligência artificial, acessível para professores e profissionais, que
verão seu trabalho facilitado e melhorado. O Orange Canvas é gratuito e colaborativo, características
importantes que garantem sua utilidade por muito tempo. Democratizar e explicá-lo são os resultados
do esforço do Professor Sandeco.

Não é novidade que ele, atuando como embaixador do Programa Include da Campus Party e
formador de professores em IA em nossos laboratórios, possibilita a capacitação de jovens de 10 a
18 anos das periferias de todo o Brasil a entender e utilizar essa poderosa ferramenta de IA. Por essa
razão, avalio este trabalho como excepcionalmente bem-executado e de alta qualidade, fundamental
para professores e profissionais que não querem ficar de fora do novo e empolgante mundo da
Inteligência Artificial.

Francesco Farrugia
Presidente do Instituto Campus Party

5
Sumário
Prefácio
1 Democratizando a Criação de IA
1.1 Instalando o Orange Canvas
1.2 Conexão de Widgets noOrange Canvas
1.3 Importando dados no Orange
1.4 Exercícios
2 Pré-Processamento de Dados
2.1 O painel Transform
2.2 Preprocess
2.3 Valores Ausentes e Seu Impacto nos Dados
2.4 O Que São Outliers e Seu Impacto nos Dados
2.5 Normalização e Padronização dos Dados
2.6 Variáveis Categóricas
2.7 Análise de Componentes Principais (PCA)
3 Crie sua Inteligência Artificial
3.1 Marketing e Inteligência Artificial
3.2 Hora de treinar sua Rede Neural
3.3 Hora de fazer previsões
3.4 Exercícios
4 Previsão de Doenças usando IA
4.1 Previsão de Doença do Coração usando IA
4.2 Explorando o Widget Data Sampler no Orange
4.3 O widget Rank
4.4 Combinando Rank + PCA
5 Visão Computacional
5.1 Redes Neurais Convolucionais
5.2 ADD-ON Image Analytics Inteligência Artificial Visual
5.3 Detectando Covid-19 com Imagens Médicas
5.4 Embeddings
5.5 Exercícios
6 Inteligência Artificial para Textos
6.1 Add-on Text Mining
6.2 Importando documentos de texto
6.3 Pré-processamento de textos
6.4 Bag of Words
6.5 Word Cloud
6.6 Avaliando textos com as Redes Transformer
6.7 Análise de Sentimentos em Textos
6.8 Exercícios
7 ChatGPT no Orange Canvas
7.1 Obtendo aAPI Keyda OpenAI
7.1.1 Passo a Passo para Obter aAPI Key
7.1.2 Custos Associados ao Uso dos Modelos da OpenAI
7.2 Filtragem de Artigos médicos com o ChatGPT e Orange
8 Séries temporais
8.1 Instalando o Add-on de Séries Temporais
8.2 Explorando o Painel de Widgets de Séries Temporais
8.3 Exemplo Prático: Previsão do Mercado de Ações
8.4 Sliding Window
8.5 O modelo ARIMA
-
Inteligência Artificial Visual

CAPÍTULO 1
1 Democratizando a Criação de IA
A revolução da Inteligência Artificial (IA) tem sido uma jornada transformadora, moldando não apenas
a tecnologia e a indústria, mas também a forma como compreendemos e interagimos com o mundo
ao nosso redor. Esta viagem começa com oMachine Learning(ML), uma abordagem que permite
aos sistemas aprender e melhorar a partir da experiência sem ser explicitamente programados. O
ML pavimentou o caminho para que os computadores realizassem tarefas que, até então, eram
consideradas exclusivamente humanas, como reconhecimento de padrões e tomada de decisões.
À medida que a tecnologia avançava, oDeep Learning(DL), uma subcategoria do ML, emergiu
trazendo consigo capacidades ainda mais avançadas. Utilizando redes neurais profundas, o DL
conseguiu processar e interpretar vastas quantidades de dados de maneira sem precedentes. Isso
permitiu avanços significativos em áreas como visão computacional, processamento de linguagem
natural e tradução automática, aproximando ainda mais as máquinas da compreensão e interação
humanas.
A fronteira mais recente nesta jornada é a IA Generativa, que representa um salto quântico em
termos de criatividade e capacidade de geração de conteúdo por parte das máquinas. Diferentemente
dos métodos anteriores, que se concentravam mais na interpretação e análise de dados, a IA
Generativa envolve a criação de novos dados que são indistinguíveis dos dados criados por humanos.
Isso abriu portas para inovações em design, arte, música e além, onde as máquinas não são apenas
ferramentas, mas colaboradores criativos.
Esta evolução da IA, de sistemas que aprendem a partir de dados para sistemas que podem criar
algo completamente novo, marca uma era empolgante e desafiadora. Cada etapa dessa jornada não
apenas ampliou as capacidades das máquinas, mas também desafiou nossas noções prévias sobre o
que é possível. À medida que continuamos a explorar os limites da IA, estamos não apenas moldando
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 8

Inteligência Artificial Visual

o futuro da tecnologia, mas também redefinindo o próprio conceito de criatividade e inovação. Neste
cenário, oOrange Canvassurge como uma ferramenta revolucionária, democratizando o acesso à IA
ao permitir que indivíduos sem formação em programação explorem seus princípios através de uma
interface visual intuitiva. Ao possibilitar a montagem de fluxos de trabalho complexos de análise de
dados com simples arrastar e soltar de componentes, oOrange Canvasconecta-se perfeitamente a
esta nova era da IA, tornando-a acessível e compreensível, e convida a uma experimentação criativa
que reflete a própria essência da inovação em IA.
OOrange Canvasrepresenta uma revolução no campo da Inteligência Artificial (IA), principal-
mente pela sua abordagem inovadora que permite a criação e experimentação com IA através de
programação visual. Esta ferramenta, caracterizada pela sua interface gráfica intuitiva, permite
aos usuários, independentemente de sua formação em computação, montar complexos fluxos de
trabalho de análise de dados arrastando e soltando componentes visuais chamados widgets. Este
capítulo introduz o conceito fundamental doOrange Canvas, destacando como ele serve como
uma ponte entre o mundo complexo da IA e aqueles ansiosos por explorá-lo sem o obstáculo da
codificação tradicional.
A programação visual, no coração doOrange Canvas, é uma abordagem que substitui a sintaxe
de programação convencional por elementos gráficos. Essa metodologia não só simplifica a compre-
ensão dos processos de IA, mas também estimula a experimentação e a aprendizagem por meio de
uma interação direta e imediata com os dados e algoritmos. Ao disponibilizar uma vasta biblioteca de
widgets que abrangem desde a pré-processamento de dados até técnicas avançadas de modelagem
e avaliação, oOrange Canvasdemocratiza o acesso às tecnologias de IA, tornando-as acessíveis a
educadores, estudantes e profissionais de diversas áreas.
A importância doOrange Canvasestende-se para além da sua acessibilidade, residindo também
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 9

Inteligência Artificial Visual

na sua capacidade de fornecer uma compreensão visual das operações de IA. A representação
gráfica dos fluxos de dados e a visualização interativa dos resultados permitem aos usuários obter
insights profundos sobre os dados e os modelos de IA de uma maneira que a programação textual
muitas vezes não consegue. Este aspecto visual e interativo é particularmente valioso no ensino e
aprendizagem de conceitos de IA, onde a abstração e a complexidade podem rapidamente se tornar
barreiras significativas.
Para aqueles fora do campo da computação, oOrange Canvasoferece uma porta de entrada
menos intimidante para o mundo da IA. Educadores, por exemplo, podem integrar oOrangeem seus
currículos para proporcionar experiências práticas de IA, sem a necessidade de ensinar ou aprender
uma linguagem de programação complexa. Da mesma forma, profissionais de áreas como biologia,
marketing e finanças podem utilizar oOrangepara analisar dados e tomar decisões baseadas em
informações sem depender de especialistas em dados ou desenvolvedores de software.
Ao longo deste capítulo, exploraremos a fundo as funcionalidades doOrange Canvas, ilustrando
como sua abordagem de programação visual não apenas facilita, mas também amplia o entendimento
e a aplicação da IA. Destacaremos como oOrangepode ser usado para criar soluções de IA
inovadoras, com exemplos práticos e estudos de caso que demonstram seu impacto em diversas
áreas. O objetivo é mostrar que, com ferramentas como oOrange Canvas, a IA é não apenas uma
possibilidade técnica, mas também uma oportunidade expansiva para uma ampla gama de usuários.
1.1 Instalando o Orange Canvas
A instalação doOrange Canvasé o primeiro passo para desbloquear o mundo da inteligência artificial
através da programação visual. Este processo é projetado para ser simples e acessível, garantindo
que usuários de todos os níveis de habilidade técnica possam começar a explorar as capacidades
doOrangesem demora. A seguir, apresentaremos um guia passo a passo para instalar oOrange
Canvasem seu computador, abrangendo os requisitos do sistema e as etapas necessárias para
uma instalação bem-sucedida.
Requisitos do Sistema
Antes de iniciar a instalação, é importante verificar se seu sistema atende aos requisitos mínimos
necessários para executar oOrange Canvas. Embora oOrangeseja uma ferramenta relativamente
leve, garantir a compatibilidade do sistema ajudará a evitar problemas durante a instalação e o uso.
Os requisitos básicos incluem:
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 10

Inteligência Artificial Visual

Sistema operacional: Windows, macOS ou Linux.
Memória: Mínimo de 4GB de RAM.
Espaço em disco: Mínimo de 500MB livres para instalação.
Python: Algumas versões doOrangepodem ser instaladas via Python, exigindo Python 3.6 ou
superior.
Site do Orange
O site doOrange Data Miningserve como um portal abrangente para tudo relacionado aoOrange
Canvas, uma ferramenta de aprendizado de máquina e visualização de dados de código aberto.
Site: https://orangedatamining.com←Clique no link para acessar
O site destaca a principal vantagem doOrange, que é a programação visual, permitindo que os
usuários coloquem widgets na tela, os conectem e carreguem seus conjuntos de dados para extrair
insights sem a necessidade de codificação. Além de oferecer opções de download para as versões
mais recentes doOrange, o site também fornece recursos valiosos como exemplos, documentação
detalhada, blogs com atualizações regulares e informações sobre workshops. Esse rico conjunto de
recursos torna oOrangenão apenas uma ferramenta poderosa para especialistas em dados, mas
também uma plataforma educacional excelente para ensinar mineração de dados e visualização,
conforme destacado por depoimentos de profissionais e acadêmicos de diversas áreas. Além disso,
o site convida a comunidade a contribuir para o desenvolvimento e manutenção doOrange, seja
através de doações ou participação direta no projeto.
Instalação em Windows
Para usuários do Windows, oOrangepode ser instalado usando o instalador executável disponível
no site oficial doOrange. Siga estes passos:
Acesse o site oficial doOrangee navegue até a seção de download.
Baixe o instalador doOrangepara Windows.
Execute o instalador e siga as instruções na tela para completar a instalação.
Após a conclusão, você pode iniciar oOrange Canvasa partir do menu Iniciar.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 11

Inteligência Artificial Visual

Instalação em macOS
Usuários de macOS podem instalar oOrangeusando o pacote disponível no site oficial ou através
do gerenciador de pacotesHomebrew. Para a instalação direta:
Visite o site oficial doOrangee baixe o pacote de instalação para macOS.
Abra o arquivo baixado e arraste o ícone doOrangepara a pasta de Aplicativos.
Inicie oOrange Canvasa partir da pasta de Aplicativos.
Para instalação viaHomebrew:
Abra o Terminal.
2.Digite o comando: brew install –cask orange3e pressione Enter. Note que são dois
sinais de menos juntos - -, é que na compilação do livro o compilador juntou os caracteres.
Aguarde a conclusão da instalação e inicie oOrangea partir do Launchpad.
Instalação em Linux
Para usuários de Linux, oOrange Canvaspode ser instalado via linha de comando usandopip, o
gerenciador de pacotes do Python. Este método é geralmente preferido por usuários com alguma
experiência em terminal. Os comandos a seguir realizarão a instalação:
Abra o terminal.
2.Certifique-se de que o Python e o pip estão instalados executando:python3 –versionepip
–version. Note que são dois sinais de menos juntos - -.
Instale oOrangecom o comando:pip3 install orange3.
4.Após a instalação, você pode iniciar oOrange Canvasdigitando:orange-canvasno terminal.
Uma característica notável doOrange Canvasé sua utilização doMiniconda, uma versão
minimalista doAnacondaque fornece um ambiente Python simples e eficiente, ideal para criadores
de Inteligência Artificial e cientistas de dados. OMinicondavem com o gerenciador de pacotesconda,
facilitando a instalação e o gerenciamento de pacotes e dependências necessárias para oOrange
funcionar de maneira otimizada. Essa escolha reflete o compromisso doOrangecom a facilidade de
uso e acessibilidade, permitindo que mesmo aqueles com pouca experiência em gerenciamento de
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 12

Inteligência Artificial Visual

ambientes de desenvolvimento possam configurar e começar a utilizar a ferramenta rapidamente. A
integração com oMinicondaassegura uma instalação mais leve e menos propensa a conflitos de
pacotes, tornando oOrangeuma opção robusta para a exploração visual de dados e aprendizado
de máquina.
Após a instalação, você estará pronto para começar a explorar as funcionalidades doOrange
Canvas, criando fluxos de trabalho visuais para análise de dados e desenvolvimento de modelos de
IA. Lembre-se de que a comunidadeOrangee a documentação oficial são ótimos recursos caso
você encontre dificuldades ou tenha dúvidas durante a instalação ou o uso da ferramenta.
Boas-vindas aoOrange Canvas
Ao iniciar oOrange Canvas, somos recebidos por uma interface de boas-vindas projetada para
simplicidade e eficiência como mostra a Figura 8.5.
Figura 1.1: Tela de Abertura do Orange Canvas.
Com opções claramente delineadas, a tela oferece um ponto de partida intuitivo para qualquer
nível de usuário. As opções’New’,’Open’, e’Recent’são exibidamente apresentadas na parte
superior, cada uma com um ícone distintivo que facilita a criação de um novo espaço de trabalho, a
abertura de projetos previamente salvos ou a navegação por projetos recentes.
A parte inferior da tela é dedicada ao aprendizado e à exploração mais aprofundada das funcio-
nalidades doOrange.’Video Tutorials’oferece uma aprendizagem visual através de demonstrações
práticas, enquanto’Get Started’direciona os usuários para guias introdutórios.’Examples’proporci-
ona uma coleção de casos de uso, ilustrando a aplicação prática doOrange Canvasem diferentes
cenários. Por fim,’Documentation’conduz ao repositório de informações detalhadas, suportando
uma compreensão mais rica e técnica da plataforma.
No canto inferior esquerdo, a opção’Show at startup’permite aos usuários personalizar se dese-
jam ou não ver esta tela de boas-vindas a cada início do programa, enquanto’Help us improve!’no
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 13

Inteligência Artificial Visual

canto inferior direito é um convite aberto para que a comunidade contribua com o crescimento e apri-
moramento doOrange Canvas, enfatizando a natureza colaborativa deste ambiente de programação
visual.
Painéis de Widgets noOrange Canvas
OOrange Canvasé organizado em painéis de widgets, cada um representando uma categoria
distinta de funcionalidades que o usuário pode explorar. Estes painéis são a essência da experiência
de programação visual que oOrangeoferece.
Figura 1.2: Os Painéis de Widgets noOrange Canvas.
A seguir, uma visão detalhada de cada painel:
Data: Este painel contém widgets relacionados ao carregamento, manipulação e pré-processamento
de conjuntos de dados. É aqui que os projetos começam, com a importação de dados que
serão analisados.
Transform: Widgets neste painel permitem a transformação de dados, como normalização e
escalonamento, fundamentais para preparar os dados para modelagem.
Visualize: Aqui, encontram-se as ferramentas para criar representações visuais dos dados,
permitindo aos usuários identificar padrões, tendências e outliers de forma intuitiva.
Model: Este painel oferece uma seleção de algoritmos de aprendizado de máquina que podem
ser aplicados para construir modelos preditivos a partir dos dados.
Evaluate: Widgets de avaliação ajudam a testar a eficácia dos modelos gerados, usando
métricas e métodos para validar e refinar os modelos.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 14

Inteligência Artificial Visual

Unsupervised: Este painel é dedicado a técnicas de aprendizado não supervisionado, como
agrupamento e detecção de anomalias, que podem fornecer insights sem a necessidade de
dados rotulados.
Cada painel é facilmente acessível e fornece uma variedade de widgets que podem ser arrastados
para a área de trabalho principal, criando um fluxo de trabalho de análise de dados que é tanto visual
quanto funcional. A utilização dos painéis de widgets é fundamental para aproveitar todo o potencial
doOrange Canvasna análise de dados e na construção de soluções de IA.
Widgets do PainelData
O painelDatanoOrange Canvasé uma coleção essencial de widgets que facilita a manipulação e
análise inicial dos dados.
A Figura 1.3 abaixo ilustra os widgets disponíveis no painelDatadoOrange Canvas.
Figura 1.3: Widgets disponíveis no painelDatadoOrange Canvas.
Cada widget tem um propósito específico:
File: Usado para carregar dados de arquivos locais em vários formatos.
CSV File Import: Especializado na importação de dados de arquivos CSV.
Datasets: Permite o acesso rápido a conjuntos de dados predefinidos.
SQL Table: Facilita a conexão e importação de dados de tabelas SQL.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 15

Inteligência Artificial Visual

Data Table: Uma interface interativa para visualizar e editar dados tabulares.
Paint Data: Oferece uma ferramenta para criar dados manualmente através de um canvas
interativo.
Data Info: Exibe informações básicas sobre o conjunto de dados carregado.
Rank: Avalia e classifica as variáveis com base em sua importância.
Edit Domain: Permite a edição de metadados do domínio dos dados, como renomear variáveis
ou alterar tipos de dados.
Color: Oferece opções para colorir os dados, o que pode ser útil na visualização.
Feature Statistics: Apresenta estatísticas descritivas das características.
Save Data: Permite salvar o conjunto de dados processado para uso futuro.
Esses widgets são fundamentais para a etapa inicial de qualquer projeto de análise de dados,
proporcionando as ferramentas necessárias para carregar, processar e entender os conjuntos de
dados antes de avançar para a modelagem ou visualização mais complexa.
1.2 Conexão de Widgets noOrange Canvas
A criação de um fluxo de trabalho de análise de dados noOrange Canvasé uma tarefa intuitiva,
graças à sua interface de programação visual. Como ilustrado na Figura 1.4, conectar widgets é tão
simples e usa somente o "clicar e arrastar" para realizar conexões. A partir do widgetFile, que é
utilizado para carregar dados no ambiente, uma linha é arrastada até o widgetData Table. Este gesto
simboliza a criação de uma conexão de dados, permitindo que o conjunto de dados carregado seja
diretamente acessível e manipulável na tabela de dados. O widgetData Tableserve como um local
central para visualização e inspeção dos dados, permitindo uma interação imediata e detalhada com
as informações carregadas. Este método de conexão não apenas facilita a construção de um fluxo
de trabalho de dados eficiente, mas também representa visualmente a transferência de informações
entre diferentes etapas de análise, tornando oOrange Canvasuma ferramenta poderosa e acessível
para profissionais de todas as áreas.
Como explorar os detalhes doswidgets
OOrange Canvasé enriquecido com uma variedade dewidgetsque tornam a análise de dados
tanto uma tarefa poderosa quanto uma experiência intuitiva. Cadawidgeté desenhado para facilitar
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 16

Inteligência Artificial Visual

Figura 1.4: Criação de uma conexão de dados através de clique e arraste entre o widgetFilee o
Data TablenoOrange Canvas.
uma função específica dentro do ecossistema de análise de dados, permitindo aos usuários desde a
seleção e carregamento de datasets até a visualização e manipulação detalhada das informações
contidas neles. Esta seção detalha o uso e a funcionalidade de doiswidgetsessenciais: oFilee
oData Table. Ao dominar essas ferramentas, usuários de todos os níveis podem realizar tarefas
complexas de análise de dados com facilidade e eficiência.
Utilizando o WidgetFilepara Seleção de Dados
NoOrange Canvas, o acesso aos dados é feito de maneira direta e interativa através do widgetFile.
Conforme mostrado na Figura 1.5, um duplo clique no ícone doFileabre a janela "File - Orange".
Esta janela é o ponto de interação inicial para a seleção do conjunto de dados que se deseja analisar.
No exemplo ilustrado, o dataset "Iris Flower"é apresentado como um caso de uso comum, sendo um
conjunto de dados padrão na área de aprendizado de máquina.
A janela "File - Orange"permite ao usuário não apenas selecionar o dataset desejado, como
indicado pela letra ’b’ no diagrama, mas também visualizar e avaliar suas propriedades, como
detalhado na parte ’c’ da imagem. Isso inclui informações como o número de instâncias, a quantidade
de atributos e a classificação dos mesmos, fornecendo um entendimento inicial essencial para o
processo subsequente de análise de dados.
Explorando oWidget Data TableeScatter Plot
No ambiente interativo doOrange Canvas, o widgetData Tableé uma ferramenta essencial para a
visualização e manipulação de dados. Um duplo clique no widgetData Table, como ilustrado na
Figura 1.6, abre a janela dedicada à inspeção do conjunto de dados. O exemplo na imagem mostra
o dataset "Iris Flower", que é frequentemente utilizado como um exemplo introdutório no campo de
aprendizado de máquina.
Dentro do retângulo laranja, encontramos os controles e informações doData Table:
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 17

Inteligência Artificial Visual

Figura 1.5: Abrindo o dataset "Iris Flower"através do widgetFilenoOrange Canvas, ilustrando as
etapas de duplo clique para abertura do arquivo e visualização das propriedades do dataset.
Informações Gerais : Resumo do dataset exibindo o número total de instâncias, o número de
características, a variável alvo e a confirmação da ausência de meta atributos.
Controles de Visualização : Conjunto de opções que permitem ao usuário personalizar a
exibição dos dados, incluindo a possibilidade de mostrar rótulos das variáveis, visualizar
valores numéricos e colorir as instâncias de acordo com as classes do dataset.
Seleção : Uma opção para selecionar linhas completas, facilitando operações como filtragem e
edição.
A área destacada em verde mostra as colunas do dataset "Iris Flower", representando caracterís-
ticas como comprimento e largura das sépalas e pétalas, e uma coluna final indicando a espécie
da íris. A coloração nas linhas dos dados reflete as classes de íris, permitindo uma distinção visual
imediata entre as diferentes espécies.
A janelaData Tableé fundamental para o processo de análise de dados, fornecendo um meio
imersivo e intuitivo para que os usuários examinem, compreendam e preparem seus dados para
análises mais aprofundadas.
OOrange Canvasoferece uma ampla gama de opções para visualizar e compreender os dados
por meio de seu painel de visualizações, como ilustrado na Figura 1.7. O painel, realçado pelo
retângulo verde na imagem, contém uma série dewidgetsque permitem aos usuários explorar
os dados de diferentes perspectivas. Esteswidgetssão ferramentas gráficas que transformam
números e categorias em gráficos e diagramas intuitivos, facilitando o reconhecimento de padrões e
a identificação deinsights.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 18

Inteligência Artificial Visual

Figura 1.6: O widgetData Tableexibindo odataset"Iris Flower", com os controles e informações
disponíveis para o usuário.
Dentro deste painel, owidget Scatter Plot, destacado pelo retângulo laranja, é frequentemente
usado para visualizar as relações entre duas variáveis numéricas. Ao aplicar esta visualização aos
dados dodataset"Iris Flower", os usuários podem, por exemplo, plotar o comprimento da sépala
contra a largura da pétala para cada instância, revelando agrupamentos naturais ou tendências entre
as espécies de íris.
O painel de visualizações noOrange Canvasé uma representação poderosa da capacidade
de programação visual da ferramenta. Com apenas alguns cliques, os usuários podem selecionar
diferentes tipos de visualizações adequadas às suas necessidades específicas de análise de dados,
tornando oOrangeuma plataforma acessível tanto para principiantes quanto para profissionais
experientes em ciência de dados.
Vamos usar por enquanto somente owidget Scatter Plotpara visualizar os dados doIris flowers.
No ambiente rico e interativo doOrange Canvas, os dados podem ser explorados e compre-
endidos de múltiplas maneiras. A Figura 1.8 captura a essência dessa flexibilidade, ilustrando
duas abordagens distintas para analisar o mesmo conjunto de dados. Veja que os dados que são
carregados por meio do widgetFilepodem ser vistos tanto pelo Data Table como pelo Scatter Plot.
Essas duas visualizações não são mutuamente exclusivas, mas sim complementares, oferecendo
aos usuários doOrange Canvasum conjunto de ferramentas robustas para uma análise de dados
completa e multifacetada.
NoOrange Canvas, oScatter Ploté uma ferramenta visual poderosa, particularmente útil para o
exame de conjuntos de dados como o "Iris Flower". A Figura 1.9 apresenta a interface doScatter
Plot, destacando os controles que permitem aos usuários modificar e aprofundar sua visualização
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 19

Inteligência Artificial Visual

Figura 1.7: Painel de visualizações noOrange Canvas, mostrando uma variedade dewidgets
disponíveis para a representação gráfica dos dados.
dos dados.
Na caixa verde, os Eixos da visualização podem ser ajustados para exibir diferentes atributos
nos eixos x e y, permitindo a exploração de diversas relações entre as características dos dados.
O botãoFind Informative Projectionsé uma funcionalidade avançada que ajuda a encontrar as
projeções mais informativas com base nas características selecionadas.
A caixa laranja contém Atributos que modificam a visualização , oferecendo opções para
alterar a cor, forma, tamanho e etiquetas dos pontos no gráfico. Estes controles permitem uma
personalização detalhada da visualização, facilitando a distinção entre as diferentes categorias ou
grupos presentes nos dados.
Cada ponto noScatter Plotcorresponde a uma linha doData Table, com a visualização fornecendo
uma representação gráfica direta dessas informações tabulares. Importante destacar, as regiões
de decisão coloridas que aparecem na visualização são um exemplo de como oOrangepode ser
usado para ilustrar conceitos de classificação em Inteligência Artificial. Estas regiões indicam onde
um modelo de IA pode classificar novos dados com base nas características aprendidas.
1.3 Importando dados no Orange
Existem várias formas de importar dados para o Orange Canvas os widget "File", "CSV File Import",
"Dataset"e "SQL Table"como mostra a Figura 1.11 e vamos detalhar cada uma.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 20

Inteligência Artificial Visual

Figura 1.8: Comparação das formas de visualização de dados noOrange Canvas: em tabela através
doData Tablee em gráfico peloScatter Plot.
O Widget File
O widgetFileé uma ferramenta importante noOrange Canvas, desempenhando o papel de um portal
para o mundo da análise de dados. Ele lê dados de atributo-valor de um arquivo de entrada, atuando
como o primeiro passo no fluxo de trabalho de data mining, ao enviar o conjunto de dados para o
seu canal de saída. A capacidade do widget de manter um histórico dos arquivos recentemente
abertos simplifica o acesso rápido a dados frequentemente usados. Além disso, inclui uma diretoria
com conjuntos de dados de exemplo, pré-instalados com o Orange, que são recursos valiosos para
aprendizado e prática.
OFiletem a capacidade de ler uma variedade de formatos de arquivo populares, como Excel
(.xlsx), arquivos delimitados por tabulações (.txt), arquivos separados por vírgulas (.csv), e até
mesmo de URLs, facilitando a integração de dados de diferentes origens. Para formatos que
não são diretamente suportados, a seção ’Outros Formatos’ oferece orientações adicionais. Com
essa versatilidade, o widgetFileserve como um componente chave no Orange, permitindo aos
usuários, desde iniciantes até especialistas, começar suas análises com uma ampla gama de dados
estruturados.
1.Navegue por arquivos de dados previamente abertos ou carregue alguns dos exemplos
disponíveis.
Procure um arquivo de dados em seu computador para carregá-lo no Orange.
Recarregue o arquivo de dados atualmente selecionado para atualizar as informações.
Insira dados de endereços de URL, incluindo dados de planilhas do Google Sheets.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 21

Inteligência Artificial Visual

Figura 1.9: Interface doScatter Plotmostrando os dados do "Iris Flower"noOrange Canvas, com
controles para personalização e áreas de decisão indicativas de classificação em IA.
5.Veja informações sobre o conjunto de dados carregado, como o tamanho do conjunto, número
e tipos de características dos dados.
6.Acesse informações adicionais sobre as características no conjunto de dados. É possível
editar as características clicando duas vezes sobre elas. Aqui, você pode alterar os nomes
dos atributos, selecionar o tipo de variável para cada atributo (Contínua, Nominal, String,
Data/Hora) e definir os atributos como Características, Alvos ou Meta. Também é possível
optar por ignorar um atributo.
Navegue pelos conjuntos de dados disponíveis na documentação do Orange.
Produza um relatório sobre os dados e análises realizadas.
CSV File Import
O widget "Importação de Arquivo CSV"noOrange Canvasé uma ferramenta fundamental para a
importação de tabelas de dados de arquivos formatados em CSV. Quando um arquivo é lido pelo
widget, ele oferece duas saídas principais:
Dados : O conjunto de dados extraído do arquivo .csv.
DataFrame : Um objeto DataFrame do pandas, que é uma estrutura de dados bidimensional,
mutável em tamanho e potencialmente heterogênea.
O widget é projetado para ler arquivos separados por vírgulas, mas é flexível o suficiente para
suportar outros separadores como ponto e vírgula, espaços, tabulações ou delimitadores definidos
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 22

Inteligência Artificial Visual

Figura 1.10: Vários modos de importação de dados no Orange Canvas
manualmente. Além disso, mantém um histórico dos arquivos mais recentemente abertos para
facilitar o acesso.
As opções de importação são uma parte crucial do processo, fornecendo uma janela onde o
usuário define os parâmetros de importação. Esta janela pode ser reaberta pressionando-se "Opções
de Importação"no próprio widget.
Uma funcionalidade interativa permite ao usuário clicar com o botão direito do mouse no nome da
coluna para definir o tipo da coluna. Da mesma forma, clicar com o botão direito no índice da linha
(à esquerda) permite marcar uma linha como cabeçalho, ignorada ou uma linha de dados normal. A
Figura 1.14 mostra como é feita a importação de csv.
Codificação do Arquivo : A codificação padrão utilizada é UTF-8, que suporta uma ampla
gama de caracteres para diferentes idiomas e símbolos.
Configurações de Importação : Aqui, o usuário pode definir como os dados estão organizados
no arquivo CSV.
- Delimitador de Células : Pode ser tabulação, vírgula, ponto e vírgula ou espaço. Existe
também a opção ’Outro’ para definir um delimitador personalizado.
- Caractere de Citação : Define o caractere usado para delimitar textos que podem conter
o delimitador de células, comumente as aspas duplas ou simples.
- Separadores de Números : Inclui separadores de agrupamento para milhares (como em
1,000) e separadores decimais para valores fracionários (como em 1.234).
Tipo de Coluna : Permite selecionar uma coluna no pré-visualizador e definir seu tipo, o qual
pode ser ajustado também clicando com o botão direito na coluna selecionada.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 23

Inteligência Artificial Visual

Figura 1.11: O widget File
Automático : O Orange tentará determinar automaticamente o tipo da coluna.
Numérico : Para tipos de dados contínuos, como números fracionários.
Categórico : Para tipos de dados discretos, como categorias ou etiquetas.
Texto : Para tipos de dados de texto ou strings.
Data/Hora : Para variáveis de tempo e data.
Ignorar : A coluna não será incluída na saída de dados.
4.Pressionar Reset reverterá as configurações para o estado anteriormente definido (salvo
ao pressionar OK no diálogo de Opções de Importação). Restaurar Padrões voltará as
configurações para seus valores padrão. Cancelar aborta a importação, enquanto OK importa
os dados e salva as configurações.
Datasets
O widget "Datasets"oferece acesso imediato a uma variedade de conjuntos de dados previamente
carregados, que são essenciais para análise e treinamento em ciência de dados. Quando selecio-
nado, o conjunto de dados é recuperado de um servidor e enviado ao canal de saída do widget. Isso
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 24

Inteligência Artificial Visual

Figura 1.12: O widget CSV File Import
significa que o arquivo é baixado para a memória local, tornando-o instantaneamente disponível,
mesmo sem uma conexão com a internet.
Cada conjunto de dados no repositório do widget vem acompanhado de uma descrição detalhada
que oferece um entendimento mais profundo do conteúdo e contexto dos dados. Adicionalmente,
são fornecidas informações vitais como o tamanho do arquivo, o número de instâncias e variáveis
presentes, e a natureza do alvo (target), que pode ser categórico ou numérico. Os conjuntos de
dados também estão etiquetados com tags relevantes, facilitando a identificação e seleção do
conjunto de dados mais adequado para tarefas específicas.
1.Informações sobre o número de conjuntos de dados disponíveis e o número deles baixados
para a memória local.
2.Conteúdo dos conjuntos de dados disponíveis. Cada conjunto de dados é descrito com o
tamanho, número de instâncias e variáveis, tipo da variável alvo e etiquetas.
Descrição formal do conjunto de dados selecionado.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 25

Inteligência Artificial Visual

Figura 1.13: O widget Datasets
4.Se a opção Enviar Dados Automaticamente estiver marcada, o conjunto de dados selecionado
é comunicado automaticamente. Alternativamente, pressione Enviar Dados.
SQL Table
O widget "SQL Table"oferece uma porta de entrada para o acesso a dados armazenados em um
banco de dados SQL, permitindo a conexão com sistemas de gerenciamento de banco de dados
como PostgreSQL, para o qual é necessário o módulo psycopg2, ou SQL Server, que requer o
módulo pymssql. Uma das características mais notáveis deste widget é sua capacidade de manipular
grandes bancos de dados. Para isso, o Orange tenta executar parte dos cálculos diretamente
no banco de dados, evitando a necessidade de baixar os dados. Isso é particularmente eficaz
com bancos de dados PostgreSQL e requer que as extensões quantile e tsm-system-time estejam
instaladas no servidor. Caso essas extensões não estejam presentes, o widget irá proceder com o
download dos dados para a memória local.
Tipo de banco de dados: Pode ser PostgreSQL ou MSSQL.
Nome do host: O endereço do servidor onde o banco de dados está hospedado.
3.Nome do banco de dados: O nome específico do banco de dados ao qual você deseja se
conectar.
Nome de usuário: O identificador para o login no banco de dados.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 26

Inteligência Artificial Visual

Figura 1.14: O widget SQL Table
Senha: A chave de segurança para acesso ao banco de dados.
6.Pressione o botão azul para se conectar ao banco de dados. Em seguida, selecione a tabela
desejada no menu suspenso.
7.A opção ’Auto-discover categorical variables’ classificará automaticamente as colunas INT
e CHAR com menos de 20 valores distintos como variáveis categóricas (encontrar todos os
valores distintos pode ser lento em tabelas grandes). Quando não selecionado, INT será
tratado como numérico e CHAR como texto. ’Download to local memory’ baixará a tabela
selecionada para sua máquina local.
Feature Statistics
O widget Feature Statistics no Orange é usado para inspecionar e identificar características interes-
santes em um conjunto de dados. Ele exibe estatísticas básicas para recursos de dados e permite
que os usuários visualizem a distribuição de valores de recursos por meio de histogramas. Os tipos
de recursos podem ser categóricos, numéricos, temporais ou de texto, e diferentes estatísticas são
calculadas dependendo do tipo de recurso. Este widget é útil para examinar conjuntos de dados
e selecionar recursos potencialmente interessantes para análises mais profundas. A Figura 1.15
mostra como conecar o feature statistics no Orange.
A análise exploratória de dados, permitindo aos cientistas de dados um exame rápido e abran-
gente das características dos dados. Ao revelar as distribuições e tendências subjacentes por meio
de histogramas e estatísticas como média, mínimo, máximo, modo e dispersão, os analistas podem
identificar padrões, anomalias ou necessidades de limpeza dos dados.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 27

Inteligência Artificial Visual

Figura 1.15: O widget Feature Statistics
Utilizar oFeature Statisticspode ser extremamente útil para orientar decisões de pré-processamento,
como a escolha de variáveis para transformação ou remoção, melhorando assim a qualidade do
modelo demachine learning. A habilidade de discernir características categóricas e numéricas e
entender sua relevância através da visualização direta torna o widget uma ferramenta poderosa no
arsenal do Orange para a preparação e otimização de dados para análises subsequentes. Ela revela
estatísticas cruciais, como a média, valores mínimos e máximos para características numéricas, e a
moda e dispersão para ambos os tipos numéricos e categóricos, o que é essencial para compreen-
der a variação e a predominância de determinados valores. Além disso, as barras do histograma
podem ser divididas com base no valor de outra variável, permitindo uma análise multifacetada e
aprofundada dos dados. A Figura 1.16 mostra os detalhes do widget Feature Statistics.
Figura 1.16: O widget Feature Statistics
Tipo da característica - pode ser categórica, numérica, temporal ou textual.
Nome da característica.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 28

Inteligência Artificial Visual

3.Histograma mostrando a distribuição dos valores da característica. Valores de características
numéricas são divididos em intervalos.
4.Colunas adicionais mostram diferentes estatísticas. Média, valor mínimo e máximo são
calculados apenas para características numéricas. Moda indica o valor mais comum para
características numéricas ou categóricas. Dispersão mostra o coeficiente de variação para
características numéricas e entropia para categóricas.
5.As barras no histograma podem ser divididas ainda mais pelo valor de outra variável. A escolha
padrão é a variável alvo, mas o usuário pode alterar isso para uma característica arbitrária ou
nenhuma.
1.4 Exercícios
1.Utilizando o widgetFile, carregue um conjunto de dados e identifique o tipo de cada variável
(categórica, numérica, temporal ou textual).
2.Com o widgetData Table, explore o conjunto de dados ’Iris Flower’ e determine o número de
instâncias e variáveis presentes.
3.Crie um histograma utilizando o widgetFeature Statisticse interprete a distribuição de uma
das características numéricas do conjunto de dados ’Iris Flower’.
4.Utilize o widgetScatter Plotpara visualizar a relação entre duas características do conjunto de
dados ’Iris Flower’ e descreva qualquer padrão observado.
5.Reflita sobre como o conceito de programação visual do Orange Canvas pode tornar a IA mais
acessível e proponha uma atividade educacional que poderia ser realizada em uma sala de
aula para crianças.
CAPÍTULO 1. DEMOCRATIZANDO A CRIAÇÃO DE IA 29

Inteligência Artificial Visual

CAPÍTULO 2
2 Pré-Processamento de Dados
Na era da inteligência artificial, os dados são o novo petróleo, pré-processamento o refino,
e a IA o foguete. Prof. Sandeco Macedo.
Na vanguarda da revolução tecnológica, o pré-processamento de dados emerge como uma
etapa indispensável no ciclo de vida dos projetos de inteligência artificial. Esta fase, muitas vezes
considerada a coluna vertebral do desenvolvimento de modelos de IA, é responsável por transformar
dados brutos e não estruturados em um formato limpo, compreensível e pronto para análise. Com
cerca de 80% do esforço em projetos de IA dedicados ao pré-processamento, essa etapa abrange
uma ampla gama de atividades essenciais, incluindo a limpeza de dados, o tratamento de valores
ausentes, a normalização, a transformação e a redução de dimensionalidade, desempenhando um
papel crucial na determinação da qualidade e eficácia dos modelos subsequentes.
A relevância do pré-processamento decorre da natureza imperfeita dos dados brutos, que são
frequentemente marcados pela incompletude, inconsistência ou tendenciosidade. Ao aplicar métodos
de pré-processamento criteriosos, é possível aprimorar significativamente a qualidade dos dados,
garantindo que os modelos de IA sejam alimentados com informações precisas e relevantes. Esse
cuidado meticuloso não apenas melhora a acurácia das previsões, mas também é fundamental
para evitar o fenômeno deoverfitting, no qual um modelo se ajusta excessivamente aos dados de
treinamento e perde a capacidade de generalizar para novos conjuntos de dados.
Além disso, o pré-processamento de dados inclui atividades vitais como a seleção e engenharia
de características, que são essenciais para construir modelos robustos e interpretáveis. Esta fase do
pré-processamento não é apenas técnica, mas também uma forma de arte, exigindo um profundo
conhecimento das técnicas estatísticas e uma compreensão intuitiva do contexto em que os dados
serão aplicados. Trata-se de encontrar o equilíbrio certo entre preservar informações cruciais e
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 25

Inteligência Artificial Visual

preparar os dados de uma maneira que os torne mais acessíveis e úteis para modelagem e análise
futuras.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 26

Inteligência Artificial Visual

Portanto, o pré-processamento de dados não é apenas um passo preliminar, mas um elemento
fundamental que define o caminho para o sucesso de qualquer projeto de IA. Ao dedicar atenção
e recursos adequados a esta etapa, os praticantes de IA podem assegurar que estão construindo
sobre uma fundação sólida, maximizando assim as chances de alcançar resultados significativos
e impactantes. A medida que avançamos nesta era digital, torna-se cada vez mais claro que
uma preparação de dados cuidadosa é indispensável para desbloquear o verdadeiro potencial da
inteligência artificial.
Pré-processamento no Orange Canvas
A tarefa de pré-processamento de dados em ambientes de inteligência artificial tradicionais pode ser
bastante exigente em termos de tempo e conhecimento técnico. Ferramentas como oPandasno
Python são amplamente utilizadas por engenheiros e cientistas de dados para limpar, transformar e
analisar dados. No entanto, a necessidade de escrever código detalhado para cada etapa desse
processo pode ser uma barreira significativa para aqueles que não são proficientes em programação.
Além disso, a depuração e otimização do código podem consumir uma quantidade considerável de
tempo, atrasando outras etapas do projeto de inteligência artificial. O uso de uma ferramenta visual
como o Orange para o pré-processamento de dados apresenta uma economia de tempo substancial
para engenheiros de inteligência artificial. Ao permitir a manipulação de dados através de uma
interface gráfica intuitiva, o Orange elimina a necessidade de codificação extensiva, acelerando o
processo de pré-processamento e permitindo que os profissionais se concentrem em aspectos mais
críticos de seus projetos.
Após a aceleração do pré-processamento de dados com o uso de ferramentas visuais, as etapas
subsequentes da análise de dados se tornam mais ágeis e eficazes. O pré-processamento abrange
uma gama de técnicas essenciais, como a limpeza, transformação e redução de dados, cada uma
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 27

Inteligência Artificial Visual

delas crítica para aprimorar a qualidade dos dados antes de prosseguir para a modelagem. Através
de uma interface visual como a do Orange, essas técnicas são aplicadas de maneira mais intuitiva
e menos propensa a erros, especialmente para usuários menos experientes em codificação. A
visualização do fluxo de dados, por meio de um esquema gráfico, permite uma compreensão mais
clara do processo de tratamento dos dados, desde a correção de valores ausentes até técnicas mais
complexas como a normalização e a redução de dimensionalidade. Essa abordagem visual não
apenas simplifica o entendimento e a aplicação das técnicas de pré-processamento, mas também
contribui para uma análise de dados mais eficiente e eficaz.
2.1 O painel Transform
O painel Transform no Orange Canvas é uma central de recursos dedicados ao pré-processamento
de dados, uma etapa fundamental na preparação dos dados para análise posterior. Este painel reúne
uma variedade de widgets que simplificam tarefas como amostragem de dados (Data Sampler),
seleção de atributos (Select Columns) e transposição de dados (Transpose), permitindo que os
usuários manipulem e transformem os dados de forma eficaz. Entre as operações disponíveis,
destacam-se a mesclagem (Merge Data), concatenação (Concatenate) e remoção de duplicatas
(Unique), cada uma desenhada para otimizar a preparação dos dados para análises complexas.
Para análises mais avançadas, os usuários podem recorrer ao agrupamento de colunas (Ag-
gregate Columns) ou à criação de tabelas dinâmicas (Pivot Table). Além disso, widgets como
Preprocess,ImputeeDiscretizesão indispensáveis para o tratamento de dados faltantes, normaliza-
ção e categorização de variáveis contínuas. O widgetRandomizeajuda a evitar vieses na análise,
enquanto oPython Scriptproporciona uma flexibilidade adicional para scripts de pré-processamento
personalizados.
Este conjunto de ferramentas no painel Transform do Orange Canvas foi cuidadosamente pro-
jetado para ser intuitivo, permitindo aos usuários criar fluxos de trabalho de pré-processamento
personalizados e eficazes, cruciais para análises detalhadas e modelagem estatística. A Figura 3.1
ilustra o painel Transform, evidenciando os widgets que facilitam o pré-processamento de dados
dentro deste ambiente de programação visual.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 28

Inteligência Artificial Visual

Figura 2.1: Painel Transform do Orange Canvas
Data Sampler: Permite a seleção de uma amostra de dados
a partir de um conjunto maior, o que é útil para trabalhar
com grandes conjuntos de dados ou para criar conjuntos de
treinamento e teste.
Select Columns: Dá ao usuário a capacidade de selecionar e
filtrar as colunas de dados que deseja incluir em sua análise.
Select Rows: Similar aoSelect Columns, mas focado na
seleção de linhas específicas de dados.
Transpose: Utilizado para transpor os dados, transformando
colunas em linhas e vice-versa, o que pode ser necessário
dependendo da estrutura exigida por certos algoritmos de
análise.
Merge Data: Combina dois conjuntos de dados baseando-se
em uma coluna comum ou sequencialmente.
Concatenate: Permite a concatenação de conjuntos de dados,
adicionando os dados de um ao final do outro.
Select by Data Index: Seleciona dados com base em um
índice fornecido, o que pode ser útil para tarefas de segmen-
tação de dados.
Unique: Remove duplicatas nos dados, deixando apenas
instâncias únicas.
Aggregate Columns: Agrega dados de colunas selecionadas
usando funções como soma, média, mediana, entre outras.
Group by: Agrupa os dados com base em um ou mais atribu-
tos.
Pivot Table: Remodela a tabela de dados com base nos valo-
res das colunas.
Apply Domain: mapeia novos dados em um espaço transfor-
mado
Preprocess: Proporciona opções de pré-processamento de
dados, como normalização e escalonamento.
Impute: Permite tratar dados faltantes, preenchendo-os com
valores médios, medianos ou mais frequentes.
Continuize: Converte variáveis categóricas em variáveis contí-
nuas, o que é muitas vezes necessário para certos tipos de
análise.
Discretize: O oposto doContinuize, transformando variáveis
contínuas em categóricas.
Randomize: Permite embaralhar os dados, o que pode ser útil
para quebrar qualquer viés de ordenação pré-existente.
Purge Domain: Remove atributos desnecessários do domínio
dos dados.
Melt: Transforma os dados de formato "longo", onde múltiplas
colunas são condensadas em uma ou duas, mantendo a iden-
tidade de cada valor.
Formula: Permite a criação de novas características a partir
de fórmulas matemáticas aplicadas aos dados.
Create Class: Auxilia na criação de uma variável de classe
para tarefas de classificação.
Create Instance: Ajuda a criar instâncias de dados com base
em regras definidas pelo usuário.
Python Script: Oferece a flexibilidade de escrever scripts
Python personalizados para o pré-processamento de dados.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 29

Inteligência Artificial Visual

Cada widget é projetado para ser intuitivo e fácil de usar, arrastando e soltando dentro do fluxo
de trabalho e configurando suas opções específicas. A combinação e a sequência de uso desses
widgets podem ser adaptadas conforme as necessidades específicas de pré-processamento de
dados do usuário, oferecendo um alto grau de personalização e controle sobre o processo de análise
de dados.
2.2 Preprocess
Uma das coisas que mais gosto no Orange é o fato de juntar várias funcionalidades em um único
widget. O pré-processamento tem várias facetas, porém as mais comuns, aquelas que a gente
usa no dia-a-dia são: imputar valores ausentes, busca outliers, normalizar features, Análise de
Componentes Principais, discretizar variáveis contínuas e tratar variáveis categóricas. Boa parte
dessas operações podem ser encontradas no widget Preprocess. A Figura 2.2 mostra a conexão
entre o widget Preprocess e o widget File.
Figura 2.2: Widget Preprocess
2.3 Valores Ausentes e Seu Impacto nos Dados
No Orange Canvas, a manipulação de valores ausentes é realizada atravésPreprocess. Valores
ausentes em conjuntos de dados são um desafio comum na análise de dados e podem surgir por
diversas razões, como erros na coleta de dados, perda durante a transferência ou mesmo porque
certas informações não são aplicáveis em determinados contextos. A presença de valores ausentes
pode levar a distorções significativas na análise estatística, resultando em conclusões errôneas. Por
exemplo, a média de uma variável seria subestimada ou superestimada se os valores ausentes não
fossem aleatórios e tivessem alguma tendência. Da mesma forma, modelos de aprendizado de
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 30

Inteligência Artificial Visual

máquina podem falhar ou produzir resultados inesperados se não forem adequadamente treinados
para lidar com dados incompletos. A Tabela 2.1 mostra um exemplo de um conjunto de dados de
pacientes com dados faltantes "NaN".
Paciente Idade Nível de Glicose
Alice 28 90 mg/dL
Bruno NaN 85 mg/dL
Carla 34 NaN
David NaN 120 mg/dL
Eva 42 NaN
Tabela 2.1: Dados de Pacientes com Valores Ausentes
Ao lidar com valores ausentes em um conjunto de dados, uma das técnicas mais diretas é a
remoção de linhas que contêm esses dados faltantes. Essa abordagem é frequentemente atraente
pela sua simplicidade e pela promessa de um conjunto de dados "limpo". No entanto, essa técnica
pode trazer problemas significativos que precisam ser cuidadosamente considerados. A eliminação
de linhas contendo valores ausentes, embora pareça uma solução direta para purificar o conjunto de
dados, pode acarretar consequências significativas na integridade e representatividade dos dados.
Por exemplo, ao considerar a aplicação dessa abordagem na Tabela 2.1, a exclusão de todas as
linhas que apresentam valores "NaN"poderia resultar em uma tabela residual com apenas uma única
linha. A linha da paciente "Alice".
A redução drástica do conjunto de dados, resultante da remoção de linhas com valores ausentes,
não somente prejudica a viabilidade do conjunto para análises estatísticas rigorosas e treinamento de
modelos de aprendizado de máquina, mas também pode levar à introdução de viéses substanciais.
Isso ocorre porque os valores ausentes podem não estar distribuídos de forma aleatória, mas sim
associados sistematicamente a determinadas condições ou características intrínsecas ao conjunto
de dados. Ao excluir esses registros, corre-se o risco de eliminar informações cruciais ligadas aos
valores ausentes, comprometendo a integridade e a representatividade dos dados analisados.
Além disso, a causalidade por trás dos dados ausentes merece atenção especial. Caso a ausência
de dados tenha uma razão subjacente significativa, a remoção desses registros pode ocultar padrões
ou tendências relevantes, essenciais para uma compreensão abrangente do fenômeno estudado. A
exclusão de dados também pode impedir a exploração de técnicas avançadas de imputação, que
preencheriam essas lacunas de maneira significativa, preservando a integridade do conjunto de
dados e possibilitando uma análise mais completa e enriquecedora.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 31

Inteligência Artificial Visual

Fezendo melhor
A imputação de valores ausentes é essencial no tratamento de conjuntos de dados incompletos,
impactando diretamente a qualidade das análises e a eficácia dos modelos de aprendizado de
máquina. A imputação pela média, mediana e moda são técnicas fundamentais nesse processo,
cada uma com suas especificidades e contextos de aplicação ideais. Utilizar a média para imputar
valores ausentes é comum em dados contínuos, substituindo os valores faltantes pelo valor médio
da variável. Essa abordagem é eficaz quando os dados ausentes são distribuídos aleatoriamente e
não há uma tendência de viés. No entanto, é sensível a outliers, podendo distorcer a imputação se a
distribuição dos dados for assimétrica.
A mediana, por sua vez, oferece uma alternativa robusta aos outliers, representando o valor
central de um conjunto de dados. Essa técnica é particularmente útil para dados com distribuições
assimétricas, garantindo que a imputação preserve a tendência central dos dados sem ser influenci-
ada por valores extremos. Para dados categóricos ou discretos, a imputação pela moda é a mais
indicada, substituindo os valores ausentes pela categoria ou valor mais frequente. Essa abordagem
mantém a distribuição original dos dados, sendo especialmente útil em situações onde existe uma
categoria dominante.
Cada método de imputação tem suas vantagens e limitações, e a escolha do método mais
adequado depende da natureza dos dados e do objetivo da análise. A compreensão detalhada
das características do conjunto de dados é crucial para a seleção da técnica de imputação mais
apropriada, assegurando a integridade e a confiabilidade dos resultados analíticos.
Se aplicarmos a técnica da média ou mediana a Tabela 2.1 a tabela resultante seria a Tabela
2.2 com os dados imputados. Veja que nesse caso, salvamos todas as linhas de dados com a
imputação.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 32

Inteligência Artificial Visual

Paciente Idade Nível de Glicose
Alice 28 90 mg/dL
Bruno 34.67 85 mg/dL
Carla 34 98.33 mg/dL
David 34.67 120 mg/dL
Eva 42 98.33 mg/dL
Tabela 2.2: Dados de Pacientes com Valores Ausentes após Imputação
Nesse exemplo, aplicamos a imputação pela média para tratar os valores ausentes (NaN) na
Tabela 2.1. Para as idades, calculamos a média das idades disponíveis (28, 34, 42), resultando
em 34.67. Da mesma forma, para o nível de glicose, a média dos valores disponíveis (90, 85, 120)
foi de 98.33 mg/dL. Os valores imputados estão destacados em vermelho e negrito para indicar
a modificação. Esta técnica de imputação permite manter a integridade do conjunto de dados,
minimizando o impacto da falta de informações e possibilitando uma análise estatística mais precisa.
Figura 2.3: Aplicação da técnica de imputação com o Orange Canvas
O widgetPreprocessnoOrange Canvasinclui uma opção específica para o tratamento de
valores ausentes, denominadaImpute Missing Values. Esta opção é visualmente representada na
interface do usuário e pode ser facilmente acessada e manipulada através de um simplesdrag-and-
drop(arrastar e soltar), conforme ilustrado na Figura 2.4 de como aplicar o tratamento de missing
values (dados faltantes) no Orange. Este método visual elimina a necessidade de codificação
manual, tornando o pré-processamento de dados mais acessível para usuários de todos os níveis de
habilidade. Ao selecionar oImpute Missing Values, são apresentados várias estratégias para lidar
com valores ausentes, permitindo a escolha do método mais adequado de acordo com a natureza
dos dados e o contexto da análise. As opções incluem:
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 33

Inteligência Artificial Visual

Média/Mais Frequente : Esta opção imputa valores ausentes substituindo-os pela média (para
variáveis contínuas) ou pelo valor mais frequente (para variáveis categóricas). É uma técnica
básica, mas eficaz, que pode ser aplicada quando não se espera que a ausência dos dados
esteja correlacionada com outras variáveis.
Substituir por Valor Aleatório : Esta estratégia substitui os valores ausentes por um valor
aleatório selecionado da distribuição dos dados existentes. Esta abordagem pode ser útil para
manter a distribuição geral dos dados, especialmente em casos onde a remoção de linhas
com valores ausentes resultaria na perda de uma grande parte do conjunto de dados.
Remover Linhas com Valores Ausentes : A opção mais direta, que simplesmente exclui
todas as linhas do conjunto de dados que contêm um ou mais valores ausentes. Embora esta
abordagem possa parecer atraente pela sua simplicidade, é importante considerar o impacto
potencial na representatividade e na integridade dos dados antes de optar por essa solução.
Cada uma dessas opções tem suas vantagens e limitações, e a escolha entre elas deve ser
guiada por uma consideração cuidadosa das características específicas do conjunto de dados em
análise e dos objetivos da pesquisa ou projeto.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 34

Inteligência Artificial Visual

2.4 O Que São Outliers e Seu Impacto nos Dados
Outlierssão pontos de dados que se desviam significativamente do padrão observado no conjunto
de dados. Esses valores atípicos podem surgir devido a variabilidade na medição, erros de entrada
de dados, ou podem indicar uma variação real no fenômeno estudado. O impacto dosoutliers
nos dados é profundo, pois podem levar a análises e interpretações errôneas. Por exemplo, em
estatísticas descritivas, um únicooutlierpode distorcer a média de um conjunto de dados, reduzindo
a representatividade da mediana e do modo. Além disso, osoutlierspodem afetar a distribuição dos
dados, levando a inferências estatísticas equivocadas que não refletem as verdadeiras características
da população ou do fenômeno em estudo.
No contexto de machine learning, osoutlierspodem ter efeitos adversos significativos nos
algoritmos e nos modelos resultantes. Muitos algoritmos de aprendizado de máquina são sensíveis
a variações nos dados de treinamento, o que significa queoutlierspodem levar a um modelo
sobreajustado (overfitting), onde o modelo aprende os ruídos nos dados de treinamento, incluindo
osoutliers, ao invés de generalizar a partir do padrão subjacente. Isso resulta em um modelo com
baixo desempenho em dados novos ou de teste. Portanto, a identificação e o tratamento adequados
dosoutlierssão etapas cruciais no pré-processamento de dados para aprendizado de máquina,
garantindo que os modelos sejam robustos, precisos e capazes de generalizar bem a partir de dados
novos.
Tem uma brincadeira e uma analogia direta que sempre faço com meus alunos para explicar
deforma visual e direta o que é Outlier (Anomalia). É a brincadeira do boneco assassino Chucky
(kkkk).
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 35

Inteligência Artificial Visual

Brincadeiras a parte, remover outlier é um pré-processamento importante em IA. O widgetOutliers
no Orange é uma ferramenta poderosa destinada à detecção de valores atípicos (outliers) em con-
juntos de dados. Ao contrário do tratamento de valores ausentes (missing values), que se encontra
no contexto de pré-processamento de dados, a detecção deoutliersé classificada sob o painel
"Unsupervised"no Orange, refletindo sua natureza de análise exploratória não supervisionada. Este
posicionamento enfatiza a importância de identificar observações que se desviam significativamente
do padrão geral dos dados, sem a necessidade de uma variável de resposta previamente definida.
O widgetOutliersoferece várias metodologias para a detecção deoutliers, permitindo a aplicação
de técnicas sofisticadas que variam de acordo com a natureza e a dimensionalidade dos dados.
Entre os métodos disponíveis estão oOne-Class SVM,Covariance Estimator,Local Outlier Factor
eIsolation Forest, cada um com parâmetros específicos que podem ser ajustados para otimizar
a detecção deoutliers. OLocal Outlier Factor, por exemplo, é eficaz em conjuntos de dados de
dimensão moderada, calculando um escore que reflete o grau de anormalidade das observações
com base na densidade local em relação aos seus vizinhos. Já oIsolation Foresté indicado para
conjuntos de dados de alta dimensão, isolando observações ao selecionar aleatoriamente um atributo
e então um valor de divisão entre os valores máximo e mínimo desse atributo selecionado.
Utilizar o widgetOutliersé simples e intuitivo: após a seleção do método e ajuste dos parâme-
tros desejados, os dados são processados para identificaroutlierseinliers(dados que não são
considerados atípicos). O resultado é um conjunto de dados anotado com uma variávelOutlier,
facilitando a análise subsequente e a tomada de decisões sobre como tratar essas observações
atípicas. Diferentemente da abordagem direta de tratamento de valores ausentes, a identificação de
outliersrequer uma análise mais detalhada e considerações sobre a possível remoção ou ajuste
desses pontos, dependendo do contexto específico da análise de dados ou dos objetivos do projeto
de machine learning.
A Figura 2.5, mostra a saída de conexão do widgetOutliersaoScatter Plotno Orange, um passo
crucial para a análise visual deoutliers. Após carregar os dados através do widgetFile, utilizamos o
widgetOutlierspara identificar os valores atípicos. A seguir, a conexão é estabelecida diretamente
arrastando-se os outputs deinlierseoutliersdo widgetOutlierspara oScatter Plotatravés da
interface de edição de links.
A identificação deoutliersé especialmente crítica no contexto de detecção de fraudes, onde esses
pontos atípicos podem representar atividades irregulares ou tentativas de fraude. Em muitos casos,
as fraudes se manifestam como padrões incomuns nos dados, diferenciando-se significativamente
das operações normais ou legítimas. Ao buscar poroutliers, analistas e sistemas de segurança
podem sinalizar transações, comportamentos ou padrões suspeitos para investigação adicional. Esta
abordagem não apenas ajuda a proteger recursos e ativos, mas também aprimora a precisão dos
modelos de detecção de fraude ao identificar e aprender com essas anomalias. Assim, a capacidade
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 36

Inteligência Artificial Visual

Figura 2.4: Aplicação da técnica de detecção de outliers com o Orange Canvas
de detectar efetivamenteoutlierstorna-se um componente essencial das estratégias de segurança e
monitoramento, contribuindo significativamente para a mitigação de riscos e a prevenção de perdas
financeiras.
Inliers
Quando você quiser excluir todos os outliers da usa análise, basta selecionar na conexão de saída
os dados inversos aos outliers, ou seja, selecione os "inliers"que são os dados que são importantes
para análise. A Figura 2.8 mostra o fluxo de pré-processamento que fizemos até agora.
2.5 Normalização e Padronização dos Dados
A normalização e padronização dos dados são etapas cruciais no pré-processamento de dados para
análise e modelagem em aprendizado de máquina. Essas técnicas ajustam a escala das variáveis,
permitindo que algoritmos que dependem da distância entre os pontos de dados operem de maneira
mais eficaz e justa. Sem essa etapa, variáveis com escalas significativamente diferentes podem
distorcer os resultados, fazendo com que algumas características tenham um peso desproporcional
na análise ou no modelo.
A normalização, frequentemente realizada através da escala min-max, transforma os dados para
que fiquem dentro de um intervalo específico, como 0 a 1. Este método é particularmente útil quando
sabemos que a distribuição dos dados não segue uma distribuição Gaussiana, ou quando não
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 37

Inteligência Artificial Visual

Figura 2.5: Conexão de saída do widget outlier
assumimos uma distribuição específica para os dados. Por outro lado, a padronização transforma os
dados para que tenham média zero e desvio padrão de um, seguindo a distribuição normal. Isso é
essencial para técnicas que assumem uma distribuição normal dos dados, ou para algoritmos que
são sensíveis à variação nos dados, como PCA (Análise de Componentes Principais).
Ambas as técnicas têm impacto significativo no desempenho dos algoritmos de aprendizado de
máquina. Por exemplo, algoritmos baseados em distância, como k-Nearest Neighbors (k-NN), e
algoritmos que utilizam gradiente descendente para encontrar o mínimo global, como redes neurais,
são diretamente afetados pela escala dos dados. Sem a normalização ou padronização, esses
algoritmos podem convergir lentamente ou convergir para soluções subótimas, comprometendo
a eficácia do modelo. Além disso, a normalização e padronização facilitam a interpretação dos
resultados. Ao padronizar os coeficientes de um modelo linear, por exemplo, é possível entender
a importância relativa de cada característica, já que todas estão na mesma escala. Isso permite
uma comparação direta entre os coeficientes, ajudando a identificar quais características têm mais
influência nas previsões do modelo.
Normalização e Padronização dos Dados no Orange
No Orange, a normalização e padronização dos dados são processos simplificados pelo widget
Preprocess, especificamente através da opçãoNormalize Features. Este widget fornece uma inter-
face intuitiva que permite aos usuários aplicar diferentes métodos de normalização e padronização
aos seus conjuntos de dados de maneira eficiente, sem a necessidade de codificação manual. Ao
selecionar esta opção, como mostrado na imagem, os usuários podem escolher entre várias técnicas
de escalonamento dos dados, cada uma adequada a diferentes necessidades de análise.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 38

Inteligência Artificial Visual

Figura 2.6: Conexão de saída dos dados tratados do widget outlier
Entre as opções disponíveis, encontram-se:
Padronizar para média μ= 0 , desvio padrão σ= 1: Esta técnica ajusta os dados de forma
que a média dos valores seja 0 e o desvio padrão seja 1, transformando os dados para seguir
uma distribuição normal. É particularmente útil para algoritmos que assumem que os dados
estão normalmente distribuídos.
Centralizar para média μ= 0: Simplesmente subtrai a média de cada característica de seus
valores, centralizando os dados em torno de 0 sem alterar seu desvio padrão.
Escalar para variância σ^2 = 1: Ajusta os dados de forma que a variância de cada caracterís-
tica seja 1, mantendo a média inalterada.
Normalizar para intervalo [−1, 1] ou [0, 1]: Escala os dados para que se ajustem a um
intervalo específico, mantendo a proporção dos valores. É útil quando os algoritmos requerem
que os dados estejam em uma escala limitada.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 39

Inteligência Artificial Visual

Figura 2.7: Normalização com widget Preprocess
Figura 2.8: Normalização com widget Preprocess
A escolha do método depende do algoritmo de machine learning a ser aplicado e da natureza dos
dados. Por exemplo, a padronização é frequentemente preferida para algoritmos sensíveis à escala
dos dados, como máquinas de vetor de suporte (SVMs) e redes neurais, enquanto a normalização
para um intervalo específico pode ser mais adequada para algoritmos que requerem entrada de
dados não negativos.
Após a seleção do método apropriado, basta arrastar e soltar a opção desejada para o fluxo de
trabalho, aplicando automaticamente a normalização ou padronização ao conjunto de dados. Esta
abordagem facilita a preparação dos dados, garantindo que sejam tratados de forma a maximizar o
desempenho dos modelos de aprendizado de máquina, tudo isso dentro de uma interface gráfica
amigável e acessível, característica do ambiente Orange.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 40

Inteligência Artificial Visual

2.6 Variáveis Categóricas
Variáveis categóricas são fundamentais em muitos conjuntos de dados, pois capturam características
qualitativas dos dados, como gênero, tipo de produto, ou nível de satisfação. Essas variáveis podem
ser cruciais para a análise, fornecendo informações ricas que ajudam a explicar variações nos dados
ou a prever resultados. Por exemplo, a categoria de um produto pode influenciar significativamente
seu preço ou popularidade, tornando a variável categórica um preditor valioso em modelos de
previsão. Para incluir variáveis categóricas em análises e modelos preditivos, é comum aplicar
técnicas de codificação que transformam essas variáveis em formatos numéricos. Algumas das
técnicas mais comuns incluem:
Codificação One-Hot : Cria novas colunas para cada categoria de uma variável, onde cada
coluna corresponde a uma categoria e contém 1 se a observação pertence àquela categoria e 0 caso
contrário. Embora eficaz, essa abordagem pode aumentar significativamente a dimensionalidade do
conjunto de dados, especialmente com variáveis de muitas categorias.
Codificação Ordinal : Atribui um valor numérico único a cada categoria, com base em sua ordem
ou classificação. Esta técnica é útil para variáveis ordinais, mas deve ser usada com cuidado para
variáveis nominais, pois pode introduzir uma ordem artificial que não existe.
Codificação de Frequência ou de Contagem : Substitui as categorias pela frequência ou
contagem de suas ocorrências no conjunto de dados. Isso pode ajudar a destacar a importância
relativa das categorias com base em sua prevalência.
Aplicando essas técnicas, as variáveis categóricas podem ser efetivamente incorporadas em
modelos de machine learning, permitindo que os algoritmos aproveitem essas informações impor-
tantes. No entanto, é crucial escolher a técnica de codificação apropriada, considerando o tipo de
variável (nominal ou ordinal) e o impacto na dimensionalidade dos dados, para evitar a maldição da
dimensionalidade ou a introdução de viés nos modelos.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 41

Inteligência Artificial Visual

One-hot-encoding no Orange
One-hot-encoding é com certeza a técnica mais usada no tratamento de colunas com dados
categóricos. A Figura 2.9 demonstra a aplicação doone-hot encodingem uma variável categórica no
ambiente do Orange, transformando uma única coluna categórica em múltiplas colunas numéricas.
Este processo é essencial para preparar dados categóricos para análises e modelos de machine
learning que exigem entrada numérica. A variável categórica em questão, denominada "status",
possui categorias distintas representadas originalmente em uma única coluna. Através doone-hot
encoding, cada categoria única dessa variável é convertida em uma nova coluna binária, onde
"1"indica a presença da categoria e "0"sua ausência.
Figura 2.9: One-hot-encoding no Orange Canvas
No exemplo da Figura 2.9, a variável categórica "status"é transformada em quatro novas colunas:
"status=crew", "status=first", "status=second"e "status=third". Cada uma dessas colunas corresponde
a uma categoria da variável original e recebe um valor binário que reflete se a instância pertence
à categoria representada pela coluna. Esse método permite que modelos de machine learning
interpretem e utilizem efetivamente as informações contidas nas variáveis categóricas, tratando cada
categoria como uma característica independente.
A aplicação doone-hot encodingé realizada no Orange utilizando o widgetContinuize, onde a
opção "One-hot encoding"é selecionada. Este procedimento simplifica o tratamento de variáveis
categóricas, eliminando a necessidade de codificação manual complexa e facilitando a inclusão
dessas variáveis em análises subsequentes. Após a transformação, os dados estão prontos para
serem utilizados em diversos algoritmos de aprendizado de máquina, garantindo que a informação
categórica seja adequadamente considerada na modelagem.
Este exemplo ilustra não apenas a facilidade e eficiência doone-hot encodingno Orange, mas
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 42

Inteligência Artificial Visual

também destaca a importância de transformar variáveis categóricas para análises numéricas. Ao
converter categorias em formatos numéricos binários, o Orange permite aos usuários explorar
plenamente o potencial de seus dados, facilitando a descoberta de padrões e a construção de
modelos preditivos precisos e robustos.
2.7 Análise de Componentes Principais (PCA)
A Análise de Componentes Principais (PCA) é uma técnica estatística poderosa utilizada para redu-
ção de dimensionalidade, facilitando o entendimento e a análise de conjuntos de dados complexos.
Em essência, o PCA busca transformar o conjunto de dados original, possivelmente correlacio-
nado, em um conjunto de valores de variáveis linearmente não correlacionadas conhecidas como
componentes principais. Este processo é fundamental quando se lida com a "maldição da dimensio-
nalidade", um fenômeno que descreve como o aumento do número de variáveis (dimensões) pode
levar a dificuldades na organização e na análise dos dados, além de aumentar significativamente
o custo computacional. Ao reduzir a dimensionalidade, o PCA ajuda a mitigar esses problemas,
preservando ao mesmo tempo a maior parte da variação presente no conjunto de dados original.
A importância do PCA estende-se por várias áreas de aplicação, desde a visualização de dados
até o aprimoramento de modelos de aprendizado de máquina. Ao identificar os componentes
principais que capturam a maior variação nos dados, analistas e cientistas de dados podem eliminar
variáveis menos significativas, reduzindo o ruído e focando nas características mais impactantes.
Isso não apenas simplifica a análise visual dos dados, mas também melhora o desempenho e a
precisão dos algoritmos de aprendizado de máquina ao eliminar redundâncias e destacar as relações
fundamentais entre as variáveis.
O PCA deve ser usado quando se deseja entender a estrutura subjacente dos dados, quando
se necessita reduzir o número de variáveis mas manter as informações cruciais, ou quando se
prepara dados para algoritmos de aprendizado de máquina, especialmente em casos de alta
dimensionalidade. No entanto, é crucial reconhecer que, ao reduzir a dimensionalidade, alguma
informação é inevitavelmente perdida. Portanto, a aplicação do PCA deve ser cuidadosamente
considerada e equilibrada com a necessidade de preservar a integridade dos dados originais. A
"maldição da dimensionalidade"representa um desafio significativo na análise de dados, mas com
técnicas como o PCA, é possível explorar dados complexos de maneira mais eficaz, identificando
padrões e tendências que seriam difíceis de detectar em espaços de alta dimensão.
O PCA (Análise de Componentes Principais) inicia sua abordagem de redução de dimensio-
nalidade pelo cálculo da matriz de covariância dos dados. Esta etapa é crucial, pois a matriz de
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 43

Inteligência Artificial Visual

covariância destila as relações entre todas as variáveis no conjunto de dados, destacando como as
variações em uma variável estão associadas às variações em outra. Matematicamente, se temos
um conjunto de dados com N variáveis, a matriz de covariância será uma matriz N x N onde cada
elemento representa a covariância entre um par de variáveis. Esta matriz captura a essência da
estrutura de variação dos dados, fornecendo a base para identificar as direções (ou eixos principais)
que retêm a maior parte da variação nos dados.
A seguir, o método procede com a decomposição espectral (ou análise de autovalores) da
matriz de covariância. Este processo envolve encontrar os autovalores e os autovetores da matriz
de covariância. Os autovetores representam as direções ou componentes principais no espaço
de dados original, enquanto os autovalores correspondem à quantidade de variação capturada
por cada um desses componentes. Ordenando os autovetores de acordo com seus autovalores
correspondentes, do maior para o menor, podemos então identificar as principais direções nas
quais os dados variam. Este passo é fundamental, pois permite que se identifique quais dimensões
(componentes principais) são mais significativas e quais podem ser descartadas sem perder muita
informação.
Finalmente, a redução da dimensionalidade é realizada projetando os dados originais nas direções
dos autovetores selecionados (os componentes principais). Na prática, isso é feito multiplicando
os dados originais pela matriz contendo os autovetores escolhidos. Este passo transforma os
dados de seu espaço original de alta dimensão para um novo espaço de menor dimensão, onde as
variáveis são agora os componentes principais que foram identificados. Essencialmente, ao invés de
representar os dados em termos de suas variáveis originais, agora representamos em termos de
suas principais componentes lineares, que são uma combinação linear das variáveis originais. Este
novo espaço de características reduzido retém a maior parte da informação dos dados originais, mas
com uma quantidade significativamente menor de dimensões, facilitando análises subsequentes e
visualizações.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 44

Inteligência Artificial Visual

PCA no Orange
No ambiente do Orange Canvas, a aplicação da Análise de Componentes Principais (PCA) é
realizada de maneira intuitiva e visual, conforme ilustrado na Figura 2.10. O widget PCA, encontrado
sob a categoria "Unsupervised", permite aos usuários executar a redução de dimensionalidade em
seus conjuntos de dados com facilidade. A interface do widget oferece opções para selecionar o
número de componentes principais desejados ou determinar a quantidade de variância explicada
que se pretende alcançar. Este último é particularmente útil, pois permite que os usuários ajustem o
número de componentes principais com base em um critério de variância explicada, como 92% no
exemplo da figura, focando assim nas direções mais significativas dos dados.
Figura 2.10: Aplicação do PCA no Orange Canvas.
A interface do widget PCA também inclui opções para normalizar as variáveis antes da análise, um
passo crítico para garantir que cada variável contribua igualmente para a análise, independentemente
de suas escalas originais. Após a configuração e execução do PCA, o widget exibe um gráfico de
variância explicada, que mostra tanto a variância explicada acumulada quanto a variância de cada
componente principal individualmente. Este gráfico é essencial para entender quantos componentes
são necessários para capturar a maior parte da informação contida nos dados. Com o Orange
Canvas, a complexidade da redução de dimensionalidade é simplificada, permitindo que até usuários
não especialistas em matemática apliquem técnicas avançadas de análise de dados como o PCA
em seus projetos.
Demorou mas acabou
Neste capítulo, exploramos a importância e as técnicas fundamentais do pré-processamento de
dados, uma etapa essencial no ciclo de vida de qualquer projeto de análise de dados ou aprendizado
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 45

Inteligência Artificial Visual

de máquina. Desde a limpeza de dados, tratamento de valores ausentes, até a normalização e
padronização, cada processo é projetado para aprimorar a qualidade dos dados, garantindo que os
modelos de IA sejam alimentados com informações precisas e relevantes. Este pré-processamento
não apenas aumenta a eficácia dos modelos, mas também contribui significativamente para a
precisão das previsões, destacando a interconexão entre dados de qualidade e resultados confiáveis.
Além disso, abordamos a identificação e tratamento de outliers, técnicas essenciais para refinar
ainda mais os dados, removendo ou ajustando valores que poderiam distorcer análises subsequen-
tes. A introdução à Análise de Componentes Principais (PCA) enfatizou a capacidade de reduzir a
dimensionalidade dos dados, mantendo a maior parte da informação valiosa, uma técnica particular-
mente útil para combater a maldição da dimensionalidade e melhorar a eficiência dos modelos de
aprendizado de máquina. Através destas técnicas, demonstramos como o pré-processamento pode
transformar dados brutos em um recurso mais manejável e informativo.
Pré-processar dados é demorado mesmo, mas o uso do Orange Canvas ao longo deste capítulo
não apenas facilitou a aplicação prática dessas técnicas de pré-processamento, mas também
demonstrou ser uma ferramenta valiosa para visualizar e entender o impacto dessas transformações
nos dados, que permite que mesmo os não especialistas explorem complexidades de dados com
confiança, reforçando o valor de uma preparação de dados meticulosa.
3.4 Exercícios
Tratamento de Valores Ausentes: Com um novo conjunto de dados carregado no Orange
Canvas, utilize o widgetPreprocesspara abordar valores ausentes. Experimente diferentes
métodos de imputação disponíveis no widget e compare os resultados. Discuta como cada
método afetou a qualidade dos dados e sua potencial influência em análises futuras.
Identificação e Tratamento de Outliers: Explore o widgetOutlierspara identificar e tratar
outliers em um conjunto de dados. Aplique diferentes estratégias de detecção e avalie como a
remoção ou ajuste dos outliers influencia a distribuição dos dados. Reflita sobre a importância
de tratar outliers antes de proceder com análises mais avançadas.
Normalização e Padronização de Dados: Utilize o widgetPreprocesspara normalizar e
padronizar um conjunto de dados. Aplique ambos os métodos separadamente e juntos, obser-
vando as mudanças no conjunto de dados resultante. Analise o impacto dessas transformações
na preparação dos dados para modelos de aprendizado de máquina.
Redução de Dimensionalidade com PCA: Aplique o widgetPCAa um conjunto de dados
carregado através do widgetFile. Ajuste o número de componentes principais para capturar
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 46

Inteligência Artificial Visual

uma certa porcentagem da variância explicada. Explore visualmente o impacto da redução de
dimensionalidade nos dados e discuta como o PCA pode facilitar a análise e modelagem de
dados complexos.
CAPÍTULO 2. PRÉ-PROCESSAMENTO DE DADOS 47

Inteligência Artificial Visual

CAPÍTULO 3
3 Crie sua Inteligência Artificial
A inteligência artificial (IA) transformou-se de um nicho de pesquisa acadêmica para uma força
onipresente na vida moderna, impulsionando inovações em setores tão diversos quanto saúde,
finanças, manufatura e entretenimento. No cerne desta revolução encontra-se o aprendizado de
máquina (machine learning), um subcampo da IA que permite que os sistemas aprendam e melhorem
a partir da experiência sem serem explicitamente programados. Este capítulo explora como você
pode começar a criar sua própria inteligência artificial, utilizando os princípios e técnicas de machine
learning disponíveis atualmente.
O aprendizado de máquina utiliza algoritmos para analisar dados, aprender com eles e então
fazer previsões ou decisões sem intervenção humana. Diferentes tipos de algoritmos de aprendizado
supervisionado, não supervisionado, semi-supervisionado e por reforço - fornecem um vasto leque
de possibilidades para abordar praticamente qualquer problema de dados. A escolha do algoritmo
certo depende da natureza dos seus dados e do problema específico que você está tentando resolver.
A compreensão desses fundamentos é essencial para qualquer pessoa que deseje entrar no campo
da IA.
Nos dias atuais, a acessibilidade às ferramentas de machine learning nunca foi tão grande.
Plataformas de código aberto como TensorFlow, PyTorch, e scikit-learn oferecem os blocos de
construção necessários para projetar, treinar e implementar modelos de machine learning. Além
disso, serviços em nuvem como AWS, Microsoft Azure e Google Cloud proporcionam infraestruturas
poderosas e escaláveis para treinar modelos complexos, lidando com grandes volumes de dados.
Para criar sua IA, o primeiro passo é definir claramente o problema que você deseja resolver. Isso
pode variar desde a previsão de tendências de mercado, diagnóstico de doenças até a automação
de tarefas rotineiras. Com um problema bem definido, o próximo passo é reunir e preparar seus
dados. Como discutido anteriormente, o pré-processamento de dados é uma etapa crítica, pois
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 48

Inteligência Artificial Visual

dados de alta qualidade são fundamentais para treinar um modelo eficaz.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 49

Inteligência Artificial Visual

O processo de modelagem começa com a seleção do algoritmo apropriado e a configuração de
seus parâmetros, uma etapa conhecida como tuning. O treinamento do modelo é então realizado
usando um conjunto de dados, com o modelo aprendendo a fazer previsões ou tomar decisões com
base nesses dados. Este processo é iterativo, com o modelo sendo refinado continuamente até que
seu desempenho seja satisfatório.
Após o treinamento, o modelo deve ser testado em um conjunto de dados separado para avaliar
sua performance em cenários do mundo real. Este passo é crucial para garantir que o modelo
seja generalizável e não apenas memorize os dados de treinamento, um problema conhecido
como overfitting. A avaliação do modelo ajuda a identificar quaisquer deficiências e orienta ajustes
adicionais para melhorar a precisão.
Por fim, uma vez satisfeito com o desempenho do modelo, o último passo é implementá-lo em
um ambiente de produção, onde pode começar a fornecer insights, fazer previsões ou automatizar
tarefas. A implementação bem-sucedida de um modelo de machine learning pode transformar
operações empresariais, impulsionar a inovação e oferecer vantagens competitivas significativas.
Assim, com as ferramentas e técnicas disponíveis hoje, criar sua própria inteligência artificial está
mais acessível do que nunca, abrindo um mundo de possibilidades para explorar e inovar.
Quem pode fazer IA?
Hoje em dia, a inteligência artificial (IA) está ao alcance de todos, não só dos cientistas de dados ou
dos engenheiros de software. Profissionais de diversas áreas, como médicos, advogados, cientistas
sociais, educadores e até artistas, estão descobrindo como a IA pode ajudar a resolver problemas
complexos em suas áreas de atuação. Essas pessoas têm um conhecimento profundo dos desafios
específicos de seus campos e, por isso, estão em uma posição única para identificar as melhores
oportunidades para aplicar soluções de IA.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 50

Inteligência Artificial Visual

Esses profissionais não precisam ser especialistas em tecnologia para criar ou utilizar ferramentas
de IA. Com plataformas amigáveis como oOrange Canvas, eles podem construir modelos de IA
personalizados para suas necessidades específicas sem escrever uma linha de código. Isso significa
que médicos podem desenvolver sistemas para diagnosticar doenças com mais precisão, advogados
podem automatizar a análise de grandes volumes de documentos legais, e cientistas sociais podem
analisar grandes conjuntos de dados para identificar padrões e tendências.
O mais importante é que esses profissionais, sendo os detentores dos problemas, tornam-se
peças centrais em qualquer equipe de desenvolvimento de IA. Eles trazem uma compreensão
profunda das questões que precisam ser resolvidas e podem orientar o desenvolvimento de soluções
de IA para garantir que elas sejam verdadeiramente úteis e eficazes. Ao combinar seu conhecimento
especializado com as ferramentas de IA, eles podem inovar em suas áreas, melhorando a eficiência,
a precisão e a qualidade do seu trabalho.
Tipos de Machine Learning
A aprendizagem supervisionada é um dos pilares do machine learning, caracterizando-se pelo
treinamento de um modelo em um conjunto de dados etiquetado, onde a resposta correta é conhecida.
O objetivo é que o modelo aprenda a mapear entradas para saídas esperadas, facilitando a previsão
de respostas para dados nunca vistos antes. Esse tipo de aprendizagem é amplamente utilizado em
aplicações como reconhecimento de fala, diagnóstico médico e análise de crédito, onde a relação
entre os dados de entrada e a etiqueta (ou resposta) é fundamental. O grande desafio aqui é construir
um conjunto de dados de treinamento suficientemente abrangente e representativo, garantindo que
o modelo possa generalizar bem para novos exemplos.
Por outro lado, a aprendizagem não supervisionada lida com dados que não possuem etiquetas,
significando que o sistema tenta aprender a estrutura ou padrões a partir dos dados sem orientação
explícita. Este tipo de aprendizado é ideal para descobrir agrupamentos ocultos, identificar ano-
malias ou reduzir a dimensionalidade dos dados para visualização. Técnicas como agrupamento
(clustering) e redução de dimensionalidade são comuns neste domínio e são especialmente úteis
para explorar grandes conjuntos de dados e identificar estruturas ou relações significativas que não
são imediatamente aparentes.
A aprendizagem por reforço, uma área fascinante e em rápido crescimento do machine learning,
difere dos tipos supervisionado e não supervisionado ao focar na maneira como os agentes devem
agir em um ambiente para maximizar algum conceito de recompensa cumulativa. Inspirado pela
maneira como os seres humanos e os animais aprendem a partir das consequências de suas
ações, esse modelo envolve um agente, um conjunto de estados e ações e recompensas. O agente
aprende a tomar decisões executando ações e recebendo feedback na forma de recompensas ou
penalidades. Este tipo de aprendizado é a base de sistemas de recomendação personalizados,
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 51

Inteligência Artificial Visual

jogos de inteligência artificial e robótica autônoma, onde o objetivo é desenvolver políticas de ação
que maximizem a recompensa ao longo do tempo.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 52

Inteligência Artificial Visual

O Paniel Model
O painel Model é o painel de Aprendizagem supervisionada no Orange Canvas.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 53

Inteligência Artificial Visual

Figura 3.1: Painel Transform do Orange Canvas
Constant: Este widget faz previsões usando a classe mais
frequente ou o valor médio do conjunto de treinamento. É uma
base para comparação com modelos mais complexos.
CN2 Rule Induction: Usa o algoritmo CN2 para induzir re-
gras de classificação dos dados. O CN2 é eficaz mesmo em
contextos com dados ruidosos, produzindo regras simples e
compreensíveis.
Calibrated Learner: Envolve outro aprendiz com calibração
de probabilidade e otimização do limiar de decisão para ta-
refas de classificação binária, ajustando a distribuição das
probabilidades das classes.
kNN (k-Nearest Neighbors): Classifica novas instâncias com
base na proximidade com os exemplos mais próximos do
conjunto de treinamento, sendo eficaz para uma variedade de
problemas.
Tree (Decision Tree): Cria modelos na forma de árvores
de decisão, utilizando decisões lógicas sobre os atributos
para dividir os dados em subconjuntos. É intuitivo e fácil de
interpretar.
Random Forest: Melhora a robustez e reduz o overfitting por
meio da agregação dos resultados de múltiplas árvores de
decisão, formando um "ensemble".
Gradient Boosting: Constrói um modelo forte a partir de
modelos fracos de forma sequencial, ajustando cada novo
modelo para corrigir os erros dos anteriores.
SVM (Support Vector Machines): Encontra o hiperplano
ótimo de separação entre as classes, sendo eficaz para pro-
blemas tanto de classificação quanto de regressão.
Linear Regression: Modela a relação entre uma variável
dependente contínua e variáveis independentes, ideal para
entender influências variadas.
Logistic Regression: Usada para prever a probabilidade de
uma variável dependente categórica com base em variáveis
independentes, adequada para classificação binária.
Naive Bayes: Um classificador probabilístico baseado no
Teorema de Bayes, rápido e eficiente, especialmente para
dados de alta dimensão.
AdaBoost: Combina múltiplos classificadores fracos para
criar um modelo forte, ajustando os pesos dos exemplos com
base nos erros dos classificadores anteriores.
Curve Fit: Ajusta uma função aos dados de entrada, uti-
lizando scipy.curve_fit para otimizar parâmetros da função,
adequado para regressão.
Neural Network: Constrói e treina redes neurais artificiais,
modelos inspirados pelo cérebro humano capazes de apren-
der tarefas complexas.
Stochastic Gradient Descent: Minimiza uma função de
perda com uma aproximação estocástica do gradiente des-
cendente, útil para grandes conjuntos de dados.
Stacking: Combina as previsões de múltiplos modelos para
fazer uma previsão final, melhorando a precisão e robustez.
Save Model: Permite salvar modelos treinados para uso pos-
terior, facilitando a reutilização em diferentes contextos.
Load Model: Habilita o carregamento de modelos salvos, per-
mitindo aplicação rápida a novos dados sem re-treinamento.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 54

Inteligência Artificial Visual

3.1 Marketing e Inteligência Artificial
No mundo acelerado do marketing moderno, as empresas enfrentam o desafio contínuo de identificar
e atingir o público certo com a mensagem certa no momento certo. Neste contexto, o marketing não é
apenas uma arte; é também uma ciência que combina criatividade com análise de dados para prever
comportamentos, personalizar mensagens e otimizar resultados. A ascensão da inteligência artificial
(IA) revolucionou essa área, oferecendo ferramentas e técnicas que permitem uma compreensão
mais profunda e uma tomada de decisão mais informada.
O problema que enfrentamos no universo do marketing digital é um de classificação e predição:
Como podemos prever se um cliente irá responder positivamente a uma campanha de marketing?
Esta questão está no coração de muitas estratégias de marketing, pois a capacidade de identificar
previamente os clientes mais prováveis de responder pode resultar em uma alocação de recursos
mais eficiente, maior retorno sobre o investimento e campanhas mais personalizadas e eficazes.
É aqui que entra nosso conjunto de dados de marketing e as ferramentas de IA, como o Orange
Canvas. Ao analisar os padrões nos dados dos clientes, podemos construir modelos preditivos
que nos ajudam a entender as características dos clientes que respondem às campanhas. Este
conhecimento não só melhora a eficácia das campanhas futuras, mas também contribui para uma
experiência mais personalizada e satisfatória para o cliente. Portanto, o desafio de classificação no
marketing não é apenas uma questão de vendas; é também uma questão de construir relações mais
fortes e significativas entre as empresas e seus clientes.
Neste capítulo, exploraremos um conjunto de dados de marketing com o objetivo de resolver um
problema de classificação utilizando o Orange Canvas. Um problema de classificação envolve prever
a qual de duas ou mais categorias (ou classes) uma nova observação pertence, com base em um
conjunto de dados de treinamento. No nosso caso, o objetivo é prever se um cliente responderá
positivamente a uma campanha de marketing (Resposta = 1) ou não (Resposta = 0).
O Conjunto de Dados de Marketing
O conjunto de dados que analisaremos contém informações sobre clientes de uma empresa. As
informações incluem dados demográficos, hábitos de consumo e histórico de interações com
campanhas anteriores de marketing. A Tabela 3.1 descreve cada uma das colunas presentes no
conjunto de dados:
Este conjunto de dados é rico e multifacetado, oferecendo uma excelente oportunidade para
explorar diferentes técnicas de classificação. As variáveis numéricas incluem características como
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL^55

Inteligência Artificial Visual

COLUNA DESCRIÇÃO TIPO
Ano_Nascimento Ano de nascimento do cliente Numérica
Renda Renda anual do cliente (em dólares) Numérica
Criancas_Casa Número de crianças na casa do cliente Numérica
Adolescentes_Casa Número de adolescentes na casa do cliente Numérica
Dias_Ultima_Compra Número de dias desde a última compra Numérica
Gasto_Vinhos Gastos anuais em vinho Numérica
Gasto_Frutas Gastos anuais em frutas Numérica
Gasto_Carne Gastos anuais em carne Numérica
Gasto_Peixe Gastos anuais em peixe Numérica
Gasto_Doces Gastos anuais em doces Numérica
Gasto_Ouro Gastos anuais em produtos de ouro Numérica
Num_Compras_Promocao Número de compras feitas com desconto Numérica
Num_Compras_Web Número de compras feitas através do website Numérica
Num_Compras_Catalogo Número de compras feitas usando um catálogo Numérica
Num_Compras_Loja Número de compras feitas diretamente nas lojas Numérica
Num_Visitas_Web_Mes Número de visitas ao website da empresa por mês Numérica
Educacao Nível de educação do cliente (PhD,Master,Graduation,Basic) Categórica
Estado_Civil Estado civil do cliente (Single,Married,Together, etc.) Categórica
Resposta Se o cliente respondeu à última campanha (1: sim, 0: não) Categórica (Alvo)
Tabela 3.1: Descrição das colunas do conjunto de dados de marketing
’Ano_Nascimento’, ’Renda’, ’Gastos’ em diferentes categorias, entre outras, que podem ser usadas
para construir modelos preditivos. As variáveis categóricas, como ’Educacao’ e ’Estado_Civil’, ajudam
a entender o contexto e o background dos clientes, podendo ser fundamentais na segmentação de
mercado e na personalização de campanhas.
No contexto da classificação, a variável alvo denominada ’Resposta’ desempenha um papel
crucial, pois indica se um cliente reagiu positivamente à campanha de marketing, isto é, se
realizou a compra do produto promovido. O objetivo central da nossa análise é desenvolver um
modelo preditivo capaz de antecipar a probabilidade de futuros clientes adquirirem um produto em
decorrência de uma campanha de marketing. Esta previsão nos permite otimizar a alocação de
recursos em campanhas, direcionando-as de maneira mais assertiva e eficiente para os segmentos
de clientes mais propensos à conversão.
Fluxo do Dataset de Marketing no Orange
Dataset URL - Github: https://bit.ly/sandeco-orange-marketing
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 56

Inteligência Artificial Visual

Figura 3.2: Abrindo dados de Marketing no Orange
Para começar devemos usar o widget FILE. A Figura 4.1 mostra que o Orange identificou 2798
instâncias (ou registros) e 27 características (ou atributos) na base de dados carregada. Nota-se
que o software não detectou automaticamente uma variável alvo (target variable), que é essencial
para tarefas de aprendizado supervisionado, onde um modelo aprende a prever uma saída baseada
em entradas fornecidas.
a coluna "Resposta"é inicialmente definida como um atributo categórico com os valores 0 e
Entretanto, o tipo dessa coluna deve ser alterado para "target". "Resposta"deverá ser usada
como a variável alvo na tarefa de classificação binária, onde o modelo tentará prever se um cliente
responderá positivamente (1) ou não (0) a uma campanha de marketing, baseado nos demais
atributos presentes na base de dados.
A mudança do tipo de dados da coluna "Resposta"para "target"é um passo importante no
processo de configuração do Orange para análise de dados, pois direciona o software a considerar
essa coluna como o que se deseja prever, e não apenas mais uma característica entre as muitas
que descrevem os dados. Isso permite a aplicação de algoritmos de aprendizado de máquina que
necessitam da distinção entre atributos de entrada (features) e a saída que se deseja aprender a
prever (target).
Na Figura 3.3, o processo de seleção de colunas de dados no Orange é ilustrado de forma clara.
Observe que a colunaIDdeve ser movida para a área de "Ignored". Para fazer isso, clique e arraste
a colunaIDda seção "Features"para "Ignored", conforme demonstrado pelo cursor em forma de
mão. Este passo é crucial, pois a colunaIDé um identificador único para cada registro e não carrega
informação preditiva que seja útil ao modelo de machine learning. Dados assim são ruídos. Omitir
a colunaIDgarante que o modelo irá aprender apenas dos atributos relevantes, evitando assim a
introdução de viés que poderia prejudicar a generalização do modelo para novos dados.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL^57

Inteligência Artificial Visual

Figura 3.3: Excluindo ID da análise
Convertendo colunas com widget Fórmula
Na Figura 3.4, abordamos um conceito crucial no processamento de dados para análise: a trans-
formação de dados brutos em informações significativas. Neste exemplo específico, discutimos
a coluna "Ano_Nascimento"em nosso conjunto de dados. Embora esta coluna forneça informa-
ções valiosas, ela não é imediatamente informativa para análises relacionadas à idade atual dos
indivíduos. Converter o "Ano_Nascimento"em "Idade"é um passo fundamental para obter insights
mais relevantes, pois a idade atual oferece uma perspectiva mais direta sobre o estado atual e as
possíveis necessidades ou comportamentos dos indivíduos.
Para converter o "Ano_Nascimento"em "Idade", utilizamos o widgetFormulano Orange (nesse
caso é Fórmula em inglês, sem acento mesmo), uma ferramenta poderosa que permite calcular
novas colunas combinando as existentes com uma expressão definida pelo usuário. O processo
é simples e altamente intuitivo, permitindo aos usuários adicionar novas funcionalidades ao seu
conjunto de dados sem a necessidade de conhecimento avançado em programação.
Primeiramente, abra o widgetFormulae insira um nome para a nova característica que deseja
criar, neste caso, "idade".
No campo de expressão, digite a fórmula para calcular a idade, que é2024-Ano_Nascimento.
Essa expressão subtrai o ano de nascimento do ano atual (assumindo que o ano atual é 2024)
para calcular a idade da pessoa.
Após definir a expressão, clique emSendpara aplicar as mudanças. A nova coluna "idade"será
adicionada ao seu conjunto de dados, refletindo a idade atual de cada indivíduo baseada no
ano de nascimento.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 58

Inteligência Artificial Visual

Figura 3.4: Aplicando tranformação e com "Formula"
Este procedimento destaca a flexibilidade e a eficácia do Orange para a manipulação e trans-
formação de dados. A habilidade de criar novas colunas através de expressões definidas pelo
usuário abre um leque de possibilidades para a análise de dados, tornando oFormulaum widget
indispensável para cientistas de dados, pesquisadores e analistas.
Lembre-se de que, ao trabalhar com variáveis numéricas noFormula, basta fornecer um nome e
uma expressão conforme demonstrado. Este processo não apenas simplifica a criação de novas
características mas também incentiva a exploração e a experimentação com diferentes tipos de
transformações de dados para alcançar insights mais profundos e significativos. Após criar a coluna
idade, exclua a coluna usando o widget "Select Columns"como mostra a Figura 3.5.
Figura 3.5: Excluido coluna Ano_Nascimento
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 59

Inteligência Artificial Visual

Na Figura 3.6 acionamos a detecção de "Outliers"configurado para aplicar o algoritmo Isolation
Forest. O algoritmo Isolation Forest é uma técnica eficaz para a detecção de outliers, ou anomalias,
em um conjunto de dados. A ideia central do algoritmo é "isolar"observações individuais escolhendo
aleatoriamente uma característica (feature) e, em seguida, um valor de divisão também aleatório
entre os valores máximo e mínimo dessa característica selecionada. A estrutura de árvore resultante
do particionamento recursivo reflete o número de divisões necessárias para isolar uma amostra, o
que é conhecido como comprimento do caminho na árvore, desde o nó raiz até o nó terminal. Este
comprimento do caminho, quando médio em uma floresta de tais árvores aleatórias, torna-se uma
medida da normalidade e da função de decisão do algoritmo.
Figura 3.6: Aplicando detecção de outlier
O que torna o Isolation Forest particularmente eficiente é que ele geralmente requer um número
menor de divisões para isolar amostras que são consideradas anomalias, em comparação com
amostras normais. Portanto, quando uma floresta de árvores aleatórias produz consistentemente
caminhos mais curtos para determinadas amostras, estas são consideradas com alta probabilidade
de serem anomalias. Como tal, o Isolation Forest é particularmente adequado para conjuntos de
dados com uma grande quantidade de características e pode ser usado em ambientes de big data.
Na configuração do algoritmo indicamos uma contaminação (a proporção esperada de outliers no
conjunto de dados) está definida para 10%, e a opção "Replicable training"está marcada, garantindo
que os resultados sejam replicáveis em futuras execuções.
Você pode perguntar: "Por que definir 10% na contaminação?". Ao definir o parâmetro de
contaminação, você está essencialmente orientando o modelo sobre quantos dos dados você
suspeita que sejam outliers. Por exemplo, uma contaminação de 10% sugere que você espera que
cerca de 10% do seu conjunto de dados seja composto por anomalias. O algoritmo utiliza essa
informação para ajustar o limiar no qual um ponto de dados é considerado anômalo, baseado no
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 60

Inteligência Artificial Visual

comprimento do caminho descrito anteriormente: pontos de dados que têm um comprimento de
caminho mais curto do que o esperado (com base na taxa de contaminação definida) serão marcados
como anomalias. Você deve ajustar esse hiperparâmetro e verificar a alteração da eficiência do
seu modelo empiricamente. Isso é particularmente importante porque diferentes conjuntos de
dados podem ter diferentes taxas de outliers, e ajustar a contaminação pode ajudar a otimizar o
desempenho do algoritmo para identificar corretamente as anomalias dentro de um conjunto de
dados específico.
3.2 Hora de treinar sua Rede Neural
As redes neurais são um pilar fundamental na área de inteligência artificial, representando uma
abordagem inspirada pela complexa rede de neurônios presente no cérebro humano. Essa analogia
biológica serve como base para o desenvolvimento de algoritmos capazes de realizar tarefas de
reconhecimento de padrões, classificação, e aprendizado de máquina de forma geral. A concepção
das redes neurais data da década de 1940, com o modelo de neurônio artificial proposto por Warren
McCulloch e Walter Pitts, que já indicava a capacidade dessas estruturas de realizar computações
simples baseadas em lógica booleana.
Com o passar dos anos, o campo das redes neurais se expandiu significativamente, principal-
mente a partir da década de 1980, quando o conceito de redes neurais com múltiplas camadas
ocultas e o algoritmo de retropropagação foram introduzidos. Esses avanços permitiram que as
redes neurais aprendessem a partir de exemplos complexos, ajustando seus parâmetros internos
(ou pesos) para minimizar a diferença entre as saídas previstas e as reais. Isso marcou o início da
era das redes neurais profundas, que são capazes de capturar relações de alta complexidade nos
dados.
A inspiração por trás das redes neurais vem da observação de como o cérebro humano processa
informações. Neurônios no cérebro se comunicam por meio de impulsos elétricos, e essa interação
entre neurônios é a base para o aprendizado e o processamento cognitivo. Em uma rede neural
artificial, neurônios são simulados por nós ou unidades que recebem entradas, processam essas
entradas através de uma função de ativação e então transmitem o resultado para outros nós na
rede. Essa estrutura permite que as redes neurais processem informações de maneira paralela e
altamente interconectada, similar ao cérebro humano.
Atualmente, as redes neurais são uma ferramenta indispensável em diversas aplicações de
inteligência artificial, desde o reconhecimento de fala e imagem até a geração de texto e a condução
autônoma de veículos. Seu sucesso se deve à capacidade de aprender diretamente dos dados,
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 61

Inteligência Artificial Visual

adaptando-se para melhorar seu desempenho à medida que são expostas a mais informações. As
pesquisas continuam evoluindo, buscando não apenas melhorar a eficiência e a capacidade das
redes neurais, mas também compreender os mecanismos fundamentais que permitem que esses
sistemas imitem tão bem alguns aspectos do processamento de informações do cérebro humano.
O widgetRedes Neurais(Figura 3.7) no Orange é uma implementação do algoritmo de Perceptron
de Múltiplas Camadas (MLP) com retropropagação, usando a bibliotecasklearn. Este algoritmo é
capaz de aprender modelos tanto lineares quanto não-lineares, tornando-o uma ferramenta poderosa
para uma ampla gama de tarefas de aprendizado de máquina.
Figura 3.7: Widget Neural Network
Entradas e Saídas: O widget aceita umconjunto de dados de entradae métodos depré-
processamentocomo entradas. Como saídas, ele fornece oalgoritmo de aprendizagemMLP
e ummodelo treinado, permitindo a aplicação do modelo aprendido em novos dados.
Configuração do Modelo: Para configurar a rede neural, diversos parâmetros podem ser
ajustados:
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 62

Inteligência Artificial Visual

Neurônios por camada oculta:define o número de neurônios em cada camada oculta.
Por exemplo, uma rede com três camadas ocultas pode ser definida como 100 , indicando
100 neurônios em cada camada.
Função de Ativação:para as camadas ocultas, pode ser escolhida entreIdentidade,
Logística,tanheReLu.
Solver para otimização de pesos:incluiL-BFGS-B,SGDeAdam.
Alpha:parâmetro para a penalidade L2 (termo de regularização).
Máximo de Iterações:define o número máximo de iterações para o treinamento.
Pré-processamento: Quando nenhum método de pré-processamento é especificado, o
widget aplica um pré-processamento padrão, que inclui: remoção de instâncias com valores
de alvo desconhecidos, continuização de variáveis categóricas, remoção de colunas vazias,
imputação de valores ausentes com médias e normalização dos dados. É possível remover
este pré-processamento padrão conectando um widgetPreprocessvazio ao aprendiz.
Aplicação Automática: Se a opçãoApply Automaticallyestiver ativada, o widget comunicará
alterações automaticamente. Caso contrário, o usuário deve clicar emApplypara aplicar as
mudanças.
Este widget oferece uma interface intuitiva para a configuração e treinamento de redes neurais,
tornando o processo acessível mesmo para aqueles com conhecimento limitado em aprendizado de
máquina. Com o ajuste adequado dos parâmetros e a aplicação de pré-processamentos relevantes,
os usuários podem explorar o poder das redes neurais para solucionar problemas complexos e obter
insights valiosos a partir de seus dados.
Figura 3.8: Widget Test And Score
Para treinar eficazmente uma rede neural e avaliar sua performance, o widgetTest and Score
(Figura 3.8) desempenha um papel fundamental. Esse widget permite testar algoritmos de aprendi-
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 63

Inteligência Artificial Visual

zado com dados de entrada, oferecendo um ambiente para avaliação detalhada do modelo, incluindo
redes neurais, através de diferentes esquemas de amostragem e separação de dados de teste.
1.textbfEntradas e Saídas: O widget recebe umconjunto de dados de entrada,dados de teste
separados(opcional) e um ou maisalgoritmos de aprendizagem(Learners). Como saída,
forneceresultados de avaliaçãoque quantificam a performance dos algoritmos de classificação
testados.
Medidas de Desempenho: Dentro do widget, uma tabela mostra diferentes medidas de
desempenho para classificadores, como aacurácia de classificação,área sob a curva ROC,
F1 score,precisão,recall, entre outras. Essas medidas são cruciais para entender a eficácia
da rede neural treinada em tarefas específicas de classificação.
Métodos de Amostragem: O widget suporta vários métodos de amostragem, incluindovali-
dação cruzada,amostragem aleatória,leave-one-out, entre outros. Esses métodos permitem
avaliar a robustez e generalização do modelo treinado sob diferentes condições de teste,
assegurando uma avaliação mais confiável da rede neural.
O uso do widgetTest and Scoreé essencial para iterar sobre o processo de treinamento da rede
neural, ajustando parâmetros e estratégias de pré-processamento baseado nos resultados obtidos.
Isso não apenas facilita a otimização da rede neural para alcançar performances superiores, mas
também garante que o modelo é avaliado de maneira compreensiva, considerando diversas métricas
e métodos de teste. Dessa forma, os usuários podem tomar decisões informadas sobre as melhores
configurações e abordagens para seus modelos de rede neural no contexto de suas aplicações
específicas.
Prossigamos adicionando ao nosso fluxo de trabalho os widgets ’Neural Networks’ e ’Test And
Score’. Contudo, antes de conectar esses componentes, é necessário realizar um passo crucial que
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 64

Inteligência Artificial Visual

provavelmente você notou estar ausente: o processamento de variáveis categóricas, a imputação de
valores ausentes e a normalização das características (feature scaling). Este tratamento prévio dos
dados é essencial para assegurar que a rede neural funcione de maneira otimizada e gere resultados
confiáveis durante a fase de teste e avaliação.
Figura 3.9: Fluxo de treinamento da Rede Neural
Para integrar adequadamente o modelo de Redes Neurais ao seu fluxo de trabalho no Orange,
comece por conectar o widget ’Preprocess’ ao widget ’Neural Network’. Isso irá garantir que o seu
modelo aplique as transformações de pré-processamento corretas aos dados antes da modelagem.
Figura 3.10: Definindo objeto preprocessor
Em seguida, abra o widget ’Preprocess’ e siga os seguintes passos para preparar os dados:
primeiro, trate os valores ausentes escolhendo a opção mais adequada para o seu conjunto de
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 65

Inteligência Artificial Visual

dados, como substituí-los pela média ou pela moda. Em seguida, para as variáveis discretas, decida
entre as opções disponíveis para transformá-las, como criar uma feature por valor ou tratar como
ordinal. Por fim, escolha um método de normalização de características, como a padronização para
uma média de zero e desvio padrão de um, ou a normalização para um intervalo específico. Essas
ações são cruciais para a performance otimizada do modelo de Redes Neurais, permitindo que ele
opere com dados limpos e devidamente formatados.
Figura 3.11: Escolhendo processamentos
Pode parecer inusitado para aqueles familiarizados com machine learning aplicar o preprocessa-
mento antes da rede neural e independentemente do fluxo de processamento principal. Contudo,
esta abordagem é adotada no Orange porque o software preserva, junto com o modelo, todas as
estatísticas descritivas dos dados, como média, máximo, mínimo, desvio padrão, entre outros.
Essas informações são fundamentais durante a etapa de previsão, pois permitem que o modelo
aplique as mesmas transformações aos novos dados de entrada, assegurando que a inferência seja
consistente e baseada nas características aprendidas durante o treinamento.
Agora, proceda conectando o widget ’Rede Neural’ ao ’Test and Score’ para iniciar o treinamento
do seu modelo. Observe atentamente o processo de aprendizado em ação e monitore o desempenho
da sua rede neural.
Quão boa é nossa Rede Neural?
Ao explorar os resultados no widgetTest and Scoredo Orange, deparamos com a performance da
nossa Rede Neural, evidenciada por métricas cruciais que descrevem sua precisão e eficiência em
diferentes dimensões:
AUC (Área sob a Curva ROC): 0.977 - Este valor impressionante indica a capacidade do
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 66

Inteligência Artificial Visual

Figura 3.12: Rede Neural Treinando
modelo de diferenciar entre as classes positivas e negativas. Um AUC próximo de 1 sugere uma
precisão excepcional, onde o modelo tem uma alta taxa de verdadeiros positivos, mantendo
uma baixa taxa de falsos positivos.
CA (Acurácia de Classificação): 0.931 - A acurácia nos diz que, em geral, o modelo
prevê corretamente 93.1% das instâncias. Esta é uma medida de quão frequentemente as
previsões da rede neural estão corretas, abrangendo tanto as classificações positivas quanto
as negativas.
F1: 0.931 - O F1 Score é uma média harmônica da precisão e recall, oferecendo um equilíbrio
entre as duas métricas. Um valor de 0.931 indica um equilíbrio notável entre a capacidade do
modelo de identificar corretamente as classes positivas e sua precisão ao fazê-lo.
Precisão (Prec): 0.931 - Reflete a proporção de identificações positivas que foram de fato
corretas. Neste caso, quando a rede neural prevê uma instância como positiva, há 93.1% de
chances de estar correta.
Recall: 0.931 - Também conhecido como sensibilidade, mostra a proporção de positivos reais
que foram corretamente identificados pelo modelo. Um recall de 0.931 significa que o modelo
captura 93.1% dos positivos reais.
MCC (Coeficiente de Correlação de Matthews): 0.861 - Uma medida de qualidade para
classificações binárias, que leva em consideração verdadeiros e falsos positivos e negativos.
Um valor de 0.861 é excelente, indicando previsões de alta qualidade em ambas as classes.
Estas métricas fornecem uma visão abrangente do desempenho da Rede Neural, indicando não
apenas a sua capacidade de fazer previsões corretas, mas também a qualidade dessas previsões
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 67

Inteligência Artificial Visual

Figura 3.13: Fluxo final de treinamento da Rede Neural
em termos de precisão, recall e equilíbrio entre as classes. Portanto, podemos concluir que a nossa
Rede Neuralmandou bem, apresentando um desempenho robusto e confiável na tarefa em questão.
O processo que acabamos de detalhar é conhecido como oTreino da Inteligência Artificial (IA).
Durante esta fase, a IA, através do modelo de Rede Neural, foi exposta a um conjunto de dados
derivados de campanhas de marketing anteriores. Através do processo de aprendizado, ajustando
seus pesos e funções de ativação baseado nos exemplos fornecidos, a rede aprendeu a reconhecer
padrões e correlações que indicam a probabilidade de um cliente comprar um produto em resposta
a uma campanha de marketing.
O resultado desse treinamento é notável: a IA agora é capaz de prever, com uma acurácia
impressionante de 93%, se um cliente específico realizará uma compra com base na campanha
de marketing vigente. Isso significa que, em 93 de cada 100 casos, a previsão da IA sobre o
comportamento de compra de um cliente estará correta, demonstrando não apenas a eficácia do
modelo em capturar e aprender a partir dos dados de marketing, mas também a sua aplicabilidade
prática em otimizar estratégias de marketing e maximizar o retorno sobre investimento em campanhas
futuras. Este nível de precisão abre portas para personalizações mais direcionadas e estratégias de
engajamento mais eficazes, fundamentadas eminsightsprofundos gerados pela IA.
Após o treinamento e avaliação da sua Rede Neural, um passo crucial é salvar o modelo treinado
para uso futuro. Isso permite que você reaplique o modelo a novos dados sem a necessidade de
retrabalho ou reajuste. No Orange, o processo de salvamento é intuitivo e direto, graças ao widget
Save Model.
Para salvar sua Rede Neural, você deve primeiramente garantir que tanto os dados de entrada
quanto o modelo da Rede Neural estejam corretamente conectados ao widgetSave Model. Em
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 68

Inteligência Artificial Visual

Figura 3.14: Salvando a Rede Neural
seguida, dentro do widget, você tem a opção de configurar o salvamento automático para novos
dados recebidos, mas, para garantir a persistência deste modelo específico, você deve clicar em
Save as.... Isso abrirá uma janela de diálogo onde você pode escolher o local de salvamento e o
nome do arquivo.
É recomendado salvar o modelo com a extensão.pkclspara indicar claramente que se trata de
um modelo de classificação. Por exemplo, nomeando o arquivo comomodel.pkclse escolhendo o
local desejado, você assegura que o modelo esteja acessível para futuras previsões ou avaliações.
Esta etapa de salvamento não apenas encapsula todo o conhecimento aprendido pela Rede Neural
durante o treinamento, mas também simplifica a integração deste modelo em processos de tomada
de decisão baseados em dados ou em sistemas automatizados de marketing.
3.3 Hora de fazer previsões
Com o modelo de Rede Neural já treinado e salvo, adentramos agora na fase empolgante de fazer
previsões. Esta etapa é a verdadeira prova de fogo, onde aplicaremos o conhecimento adquirido
pela IA para inferir resultados em dados novos e não vistos anteriormente. Aqui, o objetivo é
avaliar se o nosso modelo pode efetivamente generalizar o que aprendeu durante o treinamento e
aplicá-lo de maneira correta e útil. A capacidade de previsão de um modelo de IA é fundamental
para uma variedade de aplicações práticas, desde a recomendação personalizada de produtos
até a identificação de tendências futuras no comportamento dos consumidores. Ao utilizar nosso
modelo treinado, poderemos oferecer insights valiosos e decisões data-driven que podem levar a
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 69

Inteligência Artificial Visual

estratégias de negócios mais inteligentes e orientadas ao cliente. Nesta seção, vamos explorar como
carregar novos conjuntos de dados, aplicar o modelo treinado para realizar previsões e interpretar
os resultados. Isso não só demonstrará a potência do modelo em situações reais, mas também
solidificará nosso entendimento de como as redes neurais podem ser integradas em fluxos de
trabalho de ciência de dados para impulsionar a inovação e o sucesso comercial.
Para começar a previsão de novos clientes vamos
Dataset URL - Github: https://bit.ly/sandeco-orange-marketing-novos-clientes
Para começar a previsão de novos clientes, primeiro carregue os dados acessando o link fornecido
ou escaneando o QR-code dos novos clientes, garantindo que a fonte de dados esteja corretamente
configurada no widget ’File’ do Orange. Uma vez carregado, é importante ajustar a coluna ’Resposta’
no conjunto de dados para a função de ’meta’, pois ela atuará como uma referência para comparar
com as previsões da nossa IA, como mostra a Figura 3.15. Isso permite que você valide a precisão
do modelo de Rede Neural ao aplicá-lo aos novos dados. Esse passo é vital para garantir que
estamos medindo o sucesso do nosso modelo em termos de sua capacidade de prever resultados
reais, o que é a essência de trazer a ciência de dados para a tomada de decisões no mundo real.
De acordo com a Figura 3.16, é apresentada a visualização inicial dos dados carregados no
Orange através do widgetData Table. Nesta etapa, a variávelRespostajá foi definida como meta em
um passo anterior, permitindo que nos concentremos na análise das características restantes sem
pré-processamento. Esta configuração é essencial para a preparação adequada dos dados antes
de prosseguir com o treinamento de modelos de machine learning, assegurando que o conjunto
de dados esteja corretamente organizado e pronto para análise. A identificação correta da variável
Respostacomo meta facilita o processo de avaliação do modelo, permitindo comparações diretas
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 70

Inteligência Artificial Visual

Figura 3.15: Carregando novos clientes
entre as previsões geradas e os valores reais, fundamentais para a validação do desempenho do
modelo.
Figura 3.16: Visualização dos dados com a variável “Resposta” já definida como meta.
O mesmo pré-processamento aplicado no treinamento
Aplicar o mesmo pré-processamento nos dados de previsão que foi aplicado nos dados de treina-
mento é fundamental para manter a consistência e a precisão do modelo de Machine Learning.
Quando treinamos um modelo, ele aprende a fazer previsões com base nas características específi-
cas dos dados de treinamento. Se os dados de previsão não passarem pelo mesmo processo de
pré-processamento, as diferenças nas distribuições, escalas ou formatos dos dados podem levar a
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 71

Inteligência Artificial Visual

previsões imprecisas ou até errôneas.
É importante lembrar que, no Orange Canvas, ao treinar um modelo de Redes Neurais, o pré-
processamento realizado nos dados, incluindo a imputação de valores ausentes (missing values), a
conversão de variáveis categóricas e a normalização, é salvo juntamente com o modelo. Isso significa
que, ao aplicar o modelo treinado a novos dados para previsão, essas etapas de pré-processamento
são automaticamente aplicadas, garantindo que os dados de previsão sejam tratados de maneira
idêntica aos dados de treinamento.
Contudo, qualquer pré-processamento adicional que não seja automaticamente aplicado pelo
modelo, como a transformação de variáveis específicas (por exemplo, a conversão do Ano de
Nascimento em Idade), deve ser replicado manualmente antes da aplicação do modelo aos novos
dados. Isso assegura que todas as variáveis estejam no formato esperado pelo modelo, permitindo
que ele faça previsões precisas e relevantes.
Essa prática é essencial para a integridade e a eficácia do processo de Machine Learning,
garantindo que o modelo possa ser aplicado de forma efetiva a dados fora da amostra, mantendo a
alta qualidade e a confiabilidade das previsões geradas.
Figura 3.17: Fluxo de trabalho para o pré-processamento dos dados de previsão, mostrando a
transformação da variávelAno de NascimentoemIdadee a subsequente remoção da colunaAno
de Nascimento.
De acordo com a Figura 3.17, para a preparação dos dados destinados à previsão, replicamos o
mesmo processo de pré-processamento realizado durante a fase de treinamento do modelo. Isso
envolve a aplicação da fórmula para transformar oAno de NascimentoemIdadeutilizando o widget
Formula. Esta conversão é essencial para manter a consistência dos dados e assegurar que o
modelo possa interpretá-los corretamente. Após esta transformação, procedemos com a remoção da
colunaAno de Nascimentoatravés do widgetSelect Columns, uma vez que a informação relevante
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 72

Inteligência Artificial Visual

já está representada na nova colunaIdade.
Embora a detecção deoutlierstenha sido uma etapa crítica no pré-processamento do conjunto de
dados de treinamento, nesta fase de previsão, partimos do pressuposto de que os dados coletados
recentemente junto ao cliente estão corretos, omitindo inicialmente a necessidade de detecção de
outliers. Contudo, se necessário, o usuário pode optar por incluir este passo de detecção para
garantir a qualidade e a consistência dos dados a serem analisados.
Após preparar os dados de previsão com as etapas de pré-processamento necessárias, é hora
de carregar o modelo de Rede Neural que treinamos anteriormente, conforme ilustrado na Figura
3.18. Utilize o widgetLoad Modelno Orange para abrir o arquivo do modelo previamente salvo. Este
arquivo não apenas contém o modelo em si, mas também as etapas de pré-processamento aplicadas
durante o treinamento, incluindo o tratamento de valores ausentes (missing values), a conversão
de variáveis categóricas e a normalização de dados (utilizando valores de mínimo e máximo). Ao
carregar o modelo, esses passos de pré-processamento serão automaticamente aplicados aos
novos dados de previsão, garantindo que as previsões sejam feitas de forma consistente com o
treinamento. Lembre-se de selecionar o arquivo correto do modelo, geralmente com a extensão
.pkcls, navegando pelo sistema de arquivos até encontrá-lo e então carregá-lo no Orange. Este
passo é crucial para aplicar com sucesso o modelo treinado a novos dados e gerar previsões
precisas.
Figura 3.18: Carregando o modelo de Rede Neural previamente treinado, incluindo as etapas de
pré-processamento de dados.
Após carregar o modelo de Rede Neural e preparar os dados para previsão, como demonstrado
na Figura 3.19, o Orange Canvas, utilizando o widgetPredictions, realizou as previsões sobre
o conjunto de dados de teste. A Rede Neural conseguiu prever corretamente 10 de 11 casos,
alcançando uma acurácia de 90,91%. Este é um resultado notável e reflete a eficácia do modelo em
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 73

Inteligência Artificial Visual

generalizar a partir dos dados em que foi treinado para fazer previsões precisas em novos dados.
Figura 3.19: Previsões realizadas pelo modelo de Rede Neural no Orange Canvas, destacando uma
previsão incorreta entre as demais corretas.
No mundo do Machine Learning, um modelo que erra apenas uma previsão em um conjunto
de 11 casos é considerado de bom desempenho. É importante entender que a previsão perfeita é
raramente alcançável devido à complexidade e variabilidade dos dados reais. Erros de previsão
podem surgir por várias razões, incluindo limitações nos dados de treinamento, a presença de ruído
nos dados, ou simplesmente porque os padrões subjacentes nos dados são demasiado complexos
para serem capturados totalmente pelo modelo.
A tarefa de um bom engenheiro de Machine Learning não é eliminar completamente os erros, mas
sim minimizá-los e entender suas origens. Isso pode envolver o refinamento do pré-processamento
de dados, a experimentação com diferentes arquiteturas de modelo, o ajuste de parâmetros, ou a
coleta de mais dados ou dados mais representativos para o treinamento. Reconhecer e aceitar a
presença de erros como parte do processo de aprendizado de máquina permite uma abordagem
mais realista e pragmática para o desenvolvimento de sistemas de previsão eficazes.
Explorando Alternativas em IA
Apesar da eficácia da nossa Rede Neural, será que ela representa a solução definitiva para o nosso
problema? A diversidade de algoritmos de Machine Learning nos oferece uma vasta gama de
ferramentas que podem ser avaliadas para otimizar ainda mais nossas previsões. Como ilustrado na
Figura ?? , o Orange Canvas facilita a experimentação com múltiplos modelos, permitindo que os
arrastemos para o ambiente de trabalho e os conectemos ao widgetTest and Score. Esta abordagem
proporciona uma análise comparativa valiosa, fundamentada em métricas uniformes de desempenho,
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 74

Inteligência Artificial Visual

essencial para a seleção do modelo mais eficaz para nosso contexto específico.
Regressão Logística : Este método é útil para problemas de classificação binária. Através da
função logística, transforma a saída linear em uma probabilidade, oferecendo um resultado claro
entre duas classes. É amplamente utilizada devido à sua simplicidade e eficácia em casos com
relações lineares.
k-Nearest Neighbors (kNN) : Baseado na ideia de que instâncias semelhantes resultam em
saídas semelhantes, o kNN classifica um ponto de dados com base na maioria dos votos de seus k
vizinhos mais próximos. É um método não-paramétrico e intuitivo, útil para classificação e regressão.
AdaBoost : Um exemplo de algoritmo de boosting, o AdaBoost combina múltiplos classificadores
fracos para formar um modelo robusto. Ajusta-se iterativamente dando mais peso aos casos mal
classificados, melhorando a precisão do modelo final. É eficaz para aumentar a performance de
modelos simples.
Após configurar esses algoritmos, conecte-os ao widgetTest and Scorepara avaliar e comparar
suas performances. Escolha o modelo que apresentar a melhor acurácia ou outra métrica de
interesse para o seu problema. Essa abordagem garante uma seleção informada do melhor modelo
para implementação futura.
Hora da verdade
Para identificar o modelo mais eficiente em nosso conjunto de ferramentas de Inteligência Artificial,
é essencial iniciar o processo de seleção focando na métrica de acurácia. No ambiente Orange,
acesse o widgetTest and Scoree organize os modelos listados em ordem decrescente de acurácia,
clicando na coluna correspondente. O modelo AdaBoost, que se destaca com o maior valor, indica
ser o mais promissor para nossas necessidades. Em seguida, para um entendimento aprofundado
das capacidades comparativas de cada modelo, examine os detalhes nas tabelas de probabilidade,
acessíveis através da interface do widget. Esta avaliação nos permite entender as sutilezas de
cada modelo e as probabilidades associadas com suas performances. Seguindo esses passos,
garantimos uma seleção criteriosa do modelo que mais se alinha ao nosso objetivo de precisão e
confiabilidade.
Agora que finalizamos o treinamento e avaliação do nosso modelo AdaBoost, é hora de salvá-lo
para uso posterior. Clique no widgetSave Modelno Orange e escolha um nome e local para o
arquivo do modelo. Este passo é crucial pois garante que você possa reutilizar o modelo treinado,
aplicando-o a novos conjuntos de dados para previsão sem a necessidade de retrabalho, como
mostra a Figura 3.21.
Agora você pode carregar o modelo conforme mostramos na Figura 3.18 e verificar as previsões
do modelo.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL^75

Inteligência Artificial Visual

Figura 3.20: Comparação dos modelos de Machine Learning utilizando o widget Test and Score no
Orange.
5.5 Exercícios
Preparação dos Dados : Aplique um pré-processamento aos dados utilizando o widget
Preprocess. Normalize as variáveis numéricas e converta variáveis categóricas em numéricas.
Explique o impacto dessas transformações nos dados.
Visualização de Dados : Utilize o widgetScatter Plotpara visualizar a relação entre
algumas variáveis do seu dataset. Configure diferentes cores baseadas na variável alvo
Resposta. Discuta quaisquer padrões ou insights que você possa observar.
Treinamento de Modelos : Conecte o widgetTest and Scorea vários widgets de modelo
de aprendizado, comoRandom Forest,SVM, eNeural Network, todos conectados ao widget
Preprocess. Treine os modelos utilizando os dados de marketing e compare a performance
deles baseada na acurácia.
Avaliação de Modelos : Utilize o widgetConfusion Matrixconectado ao widgetTest and
Scorepara avaliar o desempenho do modelo de Rede Neural. Interprete os resultados
apresentados na matriz de confusão.
Otimização de Modelo : Experimente com diferentes configurações de parâmetros no widget
Neural Network, como alterar o número de neurônios e camadas ocultas. Avalie como essas
mudanças afetam a acurácia do modelo no widgetTest and Score.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL 76

Inteligência Artificial Visual

Figura 3.21: Salvando o modelo AdaBoost após o treinamento e avaliação.
CAPÍTULO 3. CRIE SUA INTELIGÊNCIA ARTIFICIAL^77

Inteligência Artificial Visual

CAPÍTULO 4
4 Previsão de Doenças usando IA
A Inteligência Artificial moderna pode ser um grande aliado aos profissionais e gestores da área da
saúde. As doenças cardíacas e o diabetes são duas das afecções crônicas mais prevalentes que
desafiam a saúde pública global. Estas condições não só impõem um ônus significativo sobre os
indivíduos afetados e seus familiares, mas também acarretam custos substanciais para os sistemas
de saúde. As doenças cardíacas, frequentemente caracterizadas por um espectro de distúrbios
que afetam o coração e os vasos sanguíneos, são a principal causa de morte em muitos países.
Paralelamente, o diabetes, com suas complicações crônicas, pode levar a consequências graves,
incluindo doenças cardiovasculares. Fatores de risco modificáveis, como dieta inadequada, falta
de atividade física e tabagismo, bem como fatores não modificáveis, como genética e idade, estão
fortemente associados ao desenvolvimento dessas doenças.
Neste cenário, a Inteligência Artificial (IA) surge como uma poderosa aliada, prometendo revoluci-
onar a previsão e o tratamento dessas doenças crônicas. Através de técnicas avançadas de machine
learning, é possível processar e analisar grandes volumes de dados de saúde, identificando padrões
e correlações que podem permanecer ocultos para análises tradicionais. A IA tem o potencial de
antecipar a ocorrência de eventos clínicos, facilitar diagnósticos precoces, personalizar tratamentos
e, em última análise, melhorar os resultados clínicos e a qualidade de vida dos pacientes. À medida
que avançamos, a integração de algoritmos inteligentes nos cuidados de saúde promete um futuro
no qual a prevenção e a gestão proativa de doenças se tornarão a norma, reduzindo o impacto
dessas condições crônicas na sociedade.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 78

Inteligência Artificial Visual

4.1 Previsão de Doença do Coração usando IA
Doenças cardíacas continuam a ser uma das principais causas de morbidade e mortalidade em todo
o mundo, representando um espectro amplo de condições de saúde que afetam o funcionamento do
coração e dos vasos sanguíneos. Estas condições incluem distúrbios como hipertensão, doença
arterial coronariana, arritmias, e insuficiência cardíaca, cada uma com suas particularidades e
desafios de tratamento.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 79

Inteligência Artificial Visual

Fatores de risco modificáveis como dieta, exercícios, e tabagismo têm sido o foco de campanhas
de saúde pública, mas fatores genéticos e não modificáveis também desempenham um papel crucial
no desenvolvimento dessas doenças.
Com os avanços tecnológicos e o aumento da disponibilidade de dados médicos, a Inteligência
Artificial (IA) emergiu como uma ferramenta promissora na previsão e no gerenciamento de doenças
cardíacas. Algoritmos de machine learning são capazes de identificar padrões complexos em
grandes conjuntos de dados, potencialmente antecipando o diagnóstico de condições cardíacas
antes de se tornarem clinicamente evidentes. Este campo em expansão oferece esperança não
apenas para diagnósticos mais precisos e personalizados, mas também para a otimização de
intervenções terapêuticas, adaptadas às necessidades individuais dos pacientes.
A aplicação de IA no diagnóstico e tratamento de doenças cardíacas representa uma virada
de jogo, onde modelos preditivos podem ser treinados para detectar sinais precoces de alerta a
partir de variáveis clínicas, testes laboratoriais e imagens médicas. O processamento de linguagem
natural (PLN) habilita a extração de insights valiosos a partir de históricos médicos não estruturados,
e a visão computacional permite a interpretação automática de imagens de diagnóstico, como
eletrocardiogramas (ECGs) e imagens de ressonância magnética (RM). Esta abordagem holística e
baseada em dados para a cardiologia está pavimentando o caminho para sistemas de suporte à
decisão clínica que auxiliam médicos, proporcionando recomendações baseadas em evidências e
aumentando a precisão dos cuidados ao paciente.
Porém, o caminho para a implementação efetiva dessas tecnologias está repleto de desafios.
Questões éticas e de privacidade dos dados, a necessidade de grandes conjuntos de dados anotados
e de alta qualidade para o treinamento de algoritmos, e a interpretabilidade dos modelos de IA são
apenas alguns dos obstáculos a serem superados. Além disso, a integração da IA nos fluxos de
trabalho clínicos requer uma abordagem cuidadosa para garantir que a tecnologia complemente, e
não substitua, o julgamento clínico humano. Somente através da colaboração entre engenheiros de
dados, profissionais de saúde e pacientes poderemos aproveitar plenamente o potencial da IA para
transformar o cuidado cardiovascular.
Nota: Neste capítulo, adotaremos uma abordagem direta e pragmática, aplicando diretamente
os widgets de pré-processamento de dados, modelagem e previsão já abordados nos capítulos
anteriores, consolidando nosso conhecimento através de uma implementação eficiente no
Orange.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 80

Inteligência Artificial Visual

Entendendo a Base de Dados de Doenças Cardíacas
A base de dados de doenças cardíacas que empregaremos para treinar nossos modelos de IA
contém um conjunto de variáveis clínicas importantes, cada uma fornecendo informações vitais
sobre o estado de saúde cardiovascular de um indivíduo. Uma variável particularmente crítica é
o ’diameter narrowing’, que se refere ao estreitamento dos vasos sanguíneos. Este indicador é
medido para avaliar a extensão da doença arterial coronariana, uma condição que ocorre quando as
artérias coronárias, responsáveis por fornecer sangue ao músculo cardíaco, tornam-se endurecidas
e estreitadas devido ao acúmulo de placa - uma mistura de gordura, colesterol, cálcio e outras
substâncias encontradas no sangue.
Com o tempo, o acúmulo de placa pode limitar o fluxo de sangue oxigenado ao coração, o
que pode resultar em angina (dor no peito) e outros sintomas clássicos de doença cardíaca. Em
casos mais graves, pode levar a um infarto do miocárdio, comumente conhecido como ataque
cardíaco. Portanto, ’diameter narrowing’ é uma medida crítica, pois um maior grau de estreitamento
é geralmente associado a um risco aumentado de eventos cardiovasculares adversos.
A previsão do estreitamento do diâmetro arterial com o uso de IA envolve a análise dessa variável
em conjunto com outros fatores de risco e indicadores clínicos. Modelos de machine learning são
treinados para detectar padrões e correlações entre essas variáveis, aprendendo a identificar os
sinais e sintomas que prenunciam a doença. Ao aplicar esses modelos de IA na prática clínica,
médicos podem tomar decisões mais informadas, potencialmente identificando e intervindo em
estágios mais precoces da doença, o que pode melhorar significativamente os resultados para os
pacientes. A Tabela 4.1 apresenta os detalhes das colunas de dados dessedataset.
Fluxo do Dataset deHeart Disease
Dataset URL - Github: https://bit.ly/sandeco-heart-disease
Para começar a criar nossa IA capaz de prever doenças cardíacas, o primeiro passo é carregar o
conjunto de dados no ambiente Orange. Utilize o widgetFilepara abrir seu arquivo de dados, que
contém informações cruciais para o processo de previsão. Assim que carregado, é imprescindível
definir a variável correta como alvo. Neste caso, ajuste a coluna ’diameter narrowing’ para o papel
de ’target’ no conjunto de dados, pois ela será nossa variável de previsão, indicando a presença
ou ausência de doença cardíaca. Esta ação inicial é fundamental para orientar os algoritmos de
aprendizado de máquina no processo subsequente de modelagem, como mostra a Figura 4.2.
Para iniciar a separação dos dados para treino e teste, utilize o widgetData Sampler. Defina
uma proporção fixa dos dados para criar um subconjunto para treinamento, deixando uma pequena
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 81

Inteligência Artificial Visual

Coluna Descrição Tipo
diameter narrowing Indica a presença de estreita-
mento do diâmetro arterial
Binário (Target)
age Idade do paciente Numérica
gender Gênero do paciente Categórica
chest pain Tipo de dor no peito experimen-
tada
Categórica
rest SBP Pressão arterial sistólica em re-
pouso
Numérica
cholesterol Níveis de colesterol Numérica
fasting blood sugar > 120 Indica se a glicemia em jejum é
maior que 120 mg/dL
Binário
rest ECG Resultados eletrocardiográficos
em repouso
Categórica
max HR Frequência cardíaca máxima al-
cançada
Numérica
exerc ind ang Angina induzida pelo exercício Binário
ST by exercise Depressão do segmento ST indu-
zida pelo exercício em relação ao
repouso
Numérica
slope peak exc ST A inclinação do segmento ST no
pico do exercício
Categórica
major vessels colored Número de vasos principais colo-
ridos por fluoroscopia
Numérica
thal Anomalia de talassemia Categórica
Tabela 4.1: Descrição das colunas do conjunto de dados de doenças cardíacas
parcela para a validação do modelo. Este passo é crucial para garantir que possamos avaliar a
capacidade do nosso modelo de generalizar para dados não vistos anteriormente.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 82

Inteligência Artificial Visual

Figura 4.1: Abrindo dados de Marketing no Orange
Figura 4.2: Carregamento do conjunto de dados e definição da variável alvo no widget File do
Orange.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 83

Inteligência Artificial Visual

Com oData Samplerconfigurado, conecte-o a dois widgetsData Table, um para visualizar o
subconjunto de treino e outro para o conjunto de validação, como mostram as Figuras 4.3 e 4.4.
Finalmente, verifique os conjuntos separados, garantindo que temos dados suficientes para treinar
nosso modelo de forma eficaz e para realizar uma validação significativa.
Figura 4.3: Selecionando uma proporção fixa de dados para o conjunto de treinamento usando o
widget Data Sampler.
Figura 4.4: Gerando tabelas para visualizar os dados separados para treino e validação.
Com isso coneguimos separar uma pequena porção dos dados para realizar um teste na previsão.
A Figura ?? mostra os dados de treino e validação prontos para serem usados no processo de
desenvolvimento do modelo de IA.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 84

Inteligência Artificial Visual

Figura 4.5: Dados de treino e validação prontos para serem usados no processo de desenvolvimento
do modelo de IA.
4.2 Explorando o Widget Data Sampler no Orange
O widgetData Sampleré uma ferramenta poderosa do Orange para a amostragem de dados,
permitindo que selecionemos um subconjunto específico de instâncias de um conjunto de dados
maior. Este processo é essencial para técnicas de validação e teste em modelagem preditiva. Ao
receber um conjunto de dados de entrada, oData Samplerfornece duas saídas principais: uma
Amostra de Dados, que consiste nas instâncias selecionadas para a amostragem, e osDados
Restantes, que incluem todas as outras instâncias do conjunto de dados de entrada que não foram
selecionadas.
Funcionalidades do Data Sampler
OData Sampleroferece várias funcionalidades que podem ser ajustadas de acordo com as necessi-
dades do usuário:
Proporção Fixa de Dados: Esta opção permite definir uma porcentagem específica do
conjunto de dados para ser amostrada. Por exemplo, se você desejar treinar um modelo em
70% dos dados e testá-lo nos 30% restantes, essa configuração seria ideal.
Tamanho de Amostra Fixo: Aqui você pode especificar um número exato de instâncias para
a amostra, com a opção de selecionarSample with replacement, o que possibilita a escolha
de instâncias duplicadas.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 85

Inteligência Artificial Visual

Validação Cruzada: Divida os dados em um número especificado de subconjuntos para
validação cruzada, uma técnica comum para avaliar como os resultados de um modelo
estatístico se generalizarão para um conjunto de dados independente.
Bootstrap: Utilize o método estatístico de bootstrap para inferir a amostra a partir da estatística
populacional.
Amostragem Replicável: Garante que a amostra possa ser reproduzida, criando um padrão
de amostragem que pode ser compartilhado e replicado entre diferentes usuários.
Amostra Estratificada: Tenta manter a distribuição de classes do conjunto de dados original,
garantindo que a amostra seja representativa.
Figura 4.6: Visualizando a distribuição de classes e selecionando a variável alvo no Orange.
Para iniciar a amostragem, após selecionar o método desejado, clique emSample Data. É
importante ressaltar que mesmo quando todas as instâncias são selecionadas, como ao definir a
proporção para 100% ou o tamanho da amostra para o total de instâncias, o widget ainda assim
embaralhará as instâncias antes da saída. Esta característica é particularmente útil para algoritmos
que são sensíveis à ordem dos dados.
Para verificar a distribuição de dados das classes e selecionar a variável alvo no Orange, siga
estes passos: Primeiro, conecte o widget File ao Data Sampler e então ao widget Distributions para
visualizar a distribuição das classes. No widget Distributions, selecione a variável alvo, que neste
caso é "diameter narrowing". Isso permitirá que você visualize a frequência de cada classe dentro
do conjunto de dados, essencial para entender a distribuição dos casos positivos e negativos. Ao
conectar o Data Sampler aos widgets Data Table Treino e Data Table Previsão, você pode dividir
o conjunto de dados em subconjuntos de treinamento e teste, respectivamente. Esse processo é
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 86

Inteligência Artificial Visual

crucial para a validação e teste do seu modelo de machine learning, garantindo que o modelo seja
treinado em uma parte dos dados e validado em outra, independentemente.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 87

Inteligência Artificial Visual

Vamos Treinar sua IA
Para aprimorar a análise e a precisão do seu modelo de Machine Learning, considere integrar uma
variedade de algoritmos e processos de pré-processamento, como demonstrado na Figura 4.7.
Inicie carregando seus conjuntos de dados de treinamento e de previsão através do widgetFile.
Em seguida, aplique técnicas de pré-processamento necessárias utilizando o widgetPreprocess,
ajustando os dados para as condições ideais requeridas pelos modelos de aprendizado. Este passo
é essencial para assegurar que os dados estejam prontos e otimizados para o treinamento e a
previsão.
Avance adicionando widgets para diferentes algoritmos de Machine Learning, comoRandom
Forest,SVM(Support Vector Machines) eStochastic Gradient Descent. Cada um desses algoritmos
possui características únicas e pode ser mais adequado para certos tipos de problemas em compa-
ração com outros. ORandom Foresté eficaz para lidar com datasets complexos e proporciona uma
boa métrica de importância das características. OSVMé excelente para encontrar a margem de
separação máxima entre as classes. Já oStochastic Gradient Descenté adequado para grandes
volumes de dados, oferecendo eficiência e a flexibilidade de ajustar funções de custo e regularização.
Conecte cada um dos algoritmos ao widgetTest and Scorepara avaliar seu desempenho. Este
widget facilita a comparação direta entre os modelos, ajudando a identificar qual deles apresenta o
melhor desempenho com base nas métricas selecionadas. Ao experimentar com diferentes métodos,
você pode descobrir o mais eficiente para o seu caso específico, maximizando a precisão e a
efetividade das suas previsões.
Figura 4.7: Integração de múltiplos algoritmos de Machine Learning e processos de pré-
processamento para otimização e comparação de desempenho.
Nesse problema, usaremos três novos algoritmos de Machine, cada um com suas próprias
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 88

Inteligência Artificial Visual

forças e aplicabilidades. Estes algoritmos são:Random Forest,Support Vector Machines (SVM), e
Stochastic Gradient Descent (SGD). A diversidade desses métodos permite uma avaliação ampla
sobre qual se adequa melhor ao nosso conjunto de dados e objetivo de previsão.
ORandom Foresté um algoritmo de ensemble que opera construindo múltiplas árvores de
decisão durante o treinamento e produzindo a classe que é o modo das classes (classificação) ou
predição média (regressão) das árvores individuais.Random Foresté particularmente apreciado
pela sua habilidade em lidar com grandes volumes de dados, com a capacidade de gerenciar
milhares de variáveis de entrada sem exclusão variável. Além disso, oferece uma estimativa de quais
variáveis são importantes no contexto da classificação, tornando-se um excelente ponto de partida
para análises de feature importance.
Support Vector Machines (SVM)é um poderoso algoritmo de aprendizado supervisionado usado
para classificação e regressão. A ideia central por trás do SVM é encontrar o hiperplano que melhor
divide o conjunto de dados em classes. O SVM busca maximizar a margem entre as diferentes
classes, tornando-o robusto à sobreposição de classes e à variabilidade dos dados. Devido à sua
flexibilidade, o SVM pode ser adaptado para lidar com problemas lineares e não lineares, ajustando-
se mediante o uso de diferentes funções de kernel, o que o torna versátil para uma ampla gama de
aplicações.
Stochastic Gradient Descent (SGD)é um método simples, porém eficiente, de otimização para
encontrar os valores de parâmetros que minimizam uma função de custo. É especialmente útil para
conjuntos de dados grandes, devido à sua eficiência computacional, atualizando os parâmetros
iterativamente com base em cada exemplo de treinamento. O SGD é frequentemente utilizado em
problemas de regressão e classificação, incluindo aprendizado profundo. Sua principal vantagem é
a rapidez com que consegue convergir para uma solução ótima, mesmo em espaços de parâme-
tros complexos, tornando-o uma escolha estratégica para o treinamento de modelos em grandes
conjuntos de dados.
Nota: Naturalmente, na aplicação prática, você tem a liberdade de reutilizar os algoritmos
apresentados em capítulos e exemplos anteriores, conforme julgar adequado para o seu projeto
ou para esse exemplo.
Após a configuração e treinamento dos diferentes algoritmos de Machine Learning, incluindo o
Stochastic Gradient Descent (SGD),Support Vector Machines (SVM), eRandom Forest, é crucial
avaliar e comparar o desempenho de cada um para identificar o mais eficaz para o seu problema
específico, como mostrado na Figura 4.8. Utilize o widgetTest and Scoreno Orange para esta
finalidade, assegurando que todos os algoritmos estão corretamente conectados a ele. Este widget
facilita a visualização dos resultados de desempenho utilizando várias métricas, como AUC (Área
sob a curva ROC), CA (Acurácia de Classificação), F1, Precisão (Prec), Recall e MCC (Coeficiente
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 89

Inteligência Artificial Visual

Figura 4.8: Comparação do desempenho de diferentes algoritmos de Machine Learning, destacando
os valores de desempenho do Stochastic Gradient Descent.
de Correlação de Matthews).
No caso doStochastic Gradient Descent, observamos os seguintes valores de desempenho:
AUC de 0.821, CA de 0.825, F1 de 0.824, Precisão de 0.825, Recall de 0.825, e MCC de 0.647,
destacando-se como o algoritmo com a melhor performance entre os testados. Esses resultados
sugerem que o SGD, devido à sua capacidade de otimização eficiente e adaptação às características
do conjunto de dados, é uma escolha robusta para a tarefa em questão. Ao identificar o algoritmo
com o melhor desempenho, você pode focar em otimizá-lo ainda mais para suas necessidades
específicas, refinando parâmetros ou explorando técnicas adicionais de pré-processamento de dados
para melhorar a precisão das previsões.
Vamos Melhorar?
A identificação e remoção de outliers é uma etapa crucial na preparação de dados para análise
de Machine Learning, como demonstrado na Figura 4.9. No ambiente do Orange, utilize o widget
Outliersconectado diretamente aos seus dados de treino para detectar e tratar essas anomalias.
A aplicação deste método pode resultar em melhorias significativas no desempenho do modelo,
como observado no aumento de 1 ponto na acurácia do algoritmoStochastic Gradient Descent
(SGD). Este procedimento ajuda a garantir que o modelo seja treinado em um conjunto de dados
mais representativo, reduzindo o impacto de pontos de dados atípicos que podem distorcer o
aprendizado e a performance do modelo. Ao aplicar a detecção de outliers e ajustar seu conjunto de
dados conforme necessário, você melhora a robustez e a confiabilidade do seu modelo de Machine
Learning.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 90

Inteligência Artificial Visual

Figura 4.9: Utilização do widget Outliers para melhorar a acurácia do modeloStochastic Gradient
Descentao detectar e tratar outliers no conjunto de dados.
4.3 O widget Rank
Na busca por melhorar o desempenho das nossas IA’s, vou introduzir um novo widget, o "Rank". O
widget "Rank"no Orange é uma ferramenta poderosa destinada à seleção de características, também
conhecida como seleção de variáveis ou atributos. Ele avalia e classifica as características (features)
de um conjunto de dados com base em sua importância ou contribuição para o poder preditivo
do modelo. Esse processo é essencial para melhorar a eficiência e a eficácia dos algoritmos de
Machine Learning, reduzindo a dimensão dos dados, o que pode diminuir o tempo de treinamento
do modelo e aumentar sua precisão.
Como Funciona o WidgetRank
Métodos de Pontuação : O widget oferece diversos métodos de pontuação, como Ganho
de Informação (Information Gain), Ganho de Informação Ratio, Gini Decrease, ANOVA,χ^2
(Qui-quadrado), ReliefF, e FCBF. Cada um desses métodos possui uma abordagem única para
avaliar a importância das características, permitindo aos usuários escolher aquele que melhor
se adapta à natureza de seus dados e ao problema específico que estão tentando resolver.
Seleção de Atributos : Baseado nos escores calculados, o widget pode automaticamente
selecionar um número específico das características mais importantes. Esta seleção pode
ser ajustada manualmente pelo usuário, que pode escolher manter todas as características,
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 91

Inteligência Artificial Visual

nenhuma, ou especificar um número exato das melhores características a serem incluídas.
Visualização : O widget apresenta uma lista classificada das características, mostrando as
mais importantes no topo. Isso não só facilita a identificação das variáveis mais relevantes
para o modelo, mas também oferece insights valiosos sobre os dados, possibilitando uma
interpretação mais aprofundada das relações entre as características e o alvo.
Aplicações Práticas
Redução de Dimensionalidade : Em conjuntos de dados de alta dimensionalidade, o "Rank"pode
ser usado para identificar e manter apenas as características mais significativas, reduzindo o
ruído e a complexidade dos dados.
Melhoria do Desempenho do Modelo : Ao concentrar-se nas variáveis que mais contribuem
para a previsão, os modelos tendem a treinar mais rapidamente e a produzir resultados mais
precisos.
Análise Exploratória de Dados : O "Rank"auxilia na exploração dos dados, revelando quais
características possuem maior poder discriminatório, o que pode guiar análises subsequentes
e tomadas de decisão baseadas em dados.
Ao utilizar o widget "Rank", é importante lembrar que a relevância das características pode variar
dependendo do modelo e do contexto específico do problema. Portanto, experimentar com diferentes
métodos de pontuação e avaliar o impacto na performance do modelo é uma prática recomendada.
Além disso, a seleção de características deve ser feita considerando o conhecimento de domínio,
pois características com pontuações mais baixas podem ser importantes em contextos específicos
ou em interação com outras variáveis.
Na Figura 4.10, estamos observando a aplicação do widget "Rank"do Orange para melhorar a
acurácia dos modelos de Machine Learning. Este widget avalia as variáveis de entrada com base
no seu ganho de informação, selecionando aquelas que mais contribuem para a predição do alvo.
Neste exemplo, após aplicar o "Rank"e selecionar as variáveis mais significativas, você observará
uma melhoria notável na acurácia da classificação do modelo de Descida de Gradiente Estocástico
(SGD).
Para aplicar efetivamente esta técnica, siga estes passos no Orange:
1.Selecione o método de pontuação desejado no widget "Rank", como o "Ganho de Informa-
ção"(Information Gain), que mede quão bem uma característica consegue separar as classes
de treinamento.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 92

Inteligência Artificial Visual

Figura 4.10: Melhoria na acurácia após a aplicação de "Rank"
2.Especifique o número de variáveis a serem retidas pelo modelo. Isso é feito ajustando o
parâmetro "Best ranked"para o número desejado de características superiores.
3.Conecte a saída do widget "Rank"ao seu modelo ou ao widget de preprocessamento para
aplicar esta seleção refinada de características antes do treinamento.
Neste caso específico, a implementação da seleção de características por meio do "Rank"resultou
em um aumento de 1.2 pontos percentuais na acurácia do modelo SGD, destacando-se como o
algoritmo com melhor desempenho entre os testados, com valores de AUC, CA, F1, Precisão, Recall
e MCC respectivamente de 0.836, 0.843, 0.841, 0.845, 0.843 e 0.683. Este exemplo sublinha a
importância de uma análise criteriosa das variáveis antes da modelagem, demonstrando que a
eliminação de características irrelevantes ou menos significativas pode conduzir a um modelo mais
eficaz e preciso.
4.4 Combinando Rank + PCA
Ao refinarmos nossa abordagem para aumentar a acurácia do modelo Stochastic Gradient Descent
(SGD) no Orange Canvas, aplicamos uma combinação poderosa de técnicas: PCA (Principal
Component Analysis) seguida pelo uso do widget Rank. Esta estratégia é detalhada na Figura
4.12, onde inicialmente, aplicamos o PCA para reduzir a dimensionalidade dos dados, focando
nos componentes que retêm a maior parte da variância dos dados. No exemplo, selecionamos 4
componentes principais, que explicam 45% da variância total dos dados, evidenciado pelo gráfico de
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 93

Inteligência Artificial Visual

variância acumulada no widget PCA.
Figura 4.11: Melhoria na acurácia com a aplicação de PCA + Rank.
Posteriormente, utilizamos o widget Rank para avaliar a importância dos componentes principais
gerados pelo PCA, selecionando os atributos mais relevantes para a modelagem. Este processo
nos permite não apenas reduzir o número de variáveis, mas também destacar aquelas que têm
o maior impacto na predição do modelo. Importante destacar que, para essa etapa final de otimi-
zação, mantivemos apenas o modelo SGD e excluímos os outros modelos e o widget "Test and
Score"anteriormente usados, focando nossos esforços na melhoria deste algoritmo específico.
A implementação dessas técnicas de pré-processamento demonstrou um aumento significativo
na acurácia do modelo SGD, que alcançou uma acurácia de 85%, um incremento de 0.7 pontos
percentuais em comparação ao desempenho anterior. Esse ganho reforça a importância da seleção
e transformação cuidadosa dos atributos antes da fase de modelagem, enfatizando como ajustes
aparentemente pequenos podem levar a melhorias notáveis na performance de modelos de Machine
Learning.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 94

Inteligência Artificial Visual

Figura 4.12: Aplicação de PCA e Rank para aumentar a acurácia do modelo SGD.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 95

Inteligência Artificial Visual

Predição de casos cardíacos com IA
Chegou a hora de colocar nossa inteligência artificial para trabalhar e prever potenciais casos
de doenças cardíacas. Conforme mostrado na Figura 4.13, iniciamos carregando os dados para
previsão e, em seguida, aplicamos uma série de processamentos com o objetivo de refinar e preparar
os dados para a análise final. Isso inclui a utilização do PCA para redução de dimensionalidade e a
seleção de características mais relevantes com o Rank, além de identificar e tratar possíveis outliers.
Esse processamento meticuloso garante que o modelo de Aprendizado de Máquina, especificamente
o Stochastic Gradient Descent (SGD) escolhido para esta tarefa, tenha as melhores condições
possíveis para fazer suas previsões com alta precisão.
Importante notar, como destacado na nota da Figura 4.13, que os dados destinados às previ-
sões são enviados diretamente ao widget de Predições sem passar por um pré-processamento
adicional. Esta abordagem é adotada porque o Orange gerencia o pré-processamento de novos
dados internamente, assegurando que o mesmo tratamento dado aos dados de treinamento seja
consistentemente aplicado também aos dados de previsão. Esta consistência é crucial para evitar
discrepâncias e erros na construção do modelo, permitindo previsões confiáveis e precisas. Além
disso, é digno de nota que um falso positivo identificado pelo modelo, embora indesejável, é preferível
a um falso negativo em contextos médicos, evitando assim a situação mais perigosa de não detectar
uma condição de saúde que requer atenção.
Figura 4.13: Processo de previsão de doenças cardíacas usando IA, destacando a transmissão
direta de dados para previsões e a atenção a falso positivo versus falso negativo.
CAPÍTULO 4. PREVISÃO DE DOENÇAS USANDO IA 96

Inteligência Artificial Visual

CAPÍTULO 5
5 Visão Computacional
A visão computacional é um campo fascinante da Inteligência Artificial (IA) que permite aos computa-
dores interpretarem e compreenderem o mundo visual de maneira similar aos humanos. Usando
algoritmos, a visão computacional analisa imagens e vídeos para identificar padrões, objetos e até
mesmo realizar ações baseadas nessa análise.
Um dos aspectos mais empolgantes da visão computacional é, sem dúvida, sua capacidade
de reconhecimento de objetos. Esta funcionalidade não se limita apenas a identificar objetos
estáticos em imagens; ela se estende a classificar e compreender objetos dentro de vídeos em
tempo real, abrangendo uma vasta gama de cenários e contextos. Por exemplo, sistemas de visão
computacional podem ser treinados para reconhecer diferentes tipos de veículos em uma estrada, o
que é fundamental para o desenvolvimento de sistemas de navegação autônoma de carros. Estes
sistemas não apenas detectam a presença de veículos, mas também são capazes de discernir
entre carros, caminhões, motocicletas, e até bicicletas, ajustando suas estratégias de navegação em
conformidade.
CAPÍTULO 5. VISÃO COMPUTACIONAL 97

Inteligência Artificial Visual

CAPÍTULO 5. VISÃO COMPUTACIONAL 98

Inteligência Artificial Visual

O reconhecimento de objetos em visão computacional desempenha um papel crucial também
em outras áreas, como no varejo, para inventário automatizado e na segurança pública, para
monitoramento e identificação de atividades suspeitas. O processo envolve etapas complexas,
desde a detecção inicial do objeto até sua classificação e rastreamento em sequências de imagens
ou vídeos. Esta capacidade de interpretação detalhada e adaptativa permite que os sistemas de visão
computacional forneçam insights valiosos e ações baseadas em dados precisos e contextualmente
relevantes. Assim, a evolução contínua desta tecnologia não apenas impulsiona inovações em áreas
específicas, mas também contribui para a segurança, eficiência e compreensão do mundo ao nosso
redor.
Outra aplicação notável e cada vez mais vital da visão computacional é encontrada no proces-
samento e análise de imagens médicas. Nesta área, a tecnologia pode ser um aliado crucial na
detecção precoce de diversas doenças, por meio da análise aprofundada de radiografias, tomogra-
fias, imagens de ressonância magnética (MRI) e outros tipos de exames de imagem. A capacidade
de identificar padrões sutis, muitas vezes invisíveis ao olho humano (como no problema da detecção
de covid-19 em Raio-X proposto ainda nesse capítulo), permite o diagnóstico precoce de condições
como câncer, doenças cardíacas e distúrbios neurológicos, entre outros. Aqui a visão computacional
tem um potencial significativo para revolucionar o setor de saúde, melhorando não apenas a precisão
dos diagnósticos, mas também a velocidade com que são realizados. Isso resulta em tratamentos
mais eficazes e personalizados, contribuindo significativamente para a melhora da qualidade de vida
dos pacientes. Além disso, oferece suporte valioso aos profissionais de saúde, ajudando-os a tomar
decisões informadas com maior segurança, reduzindo a carga de trabalho e possibilitando um foco
maior na atenção e no cuidado ao paciente.
E essa transformação radical da visão computacional foi viabilizada graças ao desenvolvimento
de um tipo específico de algoritmo demachine learning, conhecido como As Redes Neurais Convo-
lucionais (CNN, do inglêsConvolutional Neural Networks) foram pioneiramente desenvolvidas em
1994 pelo renomado cientista da computação Yann LeCun. Esta inovação, que representa um marco
no campo da Inteligência Artificial, desempenhou um papel crucial no avanço das capacidades
de processamento e análise de imagens digitais. O trabalho pioneiro de LeCun nas CNNs foi tão
impactante que lhe rendeu o prestigioso Prêmio Turing em 2018, frequentemente descrito como o
"Nobel da Computação", em reconhecimento à sua contribuição fundamental para o desenvolvimento
da aprendizagem profunda. E até hoje, as CNN são o estado-da-arte (o que há de melhor) em
problemas de visão computacional, e nós vamos utilizá-la aqui no Orange Canvas.
CAPÍTULO 5. VISÃO COMPUTACIONAL 99

Inteligência Artificial Visual

5.1 Redes Neurais Convolucionais
As Redes Neurais Convolucionais constituem um marco fundamental no campo do processamento de
imagens e visão computacional, sinalizando o advento do que hoje reconhecemos como Aprendizado
Profundo ou Deep Learning.
O Deep Learning (DL) é frequentemente mal compreendido em sua relação com a Inteligência
Artificial (IA) e Machine Learning (ML). Simplificadamente, a IA é a ciência que permite às máquinas
simular a cognição humana. O ML, um subconjunto da IA, aplica métodos estatísticos para otimizar
o desempenho das máquinas através da experiência. E o DL, que está sob o guarda-chuva do
ML, consiste em redes neurais de camadas múltiplas capazes de processar dados complexos.
A hierarquia entre IA, ML e DL é visualizada na Figura 5.2, que apresenta essas camadas de
complexidade.
Figura 5.1: Hierarquia entre Inteligência Artificial, Machine Learning e Deep Learning.
Este avanço significativo é caracterizado pela habilidade das CNNs em extrair, de forma autô-
noma, características intrincadas de imagens, eliminando a necessidade de programação manual e
específica para a identificação de atributos.
A essência das CNNs reside na aplicação sequencial de filtros convolucionais que, ao percorrerem
a extensão das imagens, conseguem ressaltar elementos críticos como contornos, texturas e padrões
distintos. Tal processo ocorre em múltiplas camadas, cada uma responsável por uma análise mais
refinada que as anteriores, permitindo assim a decomposição das imagens em elementos simples nos
níveis iniciais e a integração desses elementos em conceitos abstratos nas camadas subsequentes.
CAPÍTULO 5. VISÃO COMPUTACIONAL 100

Inteligência Artificial Visual

Figura 5.2: Machine Learning e Deep Learning.
Portanto, a revolução desencadeada pelas Redes Neurais Convolucionais transcende os avanços
meramente quantitativos em precisão de classificação e detecção. Ela redefine as fronteiras de
interação humano-máquina e continua a pavimentar caminhos para inovações em diversos domínios
científicos e industriais, consolidando o Aprendizado Profundo como uma das pedras angulares da
Inteligência Artificial contemporânea.
5.2 ADD-ON Image Analytics Inteligência Artificial Visual
O add-on Image Analytics do Orange Canvas é uma poderosa extensão focada em análise e
processamento de imagens usando Redes Convolucionais. Esse módulo adiciona um conjunto de
widgets especializados que permitem aos usuários realizar desde a importação e pré-processamento
de imagens até o treinamento de modelos de machine learning para tarefas como classificação de
imagens e detecção de objetos. Com interfaces intuitivas e uma abordagem de arrastar e soltar,
o add-on torna o complexo campo da visão computacional acessível mesmo para aqueles sem
profundo conhecimento em programação, abrindo novas portas para exploração visual de dados
dentro do ambiente Orange. A Figura 5.3 mostra como você pode instalar o add-on Image Analytics.
CAPÍTULO 5. VISÃO COMPUTACIONAL 101

Inteligência Artificial Visual

Figura 5.3: Como instalar o add-on Image Analytics
CAPÍTULO 5. VISÃO COMPUTACIONAL 102

Inteligência Artificial Visual

A Figura 5.4 mostra o painel Image Analytics do Orange Canvas, encontramos widgets projetados
para otimizar o trabalho com imagens:
Import Images: Facilita a importação de imagens de um ou mais diretórios, permitindo que o
usuário carregue seu conjunto de dados visual rapidamente no ambiente Orange.
Image Viewer: Um visualizador que exibe as imagens associadas a um conjunto de dados,
possibilitando a inspeção individual de cada imagem de forma conveniente.
Image Embedding: Utiliza redes neurais profundas para criar uma representação vetorial
das imagens, que é uma maneira de transformar dados visuais em um formato que pode ser
eficientemente analisado e processado.
Image Grid: Apresenta as imagens em uma grade de similaridade, facilitando a comparação
visual e a identificação de padrões ou anomalias entre as imagens.
Save Images: Permite salvar as imagens processadas na estrutura de diretórios, o que é
essencial para manter a organização do projeto e para futuras análises.
Figura 5.4: Painel Image Analytics
Cada um desses widgets desempenha um papel vital no fluxo de trabalho de análise de imagem,
desde a fase inicial de importação até o salvamento e organização de imagens processadas,
demonstrando a abrangência e a praticidade do add-on Image Analytics.
5.3 Detectando Covid-19 com Imagens Médicas
Em 27 de março de 2020, onze dias após o início do primeiro Lockdown no Brasil, realizei uma
transmissão ao vivo no YouTube para demonstrar uma técnica de detecção de COVID-19 utilizando
CAPÍTULO 5. VISÃO COMPUTACIONAL 103

Inteligência Artificial Visual

Python e as bibliotecas Tensorflow e Keras. Durante a live, compartilhei como a minha rede neural
desenvolvida atingiu uma impressionante acurácia de 96%, o que despertou o interesse de vários
órgãos governamentais na época, buscando a potencialidade e a viabilidade de implementar um
sistema de detecção automática de Covid-19 baseado em IA. O vídeo da transmissão ao vivo ainda
está disponível no Canal Sandeco, e o acesso pode ser feito através do link fornecido abaixo.
Live Covid-19 Python https://www.youtube.com/watch?v=qDuVk4HPZ1g
Replicarei com você a mesma metodologia que apliquei na Live, porém, desta vez, empregaremos
o Orange Canvas como ferramenta analítica. É crucial destacar que a técnica em pauta possui uma
aplicabilidade extensiva, podendo ser adaptada para o diagnóstico de uma variedade de doenças
identificáveis por imagens médicas. Essa versatilidade apresenta uma oportunidade significativa
para profissionais da saúde, que podem valer-se do Orange Canvas como um recurso eficaz para a
detecção de enfermidades em imagens e em tempo real.
Baixando o Dataset
É importante observar que o Orange Canvas não possui funcionalidade nativa para carregar imagens
diretamente da internet. Para realizar análises de imagens utilizando o Imagem Analytics, será
necessário primeiramente baixar o conjunto de dados desejado para o seu computador local. O
dataset específico de Imagens de Raio-X para diagnóstico de COVID-19, por exemplo, pode ser
baixado através do link fornecido abaixo:
Link dataset imagens médicas Covid-19 https://bit.ly/sandeco-covid-dataset
Após a descompactação do arquivo do dataset você observará no dataset existirá duas pastas
de imagens: train e validation (Figura 5.5. A "train"servirá para treinar nossa inteligência artificial e a
"validation"servirá para realizar predições.
Figura 5.5: Pastas de imagens do dataset Covid-19
CAPÍTULO 5. VISÃO COMPUTACIONAL 104

Inteligência Artificial Visual

Carregando as Imagens de Raio-X
O processo de carregamento de imagens para análise é feito pelo widget “Import Images”. Esse
widget é essencial para dar o primeiro passo em qualquer projeto de visão computacional no Orange,
possibilitando a importação de conjuntos de imagens diretamente do sistema de arquivos do usuário.
A Figura 5.6 ilustra essa etapa inicial, destacando a ação de importar imagens e indicando ao usuário
a necessidade de clicar no widget “Import Images” para prosseguir.
O primeiro passo para começar seu projeto de visão computacional é o uso do widget “Import
Images”. Esse widget permite que você importe conjuntos de imagens de seu sistema de arquivos
de forma simples e eficaz. A Figura 5.6 mostra como iniciar este processo, destacando o widget
“Import Images” e indicando que você deve clicar nele para prosseguir.
Uma vez selecionado o widget, uma janela de diálogo aparecerá, permitindo que você navegue
pelos seus diretórios até encontrar e selecionar o local específico das imagens a serem trabalhadas.
No nosso exemplo, você deve escolher a pasta “train” do dataset de Covid-19, que contém imagens
de radiografias classificadas em categorias, que utilizaremos para treinar modelos demachine
learningna detecção do vírus. A informação na interface do widget “1200 images / 2 categories”
confirma a seleção correta do conjunto de dados, mostrando que você tem disponível um total de
1200 imagens divididas em duas categorias para análise.
Figura 5.6: Processo de carregamento de imagens de radiografia no Orange Canvas para análise de
detecção de Covid-19.
Após importar as imagens utilizando o widgetImport Images, o próximo passo consiste em
visualizar e analisar os dados das imagens importadas. Para isso, é necessário conectar o widget
Import ImagesaoData Table, processo ilustrado na Figura 5.7. Esta conexão permite examinar
detalhadamente as informações associadas a cada imagem importada.
CAPÍTULO 5. VISÃO COMPUTACIONAL 105

Inteligência Artificial Visual

OData Tableapresenta várias colunas, tais comocategory,image name,image,size,width, e
height. Estas colunas fornecem informações valiosas sobre cada imagem, incluindo a categoria
da imagem (por exemplo,covidpara imagens de pacientes com Covid-19), o nome da imagem, o
caminho do arquivo, o tamanho do arquivo em bytes, além da largura e altura da imagem em pixels.
A visualização desses dados é crucial para entender melhor o conjunto de imagens com o qual se
está trabalhando, facilitando a preparação para etapas subsequentes de análise e modelagem no
Orange Canvas.
Figura 5.7: Visualizando os dados das imagens importadas no Orange Canvas.
Este procedimento assegura que as imagens importadas estejam corretamente organizadas
e categorizadas, permitindo também uma inspeção inicial que pode revelar a necessidade de
pré-processamento adicional antes de prosseguir para análises mais complexas.
Image Viewer
Depois de visualizar e analisar os dados das imagens importadas, é possível visualizar as próprias
imagens no Orange Canvas utilizando o widgetImage Viewer. Conecte o widgetData Tableao
Image Viewerpara exibir as imagens importadas, como demonstrado na Figura 5.8. Este widget
permite que você veja as imagens diretamente, facilitando a avaliação visual das características
relevantes para a sua análise.
NoImage Viewer, as imagens são apresentadas em miniaturas, permitindo uma rápida inspeção
visual. Você pode ajustar atributos comoImage Filename AttributeeTitle Attributepara controlar
quais informações são exibidas juntamente com as imagens. No nosso exemplo, selecionamos o
atributocategorycomo o título para cada imagem, permitindo identificar rapidamente a categoria de
cada caso, neste caso, imagens relacionadas a pacientes diagnosticados com Covid-19.
CAPÍTULO 5. VISÃO COMPUTACIONAL 106

Inteligência Artificial Visual

OImage Vieweré uma ferramenta poderosa para a inspeção visual do seu conjunto de dados
de imagens, facilitando a identificação de padrões ou características específicas que podem ser
importantes para as etapas subsequentes de análise ou modelagem.
Figura 5.8: Utilizando oImage Viewerno Orange Canvas para visualizar as imagens importadas.
5.4 Embeddings
Embeddingsde imagens representam uma técnica avançada na visão computacional e no aprendi-
zado de máquina, transformando imagens em vetores de números de alta dimensão. Esses vetores
capturam as características essenciais das imagens de uma maneira que facilita a comparação,
análise e processamento por algoritmos demachine learning. Ao invés de trabalhar diretamente
com os pixels brutos, os embeddings permitem que o modelo compreenda e opere em um espaço
de características abstratas, como formas, texturas e padrões específicos presentes nas imagens.
A geração de embeddings de imagens geralmente envolve o uso de Redes Neurais Convolucio-
nais (CNNs), que são treinadas para identificar e extrair essas características distintivas. À medida
que uma imagem é passada através das camadas da rede, cada camada processa a imagem em um
nível de abstração cada vez maior. A última camada, antes da camada de saída, muitas vezes serve
como o embedding da imagem, consolidando sua informação visual em um vetor compacto. Este
vetor pode ser usado em uma variedade de aplicações demachine learning, incluindo classificação
de imagens, busca por similaridade de imagens e até mesmo geração de imagens. A Figura 5.9
apresenta todo o processo de geração de Embeddings por uma CNN, nesse caso especifico a
InceptionV3.
CAPÍTULO 5. VISÃO COMPUTACIONAL 107

Inteligência Artificial Visual

Figura 5.9: Como uma CNN gera Embeddings
A utilização de embeddings de imagens permite uma compreensão mais profunda e nuanciada do
conteúdo visual, superando os desafios associados à grande variabilidade das imagens. Por exemplo,
duas imagens do mesmo objeto podem variar significativamente em termos de iluminação, escala,
ou perspectiva. Os embeddings ajudam a minimizar essas diferenças, destacando as características
essenciais que definem a semelhança entre as imagens. Isso torna os embeddings uma ferramenta
poderosa para tarefas de reconhecimento de padrões e classificação, onde a precisão e a capacidade
de generalização são fundamentais.
Image Embedding
Dentro do widgetImage Embedding, é oferecida uma seleção de modelos pré-treinados de redes
neurais convolucionais, como Inception v3, SqueezeNet, VGG-16, entre outros, cada um adequado
para diferentes tipos de tarefas e conjuntos de dados. O usuário tem a flexibilidade de escolher o
modelo que melhor se adapta às suas necessidades, simplesmente selecionando-o na interface
do widget. Essa escolha é crucial, pois diferentes modelos podem capturar aspectos variados das
imagens, influenciando diretamente a qualidade dos embeddings gerados e, por consequência, o
desempenho dos modelos demachine learningsubsequentes.
Osembeddingsgerados são então utilizados em uma ampla gama de tarefas, como classificação
de imagens, busca por similaridade, e até mesmo agrupamento. Esse processo enriquece significati-
vamente a análise de dados, proporcionando uma representação mais rica e abstrata das imagens
que facilita tanto a visualização quanto o processamento por modelos de aprendizado posterior. A
figura ilustrada demonstra essa etapa crucial no fluxo de análise de imagens no Orange Canvas,
marcando a transição do trabalho com imagens brutas para a manipulação de representações
CAPÍTULO 5. VISÃO COMPUTACIONAL 108

Inteligência Artificial Visual

numéricas compactas e informativas.
Figura 5.10: Escolha um Embedder de acordo com suas necessidades.
A seleção do modelo deembedderno widgetImage Embeddingdo Orange Canvas oferece
várias opções, cada uma com suas características e aplicações específicas como mostra a Figura
5.10. Aqui está uma lista dos modelos disponíveis e suas respectivas funções:
Inception v3 : Desenvolvido pela Google, o Inception v3 é um modelo de rede neural con-
volucional treinado no ImageNet. É conhecido por seu equilíbrio entre precisão e eficiência
computacional. Este modelo é amplamente utilizado para tarefas de classificação e detecção
de imagens, beneficiando-se de sua habilidade em capturar características complexas de
imagens através de múltiplas escalas de convolução.
SqueezeNet : O SqueezeNet destaca-se por sua arquitetura compacta, que alcança uma
precisão comparável à do AlexNet com um número significativamente menor de parâmetros.
Isso o torna ideal para aplicações em dispositivos com recursos limitados ou para situações
em que a eficiência de armazenamento e velocidade de processamento são críticas.
VGG-16 e VGG-19 : Os modelos VGG, desenvolvidos pela Visual Graphics Group da Universi-
dade de Oxford, são notáveis por sua arquitetura profunda, que utiliza repetidamente camadas
convolucionais pequenas. Eles têm sido fundamentais para o avanço do reconhecimento de
imagens e são frequentemente usados em tarefas que requerem a extração de características
visuais detalhadas.
Painters : Este modelo é especificamente treinado para reconhecer estilos e técnicas de
pintura, sendo útil em tarefas relacionadas à classificação de arte e à análise estilística de
CAPÍTULO 5. VISÃO COMPUTACIONAL 109

Inteligência Artificial Visual

imagens de pinturas.
DeepLoc : Projetado para a localização celular de proteínas em imagens de microscopia, o
DeepLoc é utilizado em bioinformática e biologia computacional para classificar imagens de
células com base na localização subcelular de proteínas.
openface : Baseado na rede neural Torch, o openface é especializado em reconhecimento
facial. É utilizado para identificar e verificar rostos em imagens, oferecendo uma ferramenta
robusta para aplicações de segurança e análise de mídia social.
Cada um desses modelos traz um conjunto único de capacidades para o processo de geração de
embeddings de imagens, permitindo que pesquisadores e analistas escolham o melhor modelo de
acordo com as características específicas do conjunto de dados e os objetivos da análise.
98%, UMA SUPER ACURÁCIA
Após a geração de embeddings de imagens utilizando o widgetImage Embeddingno Orange Canvas,
um passo crítico é avaliar a eficácia desses embeddings para tarefas específicas demachine learning,
como classificação. A Figura 5.11 ilustra como os embeddings podem ser avaliados conectando o
output doImage Embeddingao widgetTest and Scoreatravés de um modelo de aprendizado, neste
caso, uma Rede Neural.
O widgetTest and Scoreoferece uma avaliação abrangente do modelo aplicado, apresentando
métricas como AUC (Área sob a curva ROC), CA (Acurácia), F1 Score, Precisão, Recall, e MCC
(Coeficiente de Correlação de Matthews). Estas métricas fornecem uma visão detalhada do desem-
penho do modelo em classificar corretamente as imagens com base nos embeddings gerados. No
exemplo apresentado, observa-se uma acurácia excepcionalmente alta de 98,9%, indicando que os
embeddings capturaram de forma eficaz as características essenciais das imagens para a tarefa de
classificação realizada pela rede neural.
Este procedimento é fundamental para entender como diferentes modelos de embeddings e
arquiteturas de rede neural influenciam a capacidade de reconhecimento de padrões e classificação
de imagens. Ele permite que os usuários do Orange Canvas ajustem e otimizem suas análises
para alcançar os melhores resultados possíveis, dependendo do conjunto de dados e do problema
específico em questão.
CAPÍTULO 5. VISÃO COMPUTACIONAL 110

Inteligência Artificial Visual

Figura 5.11: Avaliação de embeddings de imagens utilizando o widgetTest and Scoreconectado a
uma Rede Neural no Orange Canvas.
6.8 Exercícios
1.Explique em suas próprias palavras como a visão computacional permite que os computadores
"vejam"e interpretem o mundo visual.
2.Além da rede neural, experimente com outros algoritmos demachine learningdisponíveis
no Orange Canvas para classificar as imagens com base nos embeddings gerados. Alguns
algoritmos que você pode explorar incluem Máquinas de Vetores de Suporte (SVM), Florestas
Aleatórias e k-Nearest Neighbors (k-NN). Compare os resultados obtidos com esses diferentes
algoritmos e discuta como cada um performa em relação à rede neural. Considere aspectos
como acurácia, tempo de treinamento e a capacidade de generalização do modelo. Qual
algoritmo você considera mais adequado para o seu conjunto de dados e por quê?
3.Após obter os embeddings de suas imagens por meio do widgetImage Embedding, proceda
com a aplicação da técnica de Análise de Componentes Principais (PCA) para reduzir a
dimensionalidade dos vetores de embeddings. Isso pode ser realizado utilizando o widget
PCA, que se encontra disponível no Orange Canvas. Com os embeddings agora de dimensão
reduzida, treine uma rede neural especificamente com as imagens relacionadas à Covid-19.
Avalie o desempenho da rede neural, considerando os embeddings originais e os embeddings
pós-PCA, e discuta os resultados observados. Concentre-se em métricas como a acurácia
do modelo, o tempo necessário para o treinamento e a complexidade do modelo. Explique
como a redução de dimensionalidade impactou o desempenho na tarefa de classificação das
CAPÍTULO 5. VISÃO COMPUTACIONAL 111

Inteligência Artificial Visual

imagens e considere as implicações da seleção de recursos no processo de treinamento de
modelos de aprendizado de máquina.
4.Utilizando o add-on Image Analytics no Orange, importe um conjunto de imagens de sua
escolha e utilize o widgetImage Viewerpara visualizá-las. Descreva o processo e quaisquer
dificuldades que você encontrou.
5.Escolha um modelo deembedderdisponível no widgetImage Embeddinge gere embeddings
para o seu conjunto de imagens. Compare os resultados obtidos com diferentes modelos (por
exemplo, Inception v3 vs. VGG-16) e discuta as diferenças observadas.
6.Com base nos embeddings gerados, utilize o widgetTest and Scorepara avaliar o desempenho
de uma rede neural na classificação de imagens. Experimente com diferentes parâmetros da
rede e discuta como cada mudança afeta a acurácia do modelo.
7.Reflita sobre o impacto da visão computacional em áreas como saúde, segurança pública e va-
rejo. Escolha um desses campos e proponha uma aplicação específica da visão computacional
que poderia trazer benefícios significativos.
CAPÍTULO 5. VISÃO COMPUTACIONAL 112

Inteligência Artificial Visual

CAPÍTULO 6
6 Inteligência Artificial para Textos
As inteligências artificiais que processam textos estão em alta no mundo da IA, representando a
essência do Processamento de Linguagem Natural (Natural Language Processing- NLP). Esta
subárea dedica-se a capacitar as máquinas para entender, interpretar e reagir à linguagem humana
de maneira significativa. Sua aplicabilidade vão desde assistentes virtuais, como Siri e Alexa, até
sistemas de tradução automática, como o Google Translate, o NLP tem sido um campo de rápido
crescimento e inovação.
A essência do NLP reside em sua habilidade de não apenas processar a vasta quantidade de
dados linguísticos disponíveis, mas também entender as complexidades e nuances da comunicação
humana. Isto inclui a compreensão de contextos, ironias, metáforas e até emoções expressas na
linguagem. Por exemplo, ao analisar resenhas de produtos, um sistema de NLP pode determinar não
apenas se uma resenha é positiva ou negativa, mas também os aspectos específicos que agradaram
ou desagradaram ao cliente.
Outro exemplo impressionante da aplicabilidade do NLP é nos chatbots de atendimento ao cliente.
Estes sistemas são programados para interpretar as consultas dos usuários e fornecer respostas
precisas, melhorando significativamente a eficiência do atendimento ao cliente e a satisfação do
usuário. Além disso, os chatbots são capazes de aprender com as interações anteriores, aprimorando
continuamente a qualidade de suas respostas.
Um desafio fundamental do NLP é o processamento de linguagem natural ambígua. A linguagem
humana está repleta de ambiguidades, sejam elas lexicais (palavras com múltiplos significados),
sintáticas (frases que podem ser estruturadas de diferentes maneiras) ou semânticas (frases com
significados que dependem do contexto). Superar essas ambiguidades requer modelos de NLP
sofisticados e um vasto corpus de dados linguísticos.
Com o advento de técnicas de aprendizado profundo e grandes conjuntos de dados, o NLP tem
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 113

Inteligência Artificial Visual

experimentado avanços significativos. Modelos como o BERT (Bidirectional Encoder Representations
from Transformers) e o GPT (Generative Pre-trained Transformer) têm estabelecido novos padrões
de desempenho em uma ampla gama de tarefas de NLP. Estes modelos são capazes de entender o
contexto de uma palavra em uma frase, capturando assim nuances que métodos anteriores poderiam
perder.
6.1 Add-on Text Mining
Text Mining é um add-on doOrange Canvasque facilita a análise e o processamento de dados
textuais. Este add-on viabiliza a análise de sentimentos, a descoberta de tópicos e outras operações
de processamento de linguagem natural, essenciais para extrair insights de textos.
Ele oferece acesso a dados publicamente disponíveis de fontes como o NY Times, Twitter,
Wikipedia e PubMed. Fornece também ferramentas para pré-processamento, construção de espaços
vetoriais utilizando técnicas de transformação que geram embeddings de texto, modelagem de
tópicos, e algoritmos de hash de similaridade. Inclui visualizações tais como mapas geográficos e
nuvens de palavras. Todos esses recursos podem ser integrados às robustas técnicas de mineração.
Para adicionar o add-on “Text” no Orange Canvas, inicie o programa e clique na opção “Options”
localizada no canto superior direito da tela principal. No menu que se abre, selecione “Add-ons...”,
conforme indicado pela seta laranja. Isso abrirá o instalador de add-ons. Localize o add-on chamado
“Text” na lista apresentada. Observe que ao lado do nome do add-on há uma caixa de seleção;
marque esta caixa. Depois de selecionar o add-on “Text”, clique no botão “OK” para iniciar a
instalação. Durante o processo de instalação, uma barra de progresso pode aparecer, indicando
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 114

Inteligência Artificial Visual

o andamento do download e da instalação. Aguarde a conclusão e, uma vez instalado, o add-on
estará disponível para uso dentro do Orange Canvas, oferecendo funcionalidades específicas para
mineração de texto, como é ilustrado na Figura 6.1.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 115

Inteligência Artificial Visual

Figura 6.1: Procedimento de adição do add-on “Text” no Orange Canvas.
No painel "Text Mining"do Orange Canvas, são oferecidos 31 widgets especializados na manipu-
lação e análise de textos. Este conjunto de ferramentas permite aos usuários desde a importação
e processamento de corpora textuais até a visualização avançada dos dados analisados. Wid-
gets como "Corpus", "Import Documents", e "Create Corpus"são fundamentais para estruturar e
preparar os dados. Enquanto isso, recursos como "Bag of Words", "Sentiment Analysis"e "Word
Cloud"possibilitam uma análise mais aprofundada e a representação gráfica das características do
texto. A combinação desses widgets viabiliza uma exploração detalhada de conjuntos de dados
textuais, tornando o Orange Canvas uma plataforma poderosa para mineração de textos.
Figura 6.2: Visão geral do painel "Text Mining"do Orange Canvas com uma rica coleção de 31
widgets.
Ao explorar a Figura 6.2, observe o painel “Text Mining” que é um componente essencial do
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 116

Inteligência Artificial Visual

Orange Canvas. Este painel fornece uma variedade de 31 widgets especializados, cada um
desenhado para facilitar um aspecto específico da mineração de textos. Utilize widgets como
“Corpus” para gerir documentos, “Preprocess Text” para preparação dos dados, “Sentiment Analysis”
para entender emoções expressas e “Word Cloud” para visualização de frequência de palavras. Com
esses recursos, amplie suas análises de textos de maneira eficiente e intuitiva. Veja abaixo a lista de
widgets do painel "Text Mining".
Corpus: Gerencia coleções de documentos textuais.
Import Documents: Carrega textos de arquivos ou pastas.
Create Corpus: Cria um corpus com dados inseridos manualmente.
The Guardian: Acessa conteúdo do jornal para análise.
NY Times: Extrai conteúdo para análise do New York Times.
Pubmed: Importa dados bibliográficos para análise do PubMed.
Twitter: Coleta e processa dados do Twitter.
Wikipedia: Acessa e analisa páginas da Wikipedia.
Preprocess Text: Realiza pré-processamento de dados textuais.
Corpus to Network: Transforma texto em redes de palavras.
Bag of Words: Converte texto em uma coleção de palavras.
Document Embedding: Gera representações vetoriais de documentos.
Similarity Hashing: Aplica hashing de similaridade em textos.
Sentiment Analysis: Analisa o sentimento expresso nos textos.
Tweet Profiler: Perfilha tweets para análise de conteúdo e padrões.
Topic Modelling: Identifica tópicos predominantes no texto.
LDAvis: Visualiza os tópicos identificados pelo LDA.
Corpus Viewer: Exibe o corpus de documentos processados.
Score Documents: Avalia documentos com base em modelos de tópicos.
Word Cloud: Gera nuvens de palavras a partir do texto.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 117

Inteligência Artificial Visual

Concordance: Encontra o contexto de palavras específicas.
Document Map: Mapeia documentos em espaço bidimensional.
Word Enrichment: Analisa enriquecimento de palavras em corpora.
Duplicate Detection: Detecta duplicatas em documentos.
Word List: Cria listas de palavras com base em critérios.
Keywords: Extrai palavras-chave significativas do texto.
Annotator: Anota documentos com palavras-chave em uma visualização.
Ontology: Trabalha com ontologias para aprimorar a análise.
Semantic Viewer: Fornece uma visualização semântica de dados textuais.
Collocations: Encontra colocações frequentes no texto.
Statistics: Fornece estatísticas descritivas de corpora de texto.
6.2 Importando documentos de texto
Para importar documentos no Orange Canvas vamos usar o widget "Import Documents", primeiro
selecione o ícone da pasta no widget para escolher a pasta desejada do seu computador. O widget
processará e carregará os arquivos de texto, incluindo formatos como .txt, .docx, .odt, .pdf, .xml e
.conllu. Se houver subpastas, elas serão utilizadas como rótulos de classe para o corpus. Após a
conclusão do carregamento, você verá o número de documentos importados, que podem então ser
examinados usando o widget "Corpus Viewer". Caso certos arquivos não sejam lidos, eles serão
ignorados, mas os arquivos processados estarão disponíveis na saída.
Iniciaremos nossa jornada exploratória no mundo do processamento de linguagem natural com
um exercício prático bastante introdutório, focando inicialmente na leitura de arquivos em formato TXT.
Esta etapa inicial servirá como alicerce para os desafios subsequentes. Em seguida, avançaremos
para um problema mais complexo, abordando a manipulação e análise de textos contidos em
documentos PDF.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 118

Inteligência Artificial Visual

Marketing e Cardiopatia
A interseção entre o marketing e a cardiopatia pode parecer, à primeira vista, improvável. Você
pode se perguntar: "Qual é a conexão entre marketing e cardiopatia?"A resposta reside na proposta
inovadora de treinar uma inteligência artificial (IA) para identificar e compreender as nuances
linguísticas específicas dos profissionais que escrevem sobre esses dois domínios distintos. O
objetivo é criar um modelo deIAque seja capaz de distinguir entre os textos voltados para o
marketing e aqueles relacionados à medicina, especificamente à cardiopatia. Este exercício não
apenas testa os limites daIAem reconhecer contextos e jargões especializados mas também abre
portas para aplicações inovadoras em análise de conteúdo digital. Para participar desta aventura
de aprendizado e contribuir para o avanço desta pesquisa, convidamos você a baixar odataset
disponível no link abaixo:
Dataset de textos Marketing vs Cardiopatia https://bit.ly/sandeco-MKT-medical-dataset
A Figura 6.3 exibe a interface do widget “Import Documents”, uma ferramenta essencial para
iniciar o seu projeto de mineração de textos.
Siga as etapas abaixo para importar seus documentos com sucesso:
Clique no widget “Import Documents” para iniciar o processo de importação.
2.Na seção “Source” do widget, clique no botão com ícone de pasta para selecionar o diretório
onde os textos que você deseja analisar estão armazenados. Nesse caso, a pasta onde estão
outras duas pastas com os textos de Marketing e Cardiopatia.
Uma vez selecionada a pasta, clique em “Reload” para carregar os documentos no Orange.
4.Defina a linguagem dos seus documentos na opção “Language”. Para textos em português,
escolha “Portuguese”.
5.O widget automaticamente marca a opção “Lemma” em “Conllu import options”, que é o padrão
para o processamento dos textos.
6.Após essas configurações, o widget exibirá o total de documentos e categorias carregadas na
parte inferior, sob a seção “Info”.
Realize essas ações no widget para preparar seus textos para a análise subsequente, que pode
incluir a classificação, análise de sentimentos, modelagem de tópicos, entre outros processos de
NLP.
Antes de qualquer coisa deixa eu te explicar o que é Corpus.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 119

Inteligência Artificial Visual

Figura 6.3: Interface do widget “Import Documents” no Orange Canvas, demonstrando como importar
documentos para análise de texto.
Umcorpusno contexto de Processamento de Linguagem Natural (NLP) é uma coleção de textos
escritos ou transcrições de fala compilados e organizados sistematicamente para serem usados
em análise linguística e treinamento de modelos demachine learning. Em NLP,corpora(plural de
corpus) são recursos vitais, pois fornecem os dados brutos necessários para desenvolver e testar
algoritmos de aprendizado de máquina em tarefas como tradução automática, reconhecimento de
fala, análise de sentimentos, sumarização de texto, entre outras.
Umcorpuspode ser anotado ou não anotado. Umcorpusanotado inclui informações adicionais,
como partes da fala (part-of-speech tags), estrutura sintática (parsing trees), entidades nomeadas e
outras formas de anotação linguística que ajudam na análise e no processamento automatizado. Es-
tas anotações são normalmente realizadas manualmente por linguistas ou geradas automaticamente
usando ferramentas de anotação.
Oscorporasão fundamentais para a criação de sistemas de NLP porque:
Treinamento de Modelos: Eles são usados para treinar modelos estatísticos e de aprendizado
profundo para entender e gerar linguagem humana.
Avaliação de Modelos: Eles também são empregados para testar e avaliar o desempenho dos
modelos, proporcionando benchmarks e métricas de sucesso.
Pesquisa Linguística: Além de seu uso em NLP computacional,corporasão usados em
linguística para estudar o uso da língua, como frequência de palavras, colocações e mudanças
linguísticas ao longo do tempo.
Desenvolvimento de Recursos: Eles permitem o desenvolvimento de léxicos, gramáticas e
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 120

Inteligência Artificial Visual

outras ferramentas linguísticas.
Exemplos decorporafamosos incluem o Corpus de Referência do Inglês Contemporâneo (COCA),
o British National Corpus (BNC), e o Google Books Ngram Corpus, cada um com diferentes focos
e propósitos. Para treinamento de modelos de NLP, é crucial que ocorpusseja grande, rico e
diversificado, para que os sistemas possam aprender a variedade e a complexidade da linguagem
humana.
Interagindo com o Corpus Viewer no Orange
O widget ‘Corpus Viewer‘ é uma ferramenta essencial no Orange para visualizar e inspecionar os
dados textuais que você carregou. A Figura 6.4 mostra a interface deste widget após a importação
de documentos.
Para trabalhar efetivamente com o ‘Corpus Viewer‘, siga estes passos:
Clique no widget ‘Import Documents‘ no seu fluxo de trabalho para carregar os textos.
Conecte o widget ‘Import Documents‘ ao ‘Corpus Viewer‘ arrastando uma linha entre eles.
Clique no ‘Corpus Viewer‘ para visualizar os documentos importados.
4.Utilize os filtros de pesquisa para refinar quais documentos são exibidos. Clique em ‘Filter...‘
na seção ‘Search features‘ e selecione o filtro desejado, como ‘category‘.
5.Examine a lista de documentos no painel central. Use a barra de rolagem para percorrer os
documentos importados ou clique em um específico para visualizá-lo.
6.Ao clicar em um documento, o conteúdo será exibido no painel da direita. Aqui você pode ler o
texto completo e analisar os dados que deseja trabalhar.
Através destas ações, você pode facilmente acessar e examinar diferentes partes do seucorpus,
o que é crucial para entender a estrutura dos dados e preparar-se para a análise subsequente.
6.3 Pré-processamento de textos
No campo do Processamento de Linguagem Natural (NLP) e, particularmente, quando aplicamos
técnicas de machine learning, o pré-processamento de textos é uma etapa fundamental que precede
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 121

Inteligência Artificial Visual

Figura 6.4: A interface do ‘Corpus Viewer‘ no Orange, ilustrando como os documentos importados
são apresentados e podem ser filtrados e examinados.
qualquer análise ou modelagem. O sucesso do seu modelo de machine learning está intrinsecamente
ligado à atenção e ao esmero dedicados neste estágio inicial.
O pré-processamento de textos pode ser comparado à preparação da matéria-prima antes da
fabricação de um produto. Essa etapa envolve várias técnicas críticas:
1. Limpeza de Dados: Remoção de informações irrelevantes ou que podem introduzir ruído,
como códigos HTML ou caracteres especiais.
2. Tokenização: Quebra do texto em unidades básicas (tokens), que podem ser palavras, frases
ou até mesmo caracteres.
3. Normalização: Conversão do texto para um formato uniforme, como a conversão para letras
minúsculas ou a remoção de acentuação.
4. Remoção de Stop Words: Exclusão de palavras comuns que tendem a aparecer frequente-
mente no texto, mas que oferecem pouco valor analítico, como preposições e artigos.
5. Stemming e Lemmatização: Redução das palavras a sua raiz ou forma base, facilitando a
análise e reduzindo a complexidade do texto.
6. Part-of-speech Tagging: Identificação da função gramatical das palavras no texto, o que pode
ser crucial para a compreensão de estruturas frasais e significados.
7. Named Entity Recognition (NER): Identificação e classificação de entidades nomeadas como
pessoas, organizações, locais, que podem ser essenciais para o entendimento do texto.
Um pré-processamento bem executado resulta em um conjunto de dados limpo e estruturado,
o que é indispensável para a eficácia do algoritmo de machine learning subsequente. Sem esse

CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 122

Inteligência Artificial Visual

cuidado, até os algoritmos mais avançados podem ser ineficazes, exemplificando o adágio "garbage
in, garbage out". Portanto, nunca subestime a importância do pré- processamento de textos em suas
aplicações de machine learning!
Preprocess Text
O widget "Preprocess Text"do Orange é uma ferramenta robusta que prepara textos para análise de
NLP e machine learning. Ele permite dividir o texto em tokens, filtrar palavras irrelevantes, aplicar
normalização (como stemming e lemmatization), criar n-grams e marcar tokens com etiquetas de
parte da fala. Os passos podem ser reorganizados para se adequar às necessidades da análise e
devem ser aplicados sequencialmente para o melhor resultado. O processo de pré-processamento é
crucial para a eficiência dos algoritmos de machine learning, impactando diretamente a qualidade
das insights geradas. A ordenação sugerida começa com a transformação do texto, seguida de
tokenização, marcação de partes da fala, normalização, filtragem e finalmente a construção de
n-grams.
Dentro do widget "Preprocess Text"do Orange, que é ilustrado na Figura 6.5, nós temos uma
variedade de opções de transformação de texto à nossa disposição. Comece explorando as opções
marcadas para uma transformação inicial, como converter todo o texto para minúsculas e remover
acentos, o que é vital para padronizar os dados de entrada. As opções não marcadas também
são importantes; "Parse html"é utilizado para extrair texto de código HTML, e "Remove urls"elimina
endereços web dos seus dados. Juntas, essas configurações garantem que o texto estará limpo e
uniforme, preparado para a análise ou para ser alimentado em modelos de machine learning. Utilize
estas ferramentas para refinar seus dados antes de prosseguir para a tokenização e outras etapas
de pré-processamento.
Na imagem da Figura 6.6 vamos usar a tokenização que é um método crucial no processamento
de texto, usado para quebrar o texto em componentes menores, como palavras, sentenças ou
bigramas, para análise no NLP. No Orange, a tokenização pode ser feita de várias maneiras,
cada uma atendendo a diferentes necessidades de análise. Se você deseja manter pontuações
juntamente com palavras, use a opção "Word & Punctuation". Para dividir apenas por espaços,
escolha "Whitespace". "Sentence"é útil quando você precisa de sentenças inteiras. Se precisar de
uma divisão personalizada, você pode fornecer sua própria expressão regular na opção "Regexp".
Por fim, a opção "Tweet"é especializada para lidar com texto de mídias sociais, mantendo hashtags,
emoticons e outros símbolos específicos. Dependendo do seu conjunto de dados e do foco da
análise, selecione a forma de tokenização que melhor atende ao seu projeto.
Na Figura 6.6, a expressão regular escolhida para a tokenização é\w+. Esta expressão é
amplamente usada para capturar sequências de caracteres alfanuméricos, tratando-os como palavras
individuais. Isso é ideal para análise de texto no NLP onde a pontuação não é relevante.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 123

Inteligência Artificial Visual

Figura 6.5: O widget "Preprocess Text"no Orange, mostrando as opções de transformação para
pré-processamento de texto.
A normalização, como apresentada na Figura 6.7, é um processo fundamental no pré-processamento
de dados em NLP que adapta o texto a uma forma mais básica ou canônica. No widget "Prepro-
cess Text"do Orange, a normalização pode ser feita por meio de diferentes técnicas como "Porter
Stemmer"ou "Snowball Stemmer", que reduzem as palavras às suas raízes, ou "Lemmatization", que
associa palavras a suas formas lexicais base. Cada método tem suas peculiaridades e a escolha
depende do objetivo da análise. O "Porter Stemmer"é rápido e eficiente para a língua inglesa,
enquanto o "Snowball Stemmer"suporta vários idiomas. Os lematizadores, como "WordNet"e "UD-
Pipe", são mais sofisticados e levam em conta o contexto das palavras para retornar a forma base
correta. Essas ferramentas são cruciais para reduzir a complexidade dos dados textuais e aumentar
a eficiência dos algoritmos de machine learning aplicados posteriormente.
Na Figura 6.7, vemos o painel de Normalização no widget "Preprocess Text"do Orange. Este
painel é utilizado para escolher como as palavras serão normalizadas. A normalização é crucial
para reduzir a variedade de formas que uma palavra pode assumir para um conjunto menor e mais
gerenciável de termos. Escolha "Porter Stemmer"ou "Snowball Stemmer"para aplicar técnicas de
stemming, ou opte por um dos lematizadores disponíveis para lematização, que é mais precisa ao
considerar o contexto da palavra. Essas ferramentas ajudam a padronizar o texto antes de prosseguir
para análises mais avançadas.
O processo de filtragem, como demonstrado na Figura 6.8, dentro do widget "Preprocess Text"do
Orange, é uma etapa crítica do pré-processamento de texto em NLP. Esta funcionalidade permite
refinar o conjunto de dados removendo ruídos e focando nas palavras significativas. A filtragem
pode ser feita de várias maneiras: você pode remover stopwords, que são palavras comuns com
pouca informação relevante, ou utilizar expressões regulares para excluir padrões de caracteres
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 124

Inteligência Artificial Visual

Figura 6.6: A seção de Tokenização no widget "Preprocess Text"do Orange, onde o usuário pode
escolher como dividir o texto em tokens.
específicos. Também é possível filtrar por frequência de documento, excluindo termos que aparecem
muito frequentemente ou raramente, e até mesmo selecionar tipos específicos de palavras, como
substantivos e verbos, para análise posterior. Cada uma dessas opções de filtragem ajuda a reduzir
o tamanho do seu conjunto de dados e a aumentar a relevância das características que serão
utilizadas em algoritmos de machine learning.
6.4 Bag of Words
O modelo Bag of Words (BoW) é uma representação simplificada usada no processamento de
linguagem natural (NLP) para transformar texto em um conjunto de características numéricas, que
podem ser utilizadas por algoritmos demachine learning. A ideia por trás do BoW é que um
documento pode ser descrito pela ocorrência de palavras, independente da ordem ou estrutura
gramatical. No modelo BoW, cada palavra única do texto é tratada como uma característica, e
a importância de cada palavra é quantificada pela frequência com que aparece no texto. Esta
representação é extremamente útil em muitas aplicações, como classificação de texto e análise de
sentimentos, pois permite que algoritmos de aprendizado trabalhem com dados textuais.
Por exemplo, consideremos as quatro frases apresentadas na Tabela 6.1: "gato gosta de peixe",
"cão gosta de osso", "gato gosta de gato", e "gato caça rato". No modelo BoW, essas frases
são transformadas em vetores numéricos com base na ocorrência de cada palavra. A palavra
"gato"aparece três vezes na terceira frase, que é indicado pelo número 2 na coluna correspondente
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 125

Inteligência Artificial Visual

Figura 6.7: O painel de Normalização no widget "Preprocess Text"do Orange, destacando as
diferentes opções de normalização de texto.
a "gato"(já que a palavra aparece duas vezes além da primeira ocorrência). Da mesma forma, as
palavras "caça"e "rato"são destacadas pela presença única na última frase. Portanto, cada frase é
representada por um vetor de números, que resume a informação sobre a presença e a frequência
das palavras no texto.
Frase caça cão de gato gosta osso peixe rato
gato gosta de peixe 0 0 1 1 1 0 1 0
cão gosta de osso 0 1 1 0 1 1 0 0
gato gosta de gato 0 0 1 2 1 0 0 0
gato caça rato 1 0 0 1 0 0 0 1
Tabela 6.1: Exemplo de Bag of Words (BoW) com frases
A representação Bag of Words (BoW) é fundamental para a criação de Word Clouds, também
conhecidas como nuvens de palavras. Word Clouds são visualizações gráficas que destacam as
palavras mais frequentes em um texto, onde a importância de cada termo é indicada pelo tamanho
da fonte ou pela cor. Através do modelo BoW, é possível quantificar a frequência de cada palavra
de maneira eficiente, transformando esses dados em uma representação visual imediatamente
perceptível. Ao revelar os termos mais proeminentes, as Word Clouds oferecem uma visão rápida e
intuitiva dos temas predominantes em um conjunto de dados textuais, tornando-se uma ferramenta
valiosa tanto para análise exploratória de dados quanto para apresentações de informações chave
ao público.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 126

Inteligência Artificial Visual

Figura 6.8: A aba de Filtragem no widget "Preprocess Text"do Orange, mostrando as opções de
filtragem de texto disponíveis para o usuário.
O Widget Bag of Words
O widget Bag of Words no Orange é uma ferramenta poderosa que transforma texto em uma matriz
de termos e sua frequência. Esse processo é conhecido como vetorização e é essencial para muitas
tarefas de NLP. Na Figura 6.9, podemos ver as opções para ajustar a frequência dos termos e como
os documentos são considerados no conjunto de dados. A regularização, que pode ser L1 ou L2,
ajuda a normalizar os vetores de termos, o que é especialmente útil para modelos de machine
learning que dependem da magnitude dos dados de entrada. Ao configurar essas opções no widget,
você está preparando o texto para análises futuras, como modelagem de tópicos ou classificação de
texto.
6.5 Word Cloud
Uma Word Cloud, ou nuvem de palavras, é uma ferramenta de visualização de dados que apre-
senta palavras de um texto em diferentes tamanhos, cores e direções. O tamanho de cada palavra
representa sua frequência ou importância no texto, tornando a Word Cloud uma maneira intuitiva
de destacar os conceitos mais proeminentes ou frequentemente discutidos. Esta técnica é ampla-
mente utilizada para análise de sentimentos, resumos de feedback e exploração de dados textuais,
permitindo aos usuários capturar rapidamente a essência de grandes volumes de texto.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 127

Inteligência Artificial Visual

Figura 6.9: Interface do widget Bag of Words no Orange, destacando as opções disponíveis para
configuração da vetorização dos termos.
Select Rows
Para gerar uma Word Cloud informativa no Orange, é interessante separar as palavras por classes,
como ’Cardio’ e ’Marketing’. O widget ’Select Rows’, como vemos na Figura 6.10, permite essa
separação de maneira eficaz. Acesse o widget e configure as condições para filtrar os dados por
categoria. Com isso, você pode criar duas Word Clouds distintas, cada uma representando as
palavras mais proeminentes em sua respectiva categoria. Essa abordagem destaca as diferenças e
particularidades de cada conjunto de textos, proporcionando insights mais aprofundados para sua
análise.
Para criar uma Word Cloud no Orange, siga estes passos. Primeiro, use o widget ’Bag of Words’
para processar seu corpus de texto. Em seguida, conecte-o ao widget ’Word Cloud’, que exibirá as
palavras em um formato visual baseado em suas frequências. As palavras maiores na nuvem são
aquelas que aparecem com mais frequência no corpus. Este processo ajuda a destacar os termos
mais importantes dentro de um conjunto de textos. A Figura 6.11 oferece uma visão poderosa sobre
a linguagem utilizada em textos relacionados a doenças cardíacas, permitindo que pesquisadores e
profissionais de saúde obtenham rapidamente uma compreensão das palavras-chave e conceitos
mais discutidos nessa área.
Agora que temos todo o processamento do texto feito, vamos criar uma IA para reconhecer
as características dos textos de forma que possamos classificar novos textos entre marketing e
cardiopatia. O primeiro passo é ajustar a capacidade do nosso modelo de rede neural para evitar
ooverfitting. Para isso, abra a configuração da rede neural no Orange Canvas e reduza o número
de neurônios nas camadas ocultas. Insira um valor que equilibre a complexidade do modelo e
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 128

Inteligência Artificial Visual

Figura 6.10: O widget ’Select Rows’ no Orange, demonstrando como selecionar e renomear dados
para as categorias ’Cardio’ e ’Marketing’.
a quantidade de dados disponíveis; um número menor de neurônios pode ajudar a prevenir o
overfitting.
Em seguida, clique no widgetNeural Networkpara abrir as suas opções. Na seção "Neurons in
hidden layers", escreva um número menor do que o inicialmente proposto; por exemplo, insira “64”.
Essa ação visa a simplificar o modelo para que ele possa generalizar melhor para dados não vistos,
ao invés de memorizar o conjunto de treinamento.
Após ajustar o modelo, vá ao widgetTest and Scoree inicie o treinamento e avaliação da sua
IA. Foque em métricas importantes como a Acurácia (CA), F1 Score e outras relevantes para o seu
problema. Se o modelo estiver performando bem, as métricas de avaliação se aproximam de 1, o
que indica uma classificação quase perfeita.
Por fim, não se esqueça de explorar outros tipos de algoritmos deMachine Learning. Cada
modelo tem suas peculiaridades e pode se adequar de forma diferente ao seu problema. Faça testes
comparativos para encontrar o melhor modelo para a sua tarefa de classificação de texto.
A seguir, a configuração de uma rede neural no Orange Canvas é ilustrada na Figura 6.12.
Transforme os textos criados em umCorpusno Orange. Comece clicando no widgetCorpuse
selecione a opção para escolher o idioma dos seus textos. É crucial selecionar a língua correta;
neste caso, escolha "Português"para assegurar que o processamento de texto será realizado de
acordo com as regras gramaticais e de tokenização específicas da língua.
No painel de configurações doCorpus, você terá a opção de definir quais características dos textos
deseja utilizar. Concentre-se na seção "Used text features"e certifique-se de que a característica
"Document"está selecionada, pois é ela que contém o corpo do texto que queremos analisar. Caso
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 129

Inteligência Artificial Visual

Figura 6.11: Word Cloud gerada a partir do corpus de texto na área de doenças cardíacas, desta-
cando os termos mais relevantes.
existam características que não são relevantes para a sua análise, como "Title"neste exemplo, você
pode optar por ignorá-las. Isso ajudará na precisão da sua modelagem e análise, pois apenas os
dados pertinentes serão considerados.
Após configurar estas opções, seus textos estarão prontos para serem processados e visuali-
zados noCorpus Viewer. Esta etapa é crucial para verificar se o pré-processamento foi aplicado
corretamente e se os textos estão prontos para serem utilizados em tarefas como a classificação ou
a clusterização.
A Figura 6.13 ilustra como configurar umCorpusno Orange, destacando a importância de
selecionar o idioma correto e as características do texto a serem utilizadas na análise.
Depois de criar seucorpus, é essencial aplicar as mesmas etapas de pré-processamento que
foram utilizadas durante o treinamento. Isso garantirá a consistência nos dados e permitirá que os
modelos deMachine Learningfuncionem corretamente. Primeiro, conecte o widgetCreate Corpus
ao widgetCorpuspara converter os dados brutos em um formato que o Orange possa interpretar.
Em seguida, arraste uma linha do widgetCorpuspara o widgetPreprocess Text. Aqui, você deve
configurar as mesmas opções de pré-processamento que usou anteriormente, como tokenização,
remoção de palavras comuns e normalização. Esses passos são cruciais para preparar os textos
para análise, transformando-os em dados uniformes e analisáveis.
Após pré-processar o texto, é hora de transformar ocorpusem um formato numérico que possa
ser usado para modelagem. Para fazer isso, conecte o widgetPreprocess Textao widgetBag of
Words. Assegure-se de que as configurações correspondam às do processo de treinamento. O
resultado final será uma matriz de termos, ou um "Bag of Words", que representa a frequência das
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 130

Inteligência Artificial Visual

Figura 6.12: Configuração de uma rede neural no Orange Canvas.
palavras dentro do seucorpus.
Esta representação é o que você usará para alimentar seu modelo de classificação ou qualquer
outro algoritmo deMachine Learningque desejar aplicar. A etapa de Bag of Words é ilustrada na
Figura 6.14, onde o fluxo de trabalho do Orange Canvas mostra como as palavras são coletadas e
transformadas em dados numéricos.
Ligue seus novos dados e a rede neural treinada ao widget "Predictions". Veja que a rede neural
acertou a classe dos textos corretamente, o que indica uma boa performance do modelo. Para isso,
primeiro, assegure-se de que a saída do widgetBag of Wordsestá conectada à entrada do modelo
treinado, neste caso, uma rede neural. O próximo passo é conectar o modelo treinado ao widget
Predictionspara classificar os novos textos.
Clique no widgetPredictionspara visualizar os resultados. Se tudo estiver correto, você verá as
previsões do modelo para cada novo texto, juntamente com a probabilidade associada a cada classe.
Esse processo é crucial para avaliar a qualidade do seu modelo em dados não vistos anteriormente
e garantir que ele está classificando os textos de forma correta.
Para uma inspeção mais detalhada, observe as previsões feitas pela IA no quadro à direita. Se
as classes dos textos foram identificadas corretamente como "marketing"ou "cardio", isso significa
que seu modelo é capaz de distinguir entre essas duas categorias de texto de maneira eficiente.
A configuração completa do fluxo de trabalho no Orange para classificação de texto está ilustrada
na Figura 6.15, que destaca a importância de uma correta configuração e avaliação de um modelo
deMachine Learning.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 131

Inteligência Artificial Visual

Figura 6.13: Configuração de umCorpusno Orange, mostrando a seleção de idioma e as caracterís-
ticas de texto utilizadas.
6.6 Avaliando textos com as Redes Transformer
Ao nos aventurarmos na vasta paisagem do Processamento de Linguagem Natural (NLP), encon-
tramos ferramentas poderosas que transformaram a maneira como as máquinas entendem o texto
humano. Uma dessas inovações são as Redes Transformer, uma arquitetura de modelo que facilitou
avanços significativos em tarefas de NLP. Nesta seção, exploraremos como os Transformers analisam
e compreendem o texto, proporcionando uma precisão sem precedentes em comparação com as
técnicas anteriores.
Os Transformers revolucionaram a compreensão de contexto e a geração de texto, superando
os modelos de redes neurais recorrentes e convolucionais ao tratar a sequência de palavras de
forma integral, em vez de partes isoladas. Eles utilizam mecanismos de atenção que ponderam a
influência de diferentes palavras na interpretação de cada palavra em uma sentença. Este método
permite que o modelo destaque as relações complexas e a relevância entre as palavras, levando a
um entendimento mais refinado do texto.
Vamos mergulhar em como essas redes podem ser treinadas para realizar uma variedade de
tarefas, desde a classificação de sentimentos até a tradução automática. Através de exemplos
práticos e interativos, demonstraremos como aplicar as Redes Transformer a conjuntos de dados
de texto, avaliar sua eficácia e interpretar suas previsões. Ao final desta seção, você terá uma
compreensão sólida de como os Transformers funcionam e como podem ser aplicados para extrair
insights valiosos de textos complexos.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 132

Inteligência Artificial Visual

Figura 6.14: Processamento de texto e transformação em Bag of Words no Orange Canvas.
Dataset de textos em PDF https://bit.ly/sandeco-papers-dataset
Acessando o link providenciado, você encontrará umdatasetrico e diversificado, disponível
para download, composto por textos em formato PDF. Este conjunto de dados é singular, pois
abrange duas áreas críticas do conhecimento moderno: a medicina e a inteligência artificial (IA). Tal
diversidade oferece uma oportunidade única para pesquisadores, desenvolvedores e entusiastas da
IAenfrentarem um desafio comum e intrigante: treinar modelos demachine learningcapazes de não
apenas diferenciar entre textos de ambas as áreas mas também extrair insights valiosos e relevantes.
Este tipo de problema, conhecido na literatura demachine learningcomo classificação de texto, é
um excelente ponto de partida para aqueles que buscam aplicar aIAem um contexto interdisciplinar,
proporcionando uma rica experiência de aprendizado e inovação. Além disso, a capacidade de
analisar e categorizar automaticamente textos médicos e deIAtem implicações práticas significativas,
desde a melhoria dos sistemas de informação em saúde até o avanço das técnicas de pesquisa
em inteligência artificial. Encorajamos os interessados a explorar estedataset, visando não apenas
resolver um problema técnico desafiador mas também contribuir para o progresso dessas áreas
vitais para o bem-estar humano e o avanço tecnológico.
Carregue odatasetque você baixou selecionando a pastaTRAIN. Os textos são artigos científicos
e estão em inglês, porém todos os procedimentos que faremos aqui servirão para o Português
também. Para iniciar o processo, clique no widgetImport Documents. No campo “Folder”, utilize
o botão de busca para navegar até o diretório onde odatasetestá localizado e selecione a pasta
TRAINque contém os documentos de treinamento.
É importante definir corretamente o idioma dos documentos para o pré-processamento. No
campo “Language”, assegure-se de escolher “English”, já que os textos a serem importados estão
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 133

Inteligência Artificial Visual

Figura 6.15: Classificação de texto usando uma rede neural no Orange e visualização dos resultados
no widget "Predictions".
neste idioma. Isso garantirá que o Orange utilize as ferramentas adequadas de tokenização e análise
para o inglês.
Assim que tiver selecionado o diretório correto e o idioma, clique em “Reload” para carregar os
textos no Orange. OImport Documentsirá processar os arquivos PDF e os converterá em um formato
legível para a plataforma, criando um novoCorpusque será utilizado nas etapas subsequentes de
análise.
O procedimento de importação de documentos em PDF é uma etapa crítica que permite a
transformação de textos não estruturados em dados analisáveis. A Figura 6.16 mostra a interface do
widgetImport Documentsno Orange Canvas, destacando as ações necessárias para carregar e
preparar os textos para o pré-processamento.
Para visualizar os textos que serão aprendidos, você pode utilizar o "Corpus Viewer"onde você
poderá ver uma lista de documentos importados, bem como detalhes específicos sobre cada um,
como categoria, nome, caminho e conteúdo.
O campo "category"mostra a classificação dos textos, facilitando o agrupamento por temas ou
assuntos. O "name"apresenta o título do documento, permitindo uma rápida identificação. No "path",
você encontrará o caminho do arquivo, que indica a localização exata do texto no seu sistema de
arquivos. Por fim, a seção "content"exibe o corpo do texto, onde você pode ler e revisar o material
importado conforme mostra a Figura 6.17
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 134

Inteligência Artificial Visual

Figura 6.16: Importação de textos em PDF no Orange Canvas, mostrando a seleção do diretório de
treinamento e a definição do idioma para o pré-processamento dos documentos.
ATENÇÃO É TUDO O QUE VOCÊ PRECISA
As Redes Transformer representam um marco no campo do Processamento de Linguagem Natural
(NLP), introduzindo uma abordagem inovadora que mudou drasticamente a capacidade das máquinas
de compreender e gerar texto. A arquitetura Transformer, introduzida em 2017 com o artigo Attention
Is All You Need , afastou-se dos modelos tradicionais baseados em redes neurais recorrentes
(RNNs) e convolucionais (CNNs), que processam sequências de texto de maneira incremental. Em
vez disso, os Transformers processam toda a sequência de texto de uma vez, permitindo que o
modelo dê atenção a cada palavra no contexto das demais, independentemente de sua posição na
sequência como mostra a Figura 6.18. Isso proporciona uma compreensão contextual muito mais
rica, capturando nuances e relacionamentos complexos entre as palavras.
O que torna as Redes Transformer revolucionárias é o mecanismo de atenção, particularmente
a atenção multi-cabeça, que permite que o modelo avalie diferentes partes da sequência de texto
simultaneamente. Este método de atenção foca em várias partes do texto ao mesmo tempo, tornando
possível para o modelo capturar um amplo espectro de dependências e correlações sem a limitação
de sequencialidade imposta pelas RNNs. A atenção multi-cabeça assegura que cada palavra
contribua para o entendimento do significado do texto como um todo, levando a interpretações que
levam em conta o contexto completo.
Os Transformers serviram como base para o desenvolvimento de uma variedade de modelos de
NLP de última geração, como o BERT (Bidirectional Encoder Representations from Transformers),
GPT (Generative Pretrained Transformer), e Gemini, entre outros. Estes modelos pré-treinados
têm demonstrado capacidades notáveis em uma vasta gama de tarefas de NLP, incluindo tradução
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 135

Inteligência Artificial Visual

Figura 6.17: Interface do "Corpus Viewer"no Orange Canvas.
automática, sumarização de texto, geração de conteúdo e compreensão de leitura. A arquitetura
Transformer permitiu que esses modelos aprendessem representações de texto profundamente
contextualizadas, resultando em um desempenho que muitas vezes supera o entendimento humano
em tarefas específicas.
A popularidade e eficácia das Redes Transformer no campo da IA são inegáveis. Sua habilidade
de captar contextos complexos e suas relações intrincadas no texto abrem caminho para aplicações
inéditas e empolgantes, onde a interpretação precisa e a geração de linguagem natural são fun-
damentais. A ascensão desses modelos tem sido tão impactante que eles estão remodelando as
técnicas de NLP, solidificando-se como a escolha preferida para pesquisadores e profissionais que
buscam a vanguarda da tecnologia de inteligência artificial.
No Orange Canvas, para criar representações vetoriais de texto, conhecidas como embeddings,
você pode recorrer ao poder das redes Transformers. Inicie selecionando o widget "Document Em-
bedding". Dentro dele, escolha a opção "Multilingual SBERT", uma variante do modelo Transformer
que suporta vários idiomas, oferecendo a flexibilidade necessária para trabalhar com conjuntos de
dados diversos. O SBERT Multilingual é uma escolha eficaz para esta tarefa, dada sua capacidade
de capturar nuances contextuais do texto.
Com o widget configurado para "Multilingual SBERT", você estará utilizando uma das implemen-
tações mais avançadas de redes Transformers, que se baseia na mesma arquitetura que alimenta
modelos de alto desempenho como GPT e BERT. O SBERT é especialmente projetado para gerar
embeddings que resumem efetivamente o conteúdo semântico dos textos, permitindo aplicações
subsequentes em tarefas como classificação, agrupamento ou recuperação de informações. Por ser
um algoritmo de alta precisão, o tempo de processamento pode ser um pouco mais extenso, mas os
resultados compensam o investimento temporal.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 136

Inteligência Artificial Visual

Figura 6.18: Arquitetura de uma Rede Transformer.
Após o processamento, para não perder os dados gerados, conecte o widget "Document Embed-
ding"ao widget "Save Data". Esta ação irá garantir que você possa salvar e reutilizar os embeddings
sem a necessidade de reprocessar seus dados, economizando tempo e recursos computacionais
em projetos futuros. A configuração de criação e salvamento dos embeddings no Orange Canvas é
ilustrada na Figura 6.19.
ATENÇÃO - Olha que Legal
Ao trabalhar com Redes Transformers, como o modelo SBERT Multilíngue no Orange Canvas, uma
vantagem notável é a eliminação da necessidade de pré-processamento manual de dados. Esses
modelos avançados são projetados para compreender texto bruto, executando internamente todas
as etapas necessárias para converter texto em uma representação numérica significativa. Isso inclui
a tokenização, a codificação posicional e a atenção múltipla, todos processos intrincados que
ocorrem sob o capô do modelo Transformer. Portanto, quando utilizamos essas redes, podemos nos
poupar do esforço de realizar tarefas de pré-processamento, confiando na capacidade inerente do
modelo de gerenciar essas operações e focar em extrair o máximo de suas aplicações de NLP.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 137

Inteligência Artificial Visual

Figura 6.19: Processo de criação de embeddings utilizando a Rede Transformer SBERT Multilíngue
no Orange Canvas e salvando os dados resultantes.
Hora de treinar com Embeddings de texto.
É hora de treinar nossa Inteligência Artificial no Orange Canvas, e um dos componentes cruciais
nesse processo é o ajuste da arquitetura da rede neural para evitar o sobreajuste, conhecido como
overfitting. Ao reduzir o número de neurônios na camada oculta, como mostrado na configuração do
widget "Neural Network", ajustamos para 64, garantimos que o modelo seja capaz de generalizar
melhor para novos dados, em vez de memorizar o conjunto de treinamento. Isso é essencial para
assegurar que nossa IA tenha um desempenho robusto quando exposta a dados que não viu durante
o treinamento.
Com o widget "Test and Score", é possível validar a eficácia do modelo. Após treinar sua rede
neural, clique neste widget para avaliar a performance da IA. Observe indicadores como AUC (Área
sob a Curva ROC), CA (Acurácia), F1 Score, Precisão e Recall. Uma pontuação de 1.000 em cada
uma dessas métricas, como ilustrado na tela, sinaliza que a IA alcançou a classificação perfeita
durante o processo de validação.
No entanto, não se limite apenas a uma abordagem. O Orange Canvas oferece uma variedade de
algoritmos de Machine Learning que podem ser explorados. Experimente diferentes modelos para
encontrar o que melhor se adequa ao seu problema específico, seja ele classificação, regressão ou
agrupamento. Lembre-se de que cada tipo de algoritmo possui suas peculiaridades e pode revelar
insights diferentes dos dados.
A Figura 6.20 ilustra o fluxo de trabalho de treinamento da IA no Orange Canvas, destacando a
importância da configuração cuidadosa da rede neural e da avaliação dos resultados do modelo.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 138

Inteligência Artificial Visual

Figura 6.20: Fluxo de trabalho de treinamento e avaliação da IA no Orange Canvas, enfatizando a
otimização da rede neural e a investigação de métricas de desempenho.
Hora de treinar com Embeddings de texto.
Quando estiver pronto para classificar novos textos usando sua IA treinada no Orange Canvas,
comece acessando seus dados de teste. Clique no widget "Import Documents"para começar a
importar os documentos que deseja classificar. No painel de configuração que aparece, selecione a
pasta "TEST"que contém seus dados de teste clicando no botão de busca e navegando até o local
apropriado. Certifique-se de clicar em "Reload"para carregar os documentos na plataforma. Isso irá
prepará-los para a classificação e permitirá que você veja como sua IA performa com dados que não
foram vistos durante o treinamento.
Definir o idioma dos documentos para "English"é crucial se o seu conjunto de teste estiver
nesse idioma, assegurando que o processamento seja feito corretamente. Após os textos estarem
carregados, você pode prosseguir para utilizar o modelo treinado, aplicando-o aos novos dados para
ver como ele os classifica.
A configuração completa para classificar novos textos no Orange Canvas é ilustrada na Figura
6.21.
Na etapa de preparação para classificar textos desconhecidos, é igualmente crucial criar embed-
dings para o conjunto de teste. No Orange Canvas, isso é realizado com o mesmo widget "Document
Embedding"usado anteriormente. Selecione "Multilingual SBERT"nas opções do widget, garantindo
que a criação dos embeddings de teste seja consistente com os embeddings de treinamento. A
coerência entre os processos de treinamento e teste é fundamental para o sucesso da classificação
subsequente. Os embeddings são representações vetoriais que capturam a essência semântica
dos textos e, ao utilizar o SBERT Multilíngue, você se beneficia de uma das arquiteturas de Trans-
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 139

Inteligência Artificial Visual

Figura 6.21: Processo de classificação de novos textos usando o Orange Canvas.
former mais avançadas, preparando seus dados de teste com a mesma precisão de alta qualidade
empregada no conjunto de treinamento.
Após a configuração, lembre-se de clicar em "Commit Automatically"para que os embeddings
sejam gerados sem a necessidade de intervenção adicional. Este passo é essencial para manter
um fluxo de trabalho eficiente no Orange Canvas. A Figura 6.22 mostra a interface do widget
"Document Embedding"configurado para gerar embeddings de teste, com a opção "Multilingual
SBERT"selecionada.
Figura 6.22: Configuração do widget "Document Embedding"para a criação de embeddings de teste
utilizando o SBERT Multilíngue no Orange Canvas.
Uma vez que os embeddings estão prontos, utilize o modelo treinado, em nosso caso, uma
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 140

Inteligência Artificial Visual

rede neural, conectando-o ao widget "Predictions". É aqui que a capacidade das Redes Trans-
former realmente brilha, classificando com sucesso textos que podem ser extensos e complexos,
demonstrando sua robustez mesmo quando lidando com grandes volumes de palavras e informações
densas. A tela "Predictions"fornecerá um panorama claro da performance da rede, onde você pode
verificar a precisão das classificações realizadas pela IA.
Como os resultados na Figura 6.23 indicam, todos os PDFs de teste foram classificados correta-
mente, um testemunho do poder do Transformer e sua habilidade de manejar e interpretar textos de
tamanho considerável. Este nível de acurácia em classificação é o que torna os modelos baseados
em Transformer, como o SBERT, ferramentas indispensáveis na caixa de ferramentas de um cientista
de dados.
Figura 6.23: Interface do Orange Canvas mostrando a classificação bem-sucedida de textos de teste
através de um modelo baseado em Transformer.
6.7 Análise de Sentimentos em Textos
A análise de sentimentos em textos é uma aplicação fascinante do Processamento de Linguagem Na-
tural (NLP), que se dedica a discernir e quantificar as emoções subjacentes nas palavras. Utilizando
algoritmos de aprendizado de máquina e inteligência artificial, esta técnica permite às máquinas
não apenas ler texto, mas também interpretar o contexto emocional, o que pode variar de positivo,
negativo a neutro. Esta capacidade é particularmente útil em áreas como o monitoramento de mídias
sociais, feedback de clientes e análise de mercado, onde entender as reações emocionais das
pessoas pode fornecer insights valiosos para as decisões de negócios e estratégias de comunicação.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 141

Inteligência Artificial Visual

Desenvolver um sistema eficaz de análise de sentimentos requer uma compreensão profunda de
nuances linguísticas e culturais, pois a expressão emocional pode ser sutil e altamente contextu-
alizada. Modelos avançados, como redes neurais e especialmente modelos de Transformer, são
treinados em grandes conjuntos de dados de texto anotados, aprendendo a identificar padrões e
indicadores que representam sentimentos específicos. Esses modelos são capazes de captar desde
expressões explícitas de emoção até o uso implícito de sarcasmo e ironia, desvendando camadas
de significado que vão além do conteúdo superficial.
A análise de sentimento não está restrita apenas à identificação da polaridade emocional; ela
também pode ser estendida para detectar intensidade, urgência e até mesmo intenções subjacentes.
Por exemplo, no domínio do atendimento ao cliente, reconhecer o nível de urgência ou frustração em
um feedback pode ajudar a direcionar recursos e atenção de forma mais eficiente, melhorando a
experiência do cliente e a eficácia operacional. Com a evolução contínua dos modelos de NLP e o
aumento da disponibilidade de dados textuais, a análise de sentimentos está se tornando cada vez
mais sofisticada, abrindo novas fronteiras para a interação humana-computador.
Dataset de Tweetts https://bit.ly/sandeco-tweets-analise-sentimento
Para começar, clique no widget "File"e insira a URL fornecida na caixa de opções "URL", que
permite carregar diretamente um arquivo CSV de tweets para análise. Após inserir o endereço,
clique em "Reload"para que o Orange Canvas processe e carregue os dados conforme mostra a
Figura 6.24.
O arquivo CSV importado via URL traz um conjunto de tweets prontos para serem analisados,
contendo instâncias textuais que refletem diferentes sentimentos expressos pelos usuários. Esta
abordagem direta permite aos pesquisadores e analistas uma forma rápida e eficaz de iniciar o
processo de análise de sentimentos, economizando tempo e esforço que poderiam ser gastos em
etapas preliminares de coleta de dados.
Para transformar esses dados em um formato compatível para análise de sentimentos, encaminhe-
os para o widget "Corpus". Este processo converte o CSV em um "Corpus", que é um conjunto de
dados especial que o Orange utiliza para operações de NLP.
Uma vez que seu arquivo CSV está carregado como um Corpus, avance para o widget "Sentiment
Analysis"para iniciar a análise de sentimentos propriamente dita. Aqui, é importante selecionar o
método "Multilingual sentiment"com o idioma definido para "Portuguese". Essa escolha habilita o
Orange a processar e analisar o sentimento dos textos em português, aplicando modelos treinados
que podem capturar com precisão a polaridade emocional expressa nos dados.
O widget "Sentiment Analysis"do Orange é uma ferramenta poderosa que permite uma análise
de sentimentos abrangente, capaz de processar textos em diferentes idiomas. A Figura 6.25 mostra
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 142

Inteligência Artificial Visual

Figura 6.24: Carregamento de dados de tweets para análise de sentimentos utilizando o widget
"File"no Orange Canvas.
a configuração deste widget para a análise de sentimentos em português, uma funcionalidade
essencial para quem trabalha com dados em múltiplos idiomas.
Figura 6.25: Configuração do widget "Sentiment Analysis"para análise de sentimentos multilíngue
em português no Orange Canvas.
Após realizar a análise de sentimentos no Orange Canvas, os resultados são exibidos no widget
"Data Table". Aqui, você pode examinar cada texto juntamente com o sentimento associado, quantifi-
cado numericamente. Valores positivos refletem sentimentos positivos, enquanto valores negativos
indicam sentimentos negativos. Uma pontuação de zero geralmente denota uma neutralidade
emocional no texto. Esta tabela facilita a identificação rápida de padrões e tendências nos dados,
permitindo uma análise mais detalhada de como os sentimentos são distribuídos através do conjunto
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 143

Inteligência Artificial Visual

de dados.
É essencial examinar esses números cuidadosamente, pois eles representam a interpretação
computacional dos sentimentos expressos. Avaliar os resultados numericamente ajuda a compreen-
der a eficácia do modelo de análise de sentimentos utilizado e a precisão com que ele reflete as
emoções humanas expressas textualmente. A quantificação de sentimentos abre portas para uma
variedade de aplicações práticas, desde o monitoramento da percepção da marca até a otimização
da experiência do cliente.
A Figura 6.26 no seu documento LaTeX apresenta a interface do widget "Data Table"com os
resultados da análise de sentimentos, destacando como o Orange pode ser usado para converter
eficientemente grandes volumes de texto em dados emocionais quantificáveis.
Figura 6.26: Resultados da análise de sentimentos exibidos no widget "Data Table"do Orange
Canvas.
Considerações Finais desse importante capítulo
O estudo e a prática do Processamento de Linguagem Natural (NLP) são indiscutivelmente pilares
fundamentais na vanguarda da inteligência artificial, uma vez que possibilitam às máquinas não
apenas compreender, mas também interagir com a linguagem humana de maneira eficiente e signifi-
cativa. A evolução dos modelos de NLP, especialmente com a introdução das Redes Transformer,
representou um salto quântico na área, permitindo que nuances contextuais e sutilezas da comuni-
cação sejam capturadas com precisão sem precedentes. Esses avanços são cruciais em uma era
dominada pela informação, onde a habilidade de analisar grandes volumes de texto rapidamente e
extrair insights valiosos é uma vantagem competitiva inestimável.
A arquitetura Transformer, em particular, com seu mecanismo de atenção inovador, desencadeou
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 144

Inteligência Artificial Visual

uma série de desenvolvimentos que têm remodelado continuamente o campo do NLP. Tarefas que
antes eram consideradas desafiadoras, como a tradução automática, a sumarização de textos e a
análise de sentimentos, agora são realizadas com uma facilidade que rivaliza com a compreensão
humana. Este capítulo demonstrou a aplicabilidade dessas tecnologias avançadas no Orange
Canvas, uma plataforma que democratiza o acesso ao NLP, abrindo portas para usuários sem
formação especializada em programação.
Com a interface intuitiva e visual do Orange Canvas, a análise de textos torna-se acessível a
um público mais amplo, rompendo a barreira da complexidade técnica. Pesquisadores, analistas de
mercado, e profissionais de diversas áreas agora podem implementar fluxos de trabalho de NLP
robustos com apenas alguns cliques, explorando dados textuais com a mesma profundidade que
um cientista de dados especializado. Isso prova que a combinação de modelos de NLP poderosos
com ferramentas amigáveis ao usuário é uma força a ser reconhecida, facilitando a descoberta de
tendências, a identificação de padrões e a tomada de decisão informada em várias frentes.
Em conclusão, este capítulo ressalta não apenas a importância do NLP e das Redes Transformer
na era da informação, mas também celebra a simplicidade e a eficácia com que tais tecnologias
podem ser aplicadas no Orange Canvas. Ao permitir que usuários sem habilidades avançadas de
codificação mergulhem na análise de textos, o Orange Canvas está equipando uma nova geração de
analistas para enfrentar os desafios da era digital, impulsionando a inovação e a criatividade através
do poder da linguagem processada por máquinas.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 145

Inteligência Artificial Visual

6.8 EXERCÍCIOS
1.Explique o conceito de Redes Transformer e discuta sua importância para o Processamento
de Linguagem Natural moderno. Compare e contraste com modelos anteriores baseados em
RNN e CNN.
2.Descreva o mecanismo de atenção utilizado pelas Redes Transformer e como ele permite que
esses modelos compreendam o contexto de uma palavra dentro de uma sentença.
3.Defina o modelo Bag of Words (BoW) e discuta suas limitações. Como os modelos de
embeddings, como o SBERT, superam essas limitações?
4.Discuta a importância do pré-processamento no pipeline de NLP e descreva as etapas típicas
realizadas durante esse processo.
5.Explique o que é umcorpusno contexto de NLP e sua importância para o treinamento de
modelos demachine learning.
6.No Orange Canvas, utilize o widget "Corpus"para importar um conjunto de documentos.
Configure o idioma apropriadamente e explore os textos utilizando o widget "Corpus Viewer".
7.Crie uma Word Cloud no Orange Canvas utilizando o widget "Bag of Words"seguido do widget
"Word Cloud". Selecione um conjunto de dados e gere uma visualização das palavras mais
frequentes.
8.Realize uma análise de sentimentos em um conjunto de tweets em português usando o
widget "Sentiment Analysis"no Orange Canvas. Analise os resultados e identifique padrões de
sentimentos positivos e negativos.
9.Utilize o widget "Document Embedding"no Orange Canvas para gerar embeddings de um
conjunto de textos. Salve os dados processados com o widget "Save Data".
Treine um modelo de classificação de texto no Orange Canvas usando uma rede neural. Ajuste
o número de neurônios na camada oculta para preveniroverfittinge avalie o modelo com o
widget "Test and Score". Varie a configuração de neurônios e compare o desempenho.
CAPÍTULO 6. INTELIGÊNCIA ARTIFICIAL PARA TEXTOS 146

Inteligência Artificial Visual

CAPÍTULO 7
7 ChatGPT no Orange Canvas
Este capítulo explora a integração do ChatGPT com o Orange Canvas, abrindo novos caminhos
para o ensino e a aplicação prática de inteligência artificial (IA) sem a necessidade de habilidades
avançadas em programação. A colaboração entre essas duas poderosas ferramentas amplia
a acessibilidade e a interatividade no campo da IA, tornando-a mais tangível para educadores,
estudantes e entusiastas da tecnologia.
Com a inclusão dos widget do ChatGPT, uma IA avançada capaz de entender e gerar linguagem
humana de maneira coesa, os usuários podem agora engajar-se em diálogos interativos para
explorar conceitos complexos de IA, receber explicações detalhadas e até mesmo obter assistência
na resolução de problemas específicos de seus projetos de dados.
Este capítulo detalhará como essas interações são possíveis, demonstrando casos de uso
que ilustram como o ChatGPT pode servir como um assistente virtual dentro do Orange Canvas.
Também serão abordadas as configurações técnicas necessárias para essa integração, garantindo
que mesmo os novatos em tecnologia possam se beneficiar dessa fusão entre IA conversacional e
visualização de dados.
Ao final, espera-se que o leitor tenha não apenas uma compreensão clara de como utilizar o
ChatGPT no Orange Canvas, mas também inspiração para aplicar essas ferramentas em ambientes
educacionais ou profissionais, democratizando ainda mais o acesso à inteligência artificial.
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 147

Inteligência Artificial Visual

7.1 Obtendo aAPI Keyda OpenAI
Para integrar o ChatGPT ao Orange Canvas, é essencial obter umaAPI Keyda OpenAI. AAPI Key
funciona como uma senha que permite ao Orange Canvas acessar os serviços de IA fornecidos pela
OpenAI. Seguir os passos abaixo garantirá que você tenha aAPI Keynecessária para começar.
7.1.1 Passo a Passo para Obter aAPI Key
Crie uma Conta na OpenAI: Acesse o site da OpenAI (https://www.openai.com) e clique em
Sign Uppara criar uma nova conta. Preencha os campos necessários, como seu e-mail e
senha, e confirme seu e-mail através do link enviado pela OpenAI.
Acesse o Painel de Controle: Após a criação da conta, faça ologine acesse oDashboard
(Painel de Controle). Este painel é onde você gerencia suas chaves de API e configurações de
conta.
Navegue até asAPI Keys: No painel de controle, encontre a seção deAPI Keys. Geralmente,
ela está localizada no menu lateral ou em uma aba específica dedicada a desenvolvedores.
Gere uma NovaAPI Key: Clique emCreate New API Key(Criar Nova Chave de API). Dê
um nome à sua chave para fácil identificação, especialmente se você planeja usar múltiplas
chaves para diferentes projetos.
Copie e Armazene a Chave com Segurança: Após gerar aAPI Key, copie-a e armazene-a
em um local seguro. Esta chave será usada no Orange Canvas para habilitar a integração
com o ChatGPT. Lembre-se de que aAPI Keyé sensível e deve ser tratada com a mesma
segurança que uma senha.
7.1.2 Custos Associados ao Uso dos Modelos da OpenAI
É importante notar que o uso dos modelos da OpenAI, incluindo o ChatGPT, envolve custos. A
OpenAI adota uma estrutura de preços baseada no consumo, onde você paga pela quantidade de
texto gerado ou processado. A seguir estão alguns pontos chave sobre os custos:
Modelos Diferentes, Preços Diferentes: A OpenAI oferece vários modelos de linguagem
com capacidades e custos variados. Modelos mais avançados, como o GPT-4, tendem a ser
mais caros que seus predecessores.
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 148

Inteligência Artificial Visual

Cobrança por Tokens: A OpenAI cobra com base no número de tokens processados. Tokens
podem ser palavras inteiras ou partes de palavras, dependendo da complexidade do texto.
Plano de Assinatura: Para usuários frequentes, a OpenAI pode oferecer planos de assinatura
que podem reduzir os custos em comparação com a cobrança por uso avulso.
Monitoramento de Uso: Utilize as ferramentas de monitoramento no painel de controle da
OpenAI para acompanhar seu uso e evitar surpresas na fatura. Isso ajuda a gerenciar e
otimizar os custos conforme necessário.
Figura 7.1: Alerta sobre a manipulação daAPI Keyda OpenAI e os custos associados.
Ao compreender como obter aAPI Keye estar ciente dos custos envolvidos, você estará prepa-
rado para integrar de maneira eficiente o ChatGPT ao Orange Canvas, abrindo novas possibilidades
para a aplicação de inteligência artificial em seus projetos.
7.2 Filtragem de Artigos médicos com o ChatGPT e Orange
O processo de leitura e exclusão de artigos, ao realizar uma revisão bibliográfica, é crucial para
garantir a relevância e a qualidade dos artigos que serão considerados em sua pesquisa. Esse
procedimento começa pela leitura atenta do título e do abstract de cada artigo. O título fornece uma
visão geral do conteúdo do artigo, enquanto o abstract oferece um resumo mais detalhado, incluindo
o objetivo do estudo, a metodologia empregada, os resultados principais e as conclusões.
Ao avaliar tanto o título quanto o abstract, o pesquisador deve verificar se o artigo está alinhado
com os temas centrais da pesquisa. Artigos que não se relacionam diretamente com o tema devem
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 149

Inteligência Artificial Visual

ser descartados para manter o foco e a qualidade da revisão. Este processo também ajuda a
identificar pesquisas de ponta e as lacunas existentes no campo de estudo, o que é essencial para
formular questões de pesquisa mais precisas e direcionadas.
Ao ler o título e o abstract, faça as seguintes perguntas: O tema do artigo está diretamente
relacionado ao meu campo de pesquisa? As metodologias ou tecnologias discutidas são relevantes
para o meu trabalho? Os resultados contribuem de forma significativa para o conhecimento existente
ou para a prática na minha área? Se a resposta para qualquer dessas perguntas for negativa, é
aconselhável considerar a exclusão do artigo da sua lista.
Esse método criterioso garante que apenas os artigos mais pertinentes sejam incluídos na
revisão, o que eleva a qualidade acadêmica e a aplicabilidade prática dos resultados da pesquisa.
Este processo de leitura e exclusão de artigos pode ser significativamente automatizado e facilitado
utilizando o ChatGPT através do Orange Canvas. Ao integrar o ChatGPT, você pode programar o
sistema para analisar automaticamente títulos e abstracts, identificando a relevância de cada artigo
com base em critérios predefinidos. Isso permite uma triagem rápida e eficiente, economizando
tempo e esforço significativos que seriam normalmente dedicados à leitura manual.
Selecionando artigos com o Pubmed
O PubMed é uma base de dados de livre acesso, mantida pela Biblioteca Nacional de Medicina
dos Estados Unidos, que compila referências e resumos de artigos científicos na área da saúde.
Abrangendo uma vasta gama de tópicos relacionados à biomedicina e ciências da saúde, o PubMed
oferece aos pesquisadores, estudantes e profissionais de saúde acesso a milhões de resumos de
artigos e, em muitos casos, ao texto completo. Sua importância reside na capacidade de fornecer
informações atualizadas e revisadas por pares, fundamentais para a evolução da prática médica e
pesquisa científica.
Para iniciar a exploração de artigos científicos no Orange, utilizaremos o widget Pubmed. Clique
no ícone do Pubmed localizado no Orange Canvas para abrir a interface de busca. Nosso foco será
analisar publicações que intersectam a área dedeep learningcom imagens médicas. No campo
"Query", insira termos específicos como "deep learning"e "medical images". Essa ação refinada
permite direcionar a pesquisa para artigos altamente relevantes para estas temáticas, facilitando
uma análise mais precisa e eficiente dos dados disponíveis.
Uma vez aberto, você verá uma interface com várias opções de configuração para a sua busca.
Concentre-se nas partes destacadas em verde na Figura 7.2. Na caixa "Number of retrievable
records for this search query", você pode visualizar a quantidade de registros disponíveis com base
em sua consulta.
Após definir sua busca, vá para a próxima caixa verde, onde você ajusta o número de registros
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 150

Inteligência Artificial Visual

que deseja recuperar. Isso permite que você limite a quantidade de artigos a serem analisados,
o que pode ser útil para focar em dados mais gerenciáveis. Por exemplo, você pode ajustar para
recuperar apenas 15 registros. Depois de ajustar essas configurações, clique em "Find records"para
executar a busca. O Orange processará sua solicitação e trará os registros conforme especificado.
Este widget é uma ferramenta eficaz para obter rapidamente dados relevantes de publicações
científicas, permitindo-lhe explorar e analisar as tendências e descobertas mais recentes em sua
área de interesse. Utilize essa funcionalidade para enriquecer sua pesquisa ou projeto com dados
atualizados e específicos.
Figura 7.2: Interface do widget Pubmed no Orange, destacando a configuração de busca e recupera-
ção de registros.
Como só podemos mandar um texto para o ChatGPT, vamos juntar o título e o abstract do
artigo em uma só coluna chamada "paper". Para fazer isso no Orange, após ter extraído os dados
desejados com o widget Pubmed, conecte-o ao widget Formula. No widget Formula, defina uma
nova variável chamada "paper". Para combinar o título e o abstract, escreva na caixa de expressão:
‘title+abstract‘. Isso concatenará ambos os campos em uma única coluna "paper", facilitando o
processamento e análise subsequente dos dados. A criação dessa nova variável é essencial para
simplificar as operações de análise de texto que você pode querer executar posteriormente. Utilize
essa técnica para preparar seus dados de maneira eficaz e garantir que todas as informações
relevantes estejam facilmente acessíveis em uma única estrutura.
Agora vamos selecionar somente aurldo artigo e a colunapaper, que contém o título e o resumo
combinados. Para isso, utilize o widgetSelect Columnsno Orange. Após processar os dados no
widgetFormula, onde a colunapaperfoi criada, arraste a conexão para o widgetSelect Columns.
Clique nele e na interface que aparece, observe as duas seções:FeatureseMetas. Mova todas
as colunas excetopapereurlpara a lista de ignorados. Essa ação é feita selecionando a coluna
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 151

Inteligência Artificial Visual

Figura 7.3: Configuração no widget Formula do Orange para combinar título e abstract em uma
coluna única.
na lista e clicando na seta que aponta para a esquerda. Certifique-se de que apenaspapereurl
estão listados sobMetas, conforme destacado em verde na Figura 7.4. Isso simplifica o conjunto de
dados para que apenas as informações essenciais sejam analisadas nas etapas subsequentes do
processamento.
Figura 7.4: Selecionando as colunaspapereurlpara análise no widget Select Columns do Orange.
Vamos criar um corpus para facilitar a análise textual dos artigos. Após a seleção das colunas
relevantes com o widgetSelect Columns, encaminhe os dados para o widgetCorpus. Neste widget,
você deve especificar quais colunas devem ser utilizadas como características de texto. No caso,
vamos focar na colunapaper, que contém os títulos e resumos combinados dos artigos. Certifique-se
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 152

Inteligência Artificial Visual

de marcarpapercomo a característica de texto usada, como mostrado na parte destacada em
verde na Figura 7.5. A colunaurlpode ser mantida como metadado para referência futura. Esse
passo é essencial para preparar os dados de maneira que possam ser processados e analisados
eficazmente, facilitando a aplicação de técnicas de processamento de linguagem natural nos passos
subsequentes.
Figura 7.5: Configuração do widget Corpus no Orange, preparando os dados para análise textual.
Para usar o ChatGPT no Orange Canvas, vamos instalar o add-onPrototypes. Primeiro, abra o
Orange e clique no ícone ’Options’ no canto superior direito da tela inicial, depois selecione ’Add-ons’
para abrir o gerenciador de add-ons. Na barra de pesquisa, digite ’Prototypes’ para encontrar
rapidamente o add-on necessário. Certifique-se de marcar a caixa ao lado dePrototypes, conforme
destacado na Figura 7.6. Clique em ’OK’ para iniciar a instalação. Após a instalação, você terá
acesso aos widgets do ChatGPT, comoChatGPT SummarizeeChatGPT Constructor, que estão
localizados na seção de ’Prototypes’ no menu de widgets do Orange. Esses widgets permitem
integrar funcionalidades do ChatGPT diretamente no seu fluxo de trabalho de análise de dados no
Orange, oferecendo capacidades avançadas de processamento de linguagem natural.
Para conectar o ChatGPT no Orange você deve inserir sua API_KEY no campo específico da
interface do ChatGPT Constructor, como mostrado na Figura 7.7. Este campo é destacado em verde
na imagem e é essencial para autenticar sua sessão, garantindo a segurança e a privacidade das
informações. Para isso, copie e cole sua chave de API no espaço reservado. Em seguida, clique no
botão "Apply"para que as configurações tenham efeito. Este processo permite que o fluxo de trabalho
do Orange se conecte ao ChatGPT, viabilizando a manipulação de dados textuais diretamente dentro
do ambiente do Orange. Atenção, evite selecionar a opção de conexão automática marcada em
vermelho, pois isso pode gerar custos indesejáveis ao realizar consultas automáticas sem sua
intervenção direta.
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 153

Inteligência Artificial Visual

Figura 7.6: Instalação do add-on Prototypes no Orange para acesso aos widgets do ChatGPT.
Na configuração do ChatGPT Constructor, é possível selecionar diferentes modelos de linguagem
para serem utilizados nas tarefas especificadas no prompt. Na Figura 7.7, dois modelos estão
disponíveis: GPT-3.5-turbo e GPT-4, como indicado na interface do usuário. A escolha do modelo
afeta diretamente a performance e o custo das operações realizadas.
O modelo GPT-3.5-turbo, representado por dois símbolos de cifrão ($$), oferece um equilíbrio
entre custo e capacidade de processamento, sendo uma opção viável para muitas aplicações que
requerem inteligência artificial. Já o GPT-4, indicado por três símbolos de cifrão ($$$), representa uma
opção de custo mais elevado. Este modelo é mais avançado, possuindo capacidades aprimoradas
de compreensão e geração de texto, o que justifica seu preço mais alto.
A escolha entre esses modelos deve considerar tanto o orçamento disponível quanto as ne-
cessidades específicas do projeto. O GPT-4, apesar de mais caro, pode ser a escolha adequada
para tarefas que exigem um nível mais alto de sofisticação e precisão no tratamento de linguagem
natural. Portanto, avalie cuidadosamente as características de cada modelo e o impacto que terão
no resultado final do seu trabalho com o Orange Canvas.
O prompt do ChatGPT Constructor, mostrado na Figura 7.7, desempenha um papel crucial
no processo de filtragem e especificação de consultas. No campo "Prompt", você deve definir
claramente a tarefa que o ChatGPT deve realizar. Por exemplo, na imagem, o prompt está configurado
para verificar se um texto enviado trata sobre um tema específico, neste caso, "SEGMENTAÇÃO
DE TUMOR". Esta instrução específica ao modelo para responder com "true"se o texto estiver
relacionado ao tema e "false"caso contrário.
Para configurar seu próprio prompt, clique no campo e escreva a instrução desejada. Este
campo permite a definição de tarefas específicas, guiando o ChatGPT para gerar respostas em
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 154

Inteligência Artificial Visual

Figura 7.7: Integração do ChatGPT com o Orange Canvas, mostrando a inserção da API_KEY e o
cuidado para não habilitar a conexão automática.
conformidade com as necessidades do seu projeto. A flexibilidade do prompt permite que você
adapte o modelo para uma variedade de aplicações, desde a filtragem de conteúdo até análises
complexas de texto.
A utilização eficiente do prompt requer uma formulação clara e precisa das perguntas ou tarefas,
garantindo que o modelo compreenda e execute exatamente o que é esperado. Portanto, dedique um
momento para pensar na melhor maneira de estruturar seu prompt antes de aplicar as configurações.
Agora vamos ver o processamento do ChatGTP filtrando os artigos que foram classificados como
"true"depois que o ChatGPT leu os títulos e abstracts dos artigos, identificando aqueles relevantes
para a pesquisa de segmentação de tumor. Como pode ser visto na Figura 7.8, a tabela de dados
mostra uma lista de URLs correspondentes a artigos científicos, cada um marcado como "true"ou
"false"sob a coluna ’Text’, indicando sua relevância para o tema.
Observe que apenas três artigos foram classificados como "true". Este resultado implica que, após
a análise do texto pelo ChatGPT Constructor, esses artigos foram identificados como tendo relevância
direta com a pesquisa de segmentação de tumor. Para visualizar esses artigos especificamente,
você deve clicar sobre cada linha marcada como "true". Isso pode ser feito de maneira mais
eficiente selecionando a opção ’Select full rows’ para destacar toda a linha de cada entrada relevante,
facilitando a visualização e a seleção dos artigos corretos.
Para continuar com a análise ou manipulação desses dados, você pode exportar a lista filtrada ou
utilizá-la como entrada para outros módulos dentro do Orange, prosseguindo com etapas adicionais
de análise ou revisão de literatura. A filtragem precisa, como demonstrado, é essencial para garantir
que os esforços subsequentes de análise se concentrem apenas nos dados mais pertinentes ao seu
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 155

Inteligência Artificial Visual

estudo.
Figura 7.8: Visualização no Orange Canvas da filtragem de artigos relevantes para a pesquisa de
segmentação de tumor utilizando o ChatGPT Constructor.
7.2 EXERCÍCIOS DO CAPÍTULO: CHATGPT NO ORANGE CANVAS
1.Explique como o ChatGPT pode ser integrado ao Orange Canvas e descreva as vantagens
dessa integração para usuários sem habilidades avançadas de programação.
2.Quais são os passos necessários para obter umaAPI Keyda OpenAI? Por que é importante
manter essa chave segura?
3.Discuta os custos associados ao uso dos modelos de linguagem da OpenAI, como o GPT-4, e
explique o conceito de cobrança por tokens.
4.Como o ChatGPT pode auxiliar na filtragem de artigos médicos durante uma revisão bibli-
ográfica? Descreva o processo que o ChatGPT utiliza para determinar a relevância de um
artigo.
5.Quais cuidados devem ser tomados ao configurar o número de registros a serem recuperados
do PubMed através do widget correspondente no Orange Canvas?
6.Descreva o processo de seleção de colunas no Orange Canvas para preparar dados para
análise textual. Por que é importante selecionar apenas as colunas relevantes?
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 156

Inteligência Artificial Visual

7.Explique o papel do widgetCorpusno Orange Canvas e como ele é utilizado para facilitar a
análise textual dos artigos.
8.Discuta a importância de configurar corretamente o prompt no ChatGPT Constructor e dê
exemplos de como um prompt pode ser estruturado para realizar tarefas específicas.
9.Com base nas configurações observadas, como você pode evitar custos indesejáveis ao usar
o ChatGPT no Orange Canvas?
Considerando a Figura 7.8 e o processo de filtragem de artigos, como a seleção de ’Select full
rows’ ajuda a melhorar a eficiência na visualização e seleção de artigos relevantes?
CAPÍTULO 7. CHATGPT NO ORANGE CANVAS 157

Inteligência Artificial Visual

CAPÍTULO 8
8 Séries temporais
A análise de séries temporais é um componente essencial da ciência de dados e da análise estatística,
aplicável em uma variedade de campos, desde a previsão de demanda econômica até a gestão de
estoques, das ciências climáticas à engenharia financeira. A capacidade de prever o futuro com
base em dados passados não é apenas um elemento de vantagem competitiva nos negócios, mas
também uma ferramenta vital para a tomada de decisões em diversas aplicações práticas.
Na disciplina de estatística, no campo da econometria, nas aplicações práticas da matemática e
no processamento de sinais, o conceito de séries temporais se destaca quando nos deparamos com
dados coletados sequencialmente ao longo do tempo. Em séries temporais, a ordem é tudo; ela não
é apenas uma lista, mas sim a espinha dorsal da análise temporal. O aspecto mais intrigante das
séries temporais é a dependência que cada ponto de dado tem em relação ao seu antecessor ,
e a meta é desenvolver modelos analíticos que capturam e utilizam essa relação sequencial para
prever comportamentos futuros e discernir padrões ocultos.
Portanto, a primeira coisa que você precisa saber é como diferenciar um conjunto de dados
que constitui uma série temporal daqueles que não se encaixam nessa categoria. Compreender a
natureza de uma série temporal é essencial para a análise de dados eficaz. Uma série temporal
é distinta por sua ordem cronológica e pela premissa fundamental de que cada ponto de dados
pode influenciar o subsequente. Eu sei que esto repetindo essa afirmação, mas ela é fundamental
para aqueles que buscam entender como treinar modelos de IA para séries temporais. Para reforçar
ainda mais veja a Tabela 8.1 sobre exemplos de problemas são e não são séries temporais.
Esta sequência interconectada não apenas reflete a progressão do tempo, mas também a
influência que cada evento anterior exerce sobre o próximo, criando um encadeamento de causas e
efeitos que é crucial para a previsão e análise temporal.
CAPÍTULO 8. SÉRIES TEMPORAIS 158

Inteligência Artificial Visual

São séries temporais Não são séries temporais
Variação do índice de preços ao consumidor mensal. Índice de preços ao consumidor em diferentes cida-
des em um único mês.
Quantidade de chuva mensal em uma região ao
longo de vários anos.
Média de precipitação anual em várias regiões.
Número de passageiros transportados mensalmente
por uma companhia aérea.
Número total de passageiros transportados por dife-
rentes companhias aéreas em um ano.
Tabela 8.1: Exemplo de Tabela com Estilo Aplicado
Considerando o exemplo do registro diário de temperaturas de um local específico ao longo de
um ano, temos uma série temporal clássica. Aqui, a temperatura de um dia não é apenas um número
isolado; ela pode ser o resultado de uma tendência anterior e pode afetar as temperaturas futuras,
ilustrando as variações sazonais. Em oposição, as temperaturas de diferentes locais registradas
em um único dia não são uma série temporal, pois esses dados não têm uma relação sequencial
direta onde um valor influencia o outro. Portanto, reconhecer essa distinção é vital, pois afeta
profundamente a abordagem analítica escolhida e a precisão das previsões ou decisões baseadas
nesses dados.
Quase sempre, a análise de séries temporais pode ser intimidadora, especialmente devido à
sua natureza complexa e à necessidade de um entendimento estatístico sofisticado. Neste capítulo,
exploraremos o poderoso módulo de séries temporais do Orange, demonstrando como ele pode ser
usado para transformar dados brutos em insights preditivos valiosos. Examinaremos os widgets
específicos fornecidos pelo Orange para a análise de séries temporais, e eu guiarei você desde a
preparação dos dados até a modelagem e avaliação de previsões.
CAPÍTULO 8. SÉRIES TEMPORAIS 159

Inteligência Artificial Visual

8.1 Instalando o Add-on de Séries Temporais
Para instalar o add-on de Séries Temporais, siga os passos abaixo:
Figura 8.1: Como instalar o add-on de Séries Temporais
1.Inicie o Orange Canvas: Abra o Orange Canvas no seu computador. Você será recebido com
uma tela de boas-vindas que apresenta opções para carregar um arquivo, abrir um espaço de
trabalho existente ou iniciar um novo.
2.Acesso ao Gerenciador de Add-ons: No menu principal na parte superior, clique em Options e,
no menu suspenso que aparece, selecione Add-ons. Isso abrirá uma janela que lista todos os
add-ons disponíveis para o Orange.
3.Selecionando o Add-on de Séries Temporais: Na janela de Add-ons, você encontrará uma lista
de add-ons disponíveis para instalação. Procure por Time Series na lista ou use a função de
busca para encontrar mais rapidamente.
4.Instalação: Marque a caixa ao lado de Time Series e clique no botão Install. O Orange cuidará
do resto, baixando e instalando o add-on para você.
5.Reinicialização: Depois de instalar o add-on de Séries Temporais, o Orange pode solicitar que
você reinicie o aplicativo para que o add-on seja ativado com sucesso.
Com o add-on instalado, você está agora equipado para lidar com dados sequenciais e executar
análises de séries temporais complexas de maneira simplificada. Estes widgets são ferramentas
CAPÍTULO 8. SÉRIES TEMPORAIS 160

Inteligência Artificial Visual

poderosas que podem ser combinadas para formar um pipeline de análise de dados robusto e
intuitivo.
8.2 Explorando o Painel de Widgets de Séries Temporais
Após a instalação do add-on de séries temporais, uma nova gama de widgets especializados é
adicionada ao seu ambiente Orange Canvas, expandindo significativamente suas capacidades
analíticas. Aqui está um resumo dos widgets disponíveis neste painel:
Figura 8.2: Como instalar o add-on de Séries Temporais
Yahoo Finance: Permite importar dados financeiros diretamente do Yahoo Finance. Este
widget é útil para análises econômicas e de mercado.
Form Timeseries: Converte dados tabulares em uma série temporal, identificando colunas
com informações de tempo e dados sequenciais.
Interpolate: Preenche os dados faltantes em uma série temporal. É particularmente útil para
lidar com dados incompletos ou lacunas em séries temporais.
Moving Transform: Aplica uma transformação móvel aos dados, como uma média móvel, que
pode ajudar a suavizar as séries e destacar tendências.
Line Chart: Fornece uma visualização direta de séries temporais, permitindo uma rápida
identificação de padrões, tendências e anomalias.
CAPÍTULO 8. SÉRIES TEMPORAIS 161

Inteligência Artificial Visual

Periodogram: Exibe o espectro de frequências de uma série temporal, útil para identificar
sazonalidades e ciclos.
Correlogram: Mostra a autocorrelação dos dados em diferentes lags, o que pode ajudar a
identificar relações temporais e a escolher parâmetros para modelos ARIMA.
Spiralogram: Visualiza dados sazonais em um formato espiral, oferecendo uma perspectiva
única sobre padrões cíclicos.
Granger Causality: Testa se uma série temporal é capaz de prever outra, útil para identificar
relações causais entre séries.
ARIMA Model: Permite ajustar um modelo ARIMA a uma série temporal, essencial para fazer
previsões futuras.
VAR Model: Fornece modelagem para sistemas representados por múltiplas séries temporais
inter-relacionadas.
Model Evaluation: Oferece ferramentas para avaliar a qualidade das previsões de um modelo,
usando métricas como RMSE e MAE.
Time Slice: Seleciona subconjuntos de dados com base em intervalos de tempo, facilitando a
análise de períodos específicos dentro de uma série.
Difference: Diferencia uma série temporal para ajudar a torná-la estacionária, um passo comum
na preparação para modelagem ARIMA.
Seasonal Adjustment: Remove componentes sazonais dos dados, o que pode melhorar a
performance dos modelos de previsão.
8.3 Exemplo Prático: Previsão do Mercado de Ações
Começaremos importando dados financeiros utilizando o widgetYahoo Finance. Este widget é
incrivelmente útil para obter dados de mercado atualizados, os quais são fundamentais para nossa
análise.
O widgetYahoo Financeé uma ferramenta interativa no Orange Canvas que permite ao usuário
importar dados financeiros para análise de séries temporais. Abaixo estão os componentes chave
da caixa de interação deste widget:
CAPÍTULO 8. SÉRIES TEMPORAIS 162

Inteligência Artificial Visual

Figura 8.3: Widget Yahoo Finance
Ticker: Campo para inserir o símbolo da ação, chamado de ticker. No exemplo, "GOOG"representa
a Alphabet Inc., que é a empresa controladora do Google.
From e To: Define o período para o qual os dados serão recuperados. No exemplo fornecido,
os dados são solicitados desde o dia 16 de fevereiro de 2019 até o dia 15 de fevereiro de 2024.
Download: Um botão que, quando pressionado, inicia o processo de download dos dados do
intervalo especificado.
Esta interface simplifica a etapa de aquisição de dados, permitindo que os analistas se concentrem
na análise e modelagem de séries temporais sem se preocuparem com o processo de coleta de
dados.
Figura 8.4: WidgetYahoo Financepara importação de dados de mercado no Orange Canvas
Após realizar o download dos dados do mercado de ações do Google (GOOG) usando o
widgetYahoo Finance, os dados são imediatamente disponibilizados no widgetData Tabledo
Orange Canvas. Este widget oferece uma visualização tabular dos dados, permitindo uma inspeção
detalhada das informações obtidas. A tabela exibe múltiplas colunas, como ’Adj Close’, ’Date’,
’Open’, ’High’, ’Low’, ’Close’ e ’Volume’, fornecendo uma análise diária do desempenho das ações.
Com 1257 instâncias e 6 recursos, o widget permite uma análise compreensiva das tendências
do mercado ao longo do tempo, essencial para a construção de modelos preditivos e tomada de
decisões baseadas em dados.
Após a coleta de dados históricos de mercado através do widgetYahoo Finance, procedemos
à etapa de análise visual. O Orange Canvas permite uma interação fluida e intuitiva entre widgets,
CAPÍTULO 8. SÉRIES TEMPORAIS 163

Inteligência Artificial Visual

Figura 8.5: Widget Yahoo
como demonstrado na figura a seguir, onde os dados são passados doYahoo Financepara oData
Tablee, posteriormente, para oLine Chart.
OLine Charté um dos widgets mais eficientes no Orange Canvas para a visualização de dados
de séries temporais. Ele fornece uma representação gráfica que ajuda os usuários a identificar
padrões, tendências e anomalias nos dados ao longo do tempo.
Figura 8.6: Conexão dos dados doYahoo Financediretamente para oLine Chart
A caixa de diálogoEdit Linksé crucial para definir como os dados são transferidos entre diferentes
etapas do processo analítico. Neste exemplo, vamos optar por transmitir a série temporal completa
doYahoo Financepara oLine Chart, que é um passo essencial para a visualização de tendências e
padrões ao longo do tempo.
Na Figura 8.7, vemos um exemplo típico de um gráfico de linhas, mostrando a série temporal
do preço ajustado de fechamento (Adj Close) de um ativo financeiro. A seguir, são destacados os
componentes e funcionalidades do widgetLine Chart:
Tipo de gráfico : Permite ao usuário selecionar o tipo de gráfico desejado, com ’linha’ sendo a
opção padrão para séries temporais.
CAPÍTULO 8. SÉRIES TEMPORAIS 164

Inteligência Artificial Visual

Figura 8.7: Exemplo de utilização doYahoo FinanceeLine Chartno Orange Canvas para análise de
séries temporais do mercado de ações.
Eixo Logarítmico : Oferece a opção de transformar o eixo y para a escala logarítmica, útil
para dados com grandes variações de amplitude.
Filtro : Facilita a seleção de quais dados devem ser visualizados no gráfico. Neste exemplo, o
’Adj Close’ está selecionado, indicando que apenas os dados de preço ajustado de fechamento
são exibidos.
Visualização do gráfico : Exibe a série temporal selecionada, permitindo uma análise visual
imediata. As flutuações no gráfico de linha indicam as mudanças no valor ’Adj Close’ ao longo
do período observado.
Informações de Dados : O canto inferior direito mostra o total de pontos de dados (1257) e
variáveis (colunas) presentes na série temporal carregada.
8.3 TRANSFORMAÇÕES MÓVEIS
RO widgetMoving Transformno Orange Canvas é uma ferramenta essencial na análise de séries
temporais. Ele permite aplicar transformações móveis aos dados, como médias móveis e suavização
exponencial, que são técnicas cruciais para a preparação e análise de dados temporais. A Figura
8.8 ilustra o ambiente de configuração do widget, destacando as diversas opções disponíveis para o
usuário.
Em séries temporais, as transformações móveis são aplicadas por várias razões:
CAPÍTULO 8. SÉRIES TEMPORAIS 165

Inteligência Artificial Visual

Suavização : As transformações ajudam a suavizar flutuações de curto prazo e destacar
tendências de longo prazo, facilitando a identificação de padrões.
Redução de Ruído : Ao calcular a média de pontos de dados dentro de uma janela deslizante,
a técnica minimiza o impacto de variações aleatórias ou atípicas, conhecidas como ruído.
Preparação para Modelagem : Modelos preditivos, como ARIMA, muitas vezes requerem que
a série seja estacionária. As transformações móveis podem ajudar a estabilizar a média da
série ao longo do tempo, um passo importante para alcançar a estacionariedade.
Destaque de Sazonalidade : Algumas transformações, como a média móvel centrada, são
úteis para evidenciar padrões sazonais em dados com flutuações periódicas.
O painel doMoving Transformoferece diferentes tipos de agregação, como janelas deslizantes
ou blocos consecutivos, cada um com suas próprias configurações, como a largura da janela e a
inclusão de instâncias líderes. Estas opções permitem personalizar a transformação de acordo com
as características específicas dos dados e os objetivos da análise.
Em resumo, o uso de transformações móveis é um passo fundamental na análise de séries
temporais. Ele melhora a qualidade dos dados para análise subsequente, permitindo que modelos e
técnicas mais avançados sejam aplicados com maior eficácia.
As transformações móveis, diferem significativamente das técnicas de regressão e classificação
em diversos aspectos. Enquanto as transformações móveis são usadas para preparar séries tempo-
rais, que são dados intrinsecamente ordenados no tempo, as técnicas de regressão e classificação
lidam com conjuntos de dados onde todas as características (features) e alvos (targets) estão
prontamente disponíveis e são geralmente considerados independentes do tempo.
Em regressão e classificação, cada instância de dados é tratada como um ponto independente
no espaço de características. A regressão foca em prever uma variável contínua, enquanto a
classificação visa prever a categoria ou classe de uma instância. Estas técnicas assumem que
não há dependência sequencial entre as instâncias de dados; cada observação é uma amostra
independente do espaço que a função de regressão ou o classificador está tentando modelar.
Por outro lado, as séries temporais e as transformações aplicadas a elas, como a média móvel,
consideram a dependência entre observações consecutivas. Estas técnicas são essenciais para
identificar tendências, ciclos e outras dinâmicas ao longo do tempo. As transformações móveis
ajudam a suavizar flutuações de curto prazo e a destacar comportamentos de longo prazo, o que é
crucial para modelagem preditiva em dados temporais.
Portanto, enquanto a regressão e a classificação buscam capturar relações entre características
e alvos em um conjunto de dados, as transformações móveis em séries temporais buscam entender
CAPÍTULO 8. SÉRIES TEMPORAIS 166

Inteligência Artificial Visual

e modelar a evolução dos dados ao longo do tempo, o que é uma distinção fundamental entre estas
abordagens analíticas.
O widgetMoving Transformda Figura 8.8 no Orange Canvas é uma ferramenta robusta para
a computação de agregações em séries temporais, seja através de uma janela deslizante, blocos
consecutivos ou períodos de tempo definidos. Essa funcionalidade é crucial em séries temporais
devido à natureza ordenada dos dados e à sua dependência sequencial.
Figura 8.8: Configuração do widgetMoving Transformno Orange Canvas para análise de séries
temporais.
O widget permite definir o método de formação de blocos de dados, cada um atendendo a
necessidades diferentes de análise:
Janela Deslizante : Utiliza uma janela de tamanho especificado que desliza ao longo da série
para suavizar os dados, frequentemente usada para reduzir a variabilidade de curto prazo e
destacar tendências de longo prazo.
Blocos Consecutivos : Agrega dados dentro de blocos consecutivos, sendo útil para resu-
mir os dados em intervalos regulares e possivelmente reduzir a dimensionalidade da série
temporal.
Períodos de Tempo Agregados : Agrega dados com base em períodos de tempo como
anos, meses ou dias, substituindo a necessidade de widgets de agregação separados e
proporcionando uma visão macroscópica da série.
A seleção de variáveis é intuitiva, com um filtro que permite a rápida localização de variáveis pelo
nome e a aplicação de diferentes agregações, como média, soma, produto, desvio padrão, entre
CAPÍTULO 8. SÉRIES TEMPORAIS 167

Inteligência Artificial Visual

outras. Um exemplo prático do uso doMoving Transformé a aplicação de uma função de suavização
sobre uma série temporal financeira, como os valores diários das ações do Google. Ao utilizar uma
janela deslizante com agregação de média para uma média móvel de 5 dias, podemos suavizar
as variações diárias e identificar tendências mais claras, como pode ser observado no widgetLine
Chart. Diferentemente das técnicas de regressão e classificação, onde todas as características e
alvos estão prontos no conjunto de dados, a transformação móvel em séries temporais prepara os
dados sequenciais para análise e modelagem. Quando aplicamos as operações destacadas em
laranja, estamos realizando o seguinte:
Média (Mean value) : Calcula a média dos dados dentro da janela deslizante ou do bloco.
Isso ajuda a suavizar a série ao nivelar picos e vales breves, o que pode revelar tendências
subjacentes mais claramente.
Soma (Sum) : A soma dos valores dentro da janela pode ser útil para entender o volume ou a
magnitude acumulada de um fenômeno ao longo de um período.
Mínimo e Máximo (Minimum e Maximum) : Essas medidas fornecem uma visão dos extremos
dentro de cada janela, o que pode ser útil para identificar outliers ou para entender a variação
total dos dados.
Desvio Padrão (Standard deviation) e Variância (Variance) : Estes indicam a dispersão dos
dados em torno da média. Um valor alto pode sugerir uma maior volatilidade ou variação nos
dados ao longo do tempo.
Mediana (Median) : Diferente da média, a mediana é menos sensível a outliers e pode fornecer
uma medida mais robusta do centro da distribuição dos dados.
Produto Cumulativo (Cumulative product) : O produto dos valores, que pode ser útil para
dados que são cumulativos por natureza ou quando estamos interessados no efeito composto
ao longo do tempo.
Essas medidas, quando aplicadas em séries temporais, ajudam a transformar os dados brutos
em informações que refletem melhor os padrões e tendências subjacentes. Por exemplo, uma média
móvel pode ajudar a suavizar uma série de preços de ações, permitindo que os analistas vejam além
das flutuações diárias e se concentrem na tendência geral. A importância dessas transformações
decorre do fato de que as séries temporais muitas vezes contêm ruídos ou flutuações que podem
obscurecer os insights significativos que buscamos extrair para previsões e análises.
Clique no campo "Adj Close"para selecionar e escolha quais operações podem ser aplicadas na
serie temporal. Você poderia, por exemplo, aplicar Média Móvel (Mean value), Soma Cumulativa
(Cumulative sum), Desvio Padrão (Standard deviation) e Diferenciação (Difference). Essas operações
CAPÍTULO 8. SÉRIES TEMPORAIS 168

Inteligência Artificial Visual

são escolhidas com base na natureza dos dados e nos objetivos da análise. Por exemplo, em dados
financeiros, onde a volatilidade é uma informação valiosa, o desvio padrão é frequentemente
calculado. Em contrastes, para séries de vendas ou de tráfego em websites, onde o interesse está no
crescimento ou declínio ao longo do tempo, a média móvel e a soma cumulativa são mais aplicadas.
Por isso a experimentação usando essas métricas é muito importante no impacto na eficiência
do modelo.
8.4 Sliding Window
O conceito de "sliding window"(janela deslizante) em séries temporais é uma técnica usada para pro-
cessar e analisar dados sequenciais ao dividir a série em subconjuntos (janelas) que se sobrepõem
ou não. Cada janela contém um número fixo de observações e "desliza"ao longo da série temporal,
avançando uma observação (ou mais) de cada vez. No Orange Canvas a técnica é aplicada onde
mostra o destaque Laranja na Figura 8.9
Figura 8.9: Aplicação de Sliding Window no Orange Canvas
O objetivo é usar um conjunto de observações consecutivas para prever o valor subsequente
ou os valores futuros na série. A janela deslizante permite transformar uma série temporal em um
problema de aprendizado supervisionado, onde os valores dentro de cada janela são tratados como
entradas (features) e o valor que se deseja prever, geralmente logo após a janela, é tratado como a
saída (target).
Por exemplo, considere uma série temporal com os valores diários de temperatura. Uma janela
deslizante de tamanho 3 transformaria a série em conjuntos de três temperaturas consecutivas
CAPÍTULO 8. SÉRIES TEMPORAIS 169

Inteligência Artificial Visual

para prever a temperatura do dia seguinte. À medida que a janela "desliza"um dia por vez, novos
conjuntos de dados são formados para treinamento ou previsão.
A técnica de janela deslizante é amplamente aplicada em diversas áreas, como análise financeira,
meteorologia, processamento de sinais e muitas outras aplicações de séries temporais.
8.5 O modelo ARIMA
O modelo ARIMA, que é um acrônimo para AutoRegressive Integrated Moving Average, é um
modelo estatístico popular usado para análise e previsão de dados de séries temporais. O ARIMA
é particularmente adequado para séries temporais que são estacionárias após diferenciações
sucessivas, que é uma técnica para tornar a série não-estacionária em estacionária removendo
tendências e sazonalidades.É uma técnica de previsão de séries temporais que combina três
componentes principais:
Autoregressivo (AR) : Este componente modela a relação entre uma observação e um número
específico de observações passadas. Se denotarmos porpa ordem do modelo autoregressivo,
isso significa que estamos usandoplags (ou seja,pobservações passadas) para prever o
valor atual na série.
Integrado (I) : Representa o processo de diferenciação que ajuda a tornar a série temporal
estacionária, isto é, com propriedades estatísticas constantes ao longo do tempo. Se a série
não for estacionária, diferenciamos os dadosdvezes, ondedé o número de diferenciações
não sazonais necessárias.
Média Móvel (MA) : Este componente modela o erro da previsão como uma combinação linear
dos erros de previsão passados. O parâmetroqrepresenta a ordem do modelo de média
móvel e indica quantos termos de erro passado estamos usando para prever o valor atual.
Para ajustar um modelo ARIMA, precisamos identificar os parâmetrosp,d, eqque melhor se
ajustam à nossa série temporal. Isso geralmente é feito através de métodos como o critério de
informação de Akaike (AIC) ou o critério de informação Bayesiano (BIC), que ajudam a encontrar o
equilíbrio entre a complexidade do modelo e o ajuste aos dados. A Figura 8.10 mostra detalhe do
widget do ARIMA no Orange Canvas.
CAPÍTULO 8. SÉRIES TEMPORAIS 170

Inteligência Artificial Visual

Figura 8.10: Aplicação de Sliding Window no Orange Canvas
8.5 EXERCÍCIOS TEÓRICOS E PRÁTICOS: SÉRIES TEMPORAIS
Questões Teóricas
1.Defina o que é uma série temporal e explique por que a ordem dos dados é crucial na análise
de séries temporais.
2.Explique o conceito de estacionariedade em uma série temporal e por que é importante
alcançá-la antes de aplicar modelos como ARIMA.
3.Descreva o papel dos componentes AR (Autoregressivo), I (Integrado) e MA (Média Móvel) em
CAPÍTULO 8. SÉRIES TEMPORAIS 171

Inteligência Artificial Visual

um modelo ARIMA.
4.Discuta como a autocorrelação pode ser utilizada para entender a dependência temporal em
uma série temporal.
5.Quais são as principais diferenças entre os dados tratados em séries temporais e outros tipos
de dados analisados em ciência de dados?
Questões Práticas
6.Utilizando o widgetYahoo Financedo Orange, importe dados de um ano de ações de sua
escolha e descreva os passos realizados.
7.Aplique uma média móvel utilizando o widgetMoving Transformpara suavizar os dados de
ações obtidos no exercício anterior. Explique sua escolha do tamanho da janela e o efeito
observado.
8.Crie um modelo ARIMA no Orange para os dados de ações que você suavizou. Defina os
parâmetrosp,d, eqe justifique suas escolhas.
9.Utilizando o widgetLine Chart, visualize as tendências dos dados após aplicar a média móvel
e o modelo ARIMA. Discuta as diferenças observadas.
Configure uma janela deslizante no widgetSliding Windowpara prever a temperatura do dia
seguinte, usando dados meteorológicos. Descreva o processo e os resultados obtidos.
CAPÍTULO 8. SÉRIES TEMPORAIS 172
