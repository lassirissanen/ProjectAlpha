# https://medium.com/holler-developers/intent-detection-using-sequence-models-ddae9cd861ee

# base class imports 
import pandas as pd
import numpy as np
import tensorflow as tf
import io

# sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# keras
from keras import utils
from keras.preprocessing.text import Tokenizer
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Dropout

# lemmatizer import
from lemmatizer import response_lemmatization

df = pd.read_csv("responses.csv")
df["response"] = [response_lemmatization(res) for res in df["response"]]

TEST_SPLIT = 0.1
RANDOM_STATE = 10
np.random.seed(RANDOM_STATE)
tf.random.set_seed(RANDOM_STATE)

#Split the dataset into train and test
x_train, x_test, y_train, y_test = train_test_split(df["response"], df["class"], 
                                                    test_size = TEST_SPLIT, random_state = RANDOM_STATE)

#Initialize a Tokenizer
tokenizer = Tokenizer()
tokenizer.fit_on_texts(list(x_train))

#Convert text to sequences
x_seq = tokenizer.texts_to_sequences(list(x_train))
x_test_seq = tokenizer.texts_to_sequences(list(x_test))

MAX_SEQ_LEN = 35

#Pad the sequences
x = utils.pad_sequences(x_seq, maxlen = MAX_SEQ_LEN, padding='post')
x_test = utils.pad_sequences(x_test_seq, maxlen = MAX_SEQ_LEN, padding='post')

#Convert labels to one-hot vectors
y = y_train.to_numpy()
encoder = LabelEncoder()
encoder.fit(y)

encoded_y = encoder.transform(y)
y_train_encoded = utils.to_categorical(encoded_y)

y_test = y_test.to_numpy()
encoded_y_test = encoder.transform(y_test)
y_test_encoded = utils.to_categorical(encoded_y_test)

VAL_SPLIT = 0.1
BATCH_SIZE = 32
EPOCHS = 20
EMBEDDING_DIM = 32
NUM_UNITS = 32
NUM_CLASSES = len(df['class'].unique())
VOCAB_SIZE = len(tokenizer.word_index) + 1

model = None
try:
    model = tf.keras.models.load_model('models/model_v1')
except:

    #Define a LSTM model
    model = Sequential()
    model.add(Embedding(input_dim = VOCAB_SIZE, output_dim = EMBEDDING_DIM, input_length = MAX_SEQ_LEN, mask_zero = True))
    model.add(LSTM(NUM_UNITS, activation='relu'))
    model.add(Dense(NUM_UNITS, activation='relu'))
    model.add(Dropout(0.4))
    model.add(Dense(NUM_CLASSES, activation='softmax'))

    #Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

    #Fit the model on training data
    lstm_history = model.fit(x, y_train_encoded, batch_size = BATCH_SIZE, epochs = EPOCHS, verbose = 1, validation_split = VAL_SPLIT)
    model.save('models/model_v1')

    model.evaluate(x_test, y_test_encoded)

# This can be used to get prediction
def tensorflow_classifier(text):
    sequence = tokenizer.texts_to_sequences([text])
    sequence = utils.pad_sequences(sequence, maxlen=MAX_SEQ_LEN, padding="post")
    probabilities = model.predict(sequence)
    prediction = probabilities.argmax(axis=-1)
    print(probabilities)
    intent_class = encoder.classes_[prediction[0]] if probabilities.max() > 0.5 else "unknown"
    return intent_class

def tensorflow_test_model(text, prob_margin):
    lemmatized_text = response_lemmatization(text)
    sequence = tokenizer.texts_to_sequences([lemmatized_text])
    sequence = utils.pad_sequences(sequence, maxlen=MAX_SEQ_LEN, padding="post")
    probabilities = model.predict(sequence)
    prediction = probabilities.argmax(axis=-1)
    intent_class = encoder.classes_[prediction[0]] if probabilities.max() > prob_margin else "unknown"
    classification_verdict = "success" if intent_class != "unknown" else "failure"
    data = {
        "verdict": classification_verdict,
        "class": intent_class,
        "classification_probability": probabilities.max(),
        "probabilities": list(probabilities)
    }
    return data

