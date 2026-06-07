DEEP LEARNING

Prefácio
É com grande entusiasmo que apresento o livro do Prof. Sandeco Macedo, que adentra o
empolgante campo do Deep Learning aplicado a criação de agentes de visão computacional.
Enquanto avançamos no século XXI, testemunhamos uma revolução na interseção
entre tecnologia e medicina. O papel do aprendizado de máquina, especialmente do Deep
Learning, tem sido profundamente transformador, capacitando profissionais de saúde a
extrair insights valiosos e precisos de vastos conjuntos de dados de imagens.
O Prof. Sandeco, renomado cientista da computação e professor e pesquisador no
Instituto Federal de Goiás (IFG) e Universidade Federal de Goiás (UFG), emerge como um
guia exemplar neste campo dinâmico. Sua paixão pela inovação e dedicação ao avanço da
ciência o consolidam como uma referência na convergência entre tecnologia e saúde.
Eu como médico, percebo que nesse livro, o Prof. Sandeco não apenas oferece uma
visão abrangente do estado atual da aplicação do Deep Learning como por exemplo em
imagens médicas que é minha de atuação, mas também compartilha insights práticos e
exemplos elucidativos, beneficiando estudantes, pesquisadores e profissionais da área
médica e das demais áreas de conhecimento humano.
Para mim, ao abordar os desafios e as oportunidades do uso do Deep Learning em
imagens médicas, este livro se destaca como um recurso indispensável para todos os
interessados em compreender e explorar todo o potencial dessa tecnologia inovadora.
Estou confiante de que este livro se tornará uma referência essencial para aqueles
que buscam aprimorar seus conhecimentos na interseção entre tecnologia e medicina,
contribuindo assim para o avanço da ciência e da saúde em escala global.
Marco Aurélio Carvalho, MD
Intensivista Infantil pela Universidade Estadual Paulista, UNESP,
Faculdade de Medicina de Botucatu
CMIO (Chief Medical Informatics Officer) da UNIMED Piracicaba
Especialista em Tecnologia da Informação em Saúde pela
Universidade Federal de São Paulo
Data Scientist da Vitalyze - Oklahoma, U.S.A.
4

Sumário
Prefácio
1 Introdução a Deep Learning
1.1 Aprendizado Profundo? Vem que te explico!
1.2 Primeiros passos com as Redes que conseguem ver
2 IA sem programar – Sim, é verdade!
2.1 IA sem mistério: agora para qualquer um
2.2 Ensinando máquinas a "ver"imagens
2.3 Construindo nossa primeira rede neural visual
2.4 Vamos treinar nossa IA? Pegue seu capacete!
2.5 A IA no comando: fazendo previsões
2.6 Ensinar a IA a ser justa: o que é generalização?
2.7 Salvando e exportando nossa invenção
2.8 Sua IA online - Servidor gratuito e sem programar
2.9 Vamos praticar com alguns exercícios
3 Inteligência Artificial Visual
3.1 O poder milagroso dos widgets. IA no Orange Canvas
3.2 Adicionando superpoderes de visão ao Orange
3.3 Doutor e IA, eu estou bem?
3.4 Embeddings: A assinatura da IA em cartório
3.5 Mais exercícios para não perder o ritmo
4 O grande olho que tudo vê!
4.1 A revolução da convolução
4.2 Mapas da mina. Mapas de ativação
4.3 Ativando sua rede com ReLU
4.4 Pooling: o que realmente importa e deixando o resto de lado
4.5 Flatten: A IA adora comida achatada como uma pizza
4.6 Os neurônios da visão por IA
4.7 Camada de saída: Sim, entendi o que eu vi
4.8 Vamos praticar
5 Aventuras com IA nas Nuvens Gratuitas
5.1 A arena gratuita de treinamento de IA
5.2 Uma GPU grátis só pra mim? Que Maravilhoso!
5.3 Vários processos de uma vez? Sim, por favor! DEEP LEARNING
6 Deep Learning - Ao infinito e além
6.1 Um problema sério a ser resolvido que IA pode ajudar
6.2 Carregando imagens para a festa no Colab
6.3 Carregando Dados, o combustível de toda IA
6.4 Validação: Toda IA também tem seu Enem
6.5 Montando uma rede neural: vamos construir juntos
6.6 Afinando a rede: os ajustes finais
6.7 O grande show: treinando nosso IAluno
6.8 Resultados: olha como a nossa IA é boa!
6.9 Hora de exercitar: vamos nessa!
7 Otimizando em Deep Learning
7.1 Eu tenho poucos dados, e agora? Vamos resolver!
7.2 Transplante de cérebro digital
7.3 Uma IA aprendendo com outra IA
7.4 A mágica dos grandes modelos prontos de visão
7.5 Transfer learning com Keras: Meu Deus como é fácil!
7.6 Fine-tuning: aquele toque final que faz diferença
7.7 Callbacks: Os assistentes secretos
7.8 Empacotando tudo
7.9 Pratique o aprendizado: hora dos exercícios
DEEP LEARNING

CAPÍTULO 1
1 Introdução a Deep Learning
A inteligência artificial (IA) é uma das inovações tecnológicas mais transformadoras do século XXI.
Seu impacto pode ser sentido em uma ampla variedade de setores, desde a saúde até o transporte,
passando por finanças, educação e entretenimento. A IA tem o potencial de revolucionar a maneira
como vivemos e trabalhamos, automatizando tarefas repetitivas e oferecendo novas formas de
resolver problemas complexos. Graças aos avanços na IA, estamos começando a ver sistemas que
podem aprender, adaptar-se e executar tarefas de forma autônoma, tornando-se cada vez mais
parte integrante de nossas vidas diárias.
Na área da saúde, a IA está proporcionando avanços significativos no diagnóstico e tratamento
de doenças. Algoritmos de aprendizado de máquina são utilizados para analisar imagens médicas,
identificar padrões que podem escapar ao olho humano e prever o desenvolvimento de doenças com
alta precisão. Além disso, assistentes virtuais baseados em IA estão ajudando médicos a acessar
informações médicas e históricos de pacientes de maneira mais eficiente, permitindo uma tomada
de decisão mais informada e rápida.
No setor de transporte, a IA está no coração do desenvolvimento de veículos autônomos. Esses
veículos utilizam uma combinação de sensores, aprendizado de máquina e processamento de dados
em tempo real para navegar e tomar decisões no trânsito. Empresas como Tesla, Waymo e Uber
estão na vanguarda dessa tecnologia, prometendo reduzir acidentes de trânsito, melhorar a eficiência
do transporte e transformar a mobilidade urbana.
O impacto da IA no mercado financeiro também é notável. Algoritmos de negociação auto-
matizada analisam grandes volumes de dados em frações de segundo para executar operações
no mercado de ações com alta precisão. Além disso, sistemas de IA são utilizados para detectar
fraudes, prever tendências de mercado e fornecer recomendações personalizadas de investimentos,
ajudando investidores a tomar decisões mais informadas e seguras.
Na educação, a IA está sendo usada para personalizar a experiência de aprendizagem. Platafor-
mas de aprendizado adaptativo ajustam o conteúdo e o ritmo de ensino com base nas necessidades
individuais dos alunos, tornando a educação mais eficaz e acessível. Assistentes virtuais ajudam
estudantes com dúvidas, fornecem feedback instantâneo e facilitam a administração de cursos,
melhorando a eficiência tanto para alunos quanto para educadores.
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 7

DEEP LEARNING

O entretenimento também foi profundamente transformado pela IA. Serviços de streaming
como Netflix e Spotify utilizam algoritmos de recomendação para sugerir conteúdos baseados nas
preferências dos usuários, aumentando o engajamento e a satisfação do cliente. Além disso, a IA
está sendo usada na criação de conteúdo, desde composições musicais geradas por máquinas
até roteiros de filmes e jogos de vídeo, abrindo novas fronteiras para a criatividade e a produção
artística.
Embora os benefícios da IA sejam vastos, também é importante considerar os desafios e
implicações éticas que acompanham essa tecnologia. Questões de privacidade, segurança, viés
algorítmico e impacto no emprego são preocupações significativas que precisam ser abordadas.
Regulamentações apropriadas e uma governança responsável são essenciais para garantir que a IA
seja desenvolvida e utilizada de maneira ética e benéfica para a sociedade.
No entanto, para entender completamente o impacto e o potencial da IA, é crucial explorar suas
subáreas, como o deep learning. O deep learning, uma técnica avançada de machine learning, está
por trás de muitos dos avanços mais impressionantes da IA. Utilizando redes neurais profundas, o
deep learning permite que sistemas de IA processem e analisem grandes volumes de dados com
uma precisão sem precedentes, abrindo caminho para inovações contínuas em diversos setores.
Imagine que você é um chefe de cozinha encarregado de preparar um prato extremamente
complexo, como um suflê de chocolate perfeito. Para alcançar a excelência, você deve seguir várias
etapas específicas: selecionar os ingredientes certos, misturar nas proporções exatas, bater as
claras em neve na consistência ideal e ajustar a temperatura do forno precisamente. Agora, suponha
que você tenha uma equipe de assistentes de cozinha, cada um especializado em uma dessas
tarefas.
No entanto, ao invés de seguir uma receita rígida, cada assistente é treinado para aprender e
melhorar continuamente com a prática. Inicialmente, cada assistente começa com um conhecimento
básico, mas conforme eles trabalham repetidamente, ajustam suas técnicas com base no feedback
recebido. Por exemplo, se o suflê não cresceu como esperado, o assistente responsável por bater as
claras em neve ajustará sua técnica na próxima tentativa. Esse processo de aprendizado contínuo e
ajuste fino é análogo ao que ocorre em uma rede neural profunda (deep learning).
No deep learning, cada camada da rede neural atua como um assistente especializado, responsá-
vel por extrair diferentes níveis de características dos dados brutos. A camada inicial pode identificar
características simples, como bordas em uma imagem, semelhante a um assistente de cozinha
identificando os ingredientes básicos. Camadas subsequentes combinam essas características
simples para formar representações mais complexas, como texturas e formas, assim como os
assistentes de cozinha combinam ingredientes e técnicas para preparar elementos mais complexos
do prato. Finalmente, as camadas superiores da rede neural agregam todas essas características
para tomar uma decisão final, como um chef combinando todos os elementos para criar o suflê
perfeito.
Assim como um chef de cozinha e sua equipe podem aprimorar continuamente suas habilidades
através da prática e do feedback, uma rede neural profunda se refina iterativamente durante o
treinamento, ajustando os pesos e os parâmetros para minimizar os erros. Esse processo permite
que o deep learning alcance resultados impressionantes em tarefas como reconhecimento de
imagem, processamento de linguagem natural e muitas outras aplicações complexas.
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 8

DEEP LEARNING

1.1 Aprendizado Profundo? Vem que te explico!
Imagine que você é um chefe de cozinha encarregado de preparar um prato extremamente complexo,
como um suflê de chocolate perfeito. Para alcançar a excelência, você deve seguir várias etapas
específicas: selecionar os ingredientes certos, misturar nas proporções exatas, bater as claras em
neve na consistência ideal e ajustar a temperatura do forno precisamente. Agora, suponha que você
tenha uma equipe de assistentes de cozinha, cada um especializado em uma dessas tarefas.
No entanto, ao invés de seguir uma receita rígida, cada assistente é treinado para aprender e
melhorar continuamente com a prática. Inicialmente, cada assistente começa com um conhecimento
básico, mas conforme eles trabalham repetidamente, ajustam suas técnicas com base no feedback
recebido. Por exemplo, se o suflê não cresceu como esperado, o assistente responsável por bater as
claras em neve ajustará sua técnica na próxima tentativa. Esse processo de aprendizado contínuo e
ajuste fino é análogo ao que ocorre em uma rede neural profunda (deep learning).
No deep learning, cada camada da rede neural atua como um assistente especializado, responsá-
vel por extrair diferentes níveis de características dos dados brutos. A camada inicial pode identificar
características simples, como bordas em uma imagem, semelhante a um assistente de cozinha
identificando os ingredientes básicos. Camadas subsequentes combinam essas características
simples para formar representações mais complexas, como texturas e formas, assim como os
assistentes de cozinha combinam ingredientes e técnicas para preparar elementos mais complexos
do prato. Finalmente, as camadas superiores da rede neural agregam todas essas características
para tomar uma decisão final, como um chef combinando todos os elementos para criar o suflê
perfeito.
Assim como um chef de cozinha e sua equipe podem aprimorar continuamente suas habilidades
através da prática e do feedback, uma rede neural profunda se refina iterativamente durante o
treinamento, ajustando os pesos e os parâmetros para minimizar os erros. Esse processo permite
que o deep learning alcance resultados impressionantes em tarefas como reconhecimento de
imagem, processamento de linguagem natural e muitas outras aplicações complexas.
O Deep Learning, também conhecido como aprendizado profundo, é uma subárea do aprendizado
de máquina que tem se desenvolvido de forma exponencial nas últimas décadas. Sua origem
remonta às primeiras redes neurais artificiais na década de 1940, mas foi somente com o advento
de poderosos processadores e grandes volumes de dados que essa tecnologia alcançou seu
potencial. O desenvolvimento de algoritmos de aprendizado profundo foi impulsionado por avanços
significativos em áreas como processamento de imagens e reconhecimento de voz, culminando em
uma revolução tecnológica que transformou diversas indústrias.
Conforme a Figura 1.1, deep learning é uma subárea do machine learning, que por sua vez é
uma subárea da inteligência artificial. Este diagrama visualiza a hierarquia e a relação entre esses
três campos. A Inteligência Artificial, representada pelo círculo maior, é a área abrangente que
inclui qualquer técnica que permita às máquinas imitar o comportamento humano. Dentro desse
grande círculo, encontra-se o machine learning, que utiliza métodos estatísticos para permitir que
as máquinas aprendam e melhorem com a experiência. Finalmente, dentro do círculo de machine
learning, está o deep learning, que usa redes neurais profundas para interpretar grandes volumes
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 9

DEEP LEARNING

Figura 1.1: Diagrama mostrando a relação entre Inteligência Artificial, Machine Learning e Deep
Learning.
de dados e extrair características complexas.
Observe como cada camada interna é um subconjunto da camada externa. A Inteligência Artificial
é o campo mais amplo, englobando todas as técnicas que permitem às máquinas realizar tarefas
que normalmente requerem inteligência humana. Machine Learning é um subconjunto da IA que se
concentra em algoritmos que permitem às máquinas aprender a partir dos dados. Deep Learning
é uma abordagem específica dentro do machine learning que utiliza redes neurais profundas com
várias camadas para lidar com a complexidade dos dados.
Essa representação é crucial para entender a progressão do geral ao específico, mostrando que
o deep learning é uma técnica avançada dentro do campo do machine learning, que por sua vez é
parte essencial da inteligência artificial. A hierarquia ilustrada ajuda a compreender a importância e
o papel específico de cada uma dessas áreas no desenvolvimento de tecnologias inteligentes.
No cerne do Deep Learning estão as redes neurais artificiais, inspiradas na estrutura e funciona-
mento do cérebro humano. Essas redes são compostas por camadas de neurônios artificiais que
processam dados de entrada, aprendem padrões complexos e fazem previsões ou classificações.
Diferentemente dos métodos tradicionais de aprendizado de máquina, que muitas vezes requerem
engenharia manual de características, as redes neurais profundas podem aprender representações
de dados de forma automática e hierárquica, o que as torna extremamente eficazes para tarefas
complexas.
Comparado a outras técnicas de aprendizado de máquina, o Deep Learning se destaca pela sua
capacidade de lidar com dados não estruturados e por sua robustez em aprender representações de
alta dimensão. Enquanto métodos como máquinas de vetores de suporte ou árvores de decisão
podem ser limitados pela necessidade de extração manual de características, as redes neurais
profundas podem aprender essas características diretamente dos dados brutos, como imagens,
áudio ou texto, permitindo um desempenho superior em muitas aplicações.
As aplicações do Deep Learning são vastas e abrangem várias áreas. Na visão computacional,
ele é usado para reconhecimento de objetos, detecção de anomalias e segmentação de imagens. Na
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 10

DEEP LEARNING

área de processamento de linguagem natural, é empregado em tarefas como tradução automática,
análise de sentimento e geração de texto. Em saúde, o Deep Learning está revolucionando o diag-
nóstico médico ao permitir a análise automática de imagens de raios-X e ressonância magnética. Em
transporte, é um componente crucial no desenvolvimento de veículos autônomos. Esses exemplos
ilustram como o Deep Learning está transformando indústrias e criando novas possibilidades.
A importância do Deep Learning na atualidade não pode ser subestimada. Ele está na vanguarda
da inteligência artificial, impulsionando inovações que antes eram consideradas ficção científica. Sua
capacidade de processar e interpretar grandes volumes de dados em tempo real está permitindo
avanços significativos em áreas como segurança, saúde, entretenimento e negócios. À medida que
os algoritmos se tornam mais sofisticados e os dados mais abundantes, o impacto do Deep Learning
continuará a crescer.
As redes neurais, componentes essenciais do Deep Learning, são compostas por neurônios
organizados em camadas. Cada neurônio recebe entradas, aplica uma função de ativação e
transmite o resultado para a próxima camada. As redes podem ser treinadas usando algoritmos de
otimização, como o gradiente descendente, que ajusta os pesos das conexões entre neurônios para
minimizar a diferença entre as previsões da rede e os valores reais. Esse processo de treinamento é
iterativo e exige grandes volumes de dados e poder computacional significativo.
As Redes Neurais Convolucionais (CNNs) representam uma arquitetura específica de redes
neurais projetada para processar dados com uma grade topológica, como imagens. Inspiradas pela
organização do córtex visual dos animais, as CNNs são altamente eficazes para tarefas de visão
computacional. Elas utilizam camadas convolucionais que aplicam filtros para extrair características
locais dos dados de entrada, preservando a relação espacial entre os pixels. Isso permite que as
CNNs aprendam características hierárquicas, desde bordas simples até padrões complexos, em
diferentes níveis de abstração.
O Deep Learning representa um avanço significativo na capacidade das máquinas de aprender
e interpretar dados complexos. Com uma base histórica sólida e uma evolução contínua, ele
se estabeleceu como uma ferramenta indispensável em diversas áreas da tecnologia moderna,
transformando a maneira como interagimos com o mundo digital e abrindo novas fronteiras para a
inovação.
1.2 Primeiros passos com as Redes que conseguem ver
Imagine que você é um fotógrafo tentando capturar a melhor imagem possível de uma paisagem.
Para obter uma foto perfeita, você precisa de uma série de filtros e ajustes que destacam diferentes
aspectos da cena. Primeiramente, você pode usar um filtro que realça as bordas dos objetos na
imagem, tornando os contornos mais nítidos. Em seguida, você pode aplicar um filtro que ajusta o
brilho e o contraste, ajudando a destacar áreas específicas da paisagem. Finalmente, você ajusta a
saturação das cores para tornar a imagem mais vibrante e atraente. Cada um desses filtros contribui
para a melhoria da imagem final, destacando diferentes características e detalhes.
Da mesma forma, uma Rede Neural Convolucional (CNN) usa várias camadas de filtros, conheci-
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 11

DEEP LEARNING

dos como convoluções, para analisar e melhorar os dados de entrada, que geralmente são imagens.
Cada camada convolucional aplica um conjunto de filtros que extrai características específicas dos
dados. As primeiras camadas podem identificar características simples, como bordas e texturas,
semelhante ao filtro do fotógrafo que realça contornos. À medida que os dados passam por camadas
mais profundas da rede, as características extraídas se tornam progressivamente mais complexas e
abstratas, como formas, padrões e objetos inteiros, tal como os ajustes subsequentes feitos pelo
fotógrafo para melhorar a imagem.
Esses filtros em uma CNN são ajustados durante o processo de treinamento, onde a rede
aprende quais características são mais importantes para a tarefa em questão, seja reconhecimento
de objetos, classificação de imagens ou qualquer outra aplicação de visão computacional. Assim
como o fotógrafo ajusta seus filtros e configurações com base na iluminação e nas condições da
cena, uma CNN ajusta seus filtros internos para otimizar o desempenho na tarefa de análise de
imagem, resultando em uma compreensão profunda e detalhada dos dados visuais.
Essa analogia ajuda a entender como as CNNs decompõem e analisam imagens de maneira
hierárquica, utilizando filtros convolucionais para capturar características em vários níveis de comple-
xidade, aprimorando a capacidade da rede de interpretar e classificar imagens com alta precisão.
As Redes Neurais Convolucionais (CNNs) são uma classe de redes neurais artificiais projetadas
especificamente para processar dados que possuem uma estrutura de grade, como imagens. A
estrutura de uma CNN é composta por várias camadas, incluindo camadas convolucionais, camadas
de pooling e camadas totalmente conectadas. As camadas convolucionais aplicam filtros, ou kernels,
aos dados de entrada para extrair características locais, preservando a relação espacial entre os
pixels.
Os filtros nas camadas convolucionais são matrizes de pesos que deslizam sobre a entrada,
realizando operações de convolução que resultam em mapas de características. Cada filtro é capaz
de detectar diferentes características, como bordas, texturas ou padrões, em várias posições da
imagem. Após a aplicação dos filtros, os mapas de características passam por uma função de
ativação não linear, como ReLU (Rectified Linear Unit), para introduzir não linearidades no modelo.
As camadas de pooling são usadas para reduzir a dimensionalidade dos mapas de características,
mantendo as informações mais relevantes. O pooling mais comum é omax pooling, que seleciona
o valor máximo em uma janela de tamanhos fixos, reduzindo a resolução espacial dos mapas de
características e, consequentemente, o número de parâmetros e a carga computacional da rede.
Além disso, camadas de normalização, como Batch Normalization, são frequentemente utilizadas
para estabilizar e acelerar o treinamento, normalizando as ativações das camadas anteriores.
Para ilustrar, considere uma rede convolucional simples composta por uma camada convolucional
com um conjunto de filtros, seguida por uma camada de pooling e uma camada totalmente conectada
que gera a saída final. Essa estrutura básica pode ser expandida para redes muito mais profundas
e complexas, como as arquiteturas VGG, ResNet e Inception, que são amplamente utilizadas em
aplicações modernas.
As CNNs oferecem várias vantagens para a classificação de imagens em comparação com redes
totalmente conectadas tradicionais. A principal vantagem é a capacidade de capturar características
espaciais hierárquicas devido à aplicação local dos filtros. Além disso, a redução de parâmetros
proporcionada pelas camadas convolucionais e de pooling torna as CNNs mais eficientes e menos
propensas aooverfitting.
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 12

DEEP LEARNING

As aplicações práticas das CNNs são vastas e incluem a classificação de imagens, a detecção de
objetos, a segmentação de imagens e o reconhecimento de ações em vídeos. Em saúde, as CNNs
são usadas para analisar imagens médicas, como raios-X e ressonâncias magnéticas, auxiliando
no diagnóstico de doenças. Em segurança, são aplicadas em sistemas de vigilância para detectar
comportamentos suspeitos ou identificar indivíduos.
Para melhorar o desempenho e a generalização das CNNs, diversas técnicas de regularização
são empregadas, comodropout,weight decayedata augmentation. Essas técnicas ajudam a
prevenir ooverfittinge melhorar a robustez do modelo.
O treinamento de uma CNN envolve a minimização de uma função de perda, como a entropia
cruzada, usando algoritmos de otimização, como o gradiente descendente estocástico (SGD).
Durante o treinamento, o modelo ajusta os pesos dos filtros para reduzir a diferença entre as
previsões e os valores reais. A avaliação de uma CNN é feita usando métricas como acurácia,
precisão, recall e F1-score, aplicadas a um conjunto de dados de validação.
Em resumo, as Redes Neurais Convolucionais são uma poderosa ferramenta no arsenal de
técnicas de aprendizado profundo, oferecendo uma abordagem eficiente e eficaz para a análise
de dados visuais. Sua capacidade de aprender representações hierárquicas de dados as torna
indispensáveis em diversas aplicações práticas.
Figura 1.2: Arquitetura VGG-16 mostrando as várias camadas convolucionais, camadas de pooling e
camadas totalmente conectadas.
CAPÍTULO 1. INTRODUÇÃO A DEEP LEARNING 13

DEEP LEARNING

CAPÍTULO 2
2 IA sem programar – Sim, é verdade!
Imagine que criar modelos de deep learning é como construir uma casa. Tradicionalmente, para
construir essa casa, você precisaria de um profundo conhecimento de arquitetura, engenharia e uma
variedade de ferramentas especializadas. Da mesma forma, desenvolver modelos de deep learning
normalmente requer um sólido entendimento de programação, matemática avançada e o uso de
frameworks complexos como TensorFlow ou PyTorch.
No entanto, ferramentas como o Teachable Machine são como kits de construção de casas
prontos para montar. Esses kits vêm com todas as peças pré-fabricadas e instruções claras,
permitindo que qualquer pessoa, mesmo sem experiência em construção, possa montar sua própria
casa de forma rápida e eficiente. Com o Teachable Machine, você não precisa ser um programador
experiente para criar modelos de deep learning poderosos. A plataforma oferece uma interface
amigável e intuitiva, onde você pode simplesmente arrastar e soltar dados, ajustar alguns parâmetros
e, em poucos cliques, ter um modelo funcional pronto para uso.
Assim como um kit de construção pode incluir peças que se encaixam perfeitamente, sem a
necessidade de ferramentas pesadas ou cálculos complexos, o Teachable Machine facilita a criação
de modelos de deep learning sem a necessidade de escrever código ou entender os detalhes
matemáticos subjacentes. Isso permite que mais pessoas, com diferentes níveis de habilidade e
conhecimento, possam explorar e utilizar a inteligência artificial para resolver problemas reais e
inovar em suas áreas de atuação.
No fim das contas, o Teachable Machine e ferramentas semelhantes estão tornando a construção
de "casas"de deep learning acessível a todos, democratizando o acesso a tecnologias avançadas e
permitindo que uma gama diversificada de usuários crie soluções inteligentes e impactantes sem as
barreiras tradicionais do desenvolvimento de software.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 14

DEEP LEARNING

2.1 IA sem mistério: agora para qualquer um
O aprendizado profundo trouxe consigo uma revolução na forma como processamos e interpretamos
dados visuais e textuais. No entanto, a complexidade envolvida no desenvolvimento e implementação
de modelos de deep learning sempre foi uma barreira significativa para muitos profissionais que não
possuem um background em programação ou em ciências da computação. OTeachable Machine,
desenvolvida pelo Google, emergiram como soluções inovadoras que permitem a criação de modelos
de aprendizado profundo de maneira intuitiva e acessível, eliminando a necessidade de programação.
Essas plataformas democratizam o acesso às tecnologias de inteligência artificial, possibilitando que
um público mais amplo explore e aplique essas técnicas em diversas áreas.
O Teachable Machine é uma plataforma baseada na web que permite aos usuários treinar
modelos de aprendizado profundo diretamente do navegador. A interface do usuário é projetada
para ser altamente intuitiva, permitindo que qualquer pessoa, desde estudantes até profissionais
de diversas áreas, crie modelos de classificação de imagens, sons e poses sem a necessidade de
escrever uma única linha de código. O processo de criação de modelos é simplificado em três etapas
principais: coleta de dados, treinamento do modelo e implementação. A coleta de dados pode ser
feita através da webcam, microfone ou upload de arquivos, tornando o processo rápido e fácil.
Uma das grandes vantagens do Teachable Machine é sua capacidade de fornecer resultados em
tempo real. Após a coleta dos dados e o treinamento do modelo, os usuários podem imediatamente
testar e ajustar seus modelos para melhorar a precisão e a eficácia. A plataforma utiliza bibliotecas de
aprendizado profundo robustas como TensorFlow.js para treinar e executar os modelos diretamente
no navegador, o que significa que os dados não precisam ser enviados para servidores externos,
garantindo maior privacidade e segurança. Além disso, os modelos treinados podem ser exportados
e integrados em outras aplicações, permitindo uma versatilidade significativa no uso dos modelos
criados.
Ferramentas como o Teachable Machine representam um passo significativo na democratização
do aprendizado profundo. Elas permitem que indivíduos e pequenas organizações, que talvez não
tenham os recursos ou a expertise técnica necessária, possam se beneficiar do poder da inteligência
artificial. Com essas ferramentas, é possível desenvolver soluções inovadoras em áreas como
educação, saúde, entretenimento e muito mais. Este capítulo explorará em detalhes como essas
ferramentas funcionam, suas aplicações práticas e como elas estão transformando a paisagem do
deep learning, tornando-o mais acessível e inclusivo para todos.
Para começar a usar o Teachable Machine, acesse o site Teachable Machine. Na página inicial,
você verá uma tela semelhante à da Figura 2.1. Aqui, você pode começar a treinar um computador
para reconhecer suas próprias imagens, sons e poses de maneira rápida e fácil. Sem necessidade
de expertise ou conhecimento em programação, basta clicar em "Get Started"para iniciar.
A interface do Teachable Machine é intuitiva e amigável. Na imagem, observe a seção central
onde está a foto de uma pessoa com pontos e linhas azuis sobrepostos ao corpo. Estes representam
um modelo de reconhecimento de poses, que utiliza keypoints para identificar e rastrear diferentes
partes do corpo em movimento. Para começar a treinar seu próprio modelo, clique em "Get Started"e
siga as instruções para coletar dados utilizando sua webcam ou carregando arquivos de imagem.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 15

