import json
import math


class database(object):
    def __init__(self, file):
        self.file = file+".json"
        
    def load(self) :  
        with open('app/'+self.file) as json_file:
            db = json.load(json_file)
            json_file.close()
            return db
    
    def update(self, db):
        with open('app/'+self.file, 'w') as outfile:
            json.dump(db, outfile)
            outfile.close()

def exist(name, db):
    """
    Returns True if exists the name else False
    """
    exist = ["True" for i, s in enumerate(db) if name == s["name"]]
    if len(exist) > 0:
        return True
    else:
        return False
    
def ACH(inicio, final, afuera_i, afuera_f):
    """
    inicio - {CO2 adendtro t1, time}
    final -  {CO2 adentro t2, time}
    afuera_i {CO2 afuera t1, time}
    afuera_f {CO2 afuera t2, time}
    
    @returns ACH
    """
    ## separar la fecha de la hora ##########
    tiempo1 = inicio['name'].split('/')[1]
    tiempo1 = tiempo1.split(':')
    tiempo1 = [float(i) for i in tiempo1]
    
    tiempo2 = final['name'].split('/')[1]
    tiempo2 = tiempo2.split(':')
    tiempo2 = [float(i) for i in tiempo2]
    
    ## minutos a horas ######################
    tiempo1[1] = tiempo1[1] / 60
    tiempo2[1] = tiempo2[1] / 60
    ## segundos a horas #####################
    tiempo1[2] = tiempo1[2] / 3600
    tiempo2[2] = tiempo2[2] / 3600
    
    tiempo1 = tiempo1[0] + tiempo1[1] + tiempo1[2]
    tiempo2 = tiempo2[0] + tiempo2[1] + tiempo2[2]
    
    ## calculo de ACH #######################
    C_amb = afuera_f['value'] + afuera_i['value'] 
    C_amb = C_amb / 2
    C_start = inicio['value']
    C_end = final['value']
    x = (C_end - C_amb) / (C_start - C_amb)
    x = -1 * math.log(x)
    x = x / (tiempo2 - tiempo1)
    
    return x