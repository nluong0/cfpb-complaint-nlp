import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

import string
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.util import ngrams
from gensim.corpora import Dictionary
import random


def get_sample(data, size):
    '''
    Takes a dictionary and a sample size and pulls randomly from the dictionary.

    Parameters
        data: json of complaints
        size: desired sample size
    '''
    key_list = [i for i in data.keys()]
    sample_keys = random.sample(key_list, size)

    return sample_keys


def preprocessing(data, n):
    '''
    Performs preprocessing tasks on raw data.

    Parameters
        data: json of complaints 
        n: desired n for ngrams
    '''
    punctuation = str.maketrans('', '', string.punctuation)
    stop_words = set(stopwords.words('english'))
    wnl = WordNetLemmatizer()
    rv = {}
    bad_ids = []

    for id, narrative in data.items():
        # Preprocessing tasks
        tokens = word_tokenize(narrative.lower()) # lower case & tokenize
        stripped = [w.translate(punctuation) for w in tokens] # strip punctuation
        words = [word for word in stripped if word.isalnum()] # remove non-alphabetic-numeric words
        words = [w for w in words if not w in stop_words] # remove stopwords
        words = [w if w  != len(w) * w[0] else '~' for w in words] # replace 'xxx' with '~' 
        words = [w if not w.isdigit() else '*' for w in words] # replace numbers with '*'
        words = [wnl.lemmatize(w) for w in words] # lemmatize

        # Remove consecutive duplicates of '~' or '*'
        final_words = []
        for i in range(0,len(words)):
          if i==0:
            final_words.append(words[i])
          else:
            if not((words[i] == '*' and final_words[-1]=='*'
                    ) or (
                        words[i] == '~' and final_words[-1]=='~')):
                final_words.append(words[i])

        # Create ngrams
        try:
          ngram_tuples = list(ngrams(final_words, n))
          ngram_words = [' '.join(ngram_tuple) for ngram_tuple in ngram_tuples]

          # Replace narratives in data with preprocessed text
          rv[id] = ngram_words

        except:
          bad_ids.append(id)
    
    return rv


def embedding(data, n):
    '''
    Creates word embeddings.

    Parameters
        data: json of complaints 
        n: desired n for ngrams
    '''
    data = preprocessing(data, n)
    docs = list(data.values())
    dictionary = Dictionary(docs) 

    # Filter out words that occur less than 20 documents, or more than 50% of the documents.
    dictionary.filter_extremes(no_below=20, no_above=0.5) 

    corpus = [dictionary.doc2bow(doc) for doc in docs]

    return data, docs, dictionary, corpus