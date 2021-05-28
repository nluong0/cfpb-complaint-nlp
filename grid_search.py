'''
Performs grid search to determine model specification.
'''

import json
from datetime import datetime
from gensim.models import LdaModel, CoherenceModel
from preprocessing import get_sample, embedding

PATH = '/data/'
NGRAMS = 2


def train_models(params):
    '''
    Trains LDA models.

    Parameters 
        params: list of dictionaries containing model parameters
    '''
    models = {}
    count = 0

    for i in params:
        count += 1
        try:
            model = eval('LdaModel')(**i)
            if count % 5 == 0 and count > 0:
                print(f'{datetime.now()}    Model {count} created.')
            models[model] = {k: v for k, v in i.items() if k != 'corpus' and k != 'id2word'}
        except Exception as e:
            print(f'Model {count} failed.   ERROR: {str(e)}')

    return models
  

def model_selection(models, docs, dictionary):
    '''
    Calcalates coherence for models resulting from 
    grid search and selects best model based on 
    highest coherence.

    Parameters
        models: model of trained models 
        docs: list of complaint texts
        dictionary: dictionary of texts
    '''
    print(f'{datetime.now()}    Entering model_selection')
    coherences = []
    best_model = None 
    for model in models:
      coherencemodel = CoherenceModel(model=model,
                                      texts=docs,
                                      dictionary=dictionary,
                                      coherence='c_v')
      coherence = coherencemodel.get_coherence()
      coherences.append(coherence)

      if coherence == min(coherences):
        best_model = model
    
    best_model.save('/model/best_lda.model')
    return best_model


def run_grid_search(params, docs, dictionary): 
    '''
    Performs grid search.

    Parameters 
        params: list of dictionaries containing model parameters
        docs: list of complaint texts
        dictionary: dictionary of texts
    '''
    print(f'{datetime.now()}    Beginning grid search.')
    models = train_models(params)
    best_model = model_selection(models.keys(), docs, dictionary)
    best_model_params = models[best_model]
    print(f'{datetime.now()}    Ending grid search.')

    return best_model, best_model_params


def go():
    h = open(PATH + 'complaints_full.json')
    narratives = json.load(h)
    sample_keys = get_sample(narratives, 35000)
    sample_data = {i: narratives[i] for i in sample_keys}

    data, docs, dictionary, corpus = embedding(sample_data, NGRAMS)

    temp = dictionary[0] 
    id2word = dictionary.id2token

    params = [{'corpus': c, 'id2word': i2w, 'num_topics': num_topics, 'chunksize': chunksize, 'passes': passes, 
           'iterations': iterations, 'random_state': random_state} \
          for c in (corpus, ) \
          for i2w in (id2word, ) \
          for num_topics in (10, 15, 20) \
          for chunksize in (1000, 2000) \
          for passes in (20, 30) \
          for iterations in (25, 50) \
          for random_state in (1, )
          ]

    best_model, best_model_params = run_grid_search(params, docs, dictionary)

    return best_model, best_model_params



