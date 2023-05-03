import csv
import string
from libvoikko import Voikko

# Initialize the Voikko library for Finnish

# mac/linux
#v = Voikko("fi")

# windows
Voikko.setLibrarySearchPath("./Voikko")
v = Voikko(language="fi", path="./Voikko")


def remove_punctuation(text):
    # create a translation table with all punctuation characters
    translator = str.maketrans('', '', string.punctuation.replace('-', ''))

    # remove all punctuation characters from the string
    return text.translate(translator).replace('-', ' ')


# Lemmatizes the response messages of the customer
def response_lemmatization(response):
    # Lemmatize the text
    response = remove_punctuation(response)
    lemmas = []
    for word in response.split():
        lemma = v.analyze(word)
        if lemma:
            lemmas.append(lemma[0]['BASEFORM'])
        else:
            lemmas.append(word)
    lemmatized_text = ' '.join(lemmas)

    return lemmatized_text