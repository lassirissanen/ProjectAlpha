# https://www.section.io/engineering-education/creating-chatbot-using-natural-language-processing-in-python/
import pandas as pd
import string
import random
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer # It has the ability to lemmatize.
import tensorflow as tensorF # A multidimensional array of elements is represented by this symbol.
from tensorflow.keras import Sequential # Sequential groups a linear stack of layers into a tf.keras.Model
from tensorflow.keras.layers import Dense, Dropout

nltk.download("punkt")# required package for tokenization
nltk.download("wordnet")# word database

def tokenize(text):
  tokens = nltk.word_tokenize(text)
  tokens = [lm.lemmatize(word) for word in tokens]
  return tokens

def wordBag(text, vocab):
  tokens = tokenize(text)
  bagOwords = [0] * len(vocab)
  for w in tokens:
    for idx, word in enumerate(vocab):
      if word == w:
        bagOwords[idx] = 1
  return np.array(bagOwords)

# Get data from csv file  
df = pd.read_csv("responses.csv")

lm = WordNetLemmatizer() #for getting words. Works only in english

# lists
classes = list(df["class"].unique())
vocabulary = []
x = list(df["response"])
y = list(df["class"])

# Each intent is tokenized into words and the patterns and their associated tags are added to their respective lists.
for text in df["response"]:
  tokens = nltk.word_tokenize(text) # tokenize: "this is a sentence" -> ["this", "is", "a" "sentence"]
  vocabulary.extend(tokens)

vocabulary = [lm.lemmatize(word.lower()) for word in vocabulary if word not in string.punctuation] # set words to lowercase if not in punctuation

vocabulary = sorted(set(vocabulary))# sorting words
classes = sorted(set(classes))# sorting classes

trainingData = [] # training list array
outEmpty = [0] * len(classes)

# Bag Of Words (BoW) model
for idx, response in enumerate(x):
    bagOfwords = wordBag(response, vocabulary)

    # One hot encoding
    outputRow = list(outEmpty)
    outputRow[classes.index(y[idx])] = 1
    trainingData.append([bagOfwords, outputRow])

random.shuffle(trainingData)
trainingData = np.array(trainingData, dtype=object)# coverting our data into an array after shuffling

x = np.array(list(trainingData[:, 0]))
y = np.array(list(trainingData[:, 1]))


inputShape = (len(x[0]),)
outputShape = len(y[0])

# create model
model = Sequential()
model.add(tensorF.keras.layers.Dense(32, input_shape=inputShape, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(32, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(outputShape, activation = "softmax"))

md = tensorF.keras.optimizers.Adam(learning_rate=0.01)
model.compile(loss='categorical_crossentropy',
              optimizer=md,
              metrics=["accuracy"])

model.fit(x, y, epochs=15, verbose=1)

# This can be used to get prediction
def getClass(text):
    probabilities = model.predict(np.array([wordBag(text, vocabulary)]))
    prediction = probabilities.argmax(axis=-1)
    prediction = classes[prediction[0]]
