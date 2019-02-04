import io
import keras
import numpy as np
import pandas as pd
import string

from keras.models import Sequential
from keras.models import load_model

MAX_NAME_LENGTH = 20

def get_model():
    global model
    model = load_model('./gender_from_name_classifier.h5')
    print('get_model(): Model loaded successfully')

def predict(name):
    name = preprocess_name(name)
    vector = string_to_vec(name)
    vector.resize((MAX_NAME_LENGTH,))
    prediction = model.predict_classes(np.array([vector,]))
    return prediction[0][0]

def string_to_vec(name):
    dictionary = {key: value for (value, key) in enumerate(string.ascii_lowercase,1)}
    vector = []
    for letter in name:
        if (letter in dictionary or letter.lower() in dictionary):
            vector.append(dictionary[letter.lower()])
    return np.array(vector)

def preprocess_name(name):
    # Light sanitisation. The vectorisation function is already protected against non-alphabetic chars.
    name = name.strip(' ')
    name = name.replace('\\','')
    name = name.replace('/','')
    # The resulting vector can be no longer than 20 chars long. We may introduce a truncation error here.
    if len(name) > 20:
        name = name[:20]
    return name

def retrain_model(data):
    # Randomly split the dataset into a training set and a testing set 80:20
    df = process_trainingdata(data)
    train = df.sample(frac=0.8,random_state=np.random.RandomState())
    test = df.drop(train.index)
    train = train.reset_index(drop=True)
    test = test.reset_index(drop=True)

    # Separate the data from the labels
    train_data = train.Name.values
    train_labels = train.Labels.values

    test_data = test.Name.values
    test_labels = test.Labels.values

    train_data = keras.preprocessing.sequence.pad_sequences(train_data, value=0, padding='post', maxlen=20)
    test_data = keras.preprocessing.sequence.pad_sequences(test_data,value=0, padding='post', maxlen=20)
    
    model.fit(train_data, train_labels, epochs=20, batch_size=5000, validation_data=(test_data, test_labels), verbose=1)     
    return

def process_trainingdata(data):
        # Obtain existing training data
        original_data = pd.read_csv('./data/name_gender_data.csv',header=None, usecols=[0,1],names=['Name','Gender'])
        # Now process incoming data
        incoming_data = pd.DataFrame(data)
        # Ignore other columns
        incoming_data = incoming_data[[0,1]]
        incoming_data.columns = ['Name','Gender']
        df = pd.concat([original_data,incoming_data], ignore_index=True)
        df['Labels'] = df.Gender
        df.Labels.replace(to_replace='M',value=0,inplace=True)     
        df.Labels.replace(to_replace='F',value=1,inplace=True)
        for i in range(0,len(df.Name)):
            df.at[i,"Name"] = string_to_vec(df.at[i,"Name"])
        return df