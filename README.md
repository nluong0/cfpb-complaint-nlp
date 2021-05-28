# Topic Modeling of CFPB Consumer Complaints
Extracting latent topics from CFPB consumer complaint narratives.

## Installation

In your preferred directory, clone the repository using git:

```bash
git clone https://github.com/nluong0/cfpb-complaint-nlp.git
```
Install required packages in a virtual environment:

```bash
pip3 install -r requirements.txt
```

## Structure

__download__ is a folder containing scripts to download and process CFPB data into JSON files.

__exploratory_analysis.ipynb__ performs exploratory analysis work prior to topic modeling tasks.

__preprocessing.py__ contains helper functions to perform all preprocessing necessary for input to LDA model.

__grid_search.py__ performs grid search on random sample to determine model specification.

__model.py__ builds and runs model resulting from grid search on full data and performs evaluation with coherence and perplexity.

__model__ is a folder that contains our final model.

__final_run_lda.ipynb__ executes preprocessing as well as building and running the final model.

__eval.ipynb__ executes evaluation of final model.

## Authors
The authors of this repository are Nguyen Luong and Ryan Webb, two graduate students at the University of Chicago.

## License
[MIT](https://choosealicense.com/licenses/mit/)

