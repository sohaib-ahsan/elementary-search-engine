import json
import time
from collections import OrderedDict
from nltk.stem.porter import PorterStemmer

start = time.time()
with open(r'E:\DSA Project\Elementry Search Engine\Backend\Indexing\forward_indexing.json', "r") as json_file:
        forward_indexing = json.load(json_file)
with open(r'E:\DSA Project\Elementry Search Engine\Backend\Indexing\inverted_indexing.json', "r") as json_file:
        inverted_indexing = json.load(json_file)
stemmer = PorterStemmer()
     
def getWords():
    word = input("Enter he word to be searched: ").split()
    word = [stemmer.stem(i) for i in word]
    total_articles = {}
    for i in word:
        document_count = 0
        for file in inverted_indexing[i]:
            if(document_count == 5):
                break
            document_count +=1
            count = 0
            with open(r"E:\DSA Project\Elementry Search Engine\Backend\Dataset\nela-gt-2021\\" + file, "r") as json_file:
                data = json.load(json_file)
            for index in forward_indexing[file][i]: 
                if(count == 2):
                    break
                if(i in data[int(index)]["title"].lower()):
                    print(data[int(index)]["title"])
                else:
                    total_articles[file, index] =  forward_indexing[file][i][index]
                count+=1
            json_file.close()
            
    total_articles = OrderedDict(sorted(total_articles.items(), key=lambda x:x[1], reverse=True))
    
    for file_index in total_articles: 
        with open(r"E:\DSA Project\Elementry Search Engine\Backend\Dataset\nela-gt-2021\\" + file_index[0], "r") as json_file:
                data = json.load(json_file)
        print(data[int(file_index[1])]["title"])
        json_file.close()
        
getWords()
end = time.time() 
print(end - start)     