DEEP LEARNING

Um gráfico de barras mostra os resultados de uma classificação. Neste caso, o modelo está
classificando a pose atual como "Wings"com uma confiança de 100%. Você pode ajustar e testar
seu modelo em tempo real, garantindo que ele esteja funcionando corretamente antes de exportá-lo
para outras aplicações.
Diferentes tecnologias e bibliotecas são compatíveis com o Teachable Machine, como TensorFlow,
p5.js, Coral, entre outros. Isso mostra a versatilidade da ferramenta e a facilidade com que você
pode integrar os modelos treinados em diversos projetos. Acesse agora e comece a explorar as
possibilidades do deep learning sem precisar programar!
Figura 2.1: Página inicial do Teachable Machine.
Clicando em "Get Started", você será direcionado para a página de criação de novos projetos no
Teachable Machine, conforme mostrado na Figura 2.2. Nesta página, você encontrará três opções
principais para iniciar seu projeto: Image Project, Audio Project e Pose Project. Cada uma dessas
opções permite que você crie modelos de aprendizado de máquina personalizados de acordo com o
tipo de dado que deseja utilizar.
Para criar um projeto baseado em imagens, clique em "Image Project". Esta opção permite que
você ensine o computador a reconhecer diferentes objetos ou categorias utilizando imagens que
podem ser capturadas pela sua webcam ou carregadas de arquivos. Este é um ótimo ponto de
partida para tarefas de classificação de imagens.
Se você está interessado em trabalhar com áudio, clique em "Audio Project". Esta opção permite
que você treine o modelo para reconhecer sons de um segundo de duração, seja através de arquivos
de áudio ou usando o microfone. É ideal para projetos que envolvem a classificação de diferentes
tipos de sons ou comandos de voz.
Por fim, para projetos que envolvem o reconhecimento de poses, clique em "Pose Project". Esta
opção utiliza a webcam para capturar e identificar diferentes poses do corpo humano, utilizando
keypoints para rastrear os movimentos. É particularmente útil para aplicações que requerem a
detecção e análise de movimentos corporais.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 16

DEEP LEARNING

Figura 2.2: Página de criação de novos projetos no Teachable Machine.
2.2 Ensinando máquinas a "ver"imagens
Vamos começar um projeto de classificação de imagens utilizando o Teachable Machine. Ao clicar
em "Image Project"na página de novos projetos, você será levado à tela exibida na Figura 2.3. Nesta
tela, você tem duas opções principais para escolher: "Standard image model"e "Embedded image
model". Cada uma dessas opções é adequada para diferentes tipos de aplicações e dispositivos.
Se você optar por "Standard image model", clique na área destacada em azul. Este modelo é
ideal para a maioria das aplicações e utiliza imagens coloridas com resolução de 224x224 pixels.
É perfeito para exportação para TensorFlow, TensorFlow Lite (TFLite) e TensorFlow.js (TF.js), e o
tamanho do modelo final será em torno de 5MB. Esta opção é recomendada para projetos que serão
executados em dispositivos com capacidade de processamento suficiente, como smartphones e
computadores.
Por outro lado, se sua aplicação envolve dispositivos com recursos limitados, como microcontrola-
dores, clique na área destacada em branco, "Embedded image model". Este modelo trabalha com
imagens em escala de cinza com resolução de 96x96 pixels e é otimizado para exportação para
TFLite for Microcontrollers, TFLite e TF.js. O tamanho do modelo resultante será em torno de 500KB,
tornando-o adequado para dispositivos de baixo consumo energético e com limitações de memória.
Escolha a opção que melhor se adapta às suas necessidades e siga adiante para começar a
coletar dados para o treinamento do seu modelo. A interface do Teachable Machine guiará você
pelo processo de captura e categorização das imagens, facilitando a criação de um modelo de deep
learning personalizado sem a necessidade de escrever código.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 17

DEEP LEARNING

Figura 2.3: Opções de modelo de imagem no Teachable Machine.
Vamos escolher o "Standard image model"para o nosso projeto. Após selecionar esta opção,
você será direcionado para a tela de coleta de amostras, como mostrado na Figura 2.4.
Esse é o nosso centro de treinamento de IA. Uma característica fundamental da inteligência
artificial (IA) em deep learning é que ela não é programada no sentido tradicional de codificação
explícita de regras e lógica. Em vez disso, os modelos de deep learning são treinados utilizando
grandes conjuntos de dados. Durante o treinamento, o modelo aprende a reconhecer padrões e
características dos dados através de um processo iterativo de ajuste de seus parâmetros internos.
Este processo, conhecido como aprendizado supervisionado, envolve a alimentação de exemplos
rotulados ao modelo, permitindo que ele aprenda a mapear entradas para as saídas corretas. Ao
contrário da programação convencional, onde cada passo do problema é resolvido com instruções
explícitas de código, o deep learning depende de algoritmos que ajustam automaticamente seus
parâmetros para minimizar o erro nas previsões.
Esta abordagem de treinamento traz várias vantagens significativas. Primeiramente, permite que
os modelos de deep learning abordem problemas complexos que seriam extremamente difíceis,
se não impossíveis, de programar manualmente. Por exemplo, tarefas como reconhecimento de
imagem, tradução de idiomas e processamento de linguagem natural envolvem uma quantidade
massiva de variáveis e nuances que não podem ser facilmente capturadas por regras rígidas. Em
segundo lugar, a capacidade de um modelo de melhorar continuamente seu desempenho com mais
dados e treinamento reflete uma forma de aprendizagem adaptativa, semelhante ao aprendizado
humano. Isso significa que, em vez de precisar de reprogramação para cada novo problema, um
modelo de deep learning pode ser refinado e ajustado com novos dados para se adaptar a diferentes
tarefas e condições.
Nessas caixas de interação você irá definir a classe de imagens escrevendo o nome da classe
em "Class 1". Na Figura 2.5, você vê a interface para adicionar amostras de imagem para uma
classe específica. Primeiro, clique no ícone do lápis ao lado de "Class 1"para renomear a classe.
Isso ajudará a organizar e identificar melhor as diferentes categorias que você deseja treinar.
Para adicionar amostras de imagem, você tem duas opções: "Webcam"e "Upload". Clique em
"Webcam"para capturar imagens diretamente da sua câmera. Esta é uma maneira prática de coletar
imagens em tempo real. Posicione o objeto ou a pessoa à frente da câmera e capture várias imagens
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 18

DEEP LEARNING

Figura 2.4: Tela de coleta de amostras no Teachable Machine.
para representar bem a classe. Se você já possui imagens armazenadas no seu computador, clique
em "Upload". Selecione os arquivos que deseja usar como amostras para essa classe.
Após adicionar todas as amostras necessárias para a classe, repita o processo para cada nova
classe que você deseja criar, clicando em "Add a class"e seguindo os mesmos passos. É importante
coletar uma quantidade suficiente de amostras para cada classe para garantir que o modelo possa
aprender e reconhecer as diferentes categorias de maneira eficaz.
Depois de adicionar as amostras de todas as classes, você estará pronto para treinar o modelo.
Certifique-se de que cada classe tenha uma representação adequada de amostras para melhorar a
precisão do modelo durante o treinamento.
Figura 2.5: Interface para adicionar amostras de imagem no Teachable Machine.
Para captar imagens direto da sua webcam, clique em "Webcam"na interface de adição de
amostras. Na Figura 2.6, vemos a tela de captura de imagens com a webcam ativada. Posicione o
objeto ou a pessoa que deseja capturar na frente da câmera. Clique e segure o botão azul "Hold
to Record"para começar a gravar uma série de imagens que serão usadas como amostras para a
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 19

DEEP LEARNING

"Class 1".
O uso da webcam facilita a coleta de múltiplas imagens de maneira rápida e eficiente. Certifique-
se de capturar diversas poses e ângulos do objeto para proporcionar uma variedade de dados ao
modelo. Isso ajudará a melhorar a capacidade do modelo de generalizar e reconhecer a classe em
diferentes condições. Quando terminar de coletar as amostras, você pode visualizar as imagens
capturadas na seção "Add Image Samples". Se necessário, ajuste as configurações clicando no
ícone de engrenagem ao lado do botão "Hold to Record".
Após capturar e adicionar todas as amostras desejadas, você pode prosseguir para adicionar
mais classes ou começar o processo de treinamento do modelo. Este método de captura de dados
garante que você tenha um conjunto de dados diversificado e representativo, fundamental para o
treinamento eficaz do modelo de deep learning.
Figura 2.6: Interface de captura de amostras utilizando a webcam no Teachable Machine.
Clique na engrenagem para alterar as configurações de captura da webcam, conforme mostrado
na Figura 2.7. Aqui, você pode ajustar vários parâmetros para otimizar a coleta de amostras. A
primeira configuração é o FPS (Frames Per Second), que determina a taxa de quadros da gravação.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 20

DEEP LEARNING

No exemplo, está definido para 24 FPS, o que é uma boa taxa para capturar movimentos suaves.
Se preferir, você pode ativar a opção "Hold to Record", o que permitirá gravar manualmente
segurando o botão de gravação. Se essa opção estiver desativada, você pode configurar o tempo de
atraso (Delay) antes de iniciar a gravação, definido aqui como 2 segundos, e a duração (Duration) da
gravação, que está configurada para 6 segundos. Essas configurações permitem capturar imagens
de forma automática e sem a necessidade de segurar o botão, facilitando a coleta de dados contínua.
Após ajustar as configurações de acordo com suas necessidades, clique em "Save Settings"para
aplicar as alterações. Essas configurações ajudarão a garantir que você colete dados de qualidade
e de maneira eficiente para treinar seu modelo. Lembre-se de ajustar esses parâmetros conforme
necessário para capturar as amostras da melhor forma possível para sua aplicação específica.
Figura 2.7: Configurações de captura de amostras utilizando a webcam no Teachable Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 21

DEEP LEARNING

2.3 Construindo nossa primeira rede neural visual
Vamos treinar uma Rede Neural Convolucional (CNN) para detectar máscaras faciais em pessoas.
O uso de máscaras é crucial em ambientes hospitalares para prevenir a disseminação de doenças
infecciosas entre pacientes e profissionais de saúde. Máscaras ajudam a bloquear partículas
respiratórias que podem conter patógenos, reduzindo a probabilidade de infecções cruzadas. Além
disso, durante a pandemia de COVID-19, o uso de máscaras se tornou uma medida vital de saúde
pública, ajudando a limitar a propagação do vírus em ambientes comunitários e de trabalho.
A importância das máscaras durante a pandemia destacou a necessidade de sistemas automati-
zados para verificar o uso adequado das mesmas. Treinando uma CNN para essa tarefa, podemos
simular a função de um supervisor humano, garantindo que apenas pessoas usando máscaras
entrem em áreas controladas, como hospitais, escritórios e espaços públicos. Esse sistema auto-
matizado não só aumenta a eficiência do controle de entrada, mas também reduz a exposição dos
seguranças e supervisores a possíveis riscos de contaminação.
Além do uso em ambientes hospitalares e durante pandemias, a detecção de máscaras faciais
pode ser aplicada em outras indústrias onde o uso de equipamentos de proteção individual (EPI) é
essencial. Por exemplo, pintores de carros e trabalhadores em ambientes industriais frequentemente
utilizam máscaras para se protegerem de vapores químicos e partículas nocivas. Um sistema de
detecção automática de máscaras pode ajudar a garantir que os trabalhadores estejam sempre
utilizando a proteção adequada, promovendo um ambiente de trabalho seguro.
Outro exemplo relevante é a indústria de alimentos, onde o uso de máscaras pode prevenir a
contaminação de produtos alimentícios por parte dos trabalhadores. A aplicação de CNNs para
monitorar o uso de máscaras em fábricas e cozinhas industriais pode melhorar significativamente os
padrões de higiene, garantindo a segurança alimentar e a saúde dos consumidores. Esses sistemas
podem ser integrados com câmeras de segurança para fornecer monitoramento contínuo e em
tempo real.
Em resumo, a implementação de uma Rede Neural Convolucional para detectar máscaras faciais
oferece uma solução eficiente e precisa para garantir a conformidade com normas de segurança e
saúde em diversos contextos. Desde hospitais até indústrias e espaços públicos, essa tecnologia
pode desempenhar um papel crucial na proteção da saúde pública e ocupacional. O desenvolvimento
de tais sistemas representa um passo importante na utilização da inteligência artificial para melhorar
a segurança e a qualidade de vida.
Criando as classes de imagens
Vamos começar a criar nossa primeira classe de imagens. A primeira classe se chamará "NO-
MASK". Ela deve conter exemplos de imagens de pessoas que não estão usando máscara. Na
Figura 2.8, vemos a interface onde as amostras de imagem para essa classe foram coletadas.
Primeiro, renomeie a classe clicando no ícone de lápis ao lado de "Class 1"e digitando "NO-MASK".
Para capturar as amostras, clique no botão "Record 6 Seconds"e posicione-se de forma que
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 22

DEEP LEARNING

Figura 2.8: Captura de amostras de imagem para a classe "NO-MASK"utilizando a webcam no
Teachable Machine.
seu rosto esteja claramente visível na câmera. O sistema capturará uma série de imagens durante
esses seis segundos, como mostrado na área de amostras à direita. O objetivo é capturar várias
expressões e ângulos do rosto sem máscara, garantindo que o modelo receba uma representação
diversificada da classe "NO-MASK".
É importante ter uma quantidade suficiente de amostras para que o modelo possa aprender cor-
retamente as características da classe. No exemplo, foram capturadas 134 imagens, proporcionando
um bom conjunto de dados para o treinamento. Repita este processo para cada nova pessoa ou
cenário sem máscara para aumentar a diversidade do conjunto de dados.
A qualidade das imagens é um fator crucial no treinamento de uma Rede Neural Convolucional
(CNN). Imagens de alta qualidade fornecem detalhes ricos e nítidos que ajudam a CNN a aprender
características significativas e distinguir entre diferentes classes com maior precisão. Quando as
imagens são de baixa resolução ou possuem ruído significativo, a rede pode ter dificuldade em
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 23

DEEP LEARNING

extrair as informações relevantes necessárias para fazer previsões precisas. Portanto, garantir que
as imagens utilizadas no treinamento sejam de alta qualidade é essencial para o desempenho geral
do modelo.
Além da resolução e da clareza, a diversidade das amostras de imagem é igualmente importante.
Uma coleção de imagens de alta qualidade, mas com pouca variação em termos de ângulos,
iluminação e contextos, pode levar a um modelo que não generaliza bem para novas situações.
Por isso, ao preparar o conjunto de dados, é fundamental incluir imagens capturadas em diferentes
condições e ambientes. Isso permite que a CNN aprenda a reconhecer o mesmo objeto ou classe
sob várias circunstâncias, melhorando sua robustez e capacidade de generalização.
A consistência na qualidade das imagens também desempenha um papel significativo. Variabili-
dade extrema na qualidade das amostras pode confundir a CNN durante o processo de aprendizado,
resultando em um modelo que tem desempenho inconsistente. Manter um padrão de qualidade
uniforme ajuda a assegurar que a rede se concentre em aprender os padrões e características rele-
vantes, em vez de ser distraída por discrepâncias na qualidade das imagens. Isso é particularmente
importante em aplicações críticas, como detecção de máscaras faciais, onde a precisão é vital.
Por fim, a pré-processamento das imagens pode aumentar ainda mais a qualidade do conjunto
de dados. Técnicas como normalização de brilho e contraste, remoção de ruído e alinhamento de
imagens podem melhorar significativamente a qualidade das amostras antes de serem alimentadas
na CNN. Além disso, aumentos de dados, como rotações aleatórias, zooms e flips horizontais,
podem aumentar a diversidade sem a necessidade de coletar mais dados. Esses passos de
pré-processamento garantem que a CNN seja treinada com um conjunto de dados otimizado,
maximizando seu desempenho e precisão nas tarefas de classificação ou detecção.
Após coletar todas as amostras para a classe "NO-MASK", prossiga para criar a próxima classe,
que conterá imagens de pessoas usando máscara. Essa segunda classe ajudará o modelo a
aprender a distinguir entre indivíduos com e sem máscara, aumentando a precisão da detecção.
Lembre-se de verificar as amostras coletadas e remover qualquer imagem que não esteja clara
ou que possa confundir o modelo. Manter um conjunto de dados limpo e bem organizado é crucial
para o sucesso do treinamento da Rede Neural Convolucional.
Agora vamos treinar a nossa segunda classe que se chamará "MASK". Ela deve conter exemplos
de imagens de pessoas que estão usando máscara. Na Figura 2.9, vemos a interface onde as
amostras de imagem para essa classe foram coletadas. Primeiro, renomeie a classe clicando no
ícone de lápis ao lado de "Class 1"e digitando "MASK".
Para capturar as amostras, clique no botão "Record 6 Seconds"e posicione-se de forma que
seu rosto com a máscara esteja claramente visível na câmera. O sistema capturará uma série de
imagens durante esses seis segundos, como mostrado na área de amostras à direita. O objetivo é
capturar várias expressões e ângulos do rosto com máscara, garantindo que o modelo receba uma
representação diversificada da classe "MASK".
É essencial coletar uma quantidade suficiente de amostras para que o modelo possa aprender
corretamente as características da classe. No exemplo, foram capturadas 131 imagens, proporcio-
nando um bom conjunto de dados para o treinamento. Repita este processo para cada nova pessoa
ou cenário com máscara para aumentar a diversidade do conjunto de dados.
Após coletar todas as amostras para a classe "MASK", prossiga para revisar as amostras
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 24

DEEP LEARNING

coletadas e remover qualquer imagem que não esteja clara ou que possa confundir o modelo. Manter
um conjunto de dados limpo e bem organizado é crucial para o sucesso do treinamento da Rede
Neural Convolucional. Com as classes "NO-MASK"e "MASK"bem definidas, você estará pronto para
iniciar o treinamento do seu modelo.
Figura 2.9: Captura de amostras de imagem para a classe "MASK"utilizando a webcam no Teachable
Machine.
Se você estiver em um problema que envolva mais classes, é essencial adicionar todas as
classes necessárias para o seu modelo. Na Figura 2.10, vemos a interface do Teachable Machine
que permite a criação de novas classes. Para adicionar uma nova classe, clique em "Add a class".
Isso permitirá que você crie uma nova categoria de amostras de imagem, essencial para treinar o
modelo de deep learning a reconhecer múltiplas classes.
Por exemplo, além das classes "MASK"e "NO-MASK"que criamos anteriormente, você pode
precisar de classes adicionais como "PARTIAL-MASK"ou "INCORRECT-MASK"para diferenciar entre
diferentes tipos de uso de máscara. Clique em "Add a class"e repita o processo de coleta de amostras
para cada nova classe, garantindo que você capture uma variedade de imagens representativas
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 25

DEEP LEARNING

para cada uma delas.
É importante que cada classe tenha uma quantidade adequada de amostras para permitir que
o modelo aprenda a distinguir entre as diferentes categorias de forma eficaz. A coleta de dados
diversificados e em diferentes condições de iluminação, ângulos e contextos aumentará a robustez e
a precisão do seu modelo. Mantenha um padrão de qualidade nas imagens coletadas para todas as
classes, garantindo que o modelo não seja influenciado por inconsistências nos dados.
Depois de adicionar todas as classes necessárias e coletar as amostras correspondentes,
você estará pronto para iniciar o treinamento do seu modelo. Certifique-se de revisar todas as
amostras coletadas para garantir que estejam corretas e bem representadas. Esse cuidado no
pré-processamento dos dados é fundamental para o sucesso do treinamento e para obter um modelo
confiável e preciso.
Figura 2.10: Interface para adicionar novas classes no Teachable Machine.
2.4 Vamos treinar nossa IA? Pegue seu capacete!
Chegou a hora de treinar nosso modelo de IA baseado em Redes Convolucionais. Na Figura 2.11,
vemos a interface do Teachable Machine pronta para iniciar o treinamento do modelo. Para começar,
clique no botão "Train Model"destacado em azul. Esse botão iniciará o processo de treinamento
utilizando as amostras de imagem que você adicionou anteriormente para cada classe.
Certifique-se de que você tenha coletado um número adequado de amostras para cada classe
antes de iniciar o treinamento. No exemplo, já temos duas classes ("MASK"e "NO-MASK"). Se ne-
cessário, adicione mais classes clicando em "Add a class"e coletando as amostras correspondentes.
Quanto mais diversificado e representativo for o seu conjunto de dados, melhor será o desempenho
do seu modelo.
Ao clicar em "Train Model", o Teachable Machine começará a ajustar os parâmetros da Rede
Neural Convolucional para minimizar os erros de classificação. Esse processo pode levar algum
tempo, dependendo da quantidade de dados e da complexidade do modelo. Durante o treinamento,
o algoritmo aprenderá a distinguir entre as diferentes classes com base nos padrões identificados
nas imagens fornecidas.
Isso aqui é muito importante, não troque de abas no momento do treinamento, deixe o Teachable
Machine trabalhar conforme necessário. Na Figura 2.12, vemos o processo de treinamento do
modelo em andamento. As classes "NO-MASK"e "MASK"já têm suas amostras de imagem coletadas
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 26

DEEP LEARNING

Figura 2.11: Interface para iniciar o treinamento do modelo no Teachable Machine.
e organizadas. O treinamento do modelo está em progresso, conforme indicado pela barra de
progresso e o tempo decorrido.
É crucial manter a aba do navegador aberta e não alternar para outras abas durante o treinamento.
O Teachable Machine exige que a aba permaneça ativa para completar o processo de treinamento de
forma eficiente. Qualquer interrupção pode resultar em um treinamento incompleto, comprometendo
a precisão do modelo.
Durante o treinamento, o modelo ajusta seus parâmetros internos para aprender a distinguir entre
as diferentes classes baseadas nas amostras fornecidas. No exemplo, temos 134 imagens para
a classe "NO-MASK"e 131 imagens para a classe "MASK". Essas amostras fornecem uma base
sólida para o modelo aprender as características específicas de cada classe.
Uma vez que o treinamento esteja concluído, você poderá revisar os resultados e testar a
precisão do modelo na seção de pré-visualização (Preview). Se os resultados não forem satisfatórios,
considere adicionar mais amostras ou revisar a qualidade das imagens coletadas. Este processo
iterativo de coleta, treinamento e ajuste é essencial para desenvolver um modelo robusto e eficaz
para detecção de máscaras faciais.
2.5 A IA no comando: fazendo previsões
Vamos realizar predições com nossa IA. Na Figura 2.13, vemos a interface de pré-visualização do
Teachable Machine, onde podemos testar o modelo treinado em tempo real. Para começar, ative a
entrada de vídeo clicando no botão "Input"e assegure-se de que a opção "Webcam"está selecionada.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 27

DEEP LEARNING

Figura 2.12: Treinamento do modelo em andamento no Teachable Machine.
Isso permitirá que o sistema utilize a webcam do seu dispositivo para capturar imagens ao vivo.
Observe que, na imagem capturada, a saída do modelo mostra uma barra laranja com a classifica-
ção "NO-MASK"e um valor de confiança de 100%. Isso indica que o modelo detectou corretamente
que a pessoa na imagem não está usando máscara. Abaixo, você também verá a classificação
"MASK"com um valor de confiança muito baixo, representando a ausência de máscara na detecção.
Para testar a precisão do modelo, posicione-se em frente à webcam e faça diferentes gestos ou
mude a posição da máscara, se estiver usando uma. A interface fornecerá feedback instantâneo
sobre a classificação, ajudando a validar a eficácia do modelo treinado. Se o modelo não estiver
classificando corretamente, considere revisar as amostras de treinamento ou adicionar mais dados
para melhorar a precisão.
Na continuidade do teste do nosso modelo, agora vamos analisar o comportamento da Rede Neu-
ral Convolucional ao detectar uma máscara. Na Figura 2.14, vemos a interface de pré-visualização
do Teachable Machine, onde o modelo está classificando uma imagem em tempo real com a pessoa
utilizando uma máscara.
Como na imagem anterior, a entrada de vídeo está ativada e a opção "Webcam"está selecionada.
Desta vez, a pessoa está usando uma máscara, e a saída do modelo mostra uma barra vermelha
com a classificação "MASK"e um valor de confiança de 100%. Isso indica que o modelo detectou
corretamente que a pessoa na imagem está usando uma máscara. A classificação "NO-MASK"agora
mostra um valor de confiança muito baixo, confirmando a detecção da máscara.
Para assegurar a robustez do modelo, é importante testar com diferentes tipos de máscaras,
ajustes de luz e ângulos de visão. Essa prática ajuda a garantir que o modelo possa generalizar
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 28

DEEP LEARNING

bem em diferentes condições e fornecer uma detecção confiável em cenários reais. Se houver erros
frequentes na detecção, considere ajustar o conjunto de dados de treinamento ou adicionar mais
exemplos para melhorar o desempenho.
2.6 Ensinar a IA a ser justa: o que é generalização?
A capacidade de generalização das Redes Neurais Convolucionais (CNNs) é um aspecto fundamental
que determina a eficácia de um modelo em aplicar o conhecimento adquirido durante o treinamento
a novos dados não vistos. Generalização refere-se à habilidade de um modelo para reconhecer
padrões e fazer predições precisas em dados que não foram usados durante o treinamento. Para
que uma CNN generalize bem, ela deve ser treinada com um conjunto de dados diversificado e
representativo das variações possíveis no ambiente de aplicação. Isso inclui diferentes ângulos,
iluminações, contextos e outras variáveis que podem afetar a aparência das imagens.
Uma CNN que generaliza bem pode ser aplicada em uma ampla gama de tarefas e condições, o
que é crucial para sua utilidade prática. Por exemplo, um modelo de detecção de máscaras faciais
que foi treinado com imagens de alta qualidade, capturadas em diferentes condições de luz e com
várias pessoas, será mais eficaz em identificar máscaras em situações do mundo real, onde as
condições podem variar significativamente. A capacidade de generalização reduz a necessidade de
re-treinamento frequente e permite que o modelo seja utilizado em diferentes cenários sem perda
significativa de precisão.
Para melhorar a capacidade de generalização de uma CNN, é comum utilizar técnicas como
aumento de dados (data augmentation), onde as imagens de treinamento são transformadas através
de rotações, flips, ajustes de brilho e outras modificações para simular variações no mundo real.
Além disso, a regularização, como dropout e penalização de pesos, ajuda a prevenir o overfitting, que
ocorre quando o modelo se torna muito especializado nos dados de treinamento e perde sua eficácia
em novos dados. Implementar estas técnicas durante o treinamento ajuda a desenvolver modelos
de CNN mais robustos e capazes de generalizar de maneira eficiente, garantindo seu desempenho
consistente em aplicações práticas diversificadas.
Vamos realizar uma classificação com uma imagem de outra pessoa com máscara utilizando um
arquivo de imagem em vez da webcam. Na Figura 2.15, vemos a interface de pré-visualização do
Teachable Machine, onde você pode alternar a fonte de entrada entre "Webcam"e "File". Para usar
um arquivo de imagem, clique na seta ao lado de "Webcam"e selecione "File"no menu suspenso.
Depois de selecionar "File", o botão "Switch Webcam"será substituído pela opção de carregar
um arquivo. Clique nessa nova opção e selecione a imagem que deseja utilizar para a classificação.
Isso é útil quando você tem imagens armazenadas em seu dispositivo e deseja testar o modelo
com essas imagens, garantindo que ele possa identificar corretamente se uma máscara está sendo
usada ou não.
A habilidade de alternar entre diferentes fontes de entrada permite testar o modelo de forma mais
abrangente e versátil. Além disso, você pode validar o desempenho do modelo com uma variedade
de imagens que não foram capturadas pela webcam, aumentando a confiança na capacidade de
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 29

DEEP LEARNING

