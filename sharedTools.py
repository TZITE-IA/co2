import json

class database(object):
    def __init__(self, file):
        self.file = file+".json"
        
    def load(self):
        with open('app/db.json') as json_file:
            db = json.load(json_file)
            json_file.close()
            return db
    
    def update(self, db):
        with open('app/db.json', 'w') as outfile:
            json.dump(db, outfile)
            outfile.close()
