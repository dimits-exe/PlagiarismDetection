import sys,os
import math

class Distance:

    def __init__(self,name_i,name_j,dist):
        self.i = name_i
        self.j = name_j
        self.score = dist * 100 #improve readability

    def __str__(self):
        return f"{self.i} - {self.j} with a {self.score:.4f} similarity score"
    

# distance function
def row_dist(a, b, word_dict):
    sum_ = 0
    for ai, bi in zip(a, b):    #find squared distance
        sum_ = sum_ + (word_dict[ai] - word_dict[bi])**2 
    return math.sqrt(sum_)

def sorted_pairs(data, file_names, word_dict):
    """
    Returns a list of Distance objects representing pairs of documents, sorted by the similarity of each pair.
    The 1st item on the list will contain the most similar pair of documents.\n

    data = The contents of each file
    file_names = The name of each file
    word_dict = a TF-IDF dictionary of all words in the documents 
    """
    N = len(data)
    dist = []

    for i in range(N):
        for j in range(N):
            if i > j: #2D symmetrical array --> list 
                dist.append(Distance(file_names[i], file_names[j], row_dist(data[i],data[j], word_dict)))

    return sorted(dist, key = lambda d : d.score)

def load_words(all_contents):
    """
    Takes a list containing the content of each document.
    Returns a list of the words from each document, and the set of all words in *all* documents.
    """
    docs = []       # text for each files in directory
    words = set()   # list of unique words that appear in it

    for file_contents in all_contents:
        docs.append(file_contents.split())
        for word in file_contents.split():
            words.add(word)

    return docs, words

def get_files(dir, txt_only, ignore_list):
    """
    Gets all files from a given directory, filters the ones who are in text form. 
    Returns a list of all suitable file names and a list of their contents.\n

    dir = the directory where the files are situated\n
    txt_only = True if only .txt files are allowed, False if all non-binary files are allowed\n
    ignore_list = a list with all the files to be ignored (such as the programs source files)
    """
    files = []
    contents = []
    for file in os.listdir(dir):
        if ((not txt_only or file.endswith(".txt"))     # ignore check if txt_only is true
        and not os.path.isdir(os.path.join(dir, file))  # ignore directories
        and file not in ignore_list):                   # ignore program files

            acceptable = True # whether or not the file can be read

            # read file content
            try:
                f_handle = open(os.path.join(dir, file), mode='r')
                content = f_handle.read().lower()
            except UnicodeDecodeError:
                print("Ignored binary file " + file)
                acceptable = False
            except PermissionError:
                print("Ignored locked file " + file)
                acceptable = False
            finally:
                f_handle.close()

            # store file content
            if content.isspace() or content == "":
                print("Ignored empty file " + file)
            elif acceptable:
                files.append(file)
                contents.append(content)

    return files, contents
            

def TFIDF(dir, txt_only, ignore_list):
    """
    Performs the TF-IDF algorithm where every suitable file in the given directory is a 'document'.\n
    Returns a list of Distance objects representing pairs of documents, sorted by the similarity of each pair.
    The 1st item on the list will contain the most similar pair of documents.\n

    dir = the directory where the files are situated\n
    txt_only = True if only .txt files are allowed, False if all non-binary files are allowed\n
    ignore_list = a list with all the files to be ignored (such as the programs source files)
    """
    file_names, contents = get_files(dir, txt_only, ignore_list)
    print(file_names)
    if len(file_names) == 0:
        raise ValueError("No suitable files found")

    docs, words = load_words(contents)
    
    # go over each unique word and calculate its term frequency, and its document frequency
    term_freq = dict()
    for word in words:
        term_freq[word] = sum(doc.count(word) for doc in docs) / len(words)
   
    doc_freq = dict()
    for word in words:
        occurences = 0
        doc_freq[word] = 0
        for doc in docs:
            if word in doc:
                occurences = 1
            doc_freq[word] += occurences/len(docs)

    # go over each line in the text and calculate its TF-IDF representation, which will be a vector
    TFIDF_dict = dict()
    for word in words:
        TFIDF_dict[word] = term_freq[word]*math.log(1/doc_freq[word],10)

    # calculate the distances between each line to find which are the closest.
    return sorted_pairs(docs, file_names, TFIDF_dict)

