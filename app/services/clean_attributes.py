from typing import List
import numpy as np

from gensim.parsing.preprocessing import remove_stopwords, strip_punctuation, strip_numeric, strip_non_alphanum, strip_multiple_whitespaces, strip_short
from textblob import TextBlob, Word

def ingridients(
    items: List[str]
):
    total_ingredients = []
    for item in items:
        item = item.lower()
        item = remove_stopwords(item)
        item = strip_numeric(item)
        item = strip_short(item,2)
        item = strip_multiple_whitespaces(item)
        item = strip_punctuation(item)
        item = strip_non_alphanum(item)
        item = (" ".join(TextBlob(item).words.singularize()))
        if item: 
            total_ingredients.append(item)
    
    return total_ingredients


def instruction(
    details: List[str]
):
    total_details= []
    for detail in details.split("."):
        detail = detail.lower()
        detail = remove_stopwords(detail)
        detail = strip_numeric(detail)
        detail = strip_short(detail,2)
        detail = strip_multiple_whitespaces(detail)
        detail = strip_punctuation(detail)
        detail = strip_non_alphanum(detail)
        detail = (" ".join(TextBlob(detail).words.singularize()))

        if detail: 
            total_details.append(detail.split())

    return total_details


#defined functions to get to embeddings for recipes
def get_sentence_embeddings(sentence, model):
    embeddingList = []
    for word in sentence:
        try:
            vector1 = model.wv[word]
            embeddingList.append(vector1)
        except Exception as e:
            continue
    sumEmbeddings = sum(embeddingList)
    return np.true_divide(sumEmbeddings, len(embeddingList))


def embeddings(instructions: List[str], fasttext_model):
    embeddingList = []
    for sentence in instructions:
        embeddingList.append(get_sentence_embeddings(sentence, fasttext_model))
    sumEmbeddings = sum(embeddingList)
    return np.true_divide(sumEmbeddings, len(instructions))  
    