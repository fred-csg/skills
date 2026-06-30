"""
Geracao de audio - Clone Digital Guilherme Facci
Skill: text-to-speech (ElevenLabs)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings

load_dotenv()

TEXTO = """
Bem-vindas e bem-vindos a loucura nossa de cada dia.

Para quem esta aqui pela primeira vez, meu nome e Guilherme Facci,
sou psicoanalista e aqui tratamos das nossas questoes humanas de maneira
descomplicada a partir do metodo psicanalitico.

Entao, me pediram para dar uma opiniao sobre esse prontuario. E gente, eu preciso dizer: isso aqui e um material clinico denso. Muito denso. Mas e exatamente o tipo de material que me interessa comentar, porque ele revela algo que eu escuto no consultorio ha mais de uma decada.

O que me salta aos olhos?

Primeiro, o fenomeno de superficie: um homem de 42 anos que pede honestidade brutal e traz, logo de saida, um documento em terceira pessoa, ja estruturado, ja categorizado. Voces estao me acompanhando, gente? Antes de ser escutado, ele ja editou o que quer ser escutado. Isso tem nome em psicanalise: intelectualizacao. E ela esta trabalhando a servico de algo.

A raiz estrutural: o lugar do secundario.

Eu vou repetir: o analisando Carlos parece ter organizado sua vida inteira a partir de uma posicao estrutural de secundario. O pai biologico que nunca existiu. O pai socioafetivo que veio e foi embora. A esposa cujo mundo interior ainda pertence, em algum nivel, ao homem que veio antes. E o proprio casamento: ele veio depois do violento.

Ha uma estrutura aqui que Freud chamaria de compulsao a repeticao. E o que me e clinicamente interessante nao e a repeticao em si, e o que ela esta tentando resolver. Cada vez que Carlos se coloca nessa posicao de homem que vem depois, ele esta, inconscientemente, tentando resolver a cena que nunca teve solucao: a crianca que nao conseguiu se tornar o escolhido da mae, antes que outro homem entrasse.

O conceito mais importante aqui: a identidade negativa.

Gente, isso e o que mais me tocou nesse material. A hipotese clinica levantada na sessao dois e precisa. Carlos construiu sua identidade em torno de um NAO-SER. Eu nao sou os homens violentos. Essa e uma identidade fragil. Sabe por que? Porque ela depende do outro para existir. Ela precisa do violento para se definir como nao-violento.

E o que acontece quando esse pilar desmorona? Quando o proprio Carlos bate em Andreia?

A negacao entra em colapso. E o sonho recorrente, onde ele fica do lado de fora, pedinte, preterido, pode ser, como o prontuario levanta com muita propriedade, uma autopunicao inconsciente. Eu nao mereco o lugar de quem nao agride. E disso que se trata.

Um ponto que eu levaria mais adiante.

O que me chama atencao clinicamente e a frase: aqui sou eu resolvendo comigo mesmo, com uma base teorica.

Vamos avancar um pouquinho. Essa formulacao e sofisticada. E e, ao mesmo tempo, uma resistencia elegante. Porque o processo analitico nao e resolver consigo mesmo. E encontrar o Outro. E ser visto por um Outro. E o que Carlos teme, la no fundo, e exatamente isso: ser visto. Nao como ele se construiu, o nao-violento, o responsavel, o resolvedor, mas como ele realmente e, com todas as contradicoes que esse prontuario comeca a desenhar.

Eu escuto isso no consultorio. A pessoa que mais resiste a analise e muitas vezes a que tem mais capacidade para ela. E o Carlos, a julgar por esse material, tem capacidade rara.

Do ponto de vista do registro clinico, gente, esse prontuario e bem construido. As hipoteses estao levantadas com cuidado, sem precipitacao. A distincao entre o que foi elaborado cognitivamente e o que ainda nao foi elaborado afetivamente esta ali, clara. Isso e importante. Nao confunda insight intelectual com elaboracao. Sao coisas muito diferentes.

O que eu recomendaria atencao em sessoes futuras: o padrao de encerramento. Duas sessoes seguidas terminadas por demanda do analisando logo apos a interpretacao mais densa. Isso nao e coincidencia, e dado transferencial. E e justamente onde a analise vai, quando avancar, ter que trabalhar com mais forca.

Pesquisem Freud, A Interpretacao dos Sonhos, o capitulo sobre o trabalho onirico. Vale muito a pena.

E isso, gente. Um material humano rico, conduzido com seriedade. A estrada e longa, mas ja comecou.

Um beijo para todo mundo e ate logo.
"""

def main() -> None:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise EnvironmentError("ELEVENLABS_API_KEY nao encontrada no .env")

    client = ElevenLabs(api_key=api_key)

    print("Gerando audio... aguarde.")

    audio = client.text_to_speech.convert(
        text=TEXTO.strip(),
        voice_id="pieg5i1qSp1QH3RuGeEp",
        model_id="eleven_multilingual_v2",
        language_code="pt",
        voice_settings=VoiceSettings(
            stability=0.45,
            similarity_boost=0.80,
            style=0.35,
            speed=1.0,
            use_speaker_boost=True,
        ),
        apply_text_normalization="auto",
    )

    output_path = Path("audio_facci_opiniao.mp3")
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"Audio salvo em: {output_path.resolve()}")


if __name__ == "__main__":
    main()
