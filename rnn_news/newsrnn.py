from tensorflow.python.keras.preprocessing.text import Tokenizer
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
import pymongo

client=pymongo.MongoClient('localhost')
### tensorboard --logdir==training:/home/dude/PycharmProjects/Rnn_Sentiment/rnn_news/Graph/ --host=127.0.0.1
##  go to http://127.0.0.1:6006

def relabel_data():
    with open('rawtext_labeled','rb') as f:
        data=pickle.load(f)
    f.close()
    datawords=[]
    dataset=[]
    for text,label in data:
        dataset.append(text)
        if(label=='neutral'):
            datawords.append((text,1))
        elif(label=='negative'):
            datawords.append((text, 2))
        elif (label == 'positive'):
            datawords.append((text, 0))
        else:
            print('['+label+']')
    print(len(datawords))
    with open('raw_labeled_num', 'wb') as f:
       pickle.dump(datawords,f)
    f.close()
    with open('alldata', 'wb') as f:
        pickle.dump(dataset, f)
    f.close()
    with open('raw_labeled_num', 'rb') as f:
        saved=pickle.load(f)
    f.close()
    print(saved[:2])

#relabel_data()
#split the dataset in train and test set percent%
def split_data(percent,length):
    return percent*length//100

## the following create the dictionary word: index and create the mapping array for each comment in the rrn_news
def rnn():
    with open('data_files/raw_labeled_num','rb') as f:
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

    y_train = tf.keras.utils.to_categorical(y_train, num_classes=3)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=3)

    #we now create the RNN
    num_words = len(tokenizer.word_index)   #chose num_words=None creating the dictionary
    print(num_words)
    model = Sequential()
    embedding_size = 8
    model.add(Embedding(input_dim=num_words+1,
                        output_dim=embedding_size,
                        input_length=max_tokens,
                        name='layer_embedding'))
    model.add(GRU(units=16, return_sequences=True)) #first GRU with 16 outputs units
    model.add(GRU(units=8, return_sequences=True))
    model.add(GRU(units=4))     #add 3rd GRU, it will be followed by a dense-layer
    model.add(Dense(3,activation='softmax'))
    optimizer=Adam(lr=1e-3)     #this gives the learning rate
    model.compile(loss='categorical_crossentropy',   #compile the keras model
                  optimizer=optimizer,
                  metrics=['accuracy'])
    print(model.summary())
    tbCallBack=tf.keras.callbacks.TensorBoard(log_dir='./Graph', histogram_freq=0,write_graph=True, write_images=True)

    model.fit(x_train_pad, y_train,
              validation_split=0.05, epochs=100, verbose=1, batch_size=64,shuffle=True,callbacks=[tbCallBack])
    result = model.evaluate(x_test_pad, y_test)
    print("Accuracy: {0:.2%}".format(result[1]))
    print(type(model))
    tf.keras.models.save_model(
        model,
        'news100model.hdf5',
        overwrite=True,
        include_optimizer=True
    )
    model.save_weights('saved_networks/news100net.h5')
    gc.collect()  # avoid arror induced by different gc sequence, if python collect session first , the program will exit successfully, if python collect swig memory(tf_session) first, the program exit with failure.



def classify():
    model=tf.keras.models.load_model(
        'saved_networks/newsmodel.hdf5',
        custom_objects=None,
        compile=True
    )
    with open('data_files/raw_labeled_num','rb') as f:
        data=pickle.load(f)
    f.close()
    dataset=[]
    for txt,label in data:
        dataset.append(txt)
    tokenizer=Tokenizer(num_words=None)
    tokenizer.fit_on_texts(dataset)
    for comment in client.spiegel.auto.find(no_cursor_timeout=True):
        texts = []
        texts.append(comment['body'])
        tokens = tokenizer.texts_to_sequences(texts)
        pad='pre'
        max_tokens=103
        tokens_pad = pad_sequences(tokens, maxlen=max_tokens,padding=pad, truncating=pad)
        #print(tokens_pad[0])
        #print(tokens_pad.shape)
        #print(model.predict(tokens_pad))
        #client.spiegel.auto.update({'_id': comment['_id']}, {"$set": {'sentiment': float(model.predict(tokens_pad)[0][0])}},upsert=True)
        print(model.predict(tokens_pad)[0])
    #print(model.predict(tokens_pad))
    gc.collect()

rnn()
#classify()


