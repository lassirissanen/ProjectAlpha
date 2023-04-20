import csv
import string
from libvoikko import Voikko

# Initialize the Voikko library for Finnish

# mac/linux
v = Voikko("fi")

# windows
#Voikko.setLibrarySearchPath("./Voikko")
#v = Voikko(language="fi", path="./Voikko")

# Open the input and output CSV files
def database_lemmatization(input_file):
     # Open the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        with open('responses_lemmatized.csv', 'w', newline='') as updatedfile:
            # Create a CSV reader object
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            
            # Create a CSV writer object
            writer = csv.writer(updatedfile)
            
            # Iterate over the rows in the input file
            for row in reader:
                # Lemmatize the text in the current row
                lemmas = []
                for word in row[0].split():
                    
                    lemma = v.analyze(word)
                    #Extract the base form, if the word is recognized
                    if lemma:
                        bf_word = lemma[0]['BASEFORM']
                    #If word is not recognized, add the original word
                    else:
                        bf_word = word
                    lemmas.append(bf_word)
                lemmatized_text = ' '.join(lemmas)
                
                # Write the lemmatized text to the output file along with the label
                writer.writerow([lemmatized_text, row[1]])

    return 'responses_lemmatized.csv'

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