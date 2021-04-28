import json
import string
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords

def preprocessing():

    f = open('narratives.json')
    data = json.load(f)

    punctuation = str.maketrans('', '', string.punctuation)
    stop_words = set(stopwords.words('english'))  

    for id, narrative in data:
        # Preprocessing tasks
        tokens = word_tokenize(narrative.lower()) # lower case & tokenize
        stripped = [w.translate(punctuation) for w in tokens] # strip punctuation
        words = [word for word in stripped if word.isalnum()] # remove non-alphabetic-numeric words
        words = [w for w in words if not w in stop_words] # remove stopwords
        words = [w if w  != len(w) * w[0] else '~' for w in words] # replace 'xxx' with '~' 
        words = [w if not w.isdigit() else '*' for w in words] # replace numbers with '*'

        # Replace narratives in data with preprocessed tasks
        data[id] = words 
