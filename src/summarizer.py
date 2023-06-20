import logging
from typing import List

import nltk
import numpy as np
import yake
import yaml
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from preprocess import remove_stopwords, remove_unwanted_words

with open("./conf/parameters.yml", "r") as stream:
    PARAMETERS = yaml.safe_load(stream)

logger = logging.getLogger(__name__)


def preprocess_text(text: str) -> List[str]:
    """
    Preprocesses the given text by removing unwanted words and tokenizes it into sentences.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        list: A list of tokenized sentences.
    """
    text = remove_unwanted_words(text)
    # Tokenize the text into sentences using nltk.tokenize.sent_tokenize
    sentences = nltk.sent_tokenize(text)
    # Perform text cleaning and preprocessing
    return sentences


def generate_sentence_embeddings(sentences: List[str]) -> np.ndarray:
    """
    Generates sentence embeddings using the Sentence-BERT model.

    Args:
        sentences (list): A list of sentences for which embeddings need to be generated.

    Returns:
        numpy.ndarray: An array of sentence embeddings.
    """
    model = SentenceTransformer(PARAMETERS["sentence_transfomer"])
    embeddings = model.encode(sentences)
    return embeddings


def calculate_similarity_scores(embeddings: np.ndarray) -> np.ndarray:
    """
    Calculates similarity scores between sentence embeddings using cosine similarity.

    Args:
        embeddings (numpy.ndarray): An array of sentence embeddings.

    Returns:
        numpy.ndarray: A similarity matrix representing the pairwise cosine similarities between sentences.
    """
    similarity_matrix = cosine_similarity(embeddings, embeddings)
    return similarity_matrix


def extract_top_sentences(
    sentences: List[str], similarity_matrix: np.ndarray, num_sentences: int
) -> List[str]:
    """
    Extracts the top-scoring sentences from a similarity matrix based on their importance scores.

    Args:
        sentences (list): A list of sentences.
        similarity_matrix (numpy.ndarray): A similarity matrix representing the pairwise cosine similarities between sentences.
        num_sentences (int): The number of top sentences to extract.

    Returns:
        list: A list of the top-scoring sentences for the summary.
    """
    # Calculate importance scores based on similarity matrix
    scores = similarity_matrix.sum(axis=1)
    # Sort sentences based on scores
    ranked_sentences = sorted(
        ((scores[i], s) for i, s in enumerate(sentences)), reverse=True
    )
    # Select top sentences for the summary
    top_sentences = [sentence for _, sentence in ranked_sentences[:num_sentences]]
    return top_sentences


def generate_extractive_summary(document_text: str, num_sentences: int) -> str:
    """
    Generates an extractive summary from the given document text.

    Args:
        document_text (str): The input document text.
        num_sentences (int): The desired number of sentences in the summary.

    Returns:
        str: The generated extractive summary.
    """
    logger.info("Generating summary...")

    # Preprocess the text and tokenize into sentences
    sentences = preprocess_text(document_text)

    # Generate sentence embeddings
    embeddings = generate_sentence_embeddings(sentences)

    # Calculate similarity scores
    similarity_matrix = calculate_similarity_scores(embeddings)

    # Extract top sentences for the summary
    summary_sentences = extract_top_sentences(
        sentences, similarity_matrix, num_sentences
    )

    # Concatenate summary sentences
    summary = " ".join(summary_sentences)

    return summary


def get_relevant_keywords(text: str) -> List[str]:
    """
    Extracts relevant keywords from the given text.

    Args:
        text (str): The input text.

    Returns:
        list: A list of relevant keywords extracted from the text.
    """
    logger.info("Extracting keywords...")

    document_text = remove_stopwords(text)
    # Extract relevant keywords
    kw_extractor = yake.KeywordExtractor(n=1, top=5, dedupLim=0.9, dedupFunc="seqm")
    keywords = kw_extractor.extract_keywords(document_text)

    relevant_keywords = []
    for kw in keywords:
        relevant_keywords.append(kw[0])

    return relevant_keywords


