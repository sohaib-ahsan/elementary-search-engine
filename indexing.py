# IMPORTING THE REQUIRED LIBRARIES
import json
import time
import os
from collections import OrderedDict
from os import listdir
from nltk.tokenize import word_tokenize
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from os.path import isfile, join

# DEFINING THE PATH TO THE JSON FILES
path = r"E:\DSA Project\Elementry Search Engine\Backend\Dataset\nela-gt-2021"
with open ("Parse.txt", "r") as log:
    parsed_file = log.readline()
    
only_files = [f for f in listdir(path) if isfile(join(path, f))]
for i in range(len(only_files)):
    if(only_files[i] != parsed_file):
        only_files.pop(i)
    else:
        break

# DEFINING THE VARIABLES
article_Counter = 0
forward_indexing = {}
inverted_indexing = {}
stemmer = PorterStemmer()

# APPENDING THE NECESSARY WORDS TO BE REMOVED FROM THE ARTICLES
unused_words = [',', ';', '“', '”', ":"] + [chr(i) for i in range(33, 65)] + \
               [chr(i) for i in range(91, 97)] + [chr(i) for i in range(123, 128)]

# PARSING THE JSON FILES
start = time.time()
for file in only_files:
    with open(r"E:\DSA Project\Elementry Search Engine\Backend\Dataset\nela-gt-2021\\" + file, "r") as json_file:
        data = json.load(json_file)
    print(json_file)
    stems = []
    index = 0;
    if article_Counter >= 100000:
        break
    
    # DEFINING THE LIMIT OF THE NUMBER OF ARTICLES TO BE PARSED
    forward_indexing.update({file: {}})
    for dict in data:
        article_Counter += 1
        tokenized_text = word_tokenize(dict['title'] + dict['content'])
        stop_words = set(stopwords.words("english"))

        # FILTERING THE DATA IN JSON FILES
        title_content = [stemmer.stem(i) for i in tokenized_text if i not in unused_words and (i.isalpha() or len(i) == 4) and i not in stop_words]
        stems = mylist = list(dict.fromkeys(title_content))
        for i in stems:  
            if i in inverted_indexing and file not in inverted_indexing[i]:
                inverted_indexing[i].append(file)
            elif(i not in inverted_indexing):
                inverted_indexing.update({i: [file]})
                
            if(i not in forward_indexing[file]):
                forward_indexing[file].update({i:{index : title_content.count(i)}})
                        
            elif(i in forward_indexing[file]):
                forward_indexing[file][i].update({index : title_content.count(i)})
            forward_indexing[file][i] = OrderedDict(sorted(forward_indexing[file][i].items(), key=lambda x:x[1], reverse=True))
        index+=1
    json_file.close()
    
with open ("Parse.txt", "w") as log:
    log.write(file)
    
end = time.time() 
print(end - start) 
   
#WRITING FORWARD AND REVERSE INDEXING INTO JSON FILES
os.makedirs("Indexing")
with open(os.path.join("Indexing", "forward_indexing.json"), "w") as outfile:
    json.dump(forward_indexing, outfile)
    
with open(os.path.join("Indexing", "inverted_indexing.json"), "w") as outfile:
    json.dump(inverted_indexing, outfile)