from pprint import pprint
from gensim.models import LdaModel, CoherenceModel
from preprocessing import get_sample, embedding

DATA_DIR = '/data/'
PRODUCTS_FILEPATH = 'products.json'
COMPLAINTS_FILEPATH = 'complaints_full.json'
NGRAMS = 2


def load_and_sample_data(products_filepath, complaints_filepath, sample_size):
    # Load original complaint types
    g = open(products_filepath)
    complaint_types = json.load(g)

    # Load full complaints data
    h = open(complaints_filepath)
    narratives = json.load(h)

    # Create sample for defining model
    sample_keys = get_sample(narratives, sample_size)
    sample_data = {i: narratives[i] for i in sample_keys}

    # Save remainder of complaints for evaluation
    eval_keys = list(set(narratives.keys())-set(sample_keys))
    eval_data = {i: narratives[i] for i in eval_keys}

    return sample_data, eval_data


def run_model():

    # Load and sample data 
    products_filepath = DATA_DIR + PRODUCTS_FILEPATH
    complaints_filepath = DATA_DIR + COMPLAINTS_FILEPATH
    sample_data, eval_data = load_and_sample_data(products_filepath, complaints_filepath)

    # Preprocess and create word embeddings
    full_data, full_docs, full_dictionary, full_corpus = embedding(sample_data, NGRAMS)
    full_temp = full_dictionary[0] 
    full_id2word = full_dictionary.id2token

    # Build LDA Model with params from grid search
    full_model = LdaModel(corpus=full_corpus,
                            id2word=full_id2word,
                            num_topics=15,
                            chunksize=1000,
                            passes=30,
                            iterations=25,
                            random_state=1
    )
    full_model.save('/model/full_lda.model')

    # Calculate coherence and log perplexity
    coherence_model = CoherenceModel(model=full_model, 
                                     texts=full_docs, 
                                     dictionary=full_dictionary, 
                                     coherence='c_v')
    coherence_lda = coherence_model.get_coherence()
    print('Coherence Score: ', coherence_lda)
    print('Perplexity Score: ', full_model.log_perplexity(full_corpus))

    return full_model, full_docs, full_dictionary, full_corpus