generalização do modelo.
Após carregar a imagem, o modelo realizará a predição e você poderá visualizar os resultados na
mesma interface. Se o modelo foi treinado adequadamente com um conjunto de dados diversificado,
ele deve ser capaz de classificar corretamente a presença ou ausência de máscara na imagem
carregada. Isso demonstra a flexibilidade do Teachable Machine em lidar com diferentes tipos de
entrada e a utilidade prática do modelo em diversos cenários.
Após carregar uma imagem para a classificação, o Teachable Machine processa a entrada e
fornece a predição correspondente. Na Figura 2.16, vemos o resultado da classificação de uma
imagem importada, onde a pessoa está utilizando uma máscara. Para carregar a imagem, certifique-
se de que a entrada está ativada (Input ON) e a opção "File"está selecionada. Em seguida, escolha
a imagem clicando em "Choose images from your files, or drag and drop here"ou importe a partir do
Google Drive clicando em "Import images from Google Drive".
Uma vez que a imagem é carregada, a predição é exibida abaixo da imagem carregada. No
exemplo mostrado, o modelo identificou corretamente que a pessoa está usando uma máscara, com
uma confiança de 100% na classe "MASK"e uma confiança muito baixa na classe "NO-MASK". Este
resultado confirma que o modelo foi treinado corretamente e está funcionando conforme o esperado.
Este método de teste com arquivos de imagem permite validar a precisão e a robustez do modelo
em diferentes condições. Testar com uma variedade de imagens, incluindo diferentes tipos de
máscaras, ângulos e iluminações, é crucial para garantir que o modelo seja generalizável e confiável
em situações reais.
Após carregar uma imagem para a classificação, o Teachable Machine processa a entrada e
fornece a predição correspondente. Na Figura 2.16, vemos o resultado da classificação de uma
imagem importada, onde a pessoa está utilizando uma máscara. Para carregar a imagem, certifique-
se de que a entrada está ativada (Input ON) e a opção "File"está selecionada. Em seguida, escolha
a imagem clicando em "Choose images from your files, or drag and drop here"ou importe a partir do
Google Drive clicando em "Import images from Google Drive".
Uma vez que a imagem é carregada, a predição é exibida abaixo da imagem carregada. No
exemplo mostrado, o modelo identificou corretamente que a pessoa está usando uma máscara, com
uma confiança de 100% na classe "MASK"e uma confiança muito baixa na classe "NO-MASK". Este
resultado confirma que o modelo foi treinado corretamente e está funcionando conforme o esperado.
Este método de teste com arquivos de imagem permite validar a precisão e a robustez do modelo
em diferentes condições. Testar com uma variedade de imagens, incluindo diferentes tipos de
máscaras, ângulos e iluminações, é crucial para garantir que o modelo seja generalizável e confiável
em situações reais.
2.7 Salvando e exportando nossa invenção
A exportação do modelo é um passo crucial após o treinamento e validação do modelo no Teachable
Machine. Este processo permite que o modelo treinado seja utilizado fora do ambiente do Teachable
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 30

DEEP LEARNING

Machine, em aplicações do mundo real. Ao clicar no botão "Export Model", como mostrado na Figura
2.17, você inicia a exportação do modelo treinado para diferentes formatos.
Existem 3 formas de exportar o seu modelo treinado no Teachable Machine, como mostrado na
Figura 2.18. Cada uma dessas opções permite que você utilize o modelo em diferentes tipos de
projetos e plataformas. Vamos explorar cada uma delas para entender suas aplicações e benefícios.
A primeira opção é "TensorFlow.js". Clique nesta opção para exportar o modelo para ser utilizado
diretamente em aplicações web. TensorFlow.js permite que você execute modelos de aprendizado
de máquina diretamente no navegador, aproveitando o poder da GPU para acelerar a inferência.
Isso é ideal para criar aplicativos interativos que requerem processamento em tempo real sem a
necessidade de back-end poderoso.
A segunda opção é "TensorFlow". Selecionando esta opção, você exporta o modelo em um
formato que pode ser utilizado em ambientes de servidor e em máquinas de alto desempenho.
TensorFlow é uma biblioteca de aprendizado de máquina amplamente utilizada para construir e
treinar modelos complexos. Exportar para TensorFlow é ideal para integrar o modelo em sistemas
de produção que exigem uma alta capacidade de processamento e escalabilidade.
A terceira opção é "TensorFlow Lite". Clique nesta opção para exportar o modelo otimizado para
dispositivos móveis e sistemas embarcados. TensorFlow Lite é uma versão leve de TensorFlow,
projetada para rodar em dispositivos com recursos limitados, como smartphones, tablets e micro-
controladores. Isso permite que você implemente soluções de aprendizado de máquina eficientes e
rápidas em aplicações móveis e IoT.
Vamos começar baixando o modelo pelo TensorFlow.js para utilizá-lo em um projeto web. Na
Figura 2.19, vemos a interface de exportação do Teachable Machine, onde você pode baixar o
modelo treinado. Primeiro, selecione a opção "Download"para obter o arquivo do modelo no seu
dispositivo. Clique no botão "Download my model"para iniciar o download.
Após o download, você verá exemplos de snippets de código para utilizar seu modelo. Na
aba "Javascript", temos um exemplo de como integrar o modelo em uma aplicação web. Este
snippet inclui HTML e JavaScript que você pode copiar e colar no seu projeto. O HTML define uma
interface básica com um botão para iniciar a captura da webcam e áreas para exibir os resultados. O
JavaScript inclui as bibliotecas necessárias, como TensorFlow.js, e configurações para carregar e
utilizar o modelo exportado.
Clique no ícone de cópia no canto superior direito do snippet de código para copiar todo o
código. Em seguida, cole-o em seu editor de código no arquivo HTML ou JavaScript do seu projeto.
Certifique-se de ajustar o caminho do modelo exportado para corresponder ao local onde você
salvou os arquivos baixados. Este exemplo configurará sua webcam e usará o modelo para fazer
predições em tempo real.
Após configurar o código e garantir que todos os arquivos necessários estão no lugar, abra
o arquivo HTML em seu navegador. Clique no botão "Start"para iniciar a webcam e observar as
predições sendo feitas em tempo real com base no modelo treinado. Este processo demonstra como
é simples integrar modelos treinados no Teachable Machine em aplicações web, permitindo que
você aproveite o poder do aprendizado de máquina diretamente no navegador.
Descompacte o arquivo que você baixou do Teachable Machine nessa estrutura. O código
copiado do Teachable Machine deve estar dentro do arquivo ‘index.html‘. Você pode criar um arquivo
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 31

DEEP LEARNING

‘.txt‘, colar o código nesse arquivo e renomear a extensão do ‘.txt‘ para ‘.html‘.
Na Figura 2.20, podemos ver a estrutura do projeto que deve ser seguida. A pasta ‘my_model‘
contém três arquivos essenciais: ‘model.json‘, ‘metadata.json‘ e ‘weights.bin‘. Esses arquivos repre-
sentam o modelo treinado, suas metainformações e os pesos da rede neural, respectivamente. O
arquivo ‘index.html‘ deve estar localizado na raiz do diretório do projeto, ao lado da pasta ‘my_model‘.
Para configurar seu ambiente de desenvolvimento, certifique-se de que todos esses arquivos
estão organizados conforme mostrado na figura. Uma vez que tudo esteja no lugar, abra o arquivo
‘index.html‘ em um navegador da web. Se você seguir corretamente essas etapas, o modelo será
carregado e poderá ser utilizado para fazer predições em tempo real usando a webcam ou arquivos
de imagem.
Ao abrir o arquivo ‘index.html‘, o código JavaScript embutido nele carregará o modelo e configurará
a webcam. Isso permitirá que você teste o modelo diretamente no navegador, verificando se ele
está funcionando conforme esperado. Se houver qualquer erro ao carregar o modelo, verifique
os caminhos dos arquivos e a estrutura do diretório para garantir que tudo esteja configurado
corretamente.
2.8 Sua IA online - Servidor gratuito e sem programar
Agora vamos colocar nosso projeto on-line usando o replit.com. Na Figura 2.21, vemos a página
inicial do Replit, uma plataforma poderosa para desenvolvimento e implantação de software. Para
começar, clique no botão "Sign up for free"para criar uma conta, ou "Log in"se você já tiver uma
conta.
Para criar nosso projeto on-line, clique no botão "+ Create Repl", escolha "HTML, CSS, JS"como
o tipo do projeto, e forneça um título apropriado para o seu projeto. Na Figura 2.22, vemos a interface
do Replit para criar um novo repositório. Aqui, o título escolhido é "Detecção de Máscaras".
Certifique-se de que a opção "Public"esteja selecionada, para que qualquer pessoa possa
visualizar e fazer um fork do seu repositório. Isso é útil para compartilhar seu trabalho e permitir que
outros colaborem ou testem seu modelo. Se preferir, você pode optar pela versão privada, mas para
isso é necessário fazer o upgrade da conta.
Depois de preencher essas informações, clique no botão "Create Repl"para criar o seu repositório.
O Replit irá configurar um novo ambiente de desenvolvimento baseado nas tecnologias escolhidas,
e você será redirecionado para o editor onde poderá fazer upload dos seus arquivos e iniciar o
desenvolvimento.
Assim que o ambiente estiver pronto, faça upload do arquivo ‘index.html‘ e da pasta ‘my_model‘
para o repositório recém-criado. Certifique-se de que a estrutura dos diretórios está correta, conforme
discutido anteriormente. Com isso, seu projeto estará disponível on-line, e você poderá compartilhar
a URL gerada pelo Replit para que outros possam acessar e testar sua aplicação de detecção de
máscaras.
Envie os arquivos para o replit.com simplesmente clicando e arrastando do seu computador
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 32

DEEP LEARNING

para o explorer de arquivos do Replit. Na Figura 2.23, vemos a interface do Replit à esquerda e
a estrutura de diretórios no explorador de arquivos do computador à direita. Para iniciar, arraste a
pasta ‘my_model‘ e o arquivo ‘index.html‘ do seu computador para o painel de arquivos no Replit.
Certifique-se de que a estrutura dos arquivos no Replit corresponda à estrutura do seu projeto
local. Isso é crucial para que o caminho relativo dos arquivos funcione corretamente e o modelo
seja carregado sem problemas. Verifique se a pasta ‘my_model‘ contém os arquivos ‘model.json‘,
‘metadata.json‘, e ‘weights.bin‘, e se o arquivo ‘index.html‘ está na raiz do repositório.
Depois de arrastar e soltar os arquivos, o Replit fará o upload automaticamente e eles aparecerão
na lista de arquivos do seu projeto. Esse processo simplifica a transferência de arquivos e garante
que todo o necessário para o seu projeto esteja disponível on-line, facilitando a visualização e o
compartilhamento.
Com os arquivos carregados corretamente, você pode clicar no botão "Run"no Replit para iniciar
o servidor e testar seu modelo de detecção de máscaras diretamente no navegador. A URL gerada
pelo Replit permitirá que você acesse o projeto de qualquer lugar e compartilhe-o facilmente com
outras pessoas para demonstração e testes.
Clique duas vezes no arquivo ‘index.html‘ na lista de arquivos à esquerda para abri-lo no editor
do Replit. Em seguida, clique no botão verde "Run"na parte superior central da interface do Replit
para iniciar seu projeto, conforme mostrado na Figura 2.24.
Depois de clicar em "Run", você verá a interface do seu projeto carregada na aba "Webview"à
direita. Esta interface contém o título "Teachable Machine Image Model"e um botão "Start". Quando
você clica no botão "Start", o código JavaScript embutido no arquivo ‘index.html‘ será executado,
configurando a webcam e carregando o modelo de detecção de máscaras.
Certifique-se de que os arquivos necessários, incluindo o modelo e seus metadados, estejam
corretamente carregados na pasta ‘my_model‘. Isso garantirá que o modelo possa ser carregado e
utilizado pelo código JavaScript. Se tudo estiver configurado corretamente, o modelo começará a
fazer predições em tempo real usando a webcam ou arquivos de imagem.
Se houver algum problema, verifique o console do navegador (pressione ‘F12‘ ou ‘Ctrl+Shift+I‘ e
vá para a aba "Console") para identificar possíveis erros. Isso ajudará a depurar qualquer problema
com o carregamento do modelo ou configuração da webcam.
Como você pode ver, treinamos e colocamos a nossa rede neural disponível em um serviço na
internet sem a necessidade de programar. Na Figura 2.25, temos a visualização do projeto em
execução no Replit. Após clicar no botão "Start", o sistema ativa a webcam, captura a imagem e
processa a detecção da máscara em tempo real.
A interface mostra o título "Teachable Machine Image Model"e um botão "Start"que inicia a
captura de imagens pela webcam. Assim que o botão é clicado, a webcam captura a imagem e
o modelo treinado analisa se a pessoa está ou não usando máscara. Na imagem, a pessoa está
usando uma máscara e o modelo corretamente identifica isso, atribuindo uma probabilidade de 1.00
para a classe "MASK"e 0.00 para a classe "NO-MASK".
Clique no botão "Start"para ativar a webcam e veja os resultados em tempo real abaixo da imagem
capturada. O sistema usa a rede neural convolucional treinada para fazer predições baseadas nos
dados de entrada da webcam, mostrando as probabilidades das classes definidas. Isso demonstra a
eficiência do modelo em realizar a tarefa de classificação com alta precisão.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 33

DEEP LEARNING

O processo inteiro, desde o treinamento até a implementação on-line, foi feito de maneira intuitiva
e acessível graças às ferramentas fornecidas pelo Teachable Machine e Replit. Isso exemplifica
como a combinação dessas plataformas pode simplificar a criação e o compartilhamento de modelos
de deep learning, mesmo para aqueles que não possuem experiência em programação.
E se você solicitar ao ChatGPT, ele pode melhorar o design do seu serviço web baseado em
Deep Learning. Na Figura 2.26, vemos uma interface de usuário mais estilizada e informativa para o
detector de máscaras. Esta interface não só indica se uma máscara está presente, mas também
apresenta uma mensagem de status clara e estilizada.
Primeiramente, clique no botão "Start"para ativar a webcam e iniciar o processo de detecção. O
código JavaScript associado ao botão captura as imagens da webcam e faz predições em tempo real
usando o modelo treinado. Conforme as imagens são processadas, o sistema verifica a probabilidade
da classe ’mask’ e atualiza a interface do usuário com uma mensagem apropriada.
Se a probabilidade de detecção de máscara for maior que 0.5, a mensagem "Mask detected"será
exibida em verde, indicando que a pessoa na imagem está usando uma máscara. Caso contrário, a
mensagem "Mask not detected"será exibida em vermelho, indicando a ausência de máscara. Essas
mensagens são dinamicamente atualizadas com base nos resultados das predições do modelo.
Essa abordagem interativa e visualmente aprimorada torna o sistema de detecção de máscaras
mais intuitivo e fácil de usar, especialmente em aplicações onde o feedback visual imediato é crítico.
Ao seguir esses passos, você pode criar uma aplicação prática e eficaz para monitoramento e
controle de uso de máscaras em ambientes variados.
Conclusão
Nesse capítulo você aprendeu a criar, treinar e implementar um modelo de deep learning para
detecção de máscaras faciais usando ferramentas acessíveis como o Teachable Machine e o
Replit. Começamos explorando o Teachable Machine, uma plataforma que permite criar modelos de
machine learning sem necessidade de programação. Através de exemplos práticos, vimos como
capturar e rotular imagens para treinar um modelo de rede neural convolucional.
Em seguida, discutimos a importância da qualidade das imagens para o treinamento eficaz de
um modelo de CNN. Abordamos aspectos como variação de ângulos, iluminação e diversidade de
exemplos, que são cruciais para a capacidade de generalização do modelo. Isso assegura que
o modelo possa realizar predições precisas em situações reais, fora do ambiente controlado de
treinamento.
Você também aprendeu a implementar o modelo treinado em um ambiente on-line usando o
Replit. Este passo envolveu a criação de um novo projeto no Replit, a organização correta dos
arquivos do modelo e a configuração de um servidor web para testar e compartilhar o projeto. Esse
processo demonstrou como as ferramentas modernas podem simplificar a implantação de modelos
de deep learning, tornando-os acessíveis para um público mais amplo.
Por fim, discutimos como melhorar a interface do usuário para tornar a aplicação mais intuitiva e
informativa. Ao estilizar a interface e fornecer feedback visual claro sobre as predições do modelo,
criamos um sistema que é não apenas funcional, mas também fácil de usar. Este capítulo forneceu
uma visão completa de todo o ciclo de desenvolvimento de um projeto de deep learning, desde a
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 34

DEEP LEARNING

coleta de dados até a implementação final, capacitando você a criar suas próprias aplicações de
machine learning de forma eficaz e acessível.
2.9 Vamos praticar com alguns exercícios
Coleta de Dados: Crie um projeto de classificação de imagens no Teachable Machine para
identificar gestos de mão correspondentes a "Pedra", "Papel"e "Tesoura". Capture pelo menos
50 amostras de imagens para cada classe. Documente o processo de coleta de dados e
discuta a importância de capturar uma variedade de ângulos e iluminações para cada gesto.
Treinamento de Modelo: Usando as amostras coletadas, treine um modelo de Rede Neural
Convolucional (CNN) no Teachable Machine. Descreva as etapas do treinamento e explique
como o modelo aprende a reconhecer os diferentes gestos de mão. Inclua capturas de tela do
processo de treinamento e dos resultados obtidos.
Teste de Modelo: Teste o modelo treinado com imagens de gestos que não foram usadas du-
rante o treinamento. Avalie a precisão do modelo e discuta quaisquer dificuldades encontradas
durante o teste. Inclua capturas de tela das predições do modelo e os valores de confiança.
Exportação e Implementação: Exporte o modelo treinado para TensorFlow.js e implemente-o
em um projeto web no Replit. Documente os passos necessários para configurar o ambiente
de desenvolvimento e fazer o upload dos arquivos. Inclua o código HTML e JavaScript utilizado
para carregar e usar o modelo.
Interatividade e Design: Melhore a interface do usuário para o jogo "Pedra, Papel e Te-
soura"no projeto web. Adicione elementos interativos que permitem ao usuário jogar contra o
modelo, como botões para iniciar o jogo e mostrar o resultado. Estilize a interface para torná-la
mais atraente e fácil de usar. Documente as mudanças feitas e inclua capturas de tela antes e
depois das melhorias.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 35

DEEP LEARNING

Figura 2.13: Interface de pré-visualização para testar o modelo treinado no Teachable Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 36

DEEP LEARNING

Figura 2.14: Interface de pré-visualização com detecção de máscara no Teachable Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 37

DEEP LEARNING

Figura 2.15: Interface para selecionar a fonte de entrada no Teachable Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 38

DEEP LEARNING

Figura 2.16: Interface de pré-visualização mostrando o resultado da classificação de uma imagem
carregada no Teachable Machine.
Figura 2.17: Interface para exportar o modelo treinado no Teachable Machine.
Figura 2.18: Opções de exportação do modelo no Teachable Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 39

DEEP LEARNING

Figura 2.19: Interface de exportação do modelo no Teachable Machine com exemplos de snippets
de código.
Figura 2.20: Estrutura de diretório do projeto para carregar e utilizar o modelo treinado do Teachable
Machine.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 40

DEEP LEARNING

Figura 2.21: Página inicial do Replit, uma plataforma para desenvolvimento e implantação de
software.
Figura 2.22: Interface do Replit para criar um novo repositório para o projeto de detecção de
máscaras.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 41

DEEP LEARNING

Figura 2.23: Envio de arquivos para o Replit arrastando do explorador de arquivos do computador
para o explorer do Replit.
Figura 2.24: Interface do Replit mostrando o arquivo ‘index.html‘ no editor e a visualização da web
após clicar em "Run".
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 42

DEEP LEARNING

Figura 2.25: Resultado da execução do modelo de detecção de máscaras no Replit usando a
webcam para capturar imagens em tempo real.
Figura 2.26: Interface estilizada para o detector de máscaras utilizando Teachable Machine e Replit.
CAPÍTULO 2. IA SEM PROGRAMAR – SIM, É VERDADE! 43

DEEP LEARNING

CAPÍTULO 3
3 Inteligência Artificial Visual
OOrange Canvasé uma inovação significativa no campo da Inteligência Artificial (IA), principalmente
devido à sua abordagem inovadora que permite a criação e experimentação com IA através de uma
programação visual. Com uma interface gráfica intuitiva, essa ferramenta possibilita que usuários,
independentemente de sua formação em computação, construam complexos fluxos de trabalho
de análise de dados simplesmente arrastando e soltando componentes visuais conhecidos como
widgets. Este capítulo apresenta os conceitos fundamentais doOrange Canvas, destacando como
ele serve como um elo entre o complexo mundo da IA e aqueles que desejam explorá-lo sem a
barreira da codificação tradicional.
A programação visual, núcleo doOrange Canvas, é uma abordagem que substitui a sintaxe
de programação convencional por elementos gráficos. Essa metodologia não apenas simplifica a
compreensão dos processos de IA, mas também promove a experimentação e a aprendizagem por
meio de uma interação direta e imediata com dados e algoritmos. Ao oferecer uma vasta biblioteca de
widgets que abrangem desde o pré-processamento de dados até técnicas avançadas de modelagem
e avaliação, oOrange Canvasdemocratiza o acesso às tecnologias de IA, tornando-as acessíveis a
educadores, estudantes e profissionais de diversas áreas.
A relevância doOrange Canvasvai além de sua acessibilidade, residindo também em sua
capacidade de fornecer uma compreensão visual das operações de IA. A representação gráfica
dos fluxos de dados e a visualização interativa dos resultados permitem aos usuários obter insights
profundos sobre os dados e modelos de IA de uma forma que a programação textual muitas vezes
não consegue. Esse aspecto visual e interativo é especialmente valioso no ensino e na aprendizagem
de conceitos de IA, onde a abstração e a complexidade podem rapidamente se tornar barreiras
significativas.
Para aqueles fora do campo da computação, oOrange Canvasoferece uma entrada menos
intimidadora para o mundo da IA. Educadores podem, por exemplo, integrar oOrangeem seus
currículos para proporcionar experiências práticas de IA sem a necessidade de ensinar ou aprender
uma linguagem de programação complexa. Da mesma forma, profissionais em áreas como biologia,
marketing e finanças podem utilizar oOrangepara analisar dados e tomar decisões baseadas em
informações sem depender de especialistas em dados ou desenvolvedores de software.
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 44

DEEP LEARNING

Ao longo deste capítulo, exploraremos detalhadamente as funcionalidades doOrange Canvas,
mostrando como sua abordagem de programação visual não apenas facilita, mas também amplia o
entendimento e a aplicação da IA na área de visão computacional. Destacaremos como oOrange
pode ser usado para criar soluções inovadoras de IA, com exemplos práticos e estudos de caso que
demonstram seu impacto em diversas áreas. O objetivo é demonstrar que, com ferramentas como
oOrange Canvas, a IA não é apenas uma possibilidade técnica, mas também uma oportunidade
expansiva para uma ampla gama de usuários.
3.1 O poder milagroso dos widgets. IA no Orange Canvas
A instalação doOrange Canvasé essencial para começar a utilizar a programação visual no campo
da inteligência artificial. Este processo foi projetado para ser fácil e acessível, garantindo que
usuários de qualquer nível de habilidade técnica possam explorar as capacidades doOrangesem
demora. A seguir, apresentaremos um guia passo a passo para instalar oOrange Canvasem
seu computador, cobrindo os requisitos do sistema e as etapas necessárias para uma instalação
bem-sucedida.
Requisitos do Sistema
Antes de iniciar a instalação, certifique-se de que seu sistema atende aos requisitos mínimos para
executar oOrange Canvas. Embora oOrangeseja uma ferramenta relativamente leve, garantir a
compatibilidade do sistema ajudará a evitar problemas durante a instalação e o uso. Os requisitos
básicos incluem:
Sistema operacional: Windows, macOS ou Linux.
Memória: Pelo menos 4GB de RAM.
Espaço em disco: Pelo menos 500MB de espaço livre.
Python: Algumas versões doOrangepodem ser instaladas via Python, exigindo Python 3.6 ou
superior.
Site do Orange
O site doOrange Data Miningé um portal completo para tudo relacionado aoOrange Canvas, uma
ferramenta de código aberto para aprendizado de máquina e visualização de dados.
Site: https://orangedatamining.com←Clique no link para acessar
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 45

DEEP LEARNING

O site enfatiza a principal vantagem doOrange, que é a programação visual, permitindo que os
usuários organizem widgets na tela, conectem-nos e carreguem seus conjuntos de dados para obter
insights sem a necessidade de codificação. Além de oferecer opções de download para as versões
mais recentes doOrange, o site também fornece recursos valiosos como exemplos, documentação
detalhada, blogs com atualizações regulares e informações sobre workshops. Esse conjunto de
recursos torna oOrangenão apenas uma ferramenta poderosa para especialistas em dados, mas
também uma excelente plataforma educacional para ensinar mineração de dados e visualização,
conforme destacado por depoimentos de profissionais e acadêmicos de diversas áreas. Além disso,
o site convida a comunidade a contribuir para o desenvolvimento e manutenção doOrange, seja
através de doações ou participação direta no projeto.
Instalação no Windows
Para usuários do Windows, oOrangepode ser instalado utilizando o instalador executável disponível
no site oficial doOrange. Siga estas etapas:
Acesse o site oficial doOrangee navegue até a seção de download.
Baixe o instalador doOrangepara Windows.
Execute o instalador e siga as instruções na tela para completar a instalação.
Após a conclusão, você pode iniciar oOrange Canvasa partir do menu Iniciar.
Instalação no macOS
Usuários de macOS podem instalar oOrangeutilizando o pacote disponível no site oficial ou através
do gerenciador de pacotesHomebrew. Para a instalação direta:
Visite o site oficial doOrangee baixe o pacote de instalação para macOS.
Abra o arquivo baixado e arraste o ícone doOrangepara a pasta de Aplicativos.
Inicie oOrange Canvasa partir da pasta de Aplicativos.
Para instalação viaHomebrew:
Abra o Terminal.
2.Digite o comando: brew install –cask orange3e pressione Enter. Note que são dois
sinais de menos juntos - -, é que na compilação do livro o compilador juntou os caracteres.
Aguarde a conclusão da instalação e inicie oOrangea partir do Launchpad.
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 46

DEEP LEARNING

Instalação no Linux
Para usuários de Linux, oOrange Canvaspode ser instalado via linha de comando usandopip, o
gerenciador de pacotes do Python. Este método é geralmente preferido por usuários com alguma
experiência em terminal. Os comandos a seguir realizarão a instalação:
Abra o terminal.
2.Certifique-se de que o Python e o pip estão instalados executando:python3 –versionepip3
–version. Note que são dois sinais de menos juntos - -.
Instale oOrangecom o comando:pip3 install orange3.
4.Após a instalação, você pode iniciar oOrange Canvasdigitando:orange-canvasno terminal.
Uma característica notável doOrange Canvasé sua utilização doMiniconda, uma versão
minimalista doAnacondaque fornece um ambiente Python simples e eficiente, ideal para criadores
de Inteligência Artificial e cientistas de dados. OMinicondavem com o gerenciador de pacotesconda,
facilitando a instalação e o gerenciamento de pacotes e dependências necessárias para oOrange
funcionar de maneira otimizada. Essa escolha reflete o compromisso doOrangecom a facilidade de
uso e acessibilidade, permitindo que mesmo aqueles com pouca experiência em gerenciamento de
ambientes de desenvolvimento possam configurar e começar a utilizar a ferramenta rapidamente. A
integração com oMinicondaassegura uma instalação mais leve e menos propensa a conflitos de
pacotes, tornando oOrangeuma opção robusta para a exploração visual de dados e aprendizado
de máquina.
Após a instalação, você estará pronto para começar a explorar as funcionalidades doOrange
Canvas, criando fluxos de trabalho visuais para análise de dados e desenvolvimento de modelos de
IA. Lembre-se de que a comunidadeOrangee a documentação oficial são ótimos recursos caso
você encontre dificuldades ou tenha dúvidas durante a instalação ou o uso da ferramenta.
3.2 Adicionando superpoderes de visão ao Orange
O add-on Image Analytics do Orange Canvas é uma extensão potente dedicada à análise e pro-
cessamento de imagens utilizando Redes Neurais Convolucionais. Este módulo incorpora uma
série de widgets especializados que permitem aos usuários executar tarefas desde a importação e
pré-processamento de imagens até o treinamento de modelos de machine learning para atividades
como classificação de imagens e detecção de objetos. Com interfaces intuitivas e uma abordagem
de arrastar e soltar, o add-on torna o campo complexo da visão computacional acessível mesmo
para aqueles sem grande conhecimento em programação, abrindo novas possibilidades para a
exploração visual de dados dentro do ambiente Orange. A Figura 3.1 ilustra como instalar o add-on
Image Analytics.
A Figura 3.2 mostra o painel Image Analytics do Orange Canvas, que inclui widgets projetados
para otimizar o trabalho com imagens:
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 47

