import pickle


# relabel data set as tuple (text,integer) given an ordered list of label present in the data set (sourceFile) and save the relabeled data set in destFile

def relabel_data(sourceFile,label_list,destFile):
    with open(sourceFile,'rb') as f:
        data=pickle.load(f)
    f.close()
    dataset=[]
    for text,label in data:
        dataset.append((text,label_list.index(label)))
    with open(destFile, 'wb') as f:
       pickle.dump(dataset,f)
    f.close()

# save a list with all the raw text in the data set passed in the source file

def dictionary_data_set(sourceFile,destFile):
    with open(sourceFile, 'rb') as f:
        data = pickle.load(f)
    f.close()
    dataset = []
    for text, label in data:
        dataset.append(text)
    with open(destFile, 'wb') as f:
        pickle.dump(dataset, f)
    f.close()


#split the dataset in train and test set percent%
def split_data(percent,length):
    return percent*length//100