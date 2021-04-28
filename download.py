import json
import gzip

def load_data():
    complaints = None
    with open('complaints.json') as file: 
        data = json.load(file) 
        complaints = [(i['_id'], i['_source']['complaint_what_happened']) for i in data]

    with gzip.open('complaints_list.gz', 'wb') as f:
        f.write(complaints)

if __name__ == '__main__':
    load_data()()