if __name__ == "__main__":
    log_fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    num_sentences = 3
    document_text = """Pedro Soares apontou que "cria enorme perplexidade ver dirigentes do BE a declararem que em matéria de guerra na Ucrânia a posição é a mesma do Governo português", 
    indicando que a posição do executivo "é a mesma da NATO".O porta-voz da moção E à XIII Convenção, Pedro Soares, defendeu este sábado que a geringonça "continua a marcar a linha política"
    do partido e criticou os deputados bloquistas por integrarem a comitiva que visitou a Ucrânia.  "A geringonça acabou mas perdura na cabeça de alguns e continua a marcar a nossa linha política", 
    criticou Pedro Soares durante a apresentação da moção E à XIII Convenção, que decorre entre este sábado e domingo em Lisboa.  O delegado, que é o rosto da oposição interna à atual direção, considerou 
    que o BE perdeu "influência política e social" e defendeu a necessidade de o partido "correr por fora, de forma autónoma e diferenciada" e se constituir como "alternativa e oposição à maioria absoluta".
    Pedro Soares, que esteve presente nas negociações que resultaram na geringonça, em 2015, indicou também as consequências "de anos de troca do programa" do partido "pela procura de acordos com o PS, sem
    qualquer base real de possibilidade, a não ser o abandono das suas bandeiras".  "Estamos aqui porque queremos lutar pelo diálogo e pela pluralidade. Por um Bloco com uma política de esquerda, polarizadora,
    com compromissos claros. Sim, com linhas vermelhas claras que não dê cobertura a uma espécie de social-democracia fora de tempo, cada vez mais liberal", afirmou, considerando que a "deriva para a 
    institucionalização é mortífera, transformaria o BE naquilo que não quis ser".    Críticas severas à posição do partido sobre Ucrânia  Loading...  Na sua intervenção, o ex-deputado falou também da 
    guerra na Ucrânia, realçando que se "exige a condenação inequívoca da Federação Russa pela invasão de um país soberano e solidariedade total com o povo ucraniano, que tem o direito de se defender".       Pedro Soares refere que "cria enorme perplexidade ver dirigentes do BE a declararem que em matéria 
    de guerra na Ucrânia a posição é a mesma do Governo português", indicando que a posição do executivo "é a mesma da NATO".  "Não menos perplexidade causa a integração do Bloco numa delegação parlamentar à 
    Ucrânia, a convite de um neonazi organizador das piores perseguições à oposição de esquerda na Ucrânia. O BE foi à Ucrânia fazer o quê? Comprometer-se com a posição euro-atlântica do prolongamento da 
    guerra e da escalada militar, foi corroborar o convite a um neonazi para discursar no nosso parlamento?", criticou.  O candidato à liderança do Bloco de Esquerda referia-se ao presidente da Assembleia 
    Nacional da Ucrânia que realizou o convite. Apontou ainda que, "se não foi nada disto", não ouviu "ainda uma única palavra de demarcação e de solidariedade com a oposição ucraniana cujos dirigentes ou 
    estão mortos ou estão presos". Sobre a vida interna do Bloco, Pedro Soares considerou que "o mal estar está instalado e transborda" e afirmou que a direção atual "não avalia os mais evidentes sinais de 
    crise".  "Os militantes e a opinião pública valorizam quem assume os seus erros e procura corrigi-los", defendeu, salientando que não basta "mudar os rostos" mas continuar com a mesma política.  
    Numa referência à moção adversária, de Mariana Mortágua, defendeu que "os tempos não estão para discursos vagos, do tipo uma vida boa para todas as pessoas", apontando que os tempos são "fraturantes e 
    exigem a clareza do compromisso político com o trabalho, com o ambiente, com os direitos mais elementares à saúde ou à habitação, e não ficar por declarações de princípio de largo espectro que não
    polarizam e só podem ter como desfecho a diluição da identidade" do Bloco. Pedro Soares avançou ainda com críticas à direita e à extrema-direita, afirmando que "são capazes de fazer o pino para que 
    o barulho do espetáculo se sobreponha à realidade social"""

    # Print the summary
    print(">>> Summary: ", generate_extractive_summary(document_text, num_sentences))
    # Print relevant keywords
    print(">>> Keywords: ", get_relevant_keywords(document_text))
