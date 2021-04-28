import pandas as pd
import subprocess
from datetime import date

#import requests
# def go():
#     url = 'https://www.consumerfinance.gov/data-research/consumer-complaints/search/api/v1/?size=2000&no_aggs=true&has_narrative=true' 
#     r = requests.get(url) 
#     complaint_list = [i['_source'] for i in r.json()['hits']['hits']] 
#     df = pd.DataFrame(complaint_list)
#     total_matches = r.json()['hits']['total'] 
#     assert total_matches == len(df)

def download_complaints():
    try:
        subprocess.call(['sh', 'download.sh'])
    except Exception as e:
        print(f'Failed download: {e}')

def go():
    with open('complaints.json') as f:
        old_complaints = json.load(f)
    old_num_complaints = len(old_complaints)

    download_complaints()
    
    with open('complaints.json') as f:
        new_complaints = json.load(f)
    new_num_complaints = len(new_complaints)

    print(f'{new_num_complaints - old_num_complaints} complaints with narrative have been sumitted.')

                            
if __name__ == '__main__':
    go()