DEEP LEARNING

Figura 3.1: Como instalar o add-on Image Analytics
Import Images: Facilita a importação de imagens de um ou mais diretórios, permitindo que o
usuário carregue rapidamente seu conjunto de dados visual no ambiente Orange.
Image Viewer: Um visualizador que exibe as imagens associadas a um conjunto de dados,
possibilitando a inspeção individual de cada imagem de maneira conveniente.
Image Embedding: Utiliza redes neurais profundas para criar uma representação vetorial das
imagens, transformando dados visuais em um formato que pode ser analisado e processado
eficientemente.
Image Grid: Apresenta as imagens em uma grade de similaridade, facilitando a comparação
visual e a identificação de padrões ou anomalias entre as imagens.
Save Images: Permite salvar as imagens processadas na estrutura de diretórios, essencial
para manter a organização do projeto e para futuras análises.
Figura 3.2: Painel Image Analytics
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 48

DEEP LEARNING

Cada um desses widgets desempenha um papel crucial no fluxo de trabalho de análise de
imagem, desde a fase inicial de importação até o salvamento e organização de imagens processadas,
demonstrando a amplitude e a praticidade do add-on Image Analytics.
3.3 Doutor e IA, eu estou bem?
Em 27 de março de 2020, onze dias após o início do primeiro Lockdown no Brasil, realizei uma
transmissão ao vivo no YouTube para demonstrar uma técnica de detecção de COVID-19 utilizando
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
de imagens: train e validation (Figura 3.3. A "train"servirá para treinar nossa inteligência artificial e a
"validation"servirá para realizar predições.
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 49

DEEP LEARNING

Figura 3.3: Pastas de imagens do dataset Covid-19
Carregando as Imagens de Raio-X
O processo de carregamento de imagens para análise é feito pelo widget “Import Images”. Esse
widget é essencial para dar o primeiro passo em qualquer projeto de visão computacional no Orange,
possibilitando a importação de conjuntos de imagens diretamente do sistema de arquivos do usuário.
A Figura 3.4 ilustra essa etapa inicial, destacando a ação de importar imagens e indicando ao usuário
a necessidade de clicar no widget “Import Images” para prosseguir.
O primeiro passo para começar seu projeto de visão computacional é o uso do widget “Import
Images”. Esse widget permite que você importe conjuntos de imagens de seu sistema de arquivos
de forma simples e eficaz. A Figura 3.4 mostra como iniciar este processo, destacando o widget
“Import Images” e indicando que você deve clicar nele para prosseguir.
Uma vez selecionado o widget, uma janela de diálogo aparecerá, permitindo que você navegue
pelos seus diretórios até encontrar e selecionar o local específico das imagens a serem trabalhadas.
No nosso exemplo, você deve escolher a pasta “train” do dataset de Covid-19, que contém imagens
de radiografias classificadas em categorias, que utilizaremos para treinar modelos demachine
learningna detecção do vírus. A informação na interface do widget “1200 images / 2 categories”
confirma a seleção correta do conjunto de dados, mostrando que você tem disponível um total de
1200 imagens divididas em duas categorias para análise.
Figura 3.4: Processo de carregamento de imagens de radiografia no Orange Canvas para análise de
detecção de Covid-19.
Após importar as imagens utilizando o widgetImport Images, o próximo passo consiste em
visualizar e analisar os dados das imagens importadas. Para isso, é necessário conectar o widget
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 50

DEEP LEARNING

Import ImagesaoData Table, processo ilustrado na Figura 3.5. Esta conexão permite examinar
detalhadamente as informações associadas a cada imagem importada.
OData Tableapresenta várias colunas, tais comocategory,image name,image,size,width, e
height. Estas colunas fornecem informações valiosas sobre cada imagem, incluindo a categoria
da imagem (por exemplo,covidpara imagens de pacientes com Covid-19), o nome da imagem, o
caminho do arquivo, o tamanho do arquivo em bytes, além da largura e altura da imagem em pixels.
A visualização desses dados é crucial para entender melhor o conjunto de imagens com o qual se
está trabalhando, facilitando a preparação para etapas subsequentes de análise e modelagem no
Orange Canvas.
Figura 3.5: Visualizando os dados das imagens importadas no Orange Canvas.
Este procedimento assegura que as imagens importadas estejam corretamente organizadas
e categorizadas, permitindo também uma inspeção inicial que pode revelar a necessidade de
pré-processamento adicional antes de prosseguir para análises mais complexas.
Image Viewer
Depois de visualizar e analisar os dados das imagens importadas, é possível visualizar as próprias
imagens no Orange Canvas utilizando o widgetImage Viewer. Conecte o widgetData Tableao
Image Viewerpara exibir as imagens importadas, como demonstrado na Figura 3.6. Este widget
permite que você veja as imagens diretamente, facilitando a avaliação visual das características
relevantes para a sua análise.
NoImage Viewer, as imagens são apresentadas em miniaturas, permitindo uma rápida inspeção
visual. Você pode ajustar atributos comoImage Filename AttributeeTitle Attributepara controlar
quais informações são exibidas juntamente com as imagens. No nosso exemplo, selecionamos o
atributocategorycomo o título para cada imagem, permitindo identificar rapidamente a categoria de
cada caso, neste caso, imagens relacionadas a pacientes diagnosticados com Covid-19.
OImage Vieweré uma ferramenta poderosa para a inspeção visual do seu conjunto de dados
de imagens, facilitando a identificação de padrões ou características específicas que podem ser
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 51

DEEP LEARNING

importantes para as etapas subsequentes de análise ou modelagem.
Figura 3.6: Utilizando oImage Viewerno Orange Canvas para visualizar as imagens importadas.
3.4 Embeddings: A assinatura da IA em cartório
Embeddings são como assinaturas em cartório das IAs, tanto para imagens quanto para textos.
Assim como uma assinatura em cartório autentica e valida a identidade de uma pessoa em um
documento legal, os embeddings autenticam e validam a identidade de palavras, frases e imagens
no mundo digital das inteligências artificiais.
Quando você leva um documento ao cartório, a assinatura é comparada com a assinatura
registrada para verificar sua autenticidade. De maneira semelhante, quando uma IA encontra uma
nova palavra, frase ou imagem, ela compara o embedding dessa entidade com os embeddings
previamente conhecidos para entender seu significado e contexto. Essa comparação permite à IA
discernir entre itens semelhantes e diferentes, garantindo precisão na compreensão e na resposta.
Para textos, os embeddings capturam a essência e as características de palavras e frases em
um espaço de alta dimensão, representando relações semânticas e contextuais. Por exemplo, os
embeddings ajudam a IA a reconhecer que "rei"e "rainha"estão relacionados, enquanto "cão"e
"gato"são diferentes, apesar de ambos serem animais de estimação. Eles permitem que a IA
compreenda nuances e contextos, assim como uma assinatura única captura a identidade individual
de uma pessoa.
No caso de imagens, os embeddings funcionam de maneira semelhante, mas em um espaço
visual. Eles capturam características visuais como formas, cores e texturas, representando a
identidade visual de uma imagem. Assim, uma IA pode reconhecer que duas fotos de um gato são
de gatos, mesmo que os gatos sejam de raças diferentes ou estejam em posições diferentes. Os
embeddings visuais permitem à IA identificar objetos, cenas e até emoções capturadas nas imagens,
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 52

DEEP LEARNING

garantindo uma compreensão profunda do conteúdo visual.
Além disso, assim como uma assinatura é única e difícil de falsificar, os embeddings são projeta-
dos para serem únicos e representarem fielmente as nuances do significado e das características
visuais. Cada dimensão em um vetor de embeddings captura uma característica específica, tornando
essa representação rica e detalhada. Para imagens, isso pode incluir desde a textura do pelo de
um animal até a cor do céu em uma paisagem, enquanto para textos, isso pode incluir desde o
significado de uma palavra até seu uso em diferentes contextos.
Embeddingsde imagens representam uma técnica avançada na visão computacional e no apren-
dizado de máquina, transformando imagens em vetores de números de alta dimensão. Esses vetores
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
de imagens, busca por similaridade de imagens e até mesmo geração de imagens. A Figura 3.7
apresenta todo o processo de geração de Embeddings por uma CNN, nesse caso especifico a
InceptionV3.
Figura 3.7: Como uma CNN gera Embeddings
A utilização de embeddings de imagens permite uma compreensão mais profunda e nuanciada do
conteúdo visual, superando os desafios associados à grande variabilidade das imagens. Por exemplo,
duas imagens do mesmo objeto podem variar significativamente em termos de iluminação, escala,
ou perspectiva. Os embeddings ajudam a minimizar essas diferenças, destacando as características
essenciais que definem a semelhança entre as imagens. Isso torna os embeddings uma ferramenta
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 53

DEEP LEARNING

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
numéricas compactas e informativas.
Figura 3.8: Escolha um Embedder de acordo com suas necessidades.
A seleção do modelo deembedderno widgetImage Embeddingdo Orange Canvas oferece
várias opções, cada uma com suas características e aplicações específicas como mostra a Figura
3.8. Aqui está uma lista dos modelos disponíveis e suas respectivas funções:
Inception v3 : Desenvolvido pela Google, o Inception v3 é um modelo de rede neural con-
volucional treinado no ImageNet. É conhecido por seu equilíbrio entre precisão e eficiência
computacional. Este modelo é amplamente utilizado para tarefas de classificação e detecção
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 54

DEEP LEARNING

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
como classificação. A Figura 3.9 ilustra como os embeddings podem ser avaliados conectando o
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
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL^55

DEEP LEARNING

de imagens. Ele permite que os usuários do Orange Canvas ajustem e otimizem suas análises
para alcançar os melhores resultados possíveis, dependendo do conjunto de dados e do problema
específico em questão.
Figura 3.9: Avaliação de embeddings de imagens utilizando o widgetTest and Scoreconectado a
uma Rede Neural no Orange Canvas.
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL 56

DEEP LEARNING

3.5 Mais exercícios para não perder o ritmo
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
CAPÍTULO 3. INTELIGÊNCIA ARTIFICIAL VISUAL^57

DEEP LEARNING

CAPÍTULO 4
4 O grande olho que tudo vê!
Imagine que você está em um museu de arte repleto de pinturas detalhadas e complexas. Para
apreciar plenamente cada obra, você não observa a pintura como um todo de uma só vez, mas sim,
percorre meticulosamente cada parte dela, analisando detalhes específicos como as pinceladas,
cores e texturas.
As Redes Neurais Convolucionais (CNNs) funcionam de maneira similar. Pense nas camadas
de uma CNN como guias especializados que percorrem a obra de arte em seções pequenas e
manejáveis. Cada guia tem uma função específica: um pode focar em identificar contornos e linhas
básicas, outro pode estar atento a formas e padrões mais complexos, enquanto um terceiro pode se
concentrar em cores e texturas.
No início, os guias mais simples examinam pequenos detalhes sem tentar entender a imagem
completa. Eles identificam bordas e formas básicas. Conforme avançamos para os guias mais
sofisticados, eles começam a juntar esses detalhes básicos para formar componentes mais com-
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 58

DEEP LEARNING

plexos. No final da visita, os guias combinam todas essas observações detalhadas para criar uma
compreensão completa e detalhada da pintura.
Assim como esses guias colaboram para proporcionar uma apreciação completa da obra de arte,
as camadas de uma CNN colaboram para entender e identificar objetos dentro de uma imagem.
Cada camada convolucional realiza uma análise detalhada e específica de diferentes aspectos da
imagem, e ao final, a rede neural combina todas essas análises para reconhecer padrões complexos
e tomar decisões precisas sobre o conteúdo da imagem.
Essa abordagem permite que as CNNs sejam extremamente eficazes em tarefas de visão
computacional, como reconhecimento de objetos, classificação de imagens e detecção de caracte-
rísticas específicas, assim como uma visita guiada ao museu permite uma compreensão profunda e
detalhada de uma obra de arte complexa.
4.1 A revolução da convolução
Imagine que você está tentando resolver um quebra-cabeça, mas em vez de ter todas as peças em
frente a você, você só pode ver uma pequena janela do quebra-cabeça de cada vez. Você move
essa janela sobre o quebra-cabeça, seccionando pequenas áreas para examinar, uma por uma. À
medida que avança, você identifica onde cada peça deve ir, baseando-se nos pequenos detalhes
visíveis através da janela.
A convolução em redes neurais convolucionais (CNNs) funciona de maneira semelhante. Pense
na janela como um filtro ou kernel que se move sobre a imagem, analisando pequenas porções
dela de cada vez. Esse filtro é programado para identificar características específicas, como bordas,
texturas ou padrões.
Cada vez que o filtro passa por uma seção da imagem, ele realiza uma operação matemática
que compara os pixels da imagem com os valores do filtro. O resultado dessa operação é um valor
que representa a presença e a intensidade da característica que o filtro está procurando naquela
seção específica da imagem.
Assim como no quebra-cabeça, onde você move a janela sobre diferentes partes para juntar a
imagem completa, a convolução envolve mover o filtro sobre toda a imagem, seção por seção. O
resultado final é um mapa de características que mostra onde e quão fortemente as características
procuradas estão presentes na imagem.
Esse processo permite que a rede neural detecte padrões e detalhes em uma imagem de
forma eficiente, mesmo que esses padrões estejam em diferentes posições ou orientações. Assim
como resolver um quebra-cabeça peça por peça, a convolução permite que a rede construa uma
compreensão detalhada e precisa da imagem, parte por parte.
As redes neurais convolucionais usam essa operação que permite entender uma imagem olhando
para partes dela. Por exemplo, um carro. O carro é formado por várias partes distintas, como
espelhos, faróis e rodas. A imagem à esquerda na Figura 4.1 mostra várias partes do carro sendo
destacadas em diferentes caixas coloridas, com especial atenção às caixas verdes que envolvem os
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 59

DEEP LEARNING

espelhos.
Clique na imagem do Orange e observe que mesmo quando olhamos apenas para os espelhos
(caixas verdes), ainda conseguimos entender que estamos vendo um carro. Isso ocorre porque
a rede neural pode extrair características relevantes dessas pequenas partes. Quando essas
características são combinadas, a rede consegue formar uma compreensão completa da imagem
original.
Portanto, a capacidade de analisar partes específicas da imagem é fundamental para que as
redes neurais possam identificar e compreender objetos complexos como um carro, mesmo quando
vistos por partes.
Figura 4.1: Exemplo de análise de partes específicas de uma imagem de um carro.
A convolução é como uma lupa. Veja o caso da tentativa de entender que letra está na imagem.
Estamos vendo que é um "X"e que, para entender isso, é feita uma convolução usando várias
"lupas"conhecidas como kernels em toda a imagem. Na Figura 4.2, a imagem original de um "X"é
processada por uma máscara específica (kernel) que procura pela diagonal do "X"ou parte dela. O
kernel mostrado na figura é uma matriz 3x3 com valores específicos: 1 nas diagonais principais e
− 1 nas demais posições. Esse kernel é movido através da imagem original, e em cada posição, é
realizada uma multiplicação elemento por elemento seguida de uma soma dos produtos. O resultado
desta operação para uma dada posição é mostrado destacado em verde na imagem.
No caso destacado, o kernel está centrado em uma posição da imagem original onde há uma
correspondência perfeita com a diagonal do "X". Portanto, a soma dos produtos para essa posição
resulta em um valor alto, indicando a presença da característica procurada (a diagonal do "X"). Esse
processo é repetido para cada posição da imagem, gerando uma nova matriz (imagem de saída)
que destaca as áreas onde a diagonal do "X"está presente.
Na Figura 4.3, apresentamos o processo de convolução utilizando uma máscara específica e
uma imagem. Inicialmente, observe a máscara destacada em verde na imagem à na parte 1. Esta
máscara realiza uma multiplicação ponto-a-ponto com a imagem, iniciando pelo canto superior
esquerdo. Cada elemento da máscara é multiplicado pelo elemento correspondente da imagem.
Por exemplo, na posição inicial, o elemento 1 na máscara multiplica o elemento 1 na imagem,
resultando em 1. Este processo é repetido para cada posição da máscara, conforme destacado em
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 60

DEEP LEARNING

Figura 4.2: Convolução de uma máscara (kernel) com a imagem original de um "X"procurando a
diagonal do "X"ou parte do "X".
verde na imagem.
Após completar a multiplicação ponto-a-ponto desde a primeira posição acima até a última de
cima para baixo e da esqueda para direita, soma-se os resultados dessas multiplicações, conforme
mostrado na parte 2. da figura. A soma total para essa posição específica da máscara é 9 , e quando
calculamos a média, obtemos o valor 1.
Desta forma, podemos dizer que a máscara encontrou um "match"completo nesta posição da
imagem, resultando em uma média de convolução de 1. A etapa seguinte consiste em deslocar a
máscara sobre a imagem e repetir o processo para todas as posições possíveis.
Figura 4.3: Processo de convolução de uma máscara sobre uma imagem.
Depois disso, o resultado da convolução desse trecho da convolução é armazenado em uma nova
imagem no ponto central correspondente onde foi aplicado a convolução. Na Figura 4.4, ilustramos
este processo com mais detalhes. Comece observando o retângulo verde na imagem à esquerda,
onde a máscara realiza a multiplicação ponto-a-ponto. Cada elemento da máscara é multiplicado
pelo elemento correspondente da imagem, e os resultados dessas multiplicações são somados.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 61

DEEP LEARNING

Como mostrado no centro da figura, temos a soma1+1+1+1+1+1+1+1+1 = 9. Dividindo
essa soma pelo número de elementos da máscara, que é 9, obtemos a média igual a 1. Este valor
resultante é então armazenado na nova imagem, no ponto central correspondente à posição onde a
convolução foi realizada.
Observe a imagem à direita na figura, onde o valor 1.0 é armazenado na nova imagem, desta-
cando o resultado da convolução. Este procedimento é repetido para todas as posições possíveis da
máscara sobre a imagem original, gerando assim a nova imagem convoluída.
Figura 4.4: Armazenamento do resultado da convolução em uma nova imagem.
Aplicando a mesma máscara em outro ponto da imagem, nesse caso no centro da imagem,
perceba que o "match"não foi perfeito. Isso ocorre porque somente 55% do padrão da máscara foi
encontrado aqui. Na Figura 4.5, observamos a máscara destacada em verde aplicada no centro da
imagem. O processo de multiplicação ponto-a-ponto é realizado novamente, resultando na soma
dos produtos individuais.
Note que, nesta posição, temos valores positivos e negativos na soma, como 1 −1 + 1−1 +
1 + 1 + 1 + 1 + 1. A soma total é 5, e ao calcular a média, obtemos0.55. Este resultado indica
que a correspondência da máscara com a região da imagem não foi perfeita, refletindo uma menor
similaridade entre o padrão da máscara e a imagem.
Este valor resultante é então armazenado na nova imagem, no ponto central correspondente.
Esse procedimento de aplicar a máscara em diferentes pontos da imagem ajuda a identificar e
destacar padrões específicos em várias regiões da imagem original.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 62

DEEP LEARNING

Figura 4.5: Aplicação da máscara no centro da imagem e cálculo da média.
Quando aplicamos toda a máscara na imagem original, obtivemos uma nova imagem onde toda
a diagonal principal do nosso "X"foi encontrado. Na Figura 4.6, podemos ver o resultado desse
processo. A imagem à esquerda mostra a aplicação da máscara em diferentes posições na imagem
original, destacadas em verde. Esta máscara realiza uma multiplicação ponto-a-ponto com a imagem
para cada posição, conforme ilustrado.
Os valores resultantes dessas multiplicações são somados e, em seguida, a média é calculada
para cada posição. Os resultados dessas médias são então armazenados na nova imagem, que
é apresentada à direita na figura. Esta nova imagem mostra a correspondência da máscara
com diferentes regiões da imagem original. Os valores altos, como 1.00 e 0.77, indicam uma
correspondência forte com o padrão da máscara, enquanto os valores baixos, como -0.11, indicam
uma correspondência fraca.
Este processo de convolução é essencial para identificar padrões específicos na imagem original,
permitindo a detecção de características como bordas, texturas e formas.
Figura 4.6: Aplicação completa da máscara na imagem original e obtenção da nova imagem
convoluída.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 63

DEEP LEARNING

4.2 Mapas da mina. Mapas de ativação
Os mapas de ativação são componentes essenciais na interpretação e compreensão das redes
neurais convolucionais (CNNs), oferecendo uma analogia interessante com mapas de mina. Imagine
que uma rede neural convolucional é como um minerador buscando ouro em uma vasta área.
Os mapas de ativação funcionam como os mapas de uma mina, destacando as regiões onde as
características mais valiosas estão localizadas.
Quando uma imagem é processada por uma CNN, diferentes camadas da rede extraem variados
níveis de abstração. As camadas iniciais podem detectar bordas e texturas simples, assim como um
minerador pode identificar sinais superficiais de ouro. Conforme avançamos para camadas mais
profundas, a rede começa a reconhecer padrões mais complexos e formas específicas, similar a
como um minerador mais experiente pode encontrar veios ricos de ouro com base em sinais mais
sutis e profundos. Os mapas de ativação, assim como os mapas da mina, mostram onde estão
concentradas as ativações mais importantes, ou seja, onde a rede encontrou "ouro".
Os mapas de ativação são gerados passando uma imagem através de convoluções. Quanto mais
intensa for a ativação, maior é a contribuição dessa região da imagem para a decisão do modelo,
similar a áreas de alta concentração de ouro no mapa de uma mina. Da mesma forma que os
mineradores ajustam suas estratégias com base nas informações do mapa, engenheiros e cientistas
de dados usam os mapas de ativação para ajustar e melhorar a performance da rede. Eles podem
identificar se a rede está focando nas partes corretas da imagem ou se está sendo desviada por
ruídos ou padrões irrelevantes.
As imagens em verde claro, laranja e rosa são os mapas de ativação provenientes da convolução
entre 3 máscaras para encontrar o "X"na imagem original. Na Figura 4.7, podemos observar como
diferentes partes do "X"são detectadas por diferentes máscaras, cada uma destacando um aspecto
específico do padrão.
A primeira máscara, destacada em verde claro, foca em partes específicas da imagem, resultando
em um mapa de ativação que evidencia as áreas onde a presença do "X"é mais forte. Clique na
imagem para ver como a máscara se aplica sobre a imagem original e observe o mapa resultante à
direita. Este mapa mostra valores altos nas regiões onde a máscara encontrou correspondências
significativas, representando a presença do padrão "X".
Da mesma forma, as máscaras laranja e rosa aplicam-se à imagem original para gerar seus
respectivos mapas de ativação. Cada uma dessas máscaras captura diferentes aspectos do "X",
contribuindo para uma visão composta e mais robusta do padrão. Se faltar alguma parte em uma
das máscaras, como indicado na imagem laranja, ainda será possível identificar um "X", mas com
uma probabilidade menor. Isso se deve à contribuição combinada das diferentes máscaras, que
juntas reforçam a presença do padrão, mesmo que individualmente possam não ser perfeitas.
Veja que em cada mapa de ativação, diferentes partes do "X"são identificadas, ilustrando como
a máquina vê e processa a imagem. Este processo é análogo a utilizar várias ferramentas de
mineração para mapear um terreno em busca de ouro; cada ferramenta pode destacar diferentes
veios, e a combinação dessas informações proporciona uma visão completa da mina. No caso dos
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 64

DEEP LEARNING

mapas de ativação, a combinação dos resultados de diferentes máscaras permite uma detecção
mais precisa e confiável do padrão desejado.
A figura também ilustra como a máquina ainda pode reconhecer o "X"mesmo quando uma parte
está ausente, embora com menor confiança. Isso é crítico para a robustez do modelo, pois em
situações reais, partes da imagem podem estar obstruídas ou distorcidas. Assim como um mapa de
mina que ainda mostra uma concentração de ouro mesmo que alguns veios sejam menos acessíveis,
os mapas de ativação permitem que a rede neural mantenha a capacidade de reconhecer padrões
importantes, aumentando a eficácia e confiabilidade do modelo.
Figura 4.7: Mapas de ativação gerados a partir da aplicação de três máscaras diferentes para
detectar o padrão "X"na imagem original.
4.3 Ativando sua rede com ReLU
Imagine uma porta automática em um supermercado que só abre quando detecta alguém se
aproximando. Essa porta, no mundo das redes neurais, é como a ReLU (Rectified Linear Unit).
Assim como a porta permite a entrada de clientes e bloqueia a passagem quando não há movimento,
a ReLU permite que valores positivos passem enquanto bloqueia os negativos, ajustando o fluxo de
informação na rede neural de forma eficiente e eficaz.
A ReLU é amplamente utilizada devido à sua capacidade de introduzir não linearidade nos mode-
los de deep learning. Isso é crucial porque permite que as redes neurais aprendam e representem
padrões complexos, algo que funções de ativação lineares não conseguem fazer. A simplicidade da
ReLU também contribui para sua popularidade, pois facilita o treinamento de redes neurais profundas
ao mesmo tempo que mantém a eficiência computacional.
Uma das grandes vantagens da ReLU é a sua capacidade de mitigar o problema do gradiente
desaparecido, que afeta outras funções de ativação como a sigmoide ou a tangente hiperbólica.
Durante o processo de treinamento, a ReLU ajuda a manter gradientes significativos, permitindo uma
propagação eficaz do erro e acelerando a convergência do modelo. Isso é especialmente importante
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 65

DEEP LEARNING

em redes neurais com muitas camadas, onde a preservação de gradientes úteis é essencial para o
sucesso do treinamento.
Na Figura 4.8, temos uma ilustração clara do efeito da função de ativação ReLU (Rectified Linear
Unit) em um mapa de ativação. Primeiramente, observe o mapa de ativação original à esquerda,
onde temos uma matriz de valores que variam entre positivos e negativos. A aplicação da ReLU,
como mostrado no mapa à direita, transforma todos os valores negativos em zero, enquanto mantém
os valores positivos inalterados.
Para entender isso, considere cada célula do mapa de ativação como uma porta automática que só
permite a passagem de valores positivos. Quando um valor negativo tenta passar, a porta permanece
fechada, bloqueando-o, enquanto valores positivos passam livremente. Essa transformação é crucial,
pois ajuda a rede neural a ignorar informações irrelevantes (valores negativos) e focar apenas nos
dados significativos (valores positivos).
Vamos nos concentrar nos elementos destacados em verde. Note como valores negativos como
-0.11 e -0.33 desaparecem no mapa de ativação resultante. Por outro lado, valores positivos como
0.77, 1.00, e 0.55 permanecem inalterados. Esse processo é visualizado pela função f(x) = max(0, x)
no centro da figura, indicando que a saída da ReLU é o máximo entre zero e o valor de entrada.
Para reforçar a compreensão, faça um exercício prático: pegue uma matriz de valores, aplique a
função ReLU manualmente, e observe os resultados. Isso consolidará a compreensão de como a
ReLU atua como uma porta seletiva no processamento de informações da rede neural.
Figura 4.8: Quando aplicamos ReLU, todos os valores negativos somem do mapa de ativação.
4.4 Pooling: o que realmente importa e deixando o resto de lado
Imagine que você está olhando para uma pintura detalhada e decide focar apenas nas partes mais
importantes para entender a essência da obra. Esse processo de simplificação e concentração
nas partes essenciais é semelhante ao que o pooling faz em redes neurais convolucionais (CNNs).
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 66

DEEP LEARNING

Pooling é uma técnica que reduz a dimensionalidade dos mapas de ativação, preservando as
características mais significativas e, ao mesmo tempo, diminuindo a complexidade computacional.
Existem diferentes tipos de pooling, sendo os mais comuns o max pooling e o average pooling.
No max pooling, a técnica seleciona o valor máximo dentro de uma região específica do mapa de
ativação, destacando as características mais fortes. Por exemplo, se considerarmos uma janela 2x2
em uma imagem, o valor máximo dentro dessa janela é escolhido e movido para o novo mapa de
ativação reduzido. Isso ajuda a enfatizar os elementos mais proeminentes, como bordas e texturas,
essencialmente resumindo a imagem em suas partes mais importantes.
O average pooling, por outro lado, adota uma abordagem mais equilibrada, calculando a média
dos valores em uma região da imagem. Isso resulta em uma representação mais suave e generali-
zada dos dados. Embora menos utilizado que o max pooling, o average pooling pode ser vantajoso
em situações onde é desejável atenuar variações e ruídos, fornecendo uma visão mais uniforme das
características presentes na imagem.
Ambas as técnicas de pooling têm suas vantagens e são escolhidas com base nas necessidades
específicas da tarefa e do conjunto de dados. O max pooling é frequentemente preferido para
realçar características salientes, enquanto o average pooling pode ser mais adequado para contextos
que requerem uma abordagem mais equilibrada. Em última análise, o pooling desempenha um
papel crucial na simplificação das representações em redes neurais convolucionais, tornando o
processamento mais eficiente e a extração de características mais robusta.
Aplicamos um pooling de máximo nos mapas de ativação que passaram pela ReLU, como
ilustrado na Figura 4.9. No lado esquerdo, temos um mapa de ativação pós-ReLU, onde valores
negativos foram zerados, deixando apenas valores positivos. Este mapa de ativação contém um
padrão, um "X", que queremos preservar enquanto reduzimos a dimensionalidade dos dados.
No centro da figura, vemos o processo de pooling de máximo com uma janela 2x2. Para cada
região 2x2 do mapa de ativação, selecionamos o valor máximo. Esta operação é visualizada pela
seta e o círculo central, indicando que estamos extraindo o valor mais alto de cada pequena região.
Este procedimento é repetido para toda a matriz, resultando no mapa de ativação reduzido à direita.
Observe atentamente os elementos destacados em verde no mapa de ativação original. Esses
valores representam as características mais importantes que serão preservadas após o pooling
de máximo. Por exemplo, veja que valores como 1.00, 0.77 e 0.55 estão presentes tanto no mapa
original quanto no reduzido. Isso ocorre porque esses valores são os máximos dentro de suas
respectivas regiões 2x2, garantindo que as informações mais salientes do padrão "X"sejam mantidas
na imagem reduzida.
Faça um exercício para consolidar este conceito: pegue uma matriz de valores e aplique o pooling
de máximo manualmente. Divida a matriz em blocos 2x2, selecione o valor máximo de cada bloco e
forme uma nova matriz com esses valores. Este processo ajudará a compreender como o pooling de
máximo contribui para reduzir a quantidade de dados enquanto preserva as características mais
importantes, melhorando o desempenho da rede neural.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 67

DEEP LEARNING

Figura 4.9: Pooling de máximo deixa somente as informações mais importantes do mapa de ativação
e reduz a quantidade de dados, melhorando o desempenho da rede. Veja que parte do "X"ainda
está na imagem reduzida.
4.5 Flatten: A IA adora comida achatada como uma pizza
Imagine que você está na cozinha preparando uma pizza. Inicialmente, a massa está em uma bola
compacta, cheia de potencial, mas precisa ser achatada para se transformar em uma pizza. Esse
processo de achatar a massa para criar uma base plana e uniforme é semelhante ao flattening em
redes neurais. Flattening é a técnica usada para converter uma matriz multidimensional em um
vetor unidimensional, preparando os dados para serem processados por camadas densas nas redes
neurais.
Nas redes neurais convolucionais, as camadas iniciais operam em matrizes multidimensionais,
que preservam a estrutura espacial dos dados de entrada, como imagens. Essas matrizes são
ricas em informações, assim como a bola de massa é rica em potencial. No entanto, para que
a rede neural possa realizar tarefas de classificação ou decisão, é necessário transformar esses
dados em um formato que possa ser utilizado pelas camadas densas. É aqui que o flattening entra,
transformando a matriz complexa em um vetor unidimensional, da mesma forma que você achata a
massa de pizza para criar uma base uniforme e pronta para receber os ingredientes.
Esse processo é essencial para a integração das diferentes etapas da rede neural. As camadas
convolucionais extraem características importantes dos dados, enquanto as camadas densas utilizam
essas características para fazer previsões. Achatar a matriz de ativação em um vetor unidimensional,
assim como achatar a massa da pizza, facilita a transição e garante que todas as características
extraídas estejam disponíveis para as camadas densas. Isso permite que a rede neural use todas as
informações relevantes de maneira eficiente.
Além de facilitar a transição entre camadas, o flattening mantém a continuidade dos dados,
assegurando que nenhuma informação importante seja perdida durante o processo. Assim como
uma base de pizza bem achatada permite uma distribuição uniforme dos ingredientes, um vetor
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 68

DEEP LEARNING

unidimensional bem estruturado permite que a rede neural utilize plenamente as características
extraídas, otimizando o desempenho nas tarefas de previsão e classificação. Este passo simples,
porém crucial, assegura que a rede neural funcione de maneira eficaz, aproveitando ao máximo os
dados disponíveis.
Na Figura 4.10, vemos o processo de flattening aplicado a um mapa de ativação resultante de
uma operação de pooling. Esse processo é essencial para preparar os dados para as camadas
densas de uma rede neural. Observe a imagem de pooling à direita, onde temos uma matriz 4x4
destacada em verde. Cada célula desta matriz contém um valor representando uma característica
extraída das camadas anteriores da rede.
Para que essas informações possam ser utilizadas em camadas totalmente conectadas, pre-
cisamos transformar essa matriz multidimensional em um vetor unidimensional. Esse processo é
conhecido como flattening. Na figura, a seta vermelha indica o achatamento da matriz original em
um único vetor contínuo. Veja como as linhas da matriz são reformatadas em uma sequência linear
de valores.
Quando você acha a matriz de ativação, você está essencialmente alinhando todos os dados
em uma única dimensão. Isso é comparável a pegar uma pilha de livros e organizá-los em uma fila,
permitindo um acesso mais simples e eficiente aos conteúdos de cada livro. Após o achatamento,
cada valor na matriz original está presente no vetor resultante, preservando todas as informações
importantes.
Esses vetores resultantes do flattening são conhecidos como embeddings, conforme destacado
em verde. Esses embeddings são fundamentais para a etapa subsequente de processamento
na rede neural, onde as camadas densas utilizam esses dados lineares para realizar tarefas de
classificação ou previsão. Clique e experimente criar uma matriz de exemplo e aplique o processo
de flattening manualmente para ver como as informações são reorganizadas.
Figura 4.10: Quando a gente achata os mapas de ativação, temos 1 único vetor que representa a
imagem original. Esse vetor é conhecido como embeddings.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 69

DEEP LEARNING

4.6 Os neurônios da visão por IA
uma rede de estradas complexas onde cada cidade está conectada a todas as outras cidades por
vias diretas. Este é um bom paralelo para entender uma rede neural densa. Em uma rede neural
densa, ou totalmente conectada, cada neurônio em uma camada está diretamente ligado a todos
os neurônios da camada seguinte, garantindo que a informação possa fluir livremente e de forma
abrangente através da rede.
Em termos de estrutura, uma rede neural densa é composta por várias camadas de neurônios,
onde cada camada é chamada de camada densa. Cada neurônio em uma camada recebe entradas
de todos os neurônios da camada anterior, realiza uma computação (geralmente uma soma pon-
derada seguida por uma função de ativação), e passa a saída para todos os neurônios da próxima
camada. Essa conectividade total permite que a rede aprenda representações complexas dos dados,
combinando múltiplos aspectos das entradas para tomar decisões precisas.
A principal vantagem de uma rede neural densa é sua capacidade de generalização. Assim como
em nossa analogia das estradas, onde cada cidade pode ser alcançada a partir de qualquer outra
cidade, uma rede neural densa pode capturar e combinar informações de todas as partes dos dados
de entrada. Isso é especialmente útil em tarefas de classificação, onde a rede precisa considerar
múltiplas características e suas interações para determinar a categoria correta de uma entrada.
Na Figura 4.11, vemos uma representação clara de como uma rede neural densa opera após o
processo de flattening. À esquerda, temos os embeddings, que são o vetor unidimensional resultante
do flattening dos mapas de ativação. Esses embeddings contêm todas as informações extraídas
pelas camadas convolucionais e de pooling.
As bolas na imagem representam neurônios artificiais. As bolas azuis são neurônios da camada
densa intermediária, e a bola verde é o neurônio da camada de saída. Cada neurônio na camada
densa está conectado a todos os valores dos embeddings, conforme indicado pelas numerosas
linhas brancas que ligam cada neurônio aos elementos do vetor. Isso ilustra a natureza totalmente
conectada da camada, onde cada neurônio recebe a informação completa dos dados de entrada.
Após o processamento na camada densa, os sinais são transmitidos para a camada de saída,
destacada em verde. Esta camada final é responsável por fazer a classificação final com base nas
informações processadas pelas camadas anteriores. Na figura, vemos que a saída determina que a
imagem é um ’X’, exemplificando como a rede neural processa os dados e chega a uma conclusão.
Clique e examine atentamente como cada parte da rede está interligada. Escreva suas observa-
ções sobre como os valores dos embeddings se conectam a cada neurônio da camada densa, e
como esses neurônios, por sua vez, influenciam a camada de saída. Este entendimento é crucial
para compreender como redes neurais densas utilizam informações de maneira integrada para
realizar classificações precisas.
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 70

DEEP LEARNING

Figura 4.11: Os embeddings são processados pela camada densa, que então influencia a camada
de saída para fazer a classificação final.
4.7 Camada de saída: Sim, entendi o que eu vi
A camada de saída é a etapa final em uma rede neural, onde a decisão final é tomada com base
nos dados processados pelas camadas anteriores. Essa camada é crucial, pois é responsável por
transformar as representações internas da rede em uma previsão ou classificação compreensível. A
camada de saída pode ser configurada de várias maneiras, dependendo do tipo de problema que a
rede neural está tentando resolver.
Em problemas de classificação, a camada de saída geralmente utiliza a função de ativação
softmax. A função softmax transforma os valores de saída dos neurônios da camada anterior em
probabilidades, permitindo que a rede faça uma previsão clara sobre a classe a que pertence a
entrada. Por exemplo, em um problema de classificação de imagens, a camada de saída produzirá
um vetor de probabilidades, onde cada elemento do vetor representa a probabilidade da imagem
pertencer a uma determinada classe.
Para problemas de regressão, a camada de saída geralmente não aplica uma função de ativação
ou utiliza uma função linear. Isso ocorre porque a rede precisa prever um valor contínuo em vez de
uma classe discreta. Nesses casos, a saída é diretamente o valor numérico predito pela rede, como
a previsão de preços de casas ou valores de séries temporais.
A configuração da camada de saída deve sempre ser adequada ao tipo de problema que a rede
está resolvendo. Clique e explore diferentes configurações de camadas de saída para entender como
elas afetam a performance da rede. Escreva suas observações sobre como a função de ativação
escolhida na camada de saída influencia os resultados finais da rede. Em resumo, a camada de
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 71

DEEP LEARNING

saída é onde a rede neural comunica a sua "compreensão"dos dados de entrada. Ao traduzir as
representações internas complexas em resultados práticos, a camada de saída desempenha um
papel vital na eficácia das redes neurais. Com a configuração correta, ela permite que a rede faça
previsões precisas e úteis, concluindo o processo de deep learning com sucesso. E é assim que as
redes convolucionais conseguem ver o mundo ao seu redor.
As redes neurais convolucionais (CNNs) têm uma ampla gama de aplicações que transformaram
diversos campos da tecnologia e da ciência. Uma das áreas mais impactadas é a visão computacio-
nal, onde CNNs são utilizadas para tarefas como reconhecimento de imagens, detecção de objetos,
e segmentação de imagens, sendo fundamentais em aplicações como sistemas de segurança,
veículos autônomos, e diagnósticos médicos por imagem. Além disso, CNNs são aplicadas em
processamento de vídeo para análise de movimento e reconhecimento de atividades, bem como
em processamento de linguagem natural para tarefas como análise de sentimentos e tradução
automática. Essas redes também encontram uso em áreas emergentes como geração de arte e
música, demonstração de sua versatilidade e poder na modelagem de dados complexos e variados.
4.8 Vamos praticar
1.Explique a diferença entre convolução e pooling em redes neurais convolucionais. Use
exemplos para ilustrar como cada técnica contribui para o processamento de uma imagem.
2.Descreva o papel da função de ativação ReLU em uma rede neural convolucional. Por que a
ReLU é preferida em muitas arquiteturas de deep learning?
3.O que é flattening em redes neurais convolucionais e por que é um passo crucial antes de
aplicar camadas densas? Dê um exemplo prático de como isso é feito.
4.Como a camada de saída de uma rede neural é configurada para problemas de classificação
versus problemas de regressão? Explique com exemplos.
5.Discuta as principais aplicações das redes neurais convolucionais (CNNs). Como as CNNs
revolucionaram o campo da visão computacional?
CAPÍTULO 4. O GRANDE OLHO QUE TUDO VÊ! 72

DEEP LEARNING

CAPÍTULO 5
5 Aventuras com IA nas Nuvens Gratuitas
Gratuitas
A inteligência artificial (IA) moderna é um campo dinâmico e em rápida evolução, que se baseia em
três pilares fundamentais: a disponibilidade de grandes volumes de dados, algoritmos avançados
de deep learning e o uso de programação paralela com GPUs (Unidades de Processamento
Gráfico). Esses elementos, trabalhando em sinergia, possibilitaram avanços significativos em várias
aplicações, desde reconhecimento de voz e imagem até tradução automática e veículos autônomos.
A confluência dessas tecnologias tem permitido que a IA alcance níveis de desempenho e eficiência
antes inimagináveis.
A disponibilidade de dados é o primeiro pilar essencial para o desenvolvimento da IA moderna.
Com o advento da internet e a proliferação de dispositivos conectados, a quantidade de dados
gerados cresceu exponencialmente. Esses dados, quando adequadamente coletados e processados,
fornecem a matéria-prima necessária para treinar algoritmos de aprendizado profundo. Bases de
dados como ImageNet, COCO e muitas outras tornaram-se recursos indispensáveis para a pesquisa
e desenvolvimento em visão computacional, permitindo que os modelos aprendam com uma vasta
diversidade de exemplos do mundo real.
O segundo pilar, os algoritmos de deep learning, revolucionou a maneira como abordamos proble-
mas complexos de IA. Redes neurais profundas, com suas arquiteturas complexas e capacidade de
aprender representações hierárquicas dos dados, têm superado métodos tradicionais em diversas
tarefas. Modelos como CNNs (Redes Neurais Convolucionais) para visão computacional, RNNs
(Redes Neurais Recorrentes) e suas variantes para processamento de linguagem natural, e GANs
(Redes Adversariais Generativas) para geração de dados sintéticos são apenas alguns exemplos
das inovações que têm impulsionado o campo.
A programação paralela usando GPUs constitui o terceiro pilar, proporcionando o poder de
processamento necessário para treinar redes neurais profundas de maneira eficiente. As GPUs,
originalmente desenvolvidas para processamento gráfico em jogos, revelaram-se extremamente efi-
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 73

DEEP LEARNING

cazes em executar operações matriciais e vetoriais, que são a base do treinamento de redes neurais.
Ferramentas como CUDA e bibliotecas como cuDNN permitiram que pesquisadores e engenheiros
aproveitassem a capacidade de paralelismo massivo das GPUs, reduzindo significativamente o
tempo de treinamento dos modelos.
A combinação desses três elementos – dados, algoritmos e GPUs – criou um ambiente propício
para a inovação e avanço contínuo na IA. A acessibilidade a dados públicos e o desenvolvimento
de frameworks de deep learning como TensorFlow, PyTorch e Keras democratizaram o acesso
à tecnologia, permitindo que um número cada vez maior de pesquisadores e desenvolvedores
contribuam para o campo. Além disso, o surgimento de plataformas que oferecem acesso gratuito a
GPUs, como Google Colab, Kaggle Kernels e outras, tem facilitado ainda mais o desenvolvimento e
experimentação em IA.
Assim, o cenário atual da IA é caracterizado por uma interconexão entre dados abundantes,
algoritmos poderosos e hardware eficiente. Esta combinação não só acelera a pesquisa e a aplicação
da IA, mas também expande os horizontes do que é possível realizar com essas tecnologias. No
próximo segmento, exploraremos como configurar e aproveitar um ambiente de IA com acesso
gratuito a GPUs, permitindo que você possa começar a desenvolver e treinar seus próprios modelos
de deep learning sem a necessidade de investimentos significativos em infraestrutura.
5.1 A arena gratuita de treinamento de IA
O Google Colab, também conhecido como Google Colaboratory, é uma plataforma gratuita fornecida
pelo Google que permite a execução de código Python diretamente no navegador. Uma de suas mai-
ores vantagens é o acesso gratuito a GPUs, facilitando o desenvolvimento e a experimentação com
modelos de deep learning sem a necessidade de hardware local potente. O Colab é particularmente
útil para pesquisadores, estudantes e profissionais que desejam treinar modelos complexos de IA,
mas não possuem acesso a recursos computacionais avançados.
Uma das características mais atrativas do Google Colab é sua integração com o Google Drive,
permitindo fácil armazenamento e compartilhamento de notebooks. Usuários podem importar e
exportar notebooks em formato Jupyter, executar códigos em tempo real e colaborar com outros
de forma síncrona, semelhante ao funcionamento de outros serviços do Google, como Google
Docs. Essa funcionalidade colaborativa é especialmente útil para projetos de equipe e para o
compartilhamento de resultados de pesquisa.
Além de suportar a execução de código em CPUs, o Google Colab oferece suporte a GPUs
NVIDIA e TPUs (Tensor Processing Units) para acelerar o treinamento de modelos de deep learning.
A plataforma é equipada com as bibliotecas mais populares de aprendizado de máquina e deep
learning, como TensorFlow, Keras e PyTorch, prontas para uso imediato. Isso permite que os
usuários iniciem seus projetos sem a necessidade de configurar o ambiente, economizando tempo e
esforço.
Outra vantagem significativa do Google Colab é sua comunidade ativa e extensa base de recursos
e tutoriais. Desde documentações detalhadas a notebooks de exemplo e fóruns de discussão, os
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 74

DEEP LEARNING

usuários têm acesso a uma vasta gama de materiais de apoio. Esses recursos tornam o Colab
uma ferramenta educativa poderosa, permitindo que iniciantes aprendam e experimentem com deep
learning de forma prática e interativa. Para usuários avançados, o Colab oferece um ambiente flexível
para prototipagem rápida e experimentação com novos algoritmos e arquiteturas.
Criando um Colab
Vamos então criar um Colab diretamente a partir do Google Drive. Esse método é prático e eficiente
para organizar e acessar seus projetos de deep learning. A imagem abaixo mostra o processo de
criação de um novo notebook do Google Colab dentro do Google Drive.
Primeiro, acesse seu Google Drive e certifique-se de que está logado na conta correta. No canto
superior esquerdo, clique no botão "Novo", destacado em verde na imagem. Isso abrirá um menu
suspenso com várias opções de criação de arquivos. Em seguida, passe o cursor sobre a opção
"Mais"na parte inferior desse menu, que também está destacada em verde. Isso abrirá um novo
submenu com opções adicionais.
Dentro desse submenu, você verá várias ferramentas adicionais que podem ser integradas ao
Google Drive. Clique na opção "Google Colaboratory", destacada em verde na imagem. Ao fazer
isso, um novo notebook Colab será criado e aberto em uma nova aba do seu navegador, permitindo
que você comece a escrever e executar seu código Python imediatamente.
O uso do Google Drive para criar e armazenar seus notebooks do Colab oferece benefícios
significativos, incluindo salvamento automático, fácil acesso e compartilhamento colaborativo. Cada
notebook criado desta forma estará automaticamente salvo no seu Drive, permitindo que você
continue seu trabalho de onde parou e compartilhe facilmente com outros colaboradores.
Quando você abrir seu Colab, comece renomeando seu notebook para algo que descreva
claramente o projeto em que você está trabalhando. Isso ajudará a manter seus arquivos organizados
e facilmente identificáveis no futuro. Na imagem abaixo, você pode ver a interface do Google Colab
logo após a criação de um novo notebook.
Para renomear o notebook, clique no nome padrão do arquivo, que inicialmente será algo
como "Untitled0.ipynb", destacado em verde na imagem. Ao clicar no nome, uma caixa de texto
editável aparecerá, permitindo que você digite um novo nome para o seu notebook. Digite um nome
descritivo que reflete o conteúdo ou o objetivo do projeto, como "Análise de Imagens com CNN"ou
"Classificação de Dados com Redes Neurais".
Renomear seus notebooks é uma prática recomendada, especialmente quando você trabalha com
múltiplos projetos ou colabora com outros profissionais. Isso facilita a localização e a identificação
rápida dos arquivos relevantes, além de ajudar a manter seu Google Drive organizado.
Lembre-se de que as alterações no nome do arquivo são salvas automaticamente no Google
Drive, portanto, não há necessidade de se preocupar em salvar manualmente. Este é mais um
benefício de utilizar o Google Colab integrado com o Google Drive, garantindo que todas as suas
modificações sejam registradas em tempo real e estejam sempre acessíveis.
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS^75

DEEP LEARNING

Figura 5.1: Criando um novo notebook Colab a partir do Google Drive
5.2 Uma GPU grátis só pra mim? Que Maravilhoso!
Vamos configurar uma GPU gratuita para você treinar sua rede neural convolucional no Google
Colab. A imagem abaixo mostra como selecionar uma GPU T4 como acelerador de hardware no seu
notebook Colab, o que pode acelerar significativamente o processo de treinamento do seu modelo
de deep learning.
Primeiro, clique no menu "Editar"no topo da interface do Google Colab, destacado em vermelho
na imagem. Isso abrirá um menu suspenso com várias opções. Desça até a parte inferior desse
menu e selecione "Configurações de notebook", também destacada em vermelho. Essa ação abrirá
uma janela de configurações específicas para o notebook atual.
Na janela de configurações, procure pela seção "Acelerador de hardware". Aqui, você terá várias
opções para escolher. Selecione "T4 GPU", destacada em vermelho, para configurar o seu notebook
para usar uma GPU T4. Utilizar uma GPU permitirá que você execute operações de treinamento de
deep learning de maneira muito mais rápida do que se estivesse usando apenas a CPU.
Além disso, marque a opção "Executar automaticamente a primeira célula ou seção em qualquer
execução", também destacada em vermelho. Esta configuração garante que a primeira célula do
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 76

DEEP LEARNING

Figura 5.2: Renomeando um notebook no Google Colab
seu notebook seja executada automaticamente sempre que o notebook for iniciado, o que pode ser
útil para inicializações repetidas e configurações de ambiente.
Após fazer essas seleções, clique no botão "Salvar"para aplicar as configurações. Seu notebook
agora estará configurado para usar uma GPU T4, proporcionando um ambiente otimizado para o
desenvolvimento e treinamento de modelos de deep learning.
Figura 5.3: Configurando uma GPU T4 no Google Colab
O Google Colab executa o código em unidades chamadas células. As células podem conter
código ou texto, e você pode executá-las independentemente umas das outras. Isso permite uma
forma interativa e flexível de desenvolver e testar o seu código, especialmente útil em projetos de
deep learning onde experimentações e ajustes são frequentes.
Para executar uma célula de código, simplesmente clique na célula desejada e pressione "Shift
+ Enter"ou clique no ícone de reprodução à esquerda da célula. O resultado da execução será
mostrado imediatamente abaixo da célula. Você pode modificar o código e executá-lo novamente
quantas vezes precisar, permitindo iterar rapidamente sobre suas ideias.
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS^77

DEEP LEARNING

Células de texto, por outro lado, são usadas para adicionar documentação, comentários e
explicações sobre o código. Essas células utilizam a sintaxe Markdown, que permite a formatação
de texto com cabeçalhos, listas, links, imagens e outros elementos de formatação. Isso ajuda a
manter o notebook bem documentado e fácil de entender, tanto para você quanto para qualquer
colaborador.
A execução por células é uma característica poderosa do Google Colab, pois permite que você
divida seu trabalho em partes menores e mais gerenciáveis. Você pode, por exemplo, ter células
separadas para carregar dados, pré-processar esses dados, definir e treinar um modelo de deep
learning, e avaliar o desempenho do modelo. Isso facilita o desenvolvimento modular e a depuração
de código, além de proporcionar um fluxo de trabalho organizado e eficiente.
Verificando a GPU
Escreva o comando ‘!nvidia-smi‘ na primeira célula e execute-a pressionando "Shift + Enter". Este
comando é utilizado para verificar o status da GPU disponível no ambiente do Google Colab. A
imagem abaixo mostra a saída do comando ‘!nvidia-smi‘, que fornece diversas informações sobre a
GPU configurada para o seu notebook.
Na saída do comando, você pode ver que a GPU disponível é uma Tesla T4, destacada em verde.
Esta informação é crucial para entender o tipo de hardware que você está utilizando para treinar
seus modelos de deep learning. Além do nome da GPU, você pode ver a temperatura atual da
GPU (59°C) e o uso de energia (10W/70W), indicando a eficiência térmica e o consumo de energia
durante a execução.
Outros detalhes importantes incluem a memória disponível e utilizada pela GPU. No caso da
Tesla T4, a memória total é de 15360 MiB, com 0 MiB em uso no momento da captura, destacada em
verde. Isso indica que a GPU está pronta para ser utilizada no treinamento do seu modelo. Monitorar
o uso da memória GPU é essencial para garantir que seus modelos não excedam a capacidade
disponível, o que pode causar erros durante a execução.
5.3 Vários processos de uma vez? Sim, por favor! DEEP LEARNING
Para entender a importância da computação paralela na inteligência artificial, imagine que você está
em uma biblioteca enorme, tentando encontrar um livro específico. Se você estivesse sozinho, teria
que percorrer cada corredor e cada estante, o que poderia levar horas. No entanto, se você tivesse
uma equipe de pessoas ajudando, cada uma procurando em uma seção diferente, a tarefa seria
concluída muito mais rapidamente. Essa é a essência da computação paralela: dividir uma grande
tarefa em várias pequenas tarefas que podem ser executadas simultaneamente.
Na computação, a computação paralela funciona de maneira semelhante. Em vez de um único
processador realizar todas as operações sequencialmente, várias unidades de processamento
trabalham ao mesmo tempo em diferentes partes de uma tarefa. Isso é especialmente útil em
inteligência artificial e aprendizado profundo, onde as operações envolvem grandes volumes de
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 78

DEEP LEARNING

Figura 5.4: Saída do comando ‘!nvidia-smi‘ no Google Colab
dados e cálculos complexos. Com a computação paralela, essas tarefas podem ser concluídas em
uma fração do tempo que levariam em um ambiente de processamento sequencial.
A importância da computação paralela se torna ainda mais evidente quando consideramos o
treinamento de modelos de deep learning. Esses modelos frequentemente requerem a execução
de milhões de operações matemáticas, que podem ser extremamente demoradas se realizadas
de maneira sequencial. Ao dividir essas operações entre múltiplos processadores, o tempo de
treinamento é significativamente reduzido, permitindo que os modelos sejam treinados de maneira
mais eficiente e em menor tempo.
A tecnologia que permite a computação paralela na inteligência artificial é, em grande parte,
baseada no uso de GPUs (Unidades de Processamento Gráfico). Originalmente desenvolvidas para
renderização gráfica em jogos, as GPUs possuem centenas ou até milhares de núcleos pequenos
que podem executar operações simultaneamente. Essa arquitetura as torna ideais para as tarefas
intensivas em cálculos necessários no treinamento de redes neurais profundas.
Uma GPU pode realizar muitas operações em paralelo, como multiplicações e somas de matrizes,
que são fundamentais nos algoritmos de aprendizado profundo. Frameworks de deep learning, como
TensorFlow e PyTorch, são projetados para tirar proveito dessa capacidade de paralelismo massivo.
Eles distribuem automaticamente as operações de treinamento entre os núcleos da GPU, otimizando
o uso do hardware disponível.
Além das GPUs, outras tecnologias também desempenham um papel importante na computação
paralela para IA. As TPUs (Unidades de Processamento de Tensor), desenvolvidas pelo Google, são
projetadas especificamente para cargas de trabalho de aprendizado profundo. Elas oferecem ainda
mais eficiência para operações de treinamento e inferência de modelos, tornando-se uma alternativa
poderosa às GPUs em certos contextos.
A computação paralela não se limita apenas ao hardware. Softwares e algoritmos também
precisam ser projetados para aproveitar o paralelismo. Isso inclui a divisão de tarefas em subtarefas
que podem ser executadas independentemente e a coordenação entre essas tarefas para garantir
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 79

DEEP LEARNING

resultados precisos. Ferramentas de computação paralela e bibliotecas, como CUDA para GPUs
NVIDIA, fornecem os recursos necessários para desenvolver e otimizar esses algoritmos.
Para implementar a computação paralela de forma eficiente, é fundamental compreender a
arquitetura dos sistemas de hardware e a natureza das tarefas a serem executadas. No contexto da
inteligência artificial, isso significa otimizar a comunicação entre as unidades de processamento e
minimizar os gargalos que podem surgir durante a execução paralela. Técnicas como paralelismo
de dados e paralelismo de tarefas são aplicadas para distribuir a carga de trabalho de maneira
equilibrada.
As melhorias contínuas na computação paralela e o desenvolvimento de novos algoritmos e
arquiteturas de hardware têm impulsionado os avanços na inteligência artificial. A capacidade de
processar grandes volumes de dados de maneira rápida e eficiente abre novas possibilidades para
aplicações complexas, como reconhecimento de imagem, processamento de linguagem natural e
sistemas de recomendação. O futuro da IA está intrinsecamente ligado à evolução da computação
paralela, e o domínio dessas técnicas é essencial para qualquer profissional da área.
Para conectar o Google Drive ao Google Colab, você pode montar o Drive no ambiente do Colab
para facilitar o acesso e o armazenamento de arquivos. Isso é especialmente útil quando você está
trabalhando com grandes conjuntos de dados ou quando deseja salvar seus resultados diretamente
no Google Drive. Aqui estão os passos detalhados para conectar o Google Drive ao Google Colab:
Importar a biblioteca necessária: Para começar, você precisa importar a biblioteca ‘drive‘
do módulo ‘google.colab‘.
Montar o Google Drive: Utilize o método ‘drive.mount‘ para montar o Google Drive no
ambiente do Colab. Isso abrirá uma janela de autorização onde você precisará permitir que o Colab
acesse seu Google Drive.
Acessar os arquivos no Google Drive: Após montar o Google Drive, os arquivos estarão
acessíveis em ‘/content/drive/My Drive/‘.
Aqui está um exemplo de código em Python para realizar esses passos:
from google.colab import drive
# Montar o Google Drive no Colab
drive.mount(’/content/drive’)
/content/drive/My Drive/
Após executar este código, você verá uma URL de autorização. Clique na URL, autorize o acesso
e copie o código de verificação que será gerado. Cole esse código na célula do Colab onde ele é
solicitado.
Uma vez que o Google Drive esteja montado, você pode navegar e acessar seus arquivos como
faria normalmente em seu ambiente local. A montagem do Google Drive é uma maneira eficiente de
trabalhar com dados no Google Colab, permitindo que você armazene grandes arquivos de forma
segura e acesse-os facilmente durante o desenvolvimento do seu projeto de deep learning.
CAPÍTULO 5. AVENTURAS COM IA NAS NUVENS GRATUITAS 80

DEEP LEARNING

CAPÍTULO 6
6 Deep Learning - Ao infinito e além
No início, construir redes neurais profundas era um processo demorado e complexo, comparável à
construção manual de um arranha-céu, onde cada detalhe precisava ser meticulosamente planejado
e executado. A evolução do deep learning ao longo dos anos foi significativamente impulsionada pelo
desenvolvimento de frameworks como TensorFlow, Keras e PyTorch. No início, a implementação de
redes neurais profundas exigia um conhecimento aprofundado de matemática e programação de
baixo nível. Pesquisadores e desenvolvedores precisavam construir tudo do zero, o que tornava o
processo demorado e propenso a erros. Com a chegada desses frameworks, tornou-se mais fácil e
rápido desenvolver, treinar e implementar modelos de deep learning, permitindo que mais pessoas,
mesmo com menos conhecimento técnico, pudessem experimentar e inovar na área.
TensorFlow, lançado pelo Google Brain em 2015, foi um dos primeiros frameworks de deep lear-
ning amplamente adotado pela comunidade. Ele oferecia uma flexibilidade enorme, permitindo que
os usuários definissem redes neurais complexas e as otimizassem usando GPUs. Sua capacidade
de escalabilidade, desde dispositivos móveis até clusters de servidores, fez com que fosse escolhido
para uma vasta gama de aplicações industriais e de pesquisa. Além disso, o suporte da comunidade
e a documentação extensiva ajudaram a reduzir a curva de aprendizado para novos usuários.
Keras, lançado por François Chollet em 2015, foi projetado para ser uma interface de alto nível para
a construção de redes neurais, sendo inicialmente compatível com Theano e posteriormente com
TensorFlow. A simplicidade e intuitividade de Keras fizeram dele uma escolha popular entre iniciantes
e pesquisadores que desejavam prototipar rapidamente modelos de deep learning. Keras permitiu
que os usuários se concentrassem mais na arquitetura da rede e nas ideias inovadoras, em vez de
se preocupar com detalhes de implementação complexos, promovendo assim a experimentação
rápida e a iteratividade.
PyTorch, desenvolvido pelo Facebook’s AI Research lab (FAIR) e lançado em 2016, trouxe uma
mudança de paradigma com sua abordagem dinâmica de construção de gráficos computacionais.
Ao contrário de TensorFlow, que inicialmente usava gráficos estáticos, PyTorch permitia a construção
de gráficos de forma dinâmica, tornando o processo de debugging mais fácil e intuitivo. Essa
flexibilidade atraiu muitos pesquisadores acadêmicos, facilitando a experimentação e adaptação de
novas ideias. Além disso, a integração com a linguagem de programação Python tornou o PyTorch
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 81

DEEP LEARNING

especialmente popular entre a comunidade de pesquisa em deep learning.
A integração desses frameworks com GPUs e TPUs revolucionou a velocidade de treinamento de
redes neurais profundas. O suporte para operações paralelas em larga escala permitiu a construção
e treinamento de modelos muito maiores e mais complexos do que era anteriormente possível.
Este avanço técnico não apenas aumentou a eficiência do treinamento, mas também possibilitou a
utilização de técnicas mais avançadas, como redes generativas adversariais (GANs) e modelos de
aprendizado por reforço profundo, que demandam recursos computacionais intensivos.
Nesse capítulo, iremos explorar em detalhes o uso combinado de TensorFlow e Keras, duas
das ferramentas mais poderosas e populares no campo do deep learning. Vamos discutir como
essas plataformas se integram para facilitar a construção, treinamento e implantação de modelos de
aprendizado profundo, proporcionando uma interface intuitiva e flexível para iniciantes e especialistas.
Abordaremos desde a configuração inicial e conceitos básicos até técnicas avançadas, ilustrando
com exemplos práticos como essas ferramentas podem ser aplicadas em diversos problemas de
visão computacional.
6.1 Um problema sério a ser resolvido que IA pode ajudar
A tuberculose (TB) é uma doença infecciosa causada pela bactériaMycobacterium tuberculosis. Ela
afeta principalmente os pulmões, mas pode atacar qualquer parte do corpo, incluindo os rins, coluna
e cérebro. A tuberculose é uma das principais causas de morte infecciosa no mundo, superada
apenas pelo HIV/AIDS. A transmissão da tuberculose ocorre pelo ar, quando pessoas com TB
pulmonar ativa expiram bactérias ao tossir, espirrar ou falar. Esses microrganismos podem ser
inalados por outras pessoas, resultando em infecção.
A detecção precoce e precisa da tuberculose é crucial para controlar a disseminação da doença
e iniciar o tratamento adequado o mais rápido possível. Métodos tradicionais de diagnóstico, como o
teste de escarro e radiografias de tórax, embora eficazes, podem ser demorados, caros e requerem
a análise por profissionais de saúde treinados. Em muitos países em desenvolvimento, onde a TB é
endêmica, esses recursos são escassos, o que dificulta o diagnóstico e o tratamento oportunos.
Nesse contexto, o uso de técnicas de deep learning para a detecção da tuberculose apresenta
um grande potencial. Deep learning, um subcampo do aprendizado de máquina, utiliza redes neurais
profundas para aprender e fazer previsões a partir de grandes quantidades de dados. Essas técnicas
têm se mostrado particularmente eficazes na análise de imagens médicas, como radiografias de
tórax, para a detecção de anomalias associadas à tuberculose.
Redes neurais convolucionais (CNNs), um tipo específico de arquitetura de deep learning, são
especialmente adequadas para tarefas de classificação de imagens. Elas podem ser treinadas para
identificar padrões complexos e sutis em imagens de radiografias que são indicativos da presença de
tuberculose. Uma vez treinada, uma CNN pode processar novas imagens em questão de segundos,
fornecendo uma segunda opinião rápida e precisa que pode auxiliar médicos e radiologistas no
diagnóstico.
A aplicação de deep learning na detecção da tuberculose não só melhora a precisão do diag-
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 82

DEEP LEARNING

nóstico, mas também aumenta a eficiência do processo de triagem. Em áreas remotas ou com
recursos limitados, onde o acesso a especialistas médicos é restrito, esses sistemas automatizados
podem desempenhar um papel vital. Eles podem ajudar a identificar casos suspeitos que necessitam
de confirmação adicional, garantindo que mais pacientes recebam o tratamento necessário mais
rapidamente.
Além disso, a implementação de sistemas de deep learning para a detecção de tuberculose pode
contribuir para a vigilância epidemiológica. Ao analisar grandes volumes de dados de radiografias,
esses sistemas podem identificar padrões e tendências na disseminação da doença, auxiliando as
autoridades de saúde pública na implementação de medidas preventivas e no controle de surtos.
Dessa forma, a integração de deep learning no combate à tuberculose pode ser uma ferramenta
poderosa na luta global contra essa doença devastadora.
Baixando o Dataset
O datasetTuberculosis (TB) Chest X-ray Databasedisponível no Kaggle é uma coleção valiosa de
imagens médicas usada para o desenvolvimento e avaliação de modelos de aprendizado profundo
voltados para a detecção da tuberculose. Esse dataset contém radiografias de tórax, que são
amplamente utilizadas na prática clínica para diagnosticar diversas condições pulmonares, incluindo
a tuberculose.
As imagens contidas no dataset são rotuladas para indicar a presença ou ausência de tuberculose,
o que é essencial para o treinamento de modelos de deep learning. Com esses rótulos, as redes
neurais podem aprender a distinguir entre radiografias de pacientes saudáveis e aquelas de pacientes
infectados com aMycobacterium tuberculosis. A qualidade e a quantidade de dados rotulados são
fatores cruciais para o desempenho de qualquer modelo de aprendizado profundo.
O dataset inclui contribuições de várias fontes, incluindo imagens de hospitais e centros de
saúde da Índia e de Shenzhen, China. Essas imagens são diversas e abrangem uma ampla gama
de casos clínicos, ajudando a treinar modelos que são robustos e capazes de generalizar melhor
quando expostos a novas imagens. Isso é particularmente importante porque a variabilidade nas
radiografias pode ser significativa, dependendo de fatores como a posição do paciente, a qualidade
do equipamento de imagem e as diferenças anatômicas individuais.
Além disso, o dataset do Kaggle facilita a comparação de diferentes abordagens e arquiteturas
de deep learning. Pesquisadores e desenvolvedores podem usar esse conjunto de dados para
treinar seus modelos e, em seguida, comparar seus resultados com benchmarks estabelecidos por
outras equipes. Essa transparência e a possibilidade de replicar resultados são fundamentais para o
avanço da ciência e para a validação das técnicas propostas.
Outro aspecto importante do dataset de tuberculose do Kaggle é que ele pode ser usado para
desenvolver soluções aplicáveis em ambientes com recursos limitados. Em muitas regiões com alta
prevalência de tuberculose, o acesso a especialistas médicos é restrito. Modelos de deep learning
treinados com esse dataset podem ser implementados em sistemas de triagem automatizada,
ajudando a identificar rapidamente casos suspeitos e priorizando-os para análise adicional por
especialistas.
O acesso a datasets como o do Kaggle promove a inovação colaborativa. Ao disponibilizar esses
dados para a comunidade global de cientistas de dados e pesquisadores, o Kaggle incentiva a
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 83

DEEP LEARNING

criação de novas metodologias e ferramentas que podem melhorar significativamente a detecção e o
tratamento da tuberculose. Isso contribui para os esforços globais de saúde pública no combate a
essa doença devastadora.
Para baixar o dataset de imagens médicas de tuberculose-19, acesse o link fornecido:
Link Tuberculosis (TB) Chest X-ray Database Clique aqui
6.2 Carregando imagens para a festa no Colab
Vamos criar um Google Colab baseado com o que foi aprendido no capítlo anterior.
O Google Drive permite compartilhar arquivos e pastas gerando links que podem ser usados
para acessá-los. Quando um arquivo é compartilhado, o link gerado contém um identificador único
que permite acessar esse arquivo específico. Esse identificador é o que usamos com o comando
‘gdown‘.
Para ilustrar, vamos considerar um exemplo de link de compartilhamento do Google Drive.
Suponha que você tenha um arquivo no Google Drive e tenha gerado um link de compartilhamento.
Esse link pode ter a seguinte aparência:
"https://drive.google.com/file/d/1gcQmEpqYE658_xyetCrAZyO4w1XYqBEd/view?usp=sharing"
Neste link, o ID do arquivo é a parte entre ‘/d/‘ e ‘/view?usp=sharing‘. No exemplo acima, o ID do
arquivo é ‘1gcQmEpqYE658_xyetCrAZyO4w1XYqBEd‘.
Agora, vamos importar nossas imagens, utilizando o comando ‘!gdown‘ para baixar o arquivo
necessário a partir do Google Drive. Esse comando é útil quando queremos obter arquivos direta-
mente do Google Drive em vez de fazer o download manual e depois carregá-los no ambiente de
desenvolvimento. O identificador do arquivo é passado como argumento para o comando ‘gdown‘.
A linha de código a seguir faz exatamente isso.
!gdown 1FtucV8KiDgXUCLpC28t5P6THRQqPDj_R
Primeiramente, o símbolo ‘¡ no início da linha indica que estamos executando um comando de
shell a partir de um ambiente Python no Google Colab. O comando ‘gdown‘ é utilizado para fazer
download de arquivos hospedados no Google Drive. Uma string única associada ao arquivo que
queremos baixar. Neste caso, ‘1FtucV8KiDgXUCLpC28t5P6THRQqPDj_R‘ é o identificador do
arquivo desejado.
Ao executar este comando, o arquivo será baixado e armazenado no diretório atual do ambiente
de desenvolvimento, pronto para ser utilizado em nossas análises subsequentes.
Depois de baixado o dataset descompacte-o usando o comando unzip em outra célula do Colab.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 84

DEEP LEARNING

!unzip tuberculose.zip
Você verá que o dataset de imagens foi descompactado na pasta ‘tuberculose‘ no painel lateral
esquerdo do Google Colab, conforme mostrado na Figura 6.1. A estrutura do diretório é organizada
em duas principais categorias: ‘train‘ e ‘valid‘. Dentro de cada uma dessas categorias, há subdi-
retórios denominados ‘tuberculose‘ e ‘saudável‘, que contêm as imagens correspondentes a cada
classe.
Para interagir com esta estrutura de diretórios, clique na seta ao lado da pasta ‘tuberculose‘ para
expandi-la e visualizar as subpastas. Dentro de ‘train‘, você encontrará as subpastas ‘tuberculose‘ e
‘saudável‘, que contêm as imagens usadas para treinamento do modelo. Da mesma forma, dentro
de ‘valid‘, há subpastas ‘tuberculose‘ e ‘saudável‘, que contêm as imagens usadas para validação do
modelo. Essa organização facilita o carregamento e o pré-processamento das imagens em etapas
subsequentes de deep learning.
Figura 6.1: Estrutura de diretórios do dataset de imagens.
6.2 HYPERPARÂMETROS: AJUSTES MÁGICOS QUE FAZEM DIFENÇA
Para entender os hyperparâmetros de uma rede neural convolucional (CNN), imagine que você
está organizando um festival de música. Cada detalhe da organização pode ser comparado aos
diferentes hyperparâmetros de uma CNN.
Primeiro, pense noIMAGE_SIZEcomo o tamanho do palco do festival. Assim como você precisa
garantir que o palco seja grande o suficiente para acomodar todos os músicos e seus equipamentos,
o tamanho da imagem precisa ser adequado para capturar todos os detalhes importantes. Redimen-
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 85

DEEP LEARNING

sionar todas as imagens para um tamanho consistente permite que a rede processe as informações
de maneira eficiente, assim como ter um palco padronizado facilita a organização do evento.
OBATCH_SIZEpode ser comparado ao número de convidados que entram no festival de uma vez.
Se você deixar muitas pessoas entrarem ao mesmo tempo, pode ficar difícil gerenciar a multidão e
garantir que todos aproveitem a experiência. Da mesma forma, umbatch_sizemuito grande pode
sobrecarregar os recursos computacionais. Por outro lado, se você deixar entrar apenas alguns
convidados de cada vez, pode demorar muito para que todos entrem. Encontrar o tamanho de
lote ideal é como encontrar o equilíbrio certo para que a entrada dos convidados seja eficiente e
organizada.
AsEPOCHSrepresentam o número de dias em que o festival será realizado. Realizar o festival
por muitos dias (muitas épocas) pode proporcionar uma experiência melhor para os convidados,
permitindo que aproveitem mais a música. No entanto, se o festival durar muito tempo, os músicos e
a equipe podem ficar cansados e a qualidade pode diminuir, semelhante aooverfittingem uma rede
neural. Um número adequado de épocas garante que o festival seja memorável sem desgastar os
envolvidos.
Finalmente, orandom_stateé como o plano de assentos para o festival. Ter um plano fixo garante
que todos os convidados saibam onde se sentar, proporcionando uma experiência consistente a
cada edição do evento. Da mesma forma, definir umrandom_statefixo garante que a inicialização
dos pesos e a divisão dos dados sejam consistentes em cada execução do modelo, facilitando a
reprodução dos resultados e a comparação dos experimentos.
Vamos definir os hyperparâmetros da nossa rede neural para o treinamento do modelo. Execute
o seguinte código:
IMAGE_SIZE = [224, 224]
EPOCHS = 30
CLASSES = 2
BATCH_SIZE = 32
INPUT_SHAPE = (224 ,224 ,3)
random_state = 42
alpha = 1e-5
Este código define vários parâmetros importantes. Vamos entender cada um deles em detalhes:
A variávelIMAGE_SIZE = [224, 224]define o tamanho das imagens que serão usadas para
treinar o modelo. Todas as imagens serão redimensionadas para 224x224 pixels. Isso é essen-
cial para garantir que todas as imagens de entrada tenham a mesma dimensão, o que facilita o
processamento pelo modelo.
O parâmetroEPOCHS = 30define o número de épocas para o treinamento do modelo. Uma
época representa uma passagem completa pelo conjunto de dados de treinamento. Portanto, neste
caso, o modelo será treinado por 100 épocas.
A variávelCLASSES = 2indica o número de classes ou categorias que o modelo deve prever.
Aqui, temos duas classes, sugerindo um problema de classificação binária.
O parâmetroBATCH_SIZE = 32especifica o tamanho do lote, ou seja, o número de amostras
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 86

DEEP LEARNING

que serão processadas antes de atualizar os parâmetros do modelo. O modelo será atualizado após
processar cada lote de 32 imagens, o que pode ajudar a acelerar o treinamento e a estabilizar a
convergência do modelo.
A variávelINPUT_SHAPE = (224,224,3)define a forma da entrada que será passada para o
modelo. Neste caso, 224x224 representa a dimensão da imagem, e 3 indica que as imagens são
coloridas, com três canais de cor: vermelho, verde e azul.
O parâmetrorandom_state = 42é usado para inicializar o gerador de números aleatórios,
garantindo que os resultados sejam reproduzíveis. Usar umrandom statefixo é uma prática comum
para assegurar consistência nos experimentos.
Finalmente, a variávelalpha = 1e-5representa um pequeno valor utilizado em certos algoritmos
de aprendizado, como a regularização, para evitaroverfitting. Esse valor é tipicamente pequeno para
não influenciar drasticamente a atualização dos parâmetros do modelo.
Definindo essas variáveis, estamos configurando os parâmetros básicos necessários para o
treinamento do nosso modelo de deep learning de visão computacional.
6.3 Carregando Dados, o combustível de toda IA
Vamos importar nossas imagens. Primeiramente, definimos os diretórios onde as imagens de
treinamento e validação estão localizadas. Execute o seguinte código:
train_dir = ’/content/train/’
val_dir = ’/content/valid/’
Aqui, estamos definindo duas variáveis:train_direvalidation_dir.
A variável/content/train/aponta para o diretório onde as imagens de treinamento estão
armazenadas. Neste caso, o diretório é’/content/train/’. O diretório de treinamento contém
imagens que serão usadas para ajustar os parâmetros do modelo durante o treinamento.
A variável/content/valid/aponta para o diretório onde as imagens de validação estão armaze-
nadas. Neste caso, o diretório é’/content/valid/’. O diretório de validação contém imagens que
serão usadas para avaliar a performance do modelo durante o treinamento, ajudando a identificar se
o modelo está sofrendo deoverfittingouunderfitting.
Definindo essas variáveis, garantimos que o modelo saiba onde encontrar as imagens necessárias
para treinamento e validação.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 87

DEEP LEARNING

Vamos importar nossas imagens e preparar o gerador de dados para o treinamento. Primeiro,
execute o seguinte código:
from tensorflow.keras.preprocessing.image import ImageDataGenerator
\# Criando o training generator
train_datagen = ImageDataGenerator(
rescale =1./255 ,
)
train_generator = train_datagen.flow_from_directory(
train_dir ,
target_size=IMAGE_SIZE ,
batch_size=BATCH_SIZE ,
shuffle=True
)
Aqui, estamos utilizando a classeImageDataGeneratordo TensorFlow Keras para realizar o
pré-processamento das imagens. O objetivo desta classe é facilitar a geração de lotes de dados de
imagem com aumentos em tempo real, o que é útil para treinar redes neurais convolucionais.
Primeiro, importamos a classeImageDataGeneratorcom a linha:
from tensorflow.keras.preprocessing.image import ImageDataGenerator
Em seguida, criamos uma instância deImageDataGeneratorchamadatrain_datagen. Esta
instância é configurada para realizar o reescalonamento das imagens, convertendo os valores dos
pixels para a faixa de 0 a 1. Isso é feito através do argumentorescale=1./255, que divide todos os
valores dos pixels por 255.
Depois, usamos o métodoflow_from_directoryda instânciatrain_datagenpara criar um
gerador de dados de treinamento (train_generator). Este método carrega as imagens a partir
do diretório especificado portrain_dir, redimensiona cada imagem para o tamanho definido por
IMAGE_SIZE, organiza as imagens em lotes de tamanhoBATCH_SIZEe embaralha as imagens
(shuffle=True) para garantir que o modelo não aprenda a ordem das imagens, mas sim os padrões
dentro das imagens.
Ao definir e configurar oImageDataGenerator, garantimos que as imagens de treinamento sejam
carregadas e pré-processadas corretamente, prontas para serem usadas no treinamento do modelo.
Ao executar o código em uma célula o keras carregará 1300 imagens entre as duas classes
(saudável e tuberculose) conforme mostra a Figura 6.2
Figura 6.2: 1300 imagens entre as duas classes (saudável e tuberculose)
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 88

DEEP LEARNING

6.4 Validação: Toda IA também tem seu Enem
Vamos importar nossas imagens e preparar o gerador de dados para validação. Para isso, utili-
zaremos uma abordagem similar à utilizada para as imagens de treinamento. Execute o seguinte
código:
val_datagen = ImageDataGenerator(rescale =1. / 255)
validation_generator = val_datagen.flow_from_directory(
validation_dir ,
target_size=IMAGE_SIZE ,
batch_size=BATCH_SIZE ,
shuffle=False
)
Começamos criando uma instância deImageDataGeneratorchamadaval_datagen, configu-
rada para reescalar os valores dos pixels das imagens para a faixa de 0 a 1. Esse pré-processamento
é idêntico ao realizado para as imagens de treinamento, utilizandorescale=1. / 255. A normali-
zação dos valores dos pixels é crucial para manter a consistência no processamento das imagens,
tanto de treinamento quanto de validação.
Em seguida, utilizamos o métodoflow_from_directorypara criar o gerador de dados de valida-
ção (validation_generator). Este método carrega as imagens a partir do diretório especificado por
validation_dir, redimensionando cada imagem para o tamanho definido porIMAGE_SIZE. Similar-
mente ao gerador de treinamento, as imagens são organizadas em lotes de tamanhoBATCH_SIZE.
Uma diferença importante é que, para o gerador de validação, a configuraçãoshuffle=Falseé
utilizada. Isso garante que as imagens de validação sejam processadas na ordem original, permitindo
uma avaliação consistente do modelo. Diferentemente do treinamento, onde o embaralhamento das
imagens (shuffle=True) ajuda a generalizar melhor o modelo, na validação precisamos de uma
ordem fixa para medir de forma precisa o desempenho do modelo.
Ao configurar oImageDataGeneratorpara validação de forma similar ao treinamento, assegura-
mos que o processo de pré-processamento das imagens seja uniforme, permitindo uma avaliação
justa e precisa do modelo.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 89

DEEP LEARNING

6.5 Montando uma rede neural: vamos construir juntos
Para criar nossa rede neural convolucional com camadas de dropout para o problema de classificação
de imagens de COVID, execute o seguinte código:
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D , MaxPooling2D
from tensorflow.keras.layers import Flatten , Dense , Dropout
model = Sequential ()
model.add(Conv2D (32, (3, 3), activation=’relu’, input_shape=INPUT_SHAPE ))
model.add(MaxPooling2D(pool_size =(2, 2)))
model.add(Dropout (0.5))
model.add(Conv2D (32, (3, 3), activation=’relu’))
model.add(MaxPooling2D(pool_size =(2, 2)))
model.add(Dropout (0.5))
model.add(Conv2D (32, (3, 3), activation=’relu’))
model.add(MaxPooling2D(pool_size =(2, 2)))
model.add(Dropout (0.5))
model.add(Flatten ())
model.add(Dense (64, activation=’relu’))
model.add(Dropout (0.5))
model.add(Dense(CLASSES , activation=’softmax ’))
Começamos importando as bibliotecas necessárias do TensorFlow Keras:Sequential,Conv2D,
MaxPooling2D,Flatten,DenseeDropout. A rede é construída usando o modelo sequencial.
Adicionamos a primeira camada convolucionalConv2Dcom 32 filtros, um tamanho de kernel de
(3, 3) e a função de ativaçãorelu. A camada de entrada tem a forma definida porINPUT_SHAPE.
Esta camada é seguida por uma camada deMaxPooling2Dcom um tamanho depoolde (2, 2) para
reduzir as dimensões espaciais da entrada. Em seguida, adicionamos uma camada deDropoutcom
uma taxa de 0.5, que ajudará a prevenir overfitting desligando aleatoriamente 50% dos neurônios
durante o treinamento.
Em seguida, adicionamos outra camadaConv2Dcom 32 filtros, um tamanho de kernel de (3, 3)
e a função de ativaçãorelu. Esta camada é também seguida por uma camada deMaxPooling2D
com um tamanho depoolde (2, 2), seguida por outra camada deDropoutcom uma taxa de 0.5.
A terceira camadaConv2Dtem 32 filtros, um tamanho de kernel de (3, 3) e a função de ativação
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 90

DEEP LEARNING

relu. Esta camada é seguida por uma camada deMaxPooling2De mais uma camada deDropout,
ambas com as mesmas configurações das anteriores.
Após as camadas convolucionais, a rede é achatada usando a camadaFlatten, convertendo os
dados 2D em um vetor 1D. Adicionamos uma camada densa (Dense) com 64 unidades e a função
de ativaçãorelu, seguida por uma camada deDropoutcom uma taxa de 0.5 para ajudar a prevenir
overfitting.
Finalmente, a camada de saída (Dense) temCLASSESunidades e usa a função de ativação
softmaxpara classificação. Esse modelo, com várias camadas de dropout, é projetado para ser
robusto contra overfitting e adequado para a tarefa de classificação de imagens de Tuberculose.
Ao todo, o modelo tem 1.404.034 parâmetros treináveis, como indicado no resumo do modelo.
Figura 6.3: Resumo do modelo convolucional criado para classificação de imagens de tuberculose.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 91

DEEP LEARNING

6.6 Afinando a rede: os ajustes finais
Vamos compilar nossa rede neural para prepará-la para o treinamento. Execute o seguinte código:
model.compile(loss=’binary_crossentropy ’,
optimizer=’adam’,
metrics =[’acc’])
Neste código, estamos utilizando o métodocompiledo Keras para configurar o processo de
treinamento do nosso modelo. A funçãocompiletoma três argumentos principais:loss,optimizer
emetrics.
Primeiro, definimos a função de perda (loss) como’binary_crossentropy’. Esta função
de perda é apropriada para problemas de classificação binária, onde temos duas classes. A
binary_crossentropymede a diferença entre as distribuições previstas e reais, penalizando
previsões incorretas e ajudando a ajustar os pesos da rede durante o treinamento.
Em seguida, especificamos o otimizador (optimizer) como’adam’. O otimizador Adam é uma
escolha popular devido à sua eficiência e capacidade de adaptação. Ele combina as vantagens do
otimizador AdaGrad, que funciona bem em problemas com gradientes esparsos, e do otimizador
RMSProp, que lida bem com problemas online e não estacionários. Utilizando o Adam, garanti-
mos que a taxa de aprendizado se ajuste automaticamente durante o treinamento, acelerando a
convergência do modelo.
Finalmente, definimos a métrica (metrics) a ser monitorada durante o treinamento comoacc,
que corresponde à acurácia. Monitorar a acurácia nos permite avaliar a performance do modelo em
termos de proporção de previsões corretas.
Ao compilar o modelo com essas configurações, estamos preparando-o para o processo de
treinamento, onde ele ajustará seus pesos para minimizar a função de perda e maximizar a acurácia.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 92

DEEP LEARNING

6.7 O grande show: treinando nosso IAluno
Chegou a hora de treinar nossa CNN (Rede Neural Convolucional). Execute o seguinte código:
history = model.fit(
train_generator ,
epochs=EPOCHS ,
shuffle=True ,
verbose=1,
validation_data=validation_generator
)
Neste código, estamos utilizando o métodofitdo Keras para iniciar o processo de treinamento
do nosso modelo. Vamos analisar cada um dos argumentos passados para este método.
Primeiro, passamos otrain_generatorcomo o conjunto de dados de treinamento. Este
gerador fornece as imagens de treinamento em lotes, conforme definido anteriormente, e aplica as
transformações de pré-processamento necessárias.
O argumentoepochs=EPOCHSdefine o número de épocas de treinamento. Cada época representa
uma passagem completa pelo conjunto de dados de treinamento. O valor deEPOCHSfoi definido
anteriormente, e aqui estamos especificando que o treinamento deve continuar por esse número
total de épocas.
Definimosshuffle=Truepara embaralhar os dados de treinamento a cada época. Isso ajuda a
garantir que o modelo não memorize a sequência dos dados e, em vez disso, aprenda os padrões
subjacentes.
O argumentoverbose=1controla a verbosidade do processo de treinamento. Comverbose=1,
o Keras exibe uma barra de progresso durante o treinamento e informações sobre a perda e as
métricas de desempenho a cada época.
Finalmente, passamos ovalidation_generatorcomo o conjunto de dados de validação. Du-
rante o treinamento, após cada época, o modelo será avaliado utilizando os dados de validação. Isso
nos permite monitorar o desempenho do modelo em dados que ele não viu durante o treinamento,
ajudando a identificar problemas como overfitting.
Ao executar esse código, o métodofitinicia o processo de treinamento do modelo, atualizando
seus pesos para minimizar a função de perda definida anteriormente e maximizar a métrica de
acurácia.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 93

DEEP LEARNING

6.8 Resultados: olha como a nossa IA é boa!
Treinando nossa CNN no Keras, a imagem na Figura 6.4 mostra o progresso do treinamento da
rede neural convolucional ao longo de 30 épocas. Cada linha na saída representa uma época de
treinamento, com informações sobre a perda (loss) e a acurácia (accuracy) tanto no conjunto de
treinamento quanto no conjunto de validação.
Observe que na primeira época, o modelo começa com uma perda de treinamento de 0.6542
e uma acurácia de 0.6731. A perda de validação é de 0.6228 e a acurácia de validação é de
0.8200. Isso indica que, mesmo no início, o modelo já está capturando alguns padrões dos dados de
treinamento, embora ainda tenha espaço para melhorias.
À medida que o treinamento progride, a perda de treinamento diminui consistentemente, o que é
um sinal positivo de que o modelo está aprendendo. Por exemplo, na época 5, a perda de treinamento
é reduzida para 0.2973 e a acurácia de treinamento aumenta para 0.8838. A perda de validação
também diminui para 0.4750 e a acurácia de validação aumenta para 0.8900, mostrando que o
modelo está melhorando sua capacidade de generalizar para dados não vistos.
Entretanto, é importante observar as flutuações na perda e acurácia de validação ao longo
das épocas. Por exemplo, na época 7, há um aumento na perda de validação para 0.7491 e uma
queda na acurácia de validação para 0.5000. Essas flutuações podem indicar que o modelo está
sobreajustando aos dados de treinamento ou que há variabilidade nos dados de validação.
Na época 11, vemos uma melhora significativa, com a perda de treinamento caindo para 0.1937
e a acurácia de treinamento atingindo 0.9246. A perda de validação também melhora, caindo para
0.4303, e a acurácia de validação aumenta para 0.8700. Esses resultados sugerem que o modelo
está se ajustando bem aos dados de treinamento e também generalizando razoavelmente bem para
os dados de validação.
Para monitorar o progresso do treinamento e detectar sinais de sobreajuste, é essencial observar
tanto a perda quanto a acurácia nos conjuntos de treinamento e validação. Um bom equilíbrio entre
esses valores indica que o modelo está aprendendo de maneira eficaz e generalizando bem para
novos dados.
Executando o código abaixo teremos a plotagem da Figura 6.5
plt.figure(figsize =(12, 4))
plt.subplot(1, 2, 1)
plt.plot(history.history[’accuracy ’], label=’Train Accuracy ’)
plt.plot(history.history[’val_accuracy ’], label=’Validation Accuracy ’)
plt.title(’Accuracy Evolution ’)
plt.xlabel(’Epochs ’)
plt.ylabel(’Accuracy ’)
plt.legend ()
plt.subplot(1, 2, 2)
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 94

DEEP LEARNING

Figura 6.4: Saída do treinamento da rede neural convolucional ao longo de 30 épocas.
plt.plot(history.history[’loss’], label=’Train Loss’)
plt.plot(history.history[’val_loss ’], label=’Validation Loss’)
plt.title(’Loss Evolution ’)
plt.xlabel(’Epochs ’)
plt.ylabel(’Loss’)
plt.legend ()
plt.show()
Na plotagem que podemos ver que o modelo converge bem, porém com certa instabilidade no
treinamento. A Figura 6.5 mostra duas curvas essenciais para avaliar o desempenho do modelo ao
longo das épocas: a evolução da acurácia (à esquerda) e a evolução da perda (à direita) tanto para
o conjunto de treinamento quanto para o conjunto de validação.
No gráfico da esquerda, "Accuracy Evolution", observamos a acurácia do treinamento (linha
azul) e a acurácia da validação (linha laranja). Inicialmente, ambas as curvas mostram um aumento
rápido na acurácia, indicando que o modelo está aprendendo a partir dos dados de treinamento.
No entanto, a curva de validação apresenta flutuações significativas, especialmente nas primeiras
épocas, sugerindo que o modelo está se ajustando de forma instável aos dados de validação. Essas
oscilações podem indicar que o modelo está experimentando diferentes ajustes de peso antes de
encontrar uma configuração mais estável.
À medida que as épocas progridem, a acurácia de treinamento continua a aumentar de forma
mais suave e consistente, alcançando valores próximos de 1.0, o que sugere um bom ajuste aos
dados de treinamento. A acurácia de validação também melhora, embora com algumas flutuações,
aproximando-se da acurácia de treinamento, o que indica que o modelo está generalizando bem,
mas ainda há instabilidades a serem corrigidas.
No gráfico da direita, "Loss Evolution", vemos a perda de treinamento (linha azul) e a perda
de validação (linha laranja). A perda de treinamento diminui rapidamente nas primeiras épocas e
continua a diminuir de forma mais gradual nas épocas subsequentes, indicando que o modelo está
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 95

DEEP LEARNING

minimizando a função de perda de maneira eficaz. A perda de validação, por outro lado, apresenta
uma queda inicial, mas também flutua ao longo das épocas, refletindo a mesma instabilidade
observada na acurácia de validação.
Essas flutuações na perda de validação podem ser indicativas de overfitting ou de um ajuste
inadequado durante certas épocas. No entanto, à medida que o treinamento avança, a perda de
validação tende a seguir a tendência de queda da perda de treinamento, sugerindo que o modelo
está se ajustando melhor aos dados de validação ao longo do tempo.
Para interpretar essas curvas, é importante focar não apenas nas flutuações, mas também na
tendência geral de convergência. Um modelo bem treinado deve apresentar uma redução consistente
na perda de treinamento e de validação, com uma acurácia de validação que acompanha a acurácia
de treinamento sem divergir significativamente. As instabilidades observadas podem ser abordadas
com técnicas adicionais de regularização ou ajustes nos hiperparâmetros do modelo.
Figura 6.5: Evolução da acurácia e da perda durante o treinamento da rede neural convolucional.
No próximo capítulo, exploraremos técnicas avançadas para otimizar o treinamento da nossa rede
neural convolucional, visando reduzir o overfitting e melhorar a generalização do modelo. Uma das
técnicas que abordaremos é odata augmentation, que consiste em gerar novas amostras de dados
a partir das existentes através de transformações como rotações, translações, zoom e flips. Essas
técnicas aumentam a diversidade do conjunto de treinamento, permitindo que o modelo aprenda a
partir de uma gama mais ampla de exemplos, o que ajuda a melhorar sua capacidade de generalizar
para novos dados.
Além disso, discutiremos o uso detransfer learning, onde aproveitamos modelos pré-treinados em
grandes datasets para inicializar nossa rede, acelerando o treinamento e melhorando a performance.
Também introduziremoscallbacksdo Keras, que são funções que podem ser aplicadas em diferentes
estágios do treinamento para monitorar e ajustar o processo. Exemplos incluemEarlyStopping, que
interrompe o treinamento quando a performance de validação não melhora, eModelCheckpoint, que
salva o melhor modelo durante o treinamento. Essas estratégias combinadas ajudam a estabilizar o
treinamento, reduzir o overfitting e, consequentemente, melhorar a generalização do modelo.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 96

DEEP LEARNING

6.9 Hora de exercitar: vamos nessa!
Discussão sobre Frameworks de Deep Learning: Descreva como o desenvolvimento de
frameworks como TensorFlow, Keras e PyTorch facilitou a construção e implementação de
redes neurais profundas. Compare e contraste as características principais de cada um desses
frameworks e explique por que cada um se tornou popular entre diferentes comunidades de
pesquisadores e desenvolvedores.
Importância dos Hyperparâmetros: Explique o papel dos hyperparâmetrosIMAGE_SIZE,
EPOCHS,BATCH_SIZEeINPUT_SHAPEna construção de uma rede neural convolucional. Use a
analogia do festival de música apresentada no capítulo para ilustrar a importância de cada um
desses hyperparâmetros no treinamento de um modelo.
Análise de Resultados de Treinamento: Examine as saídas de treinamento da rede neural
convolucional apresentadas na Figura 6.4. Identifique os padrões observados na perda e na
acurácia durante as 30 épocas de treinamento. Discuta possíveis razões para as flutuações
na acurácia de validação e na perda de validação, e proponha soluções para estabilizar o
treinamento.
Estrutura e Função das Camadas Convolucionais: Descreva a estrutura de uma rede
neural convolucional conforme criada no código do capítulo. Explique a função das camadas
convolucionais, max pooling, flatten, dense e dropout. Discuta como cada camada contribui
para o processo de aprendizado da rede.
Uso de Datasets em Deep Learning: Explique a importância de usar datasets rotulados
como oTuberculosis (TB) Chest X-ray Databasedo Kaggle para o treinamento de modelos
de deep learning. Discuta como a diversidade e a qualidade das imagens no dataset podem
afetar a performance do modelo. Descreva os passos para carregar e pré-processar esse
dataset no Google Colab, conforme detalhado no capítulo.
CAPÍTULO 6. DEEP LEARNING - AO INFINITO E ALÉM 97

DEEP LEARNING

CAPÍTULO 7
7 Otimizando em Deep Learning
Ao longo dos últimos anos, a comunidade científica tem se dedicado intensamente ao desenvolvi-
mento e aperfeiçoamento de técnicas avançadas de aprendizado profundo. Esse esforço é motivado
pela necessidade crescente de modelos mais robustos, capazes de generalizar bem para uma varie-
dade de tarefas e dados. A evolução dessas técnicas não apenas permitiu avanços significativos em
áreas como visão computacional, processamento de linguagem natural e diagnóstico médico, mas
também ampliou o acesso e a aplicabilidade do aprendizado profundo a uma gama mais ampla de
pesquisadores e profissionais.
Essas inovações têm sido possíveis graças à colaboração e compartilhamento de conhecimento
entre pesquisadores de diversas disciplinas e instituições ao redor do mundo. Conferências internaci-
onais, como NeurIPS, CVPR e ICML, têm servido como plataformas cruciais para a apresentação de
novos métodos, discussão de ideias e formação de parcerias colaborativas. A publicação de artigos
em periódicos de alto impacto e a disponibilização de código-fonte aberto também têm desempe-
nhado um papel fundamental na disseminação do conhecimento e na aceleração do progresso na
área de aprendizado profundo.
Nesse capítulo, vamos explorar três técnicas fundamentais que podem melhorar significativamente
o desempenho e a robustez dos modelos de deep learning. A primeira técnica é odata augmentation.
Esta técnica aumenta artificialmente o tamanho do conjunto de dados de treinamento aplicando
diversas transformações às imagens originais, como rotações, translações, zooms e flips. O objetivo
é criar novas amostras a partir das existentes, aumentando a diversidade do conjunto de treinamento
e melhorando a capacidade do modelo de generalizar para novos dados, ajudando a evitar o
overfitting.
Outra técnica importante é otransfer learning. Com otransfer learning, utilizamos modelos
pré-treinados em grandes datasets como ponto de partida para novas tarefas. Em vez de treinar
um modelo do zero, aproveitamos as características e padrões aprendidos por um modelo treinado
em um dataset extenso e aplicamos esse conhecimento a um problema específico com um dataset
menor. Essa abordagem não só acelera o processo de treinamento, como também pode resultar
em modelos mais precisos e eficientes, aproveitando o conhecimento já adquirido pelo modelo
pré-treinado.
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 98

DEEP LEARNING

Por fim, discutiremos oscallbacksdo Keras, que são funções chamadas em diferentes pontos
durante o treinamento de um modelo. Oscallbackspermitem monitorar o desempenho do modelo,
ajustar hiperparâmetros dinamicamente e aplicar técnicas de regularização, comoEarlyStopping,
ModelCheckpointeReduceLROnPlateau. Esses mecanismos são essenciais para controlar o
processo de treinamento, prevenir overfitting e garantir que o melhor modelo possível seja salvo e
utilizado em aplicações práticas.
Essas técnicas avançadas de deep learning são fundamentais para otimizar o desempenho dos
modelos e aumentar sua capacidade de generalização. Ao implementardata augmentation,transfer
learningecallbacks, podemos desenvolver modelos mais robustos e eficientes, que são capazes de
lidar com a variabilidade dos dados do mundo real e fornecer resultados mais precisos e confiáveis.
7.1 Eu tenho poucos dados, e agora? Vamos resolver!
Imagine que você é um chefe de cozinha preparando um novo prato para um concurso gastronômico.
Você tem um número limitado de ingredientes principais, mas quer impressionar os juízes com a
diversidade e a criatividade dos pratos que pode criar. Para fazer isso, você decide usar técnicas de
variação culinária.
Primeiro, você pega seus ingredientes principais e começa a experimentar com diferentes
métodos de preparo. Você assa, grelha, cozinha no vapor e até mesmo frita os ingredientes,
criando várias versões do prato original. Assim como nodata augmentation, onde as imagens são
transformadas por rotações, translações e zooms, você está aplicando diferentes técnicas para
modificar a essência dos ingredientes, mas sem alterar sua identidade básica.
Depois, você começa a adicionar diferentes temperos e molhos. Um pouco de sal e pimenta em
uma versão, um molho picante em outra, e talvez um toque de ervas frescas em uma terceira. Essas
variações adicionam novos sabores e texturas, assim como odata augmentationadiciona novas
características às imagens através de alterações de brilho, contraste e adição de ruído. Cada nova
variação desafia o seu modelo (os juízes, neste caso) a reconhecer os elementos principais do prato,
independentemente das mudanças externas.
Por fim, você apresenta os pratos em diferentes estilos. Em um, você corta os ingredientes
em pequenos pedaços e os serve em uma tigela; em outro, você os dispõe artisticamente em um
prato grande. Essa apresentação é análoga ao uso de técnicas comoMixupeCutMixnodata
augmentation, onde as imagens são combinadas ou misturadas para criar novos exemplos complexos.
Cada apresentação diferente força os juízes a se concentrarem nas qualidades essenciais do prato,
assim comodata augmentationajuda o modelo a se concentrar nas características importantes das
imagens.
Assim, como um chefe de cozinha criativo, você usadata augmentationpara aumentar a diversi-
dade e a robustez dos dados de treinamento, preparando seu modelo para enfrentar uma ampla
variedade de desafios no mundo real.
A técnica dedata augmentationé amplamente utilizada em deep learning para aumentar a
quantidade e a diversidade dos dados de treinamento disponíveis. Ao gerar novas amostras a partir
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 99

DEEP LEARNING

das existentes,data augmentationajuda a melhorar a capacidade de generalização do modelo,
reduzindo o risco deoverfitting.Overfittingocorre quando um modelo se ajusta excessivamente
aos dados de treinamento, perdendo sua habilidade de generalizar para novos dados. Ao criar
variações dos dados de treinamento,data augmentationforça o modelo a aprender características
mais robustas e generalizáveis.
Existem várias formas de realizardata augmentation, e as técnicas específicas podem variar
dependendo do tipo de dados e da tarefa em questão. Em visão computacional, algumas transfor-
mações comuns incluem rotações, translações, flips horizontais e verticais, zooms, alterações de
brilho e contraste, e adição de ruído. Essas transformações simulam diferentes condições de captura
das imagens, ajudando o modelo a ser mais robusto a variações que podem ocorrer no mundo real.
Por exemplo, ao rotacionar uma imagem de um raio-X, estamos ensinando o modelo a reconhecer
padrões independentemente da orientação do objeto.
Outra abordagem avançada dedata augmentationenvolve técnicas de mistura de imagens, como
MixupeCutMix. OMixupcombina duas imagens e suas respectivas etiquetas, criando uma nova
imagem e etiqueta intermediária. Já oCutMixrecorta e mistura partes de diferentes imagens. Essas
técnicas não apenas aumentam a diversidade do conjunto de dados, mas também ajudam o modelo
a aprender a partir de exemplos mais complexos e variados, o que pode melhorar sua performance
em cenários reais.
Implementardata augmentationpode ser feito de várias maneiras, e frameworks como Tensor-
Flow e PyTorch oferecem suporte nativo para muitas dessas técnicas. No TensorFlow-Keras, a classe
ImageDataGeneratorfacilita a aplicação de transformações em tempo real durante o treinamento.
Isso significa que cada imagem de treinamento pode ser transformada de forma diferente a cada
época, proporcionando uma fonte praticamente infinita de dados de treinamento. Além disso, biblio-
tecas comoalbumentationseimgaugoferecem uma ampla gama de transformações avançadas
que podem ser facilmente integradas aos pipelines de treinamento.
Um dos principais benefícios dedata augmentationé que ele permite que os modelos de deep
learning sejam treinados com maior eficácia mesmo em cenários onde há escassez de dados
rotulados. Em muitas aplicações, coletar e rotular grandes quantidades de dados pode ser caro
e demorado. Ao aumentar artificialmente o conjunto de dados, podemos maximizar o valor das
amostras disponíveis e desenvolver modelos mais robustos sem a necessidade de coletar dados
adicionais.
É importante monitorar e ajustar as técnicas dedata augmentationusadas, pois nem todas as
transformações são benéficas para todos os tipos de dados ou tarefas. Algumas transformações
podem introduzir ruído ou distorções que não são representativas das condições reais, o que pode
prejudicar o desempenho do modelo. Portanto, é essencial realizar experimentos e validações para
determinar quais técnicas dedata augmentationproporcionam os melhores resultados para o seu
caso específico.
Veja como podemos de uma única imagem gerar outras 4 que, para nossa rede neural, serão
tidas como novas imagens. Esta técnica é conhecida como data augmentation e é essencial para
aumentar a diversidade do conjunto de dados de treinamento, melhorando assim a robustez e a
generalização do modelo.
Na Figura 7.1, observe a imagem original de um cachorro no centro. A partir desta imagem,
aplicamos várias transformações simples, mas eficazes. A primeira transformação é o flip horizontal,
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 100

DEEP LEARNING

que cria uma imagem espelhada da original. Clique na imagem do flip horizontal e veja como a
orientação do cachorro se inverte, mantendo todas as características essenciais.
A segunda transformação é a rotação, onde a imagem é ligeiramente girada. Note que, mesmo
com a rotação, a rede neural ainda consegue reconhecer o objeto, pois as características principais
do cachorro são preservadas. Experimente aplicar uma rotação a uma imagem e observe como
pequenas alterações na orientação não afetam a capacidade do modelo de identificar o objeto.
A terceira transformação é o zoom, onde a imagem é ampliada para focar em uma parte específica.
Isso pode ajudar a rede a aprender a identificar o objeto em diferentes escalas. Finalmente, a última
transformação é o ajuste de brilho, que altera a intensidade da luz na imagem. Veja como o cachorro
ainda é claramente reconhecível, mesmo com variações no brilho.
Essas técnicas de data augmentation são poderosas para aumentar a quantidade e a diversidade
dos dados de treinamento, ajudando a rede neural a aprender de maneira mais eficaz e robusta.
Figura 7.1: Data augmentation: de uma imagem original, podemos criar outras 4 usando transforma-
ções como flip horizontal, rotação, zoom e ajuste de brilho.
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 101

DEEP LEARNING

Para aplicardata augmentationusando o Keras, primeiro configure umImageDataGenerator
com as transformações desejadas. Execute o seguinte código:
# Configurar o ImageDataGenerator
train_datagen = ImageDataGenerator(
rescale =1.0/255.0 , # Normalizar os valores dos pixels para [0, 1]
# Rotacionar as imagens aleatoriamente em 40 graus
rotation_range =40,
# Deslocar as imagens horizontalmente em 20% da largura
width_shift_range =0.2,
# Deslocar as imagens verticalmente em 20% da altura
height_shift_range =0.2,
# Aplicar cisalhamento nas imagens em 20%
shear_range =0.2,
# Aplicar zoom nas imagens em 20%
zoom_range =0.2,
# Permitir flips horizontais nas imagens
#horizontal_flip=True ,
# Preencher pixels vazios resultantes
fill_mode=’nearest ’
)
No código acima, estamos criando uma instância deImageDataGeneratorchamadatrain_datagen
com várias opções dedata augmentation.
Primeiro, a transformaçãorescale=1.0/255.0é aplicada para normalizar os valores dos pixels
das imagens, escalando-os para o intervalo [0, 1]. Isso é importante para garantir que os valores dos
pixels estejam na mesma escala, facilitando o processo de aprendizado do modelo.
A opçãorotation_range=40define uma rotação aleatória das imagens em até 40 graus. Isso
ajuda o modelo a aprender a reconhecer objetos independentemente de sua orientação.
Os parâmetroswidth_shift_range=0.2eheight_shift_range=0.2permitem deslocar as
imagens horizontalmente e verticalmente em até 20% da largura e altura da imagem, respectivamente.
Essas transformações ajudam o modelo a ser mais robusto a variações na posição dos objetos
dentro da imagem.
A transformaçãoshear_range=0.2aplica um cisalhamento às imagens em até 20%, o que
distorce a imagem ao deslocar um eixo enquanto mantém o outro fixo. Isso ajuda a simular diferentes
perspectivas dos objetos.
O parâmetrozoom_range=0.2permite aplicar zoom nas imagens em até 20%, o que pode
simular a captura de imagens em diferentes distâncias.
A opçãohorizontal_flip=Truepermite que as imagens sejam espelhadas horizontalmente,
ajudando o modelo a aprender a reconhecer objetos independentemente da direção em que estão
voltados.
Finalmente,fill_mode=’nearest’define como os pixels vazios, resultantes das transformações,
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 102

DEEP LEARNING

serão preenchidos. O modo’nearest’preenche esses pixels com os valores dos pixels mais
próximos, mantendo a consistência visual da imagem.
Ao configurar oImageDataGeneratorcom essas transformações, você aumenta a diversidade
do conjunto de treinamento, ajudando a melhorar a robustez e a capacidade de generalização do
seu modelo.
7.2 Transplante de cérebro digital
Para entender o conceito detransfer learning, imagine que você é um cientista realizando uma
experiência revolucionária de transplante de cérebro. O objetivo é transferir o conhecimento de um
indivíduo altamente especializado para outra pessoa, permitindo que esta última adquira habilidades
avançadas quase instantaneamente.
Suponha que você tenha o cérebro de um renomado cirurgião, que passou anos aprendendo e
aperfeiçoando suas habilidades em cirurgia. Esse cérebro é uma rede neural treinada, carregada
com vasto conhecimento e experiência em uma área específica. Agora, você quer transplantar esse
cérebro para uma pessoa que está começando na área médica. Ao invés de começar do zero e
aprender tudo do início, essa pessoa pode aproveitar o conhecimento pré-existente do cirurgião.
O processo detransfer learningfunciona de forma semelhante. Em vez de treinar uma nova
rede neural a partir do zero, você começa com um modelo pré-treinado que já aprendeu uma
vasta gama de características a partir de um grande conjunto de dados, como o ImageNet. Esse
modelo pré-treinado atua como o cérebro do cirurgião, carregado com conhecimento genérico sobre
uma ampla variedade de objetos e características visuais. A partir desse ponto, você adapta (ou
"transplanta") esse conhecimento para uma nova tarefa específica, como a detecção de tumores em
imagens médicas.
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 103

DEEP LEARNING

Assim como no transplante de cérebro, onde a pessoa receptora ainda precisa ajustar e refinar
algumas habilidades específicas para seu próprio corpo e contexto, notransfer learning, a rede
neural pré-treinada é ajustada (oufine-tuned) para a nova tarefa com um conjunto menor de dados
específicos. Este ajuste permite que o modelo aplique o conhecimento geral adquirido anteriormente
a uma aplicação específica, melhorando a eficiência e a precisão do treinamento. Dessa forma,
otransfer learningeconomiza tempo e recursos, aproveitando o conhecimento pré-existente para
resolver novos problemas de forma eficaz.
7.3 Uma IA aprendendo com outra IA
A ideia detransfer learningtem suas raízes nas pesquisas iniciais sobre aprendizado de máquina
e redes neurais. Embora o conceito básico de reutilizar conhecimento adquirido em uma tarefa
para resolver outra não seja novo, o termotransfer learninge sua aplicação sistemática ganharam
destaque com o avanço das redes neurais profundas. Uma das primeiras menções formais detransfer
learningna literatura ocorreu na década de 1990, quando pesquisadores exploraram a capacidade
de redes neurais de transferir conhecimento aprendido em uma tarefa para outra relacionada. No
entanto, foi com o surgimento de grandes datasets e o aumento da capacidade computacional que
transfer learningrealmente começou a ser amplamente aplicado e estudado.
Transfer learningse popularizou no contexto do deep learning com o advento de redes neurais
convolucionais (CNNs) treinadas em grandes datasets como o ImageNet. O ImageNet Large Scale
Visual Recognition Challenge (ILSVRC), iniciado em 2010, foi um marco importante, onde modelos
treinados neste enorme conjunto de dados demonstraram capacidades de generalização notáveis.
Modelos como AlexNet, VGG, Inception e ResNet, todos treinados no ImageNet, mostraram que as
características aprendidas em tarefas de classificação de imagens gerais podiam ser transferidas
eficazmente para novas tarefas com datasets menores e específicos.
Tecnicamente,transfer learningenvolve duas etapas principais: pré-treinamento e ajuste fino
(fine-tuning). Durante o pré-treinamento, uma rede neural é treinada em um grande conjunto de
dados para aprender representações gerais dos dados, como bordas, texturas e formas. Esse
modelo pré-treinado, que já aprendeu uma ampla gama de características visuais, pode então ser
usado como uma base para novas tarefas. No ajuste fino, as camadas iniciais do modelo, que
capturam características de baixo nível, são geralmente mantidas fixas, enquanto as camadas finais,
que capturam características específicas, são ajustadas ou substituídas para se adaptar à nova
tarefa.
A arquitetura detransfer learningpode ser exemplificada pelo uso de CNNs pré-treinadas.
Modelos como VGG, ResNet e Inception são frequentemente utilizados como base para novas tarefas
de classificação de imagens. Nestes casos, as camadas convolucionais iniciais, que aprendem
características genéricas, são congeladas, e apenas as camadas densas finais são treinadas com o
novo conjunto de dados. Esse processo define-tuningpermite que o modelo adapte o conhecimento
prévio às especificidades da nova tarefa, aproveitando a robustez das características já aprendidas.
No TensorFlow, implementartransfer learningé relativamente simples. Utilizamos funções
comotf.keras.applicationspara carregar modelos pré-treinados e definir quais camadas serão
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 104

DEEP LEARNING

congeladas e quais serão treinadas. A funçãomodel.compile()configura a nova função de perda
e o otimizador para o ajuste fino, enquanto a funçãomodel.fit()realiza o treinamento com o
novo conjunto de dados. Esse processo é eficiente em termos de tempo e recursos, permitindo
que modelos de deep learning sejam aplicados de forma eficaz em cenários onde os dados são
limitados.
Uma das principais vantagens dotransfer learningé sua eficácia em situações onde há escassez
de dados rotulados. Em muitos casos práticos, coletar e rotular grandes volumes de dados é uma
tarefa cara e demorada. Utilizando um modelo pré-treinado, podemos iniciar com uma base sólida
de conhecimento e adaptar o modelo a partir de um conjunto menor de dados, mantendo uma alta
precisão e capacidade de generalização. Isso é especialmente útil em áreas como a detecção de
doenças em imagens médicas, onde os dados são frequentemente limitados e especializados.
Contudo, é importante notar que o sucesso dotransfer learningdepende da similaridade entre a
tarefa original e a nova tarefa. Se as tarefas forem muito diferentes, as características aprendidas
pelo modelo pré-treinado podem não ser úteis ou até mesmo prejudiciais. Portanto, é essencial
avaliar a relevância do conhecimento prévio para a nova aplicação e ajustar o modelo de acordo.
Quando aplicado adequadamente,transfer learningpode ser uma ferramenta poderosa para acelerar
o desenvolvimento e melhorar a performance de modelos de deep learning em uma ampla variedade
de tarefas.
7.4 A mágica dos grandes modelos prontos de visão
OKeras Applicationsfornece uma variedade de modelos de redes neurais pré-treinados que podem
ser usados paratransfer learning. Esses modelos foram treinados em grandes conjuntos de dados,
como o ImageNet, e são amplamente utilizados pela comunidade de deep learning. Cada um desses
modelos tem características únicas que os tornam adequados para diferentes tipos de tarefas e
aplicações.
O modeloVGG16é um dos modelos mais populares disponíveis no Keras Applications. Ele
é conhecido por sua simplicidade e eficácia, com uma arquitetura composta por 16 camadas de
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 105

DEEP LEARNING

convolução e pooling. VGG16 é frequentemente usado como ponto de partida para tarefas de
classificação de imagens e detecção de objetos, devido à sua capacidade de capturar características
detalhadas das imagens.
Outro modelo amplamente utilizado é oResNet50, que introduziu a ideia de conexões residuais
para mitigar o problema de degradação em redes muito profundas. Com 50 camadas, o ResNet50 é
capaz de aprender representações muito complexas e é especialmente útil para tarefas que requerem
um modelo profundo e robusto. Sua arquitetura permite que gradientes fluam mais facilmente durante
o treinamento, facilitando o ajuste fino em novas tarefas.
OInceptionV3é conhecido por sua eficiência computacional e capacidade de aprender caracte-
rísticas multi-escala. A arquitetura Inception utiliza blocos convolucionais de diferentes tamanhos em
paralelo, permitindo que o modelo capture padrões em várias escalas simultaneamente. Isso o torna
particularmente eficaz para tarefas que envolvem imagens com detalhes em múltiplas escalas, como
a análise de cenas complexas.
Além desses, oXceptioné um modelo que combina a arquitetura Inception com a separação
de convoluções em profundidade, melhorando a eficiência computacional sem sacrificar a precisão.
O Xception é ideal para tarefas que exigem um modelo eficiente em termos de tempo e recursos
computacionais, mantendo uma alta precisão.
Por fim, oMobileNeté projetado para ser altamente eficiente e leve, tornando-o adequado para
aplicações móveis e dispositivos com recursos limitados. MobileNet utiliza convoluções separáveis
em profundidade para reduzir a complexidade computacional, permitindo que modelos complexos
sejam executados em tempo real em dispositivos móveis.
Esses modelos pré-treinados oferecidos pelo Keras Applications permitem que pesquisadores e
desenvolvedores aproveitem o poder dotransfer learningde maneira eficaz. Ao escolher o modelo
adequado para a tarefa específica, é possível iniciar com uma base sólida de conhecimento e ajustar
o modelo para alcançar uma alta performance em um curto período de tempo.
Outro modelo significativo no Keras Applications é oDenseNet, que utiliza conexões densas entre
as camadas para melhorar o fluxo de gradientes e a reutilização de características aprendidas. Essa
arquitetura inovadora permite que cada camada receba entradas de todas as camadas anteriores,
promovendo uma melhor propagação das características e resultando em um modelo altamente
eficiente para a classificação de imagens.
ONASNet(Neural Architecture Search Network) é um exemplo de arquitetura gerada automatica-
mente por meio de algoritmos de busca neural. O NASNet é projetado para ser escalável, permitindo
que diferentes tamanhos de modelos sejam utilizados dependendo dos requisitos computacionais e
da precisão desejada. Essa flexibilidade torna o NASNet uma excelente escolha para tarefas de
visão computacional que demandam alta precisão e eficiência.
Além disso, oEfficientNeté uma série de modelos projetados com uma abordagem de dimen-
sionamento composta, que otimiza a profundidade, a largura e a resolução das redes neurais de
maneira coordenada. O EfficientNet alcança uma precisão de estado da arte com uma quanti-
dade significativamente menor de parâmetros, tornando-o ideal para aplicações onde a eficiência
computacional é crítica.
OInception-ResNetcombina os pontos fortes das arquiteturas Inception e ResNet, integrando
blocos de Inception com conexões residuais. Essa fusão permite que o modelo capture caracte-
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 106

DEEP LEARNING

rísticas em múltiplas escalas enquanto mantém a capacidade de treinar redes muito profundas,
resultando em uma arquitetura poderosa para uma variedade de tarefas de visão computacional.
Por fim, oRegNet(Regularized Neural Network) é um modelo que se destaca por sua simplicidade
e eficiência. Ele foi projetado para ser escalável e alcançar um bom desempenho com menos ajustes
de hiperparâmetros. O RegNet é adequado para cenários onde a simplicidade e a eficiência são
essenciais, permitindo implementações rápidas e eficazes em ambientes de produção.
Esses modelos pré-treinados disponíveis no Keras Applications proporcionam uma base sólida
para a implementação detransfer learning, oferecendo uma ampla gama de opções para atender às
diversas necessidades de tarefas de visão computacional. Ao aproveitar esses modelos, é possível
desenvolver soluções de deep learning de alta qualidade de maneira eficiente e eficaz.
7.5 Transfer learning com Keras: Meu Deus como é fácil!
Para aplicartransfer learningusando o Keras, começamos carregando um modelo pré-treinado.
Neste exemplo, utilizaremos o modeloInceptionV3, que já foi treinado no dataset ImageNet. Execute
o seguinte código:
from tensorflow.keras.applications import InceptionV3
# Carregar o modelo InceptionV3
base_model = InceptionV3(weights=’imagenet ’,
include_top=False ,
input_shape =(224, 224, 3))
Neste código, importamos o móduloInceptionV3da bibliotecatensorflow.keras.applications.
O modeloInceptionV3é uma rede neural convolucional profunda que já foi treinada no grande
dataset ImageNet, que contém milhões de imagens categorizadas em milhares de classes. Utilizar
este modelo pré-treinado nos permite aproveitar as características visuais gerais que ele aprendeu,
aplicando esse conhecimento a uma nova tarefa específica.
A funçãoInceptionV3()carrega o modelo pré-treinado. O parâmetroweights=’imagenet’
indica que os pesos do modelo devem ser carregados com os valores obtidos do treinamento no
ImageNet. O parâmetroinclude_top=Falseespecifica que a camada final de classificação do
InceptionV3, que é específica para o ImageNet, não deve ser incluída. Isso é importante porque
substituiremos essa camada por uma nova camada de classificação que é específica para a nova
tarefa que queremos resolver.
O parâmetroinput_shape=(224, 224, 3)define o formato das imagens de entrada. Neste
caso, estamos configurando o modelo para aceitar imagens de 224x224 pixels com três canais de
cor (RGB). Esta configuração garante que as dimensões das imagens sejam compatíveis com as
camadas convolucionais do modelo InceptionV3.
Ao carregar o modelo base com essas configurações, você prepara o terreno para adicionar suas
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 107

DEEP LEARNING

próprias camadas de classificação, ajustando o modelo pré-treinado às especificidades da nova
tarefa.
O modelo InceptionV3 é uma das arquiteturas mais influentes e amplamente utilizadas em deep
learning para a classificação de imagens. Desenvolvido pelo Google, a InceptionV3 foi introduzida
no artigo "Rethinking the Inception Architecture for Computer Vision"por Szegedy et al. em 2015.
Esta versão do modelo faz parte da série de arquiteturas Inception, também conhecidas como
GoogLeNet, que foram concebidas para melhorar a eficiência computacional e a precisão em tarefas
de classificação de imagens. A InceptionV3 introduziu várias inovações, como o uso de convoluções
fatoradas, que reduzem o número de parâmetros e aumentam a profundidade da rede, permitindo
um melhor aprendizado de características.
A inspiração para o nome "Inception"vem do filme homônimo de Christopher Nolan, onde a ideia
principal é a de camadas dentro de camadas de sonhos. De maneira análoga, a arquitetura Inception
emprega "blocos de Inception", que são conjuntos de filtros de diferentes tamanhos aplicados
simultaneamente em uma camada de entrada, capturando características em múltiplas escalas.
Esses blocos permitem que a rede seja mais eficiente ao processar informações em diferentes níveis
de abstração, imitando a complexidade e a profundidade dos sonhos dentro de sonhos.
InceptionV3 melhorou significativamente as versões anteriores ao introduzir técnicas como a
regularização por Dropout, a normalização por batch (Batch Normalization), e o uso de convoluções
fatoradas que substituem as tradicionais convoluções de 5x5 por duas convoluções sequenciais
de 3x3. Estas melhorias não só reduziram o número de parâmetros e o custo computacional, mas
também aumentaram a precisão do modelo. A InceptionV3 alcançou resultados de ponta em vários
benchmarks de classificação de imagens, consolidando-se como uma escolha padrão para muitos
pesquisadores e desenvolvedores em visão computacional.
Depois de carregado o InceptionV3 como modelo base para nossotransfer learning, é necessário
adicionar camadas densas ao modelo base para que ele se adapte à nova tarefa de classificação.
Execute o seguinte código:
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers importGlobalAveragePooling2D , Flatten
# Adicionar camadas densas ao modelo base
x = base_model.output
x = GlobalAveragePooling2D ()(x)
x = Dense (512, activation=’relu’)(x)
predictions = Dense(train_generator.num_classes , activation=’softmax ’)(x)
model = Model(inputs=base_model.input , outputs=predictions)
Neste código, primeiro importamos as classes necessáriasModel,Dense,GlobalAveragePooling2D,
eFlattenda bibliotecatensorflow.keras.layersetensorflow.keras.models.
Começamos criando a variávelx, que recebe a saída do modelo basebase_model.output. Em
seguida, aplicamos uma camadaGlobalAveragePooling2D()a essa saída. Essa camada reduz
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 108

DEEP LEARNING

as dimensões espaciais da saída, convertendo-a em um vetor de características, o que facilita a
adição de camadas densas subsequentes.
Depois, adicionamos uma camada densa (Dense) com 512 neurônios e a função de ativação
ReLU (’relu’). Esta camada densa atua como uma camada intermediária, permitindo ao modelo
aprender combinações complexas das características extraídas pelo modelo base.
Finalmente, adicionamos uma camada de saída (Dense) com um número de neurônios igual
ao número de classes no conjunto de dados de treinamento (train_generator.num_classes).
A função de ativação’softmax’é usada nesta camada para produzir probabilidades de classe,
adequadas para uma tarefa de classificação multiclasse.
Por fim, criamos o modelo completo utilizando a classeModel, especificando as entradas
(base_model.input) e saídas (predictions). Este modelo agora está preparado para ser compi-
lado e treinado para a nova tarefa de classificação.
No código anterior, adicionamos novas camadas densas ao modelo base InceptionV3 para adap-
tar a rede pré-treinada a uma nova tarefa de classificação específica. A camadaGlobalAveragePooling2D()
é usada para converter as características espaciais de alta dimensão extraídas pelo InceptionV3
em um vetor de características de menor dimensão. Isso é essencial porque a camada de pooling
reduz a complexidade dos dados de entrada para as camadas densas subsequentes, facilitando o
aprendizado de padrões mais abstratos e específicos da nova tarefa.
A inclusão de uma camada densa com 512 neurônios e a função de ativação ReLU (’relu’)
permite ao modelo aprender combinações complexas das características extraídas pelo modelo
base. A função ReLU é amplamente utilizada em redes neurais porque ajuda a introduzir não-
linearidades no modelo, permitindo que ele aprenda representações mais complexas. Esta camada
atua como uma camada intermediária, essencial para capturar relações mais sofisticadas entre as
características, aumentando a capacidade do modelo de generalizar para a nova tarefa.
Por fim, a adição de uma camada de saída com um número de neurônios igual ao número de
classes no conjunto de dados de treinamento, juntamente com a função de ativação’softmax’,
é crucial para a tarefa de classificação multiclasse. A funçãosoftmaxconverte as saídas dos
neurônios em probabilidades de classe, permitindo que o modelo faça previsões probabilísticas
sobre a classe de cada amostra de entrada. Esta configuração garante que o modelo final seja
adequado para a nova tarefa de classificação, aproveitando o conhecimento prévio do modelo
InceptionV3 enquanto ajusta suas previsões às especificidades do novo conjunto de dados.
7.6 Fine-tuning: aquele toque final que faz diferença
Fine-tuning, ou ajuste fino, é uma técnica emtransfer learningonde ajustamos um modelo pré-
treinado a uma nova tarefa, refinando os parâmetros das camadas superiores para melhor se adequar
ao novo conjunto de dados. Para entender melhor, imagine que você é um escultor trabalhando
em uma peça complexa. Você começa com uma escultura parcialmente concluída feita por outro
artista renomado. A base já está estabelecida, com formas e detalhes gerais bem definidos. No
entanto, para que a escultura reflita sua visão e estilo, você precisa fazer ajustes finos, esculpindo os
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 109

DEEP LEARNING

detalhes específicos que representam sua própria assinatura artística.
Nesse processo, você não precisa começar do zero, pois a estrutura básica e as características
principais já foram cuidadosamente trabalhadas. Em vez disso, você se concentra nas áreas onde
deseja adicionar suas próprias nuances e toques pessoais. Talvez você refine o rosto, ajuste as
proporções das mãos ou adicione texturas específicas que caracterizam seu trabalho. Esse ajuste
fino permite que você crie uma obra que combina a base sólida fornecida pelo artista anterior com
as especificidades e a identidade de sua própria visão.
Da mesma forma, nofine-tuning, começamos com um modelo que já possui uma boa com-
preensão das características gerais aprendidas a partir de um grande conjunto de dados, como o
ImageNet. Em seguida, ajustamos as camadas superiores do modelo para que ele aprenda a partir
do novo conjunto de dados específico, incorporando nuances e padrões que são exclusivos da nova
tarefa. Isso permite que o modelo aproveite o conhecimento pré-existente e o adapte para alcançar
uma performance superior na nova aplicação, assim como o escultor aproveita a obra existente e a
ajusta para criar uma peça única e refinada.
Vamos descongelar algumas últimas camadas do modelo base para aplicarfine-tuning. Execute
o seguinte código:
# Descongelar camadas convolucionais da para aplicar fine -tuning
base_model.trainable = True
for layer in base_model.layers [:-5]:
layer.trainable = False
Neste código, ajustamos a propriedadetrainabledo modelo base (base_model) paraTrue,
permitindo que suas camadas sejam treináveis. Isso é essencial para realizar ofine-tuning, onde
refinamos os pesos das camadas superiores para melhor adaptar o modelo pré-treinado à nova
tarefa.
Em seguida, utilizamos um loopforpara iterar através das camadas dobase_model, configu-
rando a propriedadetrainablede todas as camadas, exceto as cinco últimas, paraFalse. Isso
significa que apenas as últimas cinco camadas do modelo base serão ajustadas durante o treina-
mento. Manter a maioria das camadas congeladas (não treináveis) preserva os conhecimentos
gerais que o modelo já aprendeu, enquanto permite que as camadas superiores sejam ajustadas
especificamente para a nova tarefa.
Esta abordagem de descongelar e treinar apenas as últimas camadas é uma prática comum em
fine-tuning. Ela ajuda a evitar ooverfitting, já que ajusta apenas uma pequena parte do modelo,
garantindo que o modelo retenha o conhecimento geral aprendido do dataset inicial e se adapte às
características específicas do novo dataset.
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 110

DEEP LEARNING

7.7 Callbacks: Os assistentes secretos
Oscallbacksdo Keras são ferramentas poderosas que permitem a execução de funções perso-
nalizadas em diferentes estágios do treinamento de um modelo de deep learning. Eles fornecem
uma maneira eficiente de monitorar e ajustar o processo de treinamento, ajudando a melhorar a
performance e a estabilidade do modelo.Callbackspodem ser usados para diversas finalidades,
como salvar checkpoints do modelo, ajustar a taxa de aprendizado, interromper o treinamento
antecipadamente e muito mais.
Um doscallbacksmais utilizados é oModelCheckpoint. Estecallbacksalva o modelo ou seus
pesos em intervalos regulares durante o treinamento, permitindo que você recupere o modelo que
teve a melhor performance no conjunto de validação. A funçãoModelCheckpointpermite especificar
o caminho para salvar o modelo, a métrica a ser monitorada e a condição para salvar o modelo
(por exemplo, quando a métrica de validação melhora). Isso é extremamente útil para garantir que
você tenha uma versão do modelo que alcançou a melhor performance, mesmo que o treinamento
subsequente leve a umoverfitting.
Outrocallbackimportante é oEarlyStopping. Essecallbackmonitora uma métrica específica du-
rante o treinamento e interrompe o processo quando a performance do modelo para de melhorar. Por
exemplo, se a acurácia de validação não melhorar após um certo número de épocas, oEarlyStopping
pode interromper o treinamento para evitaroverfittinge economizar tempo e recursos computacionais.
O uso doEarlyStoppingé particularmente benéfico quando se trabalha com datasets grandes e
modelos complexos, onde o tempo de treinamento pode ser substancial.
OReduceLROnPlateaué outrocallbackessencial no Keras. Ele reduz a taxa de aprendizado
quando uma métrica monitorada parou de melhorar, o que ajuda a ajustar a velocidade de aprendi-
zado do modelo e evitaroverfitting. A taxa de aprendizado é um hiperparâmetro crítico no treinamento
de redes neurais, e ajustá-la dinamicamente pode levar a uma melhor convergência e performance
do modelo. OReduceLROnPlateaumonitora a métrica de validação e reduz a taxa de aprendizado
quando necessário, permitindo que o modelo continue aprendendo de maneira mais estável e eficaz.
Além dessescallbacks, o Keras também oferece oTensorBoardcallback, que integra o Keras
com o TensorBoard, uma ferramenta de visualização do TensorFlow. OTensorBoardpermite que
você visualize gráficos de métricas de treinamento e validação, histogramas de pesos e ativações, e
muito mais. Usar oTensorBoarddurante o treinamento pode proporcionar insights valiosos sobre o
comportamento do modelo e ajudar a diagnosticar problemas de treinamento, comooverfittingou
underfitting.
Por fim, oLearningRateScheduleré umcallbackque permite definir uma função personalizada
para ajustar a taxa de aprendizado ao longo do treinamento. Isso pode ser útil para implementar
estratégias avançadas de ajuste de taxa de aprendizado, como o agendamento cíclico ou decaimento
exponencial. Ajustar dinamicamente a taxa de aprendizado pode melhorar a eficiência do treinamento
e ajudar o modelo a escapar de mínimos locais, alcançando uma performance melhor no conjunto
de dados.
Oscallbacksdo Keras são ferramentas essenciais para qualquer desenvolvedor ou pesquisador
em deep learning. Eles oferecem uma maneira flexível e poderosa de monitorar, ajustar e melhorar o
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 111

DEEP LEARNING

processo de treinamento de modelos, contribuindo para a construção de modelos mais robustos e
eficientes.
Vamos instanciar os callbacks do Keras, que nos ajudarão a monitorar e ajustar o treinamento do
modelo. Execute o seguinte código:
# Configurar os callbacks
checkpoint = ModelCheckpoint(’best_model.h5’,
monitor=’val_loss ’,
verbose=1,
save_best_only=True ,
mode=’min’)
early_stop = EarlyStopping(monitor=’val_loss ’,
patience =15,
verbose=1,
mode=’min’)
reduce_lr = ReduceLROnPlateau(monitor=’val_loss ’,
factor =0.2,
patience=5,
verbose=1,
mode=’min’)
callbacks = [checkpoint , early_stop , reduce_lr]
Neste código, configuramos três callbacks essenciais para o treinamento do modelo:ModelCheckpoint,
EarlyStoppingeReduceLROnPlateau.
OModelCheckpointé configurado para salvar o modelo durante o treinamento. O argu-
mento’best_model.h5’especifica o nome do arquivo onde o modelo será salvo. O parâmetro
monitor=’val_loss’indica que o desempenho do modelo será monitorado com base na perda
de validação. O argumentosave_best_only=Trueassegura que apenas o melhor modelo (com a
menor perda de validação) será salvo. O parâmetromode=’min’indica que estamos interessados
em minimizar a métrica monitorada. O argumentoverbose=1ativa a impressão de mensagens de
progresso.
OEarlyStoppingé configurado para interromper o treinamento se o modelo parar de melhorar.
O parâmetromonitor=’val_loss’define que a perda de validação será monitorada. O argumento
patience=15especifica que o treinamento será interrompido se a perda de validação não melhorar
por 15 épocas consecutivas. Omode=’min’indica que queremos minimizar a perda, e overbose=1
ativa a impressão de mensagens de progresso.
OReduceLROnPlateauajusta dinamicamente a taxa de aprendizado se a performance do modelo
parar de melhorar. O parâmetromonitor=’val_loss’define a perda de validação como a métrica a
ser monitorada. O argumentofactor=0.2reduz a taxa de aprendizado em 20% quando o callback
é acionado. Opatience=5indica que a taxa de aprendizado será reduzida se não houver melhora
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 112

DEEP LEARNING

na perda de validação por 5 épocas consecutivas. Omode=’min’indica que estamos minimizando
a métrica monitorada, e overbose=1ativa a impressão de mensagens de progresso.
Esses callbacks são adicionados a uma lista chamadacallbacks, que será passada ao método
de treinamento do modelo para serem executados durante o treinamento. Eles ajudam a salvar o
melhor modelo, interromper o treinamento antecipadamente em caso de falta de melhoria e ajustar a
taxa de aprendizado dinamicamente para melhorar a performance do modelo.
Agora adicione os callbacks ao treinamento da rede neural. Execute o seguinte código:
# Treinar o modelo com fine -tuning
history = model.fit(
train_generator ,
steps_per_epoch=train_generator.samples // train_generator.batch_size ,
validation_data=val_generator ,
validation_steps=val_generator.samples // val_generator.batch_size ,
epochs =30,
callbacks=callbacks
)
No código acima, a inclusão do parâmetrocallbacks=callbacksna funçãomodel.fit()in-
tegra os callbacks configurados anteriormente no processo de treinamento. Esses callbacks, que
incluemModelCheckpoint,EarlyStoppingeReduceLROnPlateau, são fundamentais para mo-
nitorar e ajustar o treinamento do modelo. Eles ajudam a salvar o melhor modelo baseado na
perda de validação, interromper o treinamento se a perda de validação parar de melhorar e ajustar
dinamicamente a taxa de aprendizado quando a performance do modelo estabilizar.
7.8 Empacotando tudo
Ao explorar as estratégias avançadas de deep learning discutidas neste capítulo, fica evidente que
o domínio de técnicas como data augmentation, transfer learning e o uso eficaz de callbacks são
fundamentais para maximizar o desempenho de redes neurais em variados domínios de aplicação.
Estas metodologias não apenas aprimoram a precisão e a eficiência dos modelos, mas também
ampliam as possibilidades de inovação em áreas críticas como saúde, automação industrial e
processamento de linguagem natural.
O data augmentation serve como um poderoso aliado na luta contra o overfitting, proporcionando
aos modelos uma maior capacidade de generalização. Ao manipular digitalmente os dados de
treinamento, essa técnica permite que os modelos aprendam a reconhecer padrões essenciais,
mesmo sob variações substanciais nos dados de entrada. Este método é comparável a treinar
um artista para reconhecer e replicar estilos de arte em condições variadas de luz e perspectiva,
potencializando sua adaptabilidade e criatividade.
O transfer learning, por outro lado, simboliza a transferência de conhecimento que permite que
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 113

DEEP LEARNING

um modelo treinado em um conjunto de dados grande e diversificado seja adaptado para tarefas
específicas com relativa facilidade e eficiência. Isso é especialmente útil em situações onde os dados
são escassos ou onde é necessário acelerar o processo de treinamento. Essencialmente, esta
abordagem reduz significativamente o custo e o tempo de desenvolvimento de modelos robustos,
tornando a tecnologia de deep learning mais acessível e prática para uma variedade de usuários
finais.
A implementação de callbacks oferece uma camada adicional de inteligência ao processo de
treinamento, permitindo a intervenção automatizada que pode salvar modelos, ajustar taxas de
aprendizado e parar o treinamento para evitar o consumo desnecessário de recursos. Essas
ferramentas, quando usadas estrategicamente, podem significar a diferença entre um modelo
medíocre e um altamente eficaz, que não apenas performa bem de acordo com as métricas
acadêmicas, mas que também opera de maneira ótima no mundo real.
Por fim, o uso integrado dessas técnicas estabelece um novo padrão para o treinamento de
modelos de deep learning. Os desenvolvedores e cientistas de dados são encorajados a adotar
uma abordagem holística, não apenas focando em desenvolver a "melhor"rede neural, mas também
em criar um processo de desenvolvimento que seja iterativo, informado e adaptativo. Ao considerar
cuidadosamente as características específicas de cada conjunto de dados e tarefa, os praticantes
podem usar estas técnicas para extrair o máximo valor dos seus modelos.
Em resumo, este capítulo não apenas detalhou métodos essenciais para a otimização de redes
neurais, mas também forneceu um roteiro para a aplicação prática dessas técnicas em problemas
reais de deep learning. À medida que avançamos, fica claro que o sucesso na implementação de
tais modelos dependerá cada vez mais da nossa capacidade de combinar criatividade com rigor
técnico, um desafio que os entusiastas de IA estão bem equipados para enfrentar, armados com as
estratégias descritas aqui.
7.9 Pratique o aprendizado: hora dos exercícios
1.Explique como a técnica dedata augmentationpode ajudar a prevenir o problema deoverfitting
em modelos de deep learning. Dê exemplos de duas transformações específicas que podem
ser aplicadas em imagens e descreva como cada uma pode aumentar a robustez do modelo.
2.Descreva o conceito detransfer learninge explique como ele pode ser utilizado para acelerar
o processo de treinamento de um modelo de deep learning. Utilize o modelo InceptionV3
como exemplo e discuta como ele pode ser adaptado para uma nova tarefa de classificação
de imagens.
3.Implemente um código simples em Python usando Keras para configurar oImageDataGenera-
torcom opções dedata augmentationpara treinamento de um modelo. As transformações
devem incluir rotação, zoom e flip horizontal. Comente cada linha do código explicando a
função de cada parâmetro.
4.Considerando o processo define-tuning, explique a importância de congelar as camadas
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 114

DEEP LEARNING

iniciais de um modelo pré-treinado durante o treinamento de uma nova tarefa. Discuta o que
poderia acontecer se todas as camadas fossem treinadas simultaneamente.
5.Utilize ocallback ReduceLROnPlateaudo Keras em um exemplo de código para treinar um
modelo de rede neural. Explique como a alteração da taxa de aprendizado pode influenciar o
processo de treinamento e quais os benefícios de reduzir a taxa de aprendizado quando a
métrica de performance para de melhorar.
CAPÍTULO 7. OTIMIZANDO EM DEEP LEARNING 115

This is a offline tool, your data stays locally and is not send to any server!
Feedback & Bug Reports