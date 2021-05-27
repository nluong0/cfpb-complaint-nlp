import json

def load_text_data():
    complaints = {}
    data = None
    with open('complaints.json') as file: 
        data = json.load(file) 
    
    for i in data:
        complaints[i['_id']] = i['_source']['complaint_what_happened']
    
    with open("narratives.json", "w") as outfile: 
        json.dump(complaints, outfile)

if __name__ == '__main__':
    load_text_data()