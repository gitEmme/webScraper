from tensorflow.python.keras.preprocessing.text import Tokenizer
from nltk.tokenize import word_tokenize
import pickle
import numpy as np
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense, GRU, Embedding
from tensorflow.python.keras.optimizers import Adam
import gc
import matplotlib.pyplot as plt
import tensorflow as tf
from scipy.spatial.distance import cdist

#data relabeled to have a

def relabel_data():
    with open('stem_raw_labeled','rb') as f:
        data=pickle.load(f)
    f.close()
    datawords=[]
    for text,label in data:
        if(label=='neutral'):
            datawords.append((text,0.0))
        elif(label=='negative'):
            datawords.append((text, -1.0))
        elif (label == 'positive'):
            datawords.append((text, 1.0))
        else:
            print('['+label+']')
    print(len(datawords))
    with open('raw_num_labeled', 'wb') as f:
       pickle.dump(datawords,f)
    f.close()
    with open('raw_num_labeled', 'rb') as f:
        saved=pickle.load(f)
    f.close()
    print(saved[:2])
#split the dataset in train and test set percent%
def split_data(percent,length):
    return percent*length//100

## the following create the dictionary word: index and create the mapping array for each comment in the trainset
def rnn():
    with open('raw_num_labeled','rb') as f:
        data=pickle.load(f)
    f.close()
    dataset=[]
    for txt,label in data:
        dataset.append(txt)
    tokenizer=Tokenizer(num_words=None)
    tokenizer.fit_on_texts(dataset)
    print(len(tokenizer.word_index))
    print(len(dataset))
    index=split_data(80,len(data))
    train_set=data[:index]
    x_train=[]
    y_train=[]
    for txt, label in train_set:
        x_train.append(txt)
        y_train.append(label)
    test_set=data[index:]
    x_test=[]
    y_test=[]
    for txt,label in test_set:
        x_test.append(txt)
        y_test.append(label)
    print(len(train_set))
    print(len(test_set)+len(train_set))
    x_train_tokens=tokenizer.texts_to_sequences(x_train)
    print(np.array(x_train_tokens[1]))
    x_test_tokens=tokenizer.texts_to_sequences(x_test)
    print(np.array(x_test_tokens[1]))
    num_tokens = [len(tokens) for tokens in x_train_tokens + x_test_tokens]
    num_tokens = np.array(num_tokens)
    print('vector of lengths of comments:')
    print(num_tokens)
    print('mean value of length of comments:')
    print(np.mean(num_tokens))
    print('max number of tokens in a sequence:')
    print(np.max(num_tokens))
    max_tokens = np.mean(num_tokens) + 2 * np.std(num_tokens)
    max_tokens = int(max_tokens)
    print('The max number of tokens we will allow is set to the average plus 2 standard deviations')
    print(max_tokens)
    print('this will cover the '+str(np.sum(num_tokens < max_tokens) / len(num_tokens))+'  percent of the dataset')
    pad='pre'
    x_train_pad = pad_sequences(x_train_tokens, maxlen=max_tokens,padding=pad, truncating=pad)
    x_test_pad = pad_sequences(x_test_tokens, maxlen=max_tokens,padding=pad, truncating=pad)
    print('shape of train set')
    print(x_train_pad.shape)
    print('shape of test set')
    print(x_test_pad.shape)
    print('a padded train element looks as follow:')
    print(x_train_pad[1])

    #the following allows to get back text from the array rappresentation
    idx = tokenizer.word_index
    inverse_map = dict(zip(idx.values(), idx.keys()))

    def tokens_to_string(tokens):
        # Map from tokens back to words.
        words = [inverse_map[token] for token in tokens if token != 0]

        # Concatenate all words.
        text = " ".join(words)

        return text


    #we now create the RNN
    num_words = len(tokenizer.word_index)   #chose num_words=None creating the dictionary
    model = Sequential()
    embedding_size = 8
    model.add(Embedding(input_dim=num_words+1,
                        output_dim=embedding_size,
                        input_length=max_tokens,
                        name='layer_embedding'))
    model.add(GRU(units=16, return_sequences=True)) #first GRU with 16 outputs units
    model.add(GRU(units=8, return_sequences=True))
    model.add(GRU(units=4))     #add 3rd GRU, it will be followed by a dense-layer
    model.add(Dense(1,activation='sigmoid'))
    optimizer=Adam(lr=1e-3)     #this gives the learning rate
    model.compile(loss='binary_crossentropy',   #compile the keras model
                  optimizer=optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    model.fit(x_train_pad, y_train,
              validation_split=0.05, epochs=6, batch_size=64)
    result = model.evaluate(x_test_pad, y_test)
    print("Accuracy: {0:.2%}".format(result[1]))
    print(type(model))
    gc.collect() # avoid arror induced by different gc sequence, if python collect session first , the program will exit successfully, if python collect swig memory(tf_session) first, the program exit with failure.

rnn()
