#Import the Voikko library
from libvoikko import Voikko


#Define a Voikko class for Finnish
v = Voikko(u"fi")

#Some Finnish text
txt = "Tähän jotain suomenkielistä tekstiä. Väärinkirjoitettu yhdys-sana, pahus. tää on väärin kirjoitettua tkestiä, ihan niinkuiin tekstti viesteissä voi käydäppi. tähään toimiii juurri niin kuin sen pitäää"

#Pre-process the text
txt = txt.lower().replace(".", "").replace(",", "")

#Split to list by space character
word_list = txt.split(" ")

#Initialize a list for base form words
bf_list = []

#Loop all words in the list
for w in word_list:
  
  #Analyze the word with voikko
  voikko_dict = v.analyze(w)
    
  #Extract the base form, if the word is recognized
  if voikko_dict:
    bf_word = voikko_dict[0]['BASEFORM']
  #If word is not recognized, add the original word
  else:
    if len(v.suggest(w)) != 0:
      suggested_word = v.suggest(w)
      bf_word = suggested_word[0]
    else:
      bf_word = w
    
  #Append to the list
  bf_list.append(bf_word)
  
#Print results
print("Original:")
print(word_list)
print("Lemmatized:")
print(bf_list)