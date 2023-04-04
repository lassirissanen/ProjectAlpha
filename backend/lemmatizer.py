import csv
import io
from libvoikko import Voikko

# Initialize the Voikko library for Finnish
v = Voikko("fi")

# Open the input and output CSV files
def database_lemmatization(input_file):
     # Open the input CSV file
    with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
        
        # Create a CSV reader object
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        # Create a string buffer to write the CSV data to
        csv_buffer = io.StringIO()
        
        # Create a CSV writer object
        writer = csv.writer(csv_buffer)
        
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

        return csv_buffer.getvalue()


# Lemmatizes the response messages of the customer
def response_lemmatization(response):
    # Lemmatize the text
    lemmas = []
    for word in response.split():
        lemma = v.analyze(word)[0]['BASEFORM']
        lemmas.append(lemma)
    lemmatized_text = ' '.join(lemmas)

    return lemmatized_text