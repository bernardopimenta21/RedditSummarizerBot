import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def remove_unwanted_words(string: str) -> str:
    """
    Removes unwanted words or patterns from the given string.

    Args:
        string (str): The input string to clean.

    Returns:
        str: The cleaned string.
    """
    string = string.replace("\xa0", " ")

    unwanted_patterns = [
        "(?i)(?<=\.).*?Subscreva as newsletters.*?\.",
        "(?i)Leia Também[\s\S]*",
        "(?i)Ver Twitter",
        "(?i)PartilharPartilhar no FacebookTwitterEmailWhatsappPartilhar[\s\S]*",
        "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",  # remove emails
        "(?i)(?<=\.).*?FacebookTwitterWhatsAppE-mailPartilharComentar",
        "(?i)FecharSubscrever newsletter[\s\S]*?Subscrever",
        "(?i)Partilhar este artigoFacebookTwitterWhatsAppE-mailPartilharComentários[\s\S]*",
        "(?i)Para continuar a ler[\s\S]*",
        "(?i)Os leitores são a força e a vida do jornal[\s\S]*",
        "(?i)(?<=\.).*?FacebookTwitterPartilharComentar",
        "(?:(?<=\.)|^)*[\s\S]*FacebookTwitterPartilharComentar",
        "\(\.\.\.\)",
        "(?i)\bpub\b",
        "(?i)Enviar Comentário[\s\S]*",
        "(?:(?<=\.)|^)*[\s\S]*LogoutEm Destaque",
    ]
    # Remove the matching substrings
    cleaned_string = string
    for pattern in unwanted_patterns:
        cleaned_string = re.sub(pattern, " ", cleaned_string)

    return cleaned_string


def remove_stopwords(text: str) -> str:
    """
    Removes stopwords from the given text.

    Args:
        text (str): The input text to process.

    Returns:
        str: The text with stopwords removed.
    """
    # Download stopwords if not already downloaded
    nltk.download("stopwords")

    # Get the list of stopwords for English
    stop_words = set(stopwords.words("portuguese"))

    # Read the custom stopwords from the text file
    with open("./conf/pt_stopwords.txt", "r") as file:
        custom_stopwords = file.read().splitlines()

    stop_words.update(custom_stopwords)

    # Tokenize the text into individual words
    words = word_tokenize(text)

    # Remove stopwords from the list of words
    filtered_words = [word for word in words if word.casefold() not in stop_words]

    # Join the filtered words back into a single string
    filtered_text = " ".join(filtered_words)

    return filtered_text
