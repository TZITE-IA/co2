import json
import math


def ACH(ambiente, lateral, central, dt):
    
    ## promedio del CO2 ambiental ###########
    C_amb = ambiente[0] + ambiente[1] 
    C_amb = C_amb / 2
    
    ## aportación de la fuente de CO2 #######
    f = lateral[1] - float(lateral[0])
    
    ## reescalamiento del CO2 interior ######
    C_start = float(central[0])
    C_end = central[1] - f
    
    ## ACH ##################################
    x = (C_end - C_amb) / (C_start - C_amb)
    x = -1 * math.log(x)
    x = x / dt
        
    return x, f
    

def clean_noise(signal):
    
    new_signal = []
    t = len(signal) - 1   
    ## savitsky-golay smoothing ##############################
    for i in range(t+1):
        
        ## padding in the left signal edge ###################
        if i == 0: 
            y = -21*signal[0] + 14*signal[0] + 39*signal[0] + 54*signal[0]
            y = y + 59*signal[0] + 54*signal[1] + 39*signal[2] + 14*signal[3] - 21*signal[4]
            y = y / 231
            new_signal.append(y)
        elif i == 1:
            y = -21*signal[0] + 14*signal[0] + 39*signal[0]
            y = y + 54*signal[0] + 59*signal[1] + 54*signal[2] + 39*signal[3] + 14*signal[4] - 21*signal[5]
            y = y / 231
            new_signal.append(y)
        elif i == 2:
            y = -21*signal[0] + 14*signal[0]
            y = y + 39*signal[0] + 54*signal[1] + 59*signal[2] + 54*signal[3] + 39*signal[4] + 14*signal[5] - 21*signal[6]
            y = y / 231
            new_signal.append(y)
        elif i == 3:
            y = -21*signal[0]
            y = y + 14*signal[0] + 39*signal[1] + 54*signal[2] + 59*signal[3] + 54*signal[4] + 39*signal[5] + 14*signal[6] - 21*signal[7]
            y = y / 231
            new_signal.append(y)
            
        ## padding in the right signal edge ###################
        elif i == t-3:
            y = -21*signal[t-7] + 14*signal[t-6] + 39*signal[t-5] + 54*signal[t-4] + 59*signal[t-3] + 54*signal[t-2] + 39*signal[t-1] + 14*signal[t]
            y = y - 21*signal[t]
            y = y / 231
            new_signal.append(y)
        elif i == t-2:
            y = -21*signal[t-6] + 14*signal[t-5] + 39*signal[t-4] + 54*signal[t-3] + 59*signal[t-2] + 54*signal[t-1] + 39*signal[t]
            y = y + 14*signal[t] - 21*signal[t]
            y = y / 231
            new_signal.append(y)
        elif i == t-1:
            y = -21*signal[t-5] + 14*signal[t-4] + 39*signal[t-3] + 54*signal[t-2] + 59*signal[t-1] + 54*signal[t]
            y = y + 39*signal[t] + 14*signal[t] - 21*signal[t]
            y = y / 231
            new_signal.append(y)
        elif i == t:
            y = -21*signal[t-4] + 14*signal[t-3] + 39*signal[t-2] + 54*signal[t-1] + 59*signal[t]
            y = y + 54*signal[t] + 39*signal[t] + 14*signal[t] - 21*signal[t]
            y = y / 231
            new_signal.append(y)        
            
        else:
            y = -21*signal[i-4] + 14*signal[i-3] + 39*signal[i-2] + 54*signal[i-1] + 59*signal[i]
            y = y + 54*signal[i+1] + 39*signal[i+2] + 14*signal[i+3] - 21*signal[i+4]
            y = y / 231
            new_signal.append(y) 
            
    return new_signal


def ach_computing(sensor):
    # ## read data ################################################
    # db = open(database, 'r')
    # d = db.read()
    # d = d.split(' ')[-1][1:-1]
    # d = json.loads(d)
    # db.close()   


    ## get data #################################################
    # sensores = d['Sensores']
    ambiente = sensor[0]['series']
    lateral  = sensor[1]['series']
    central  = sensor[2]['series']
    num_m = len(central) + 1

    ## time transformation ######################################
    ## separar la fecha de la hora ##########
    tiempo1 = ambiente[-2]['name'].split('/')[1]
    tiempo1 = tiempo1.split(':')
    tiempo1 = [float(i) for i in tiempo1]

    tiempo2 = ambiente[-1]['name'].split('/')[1]
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
    dt = tiempo2 - tiempo1


    ## compute ACH ##############################################
    if len(sensores[0]['series']) == 2:

        ## remove noise ##################
        for i in range(len(central)):
            ambiente[i] = ambiente[i]['value']
            lateral[i] = lateral[i]['value']
            central[i] = central[i]['value']        

        ## first filter
        ambiente = clean_noise(ambiente)
        lateral  = clean_noise(lateral)
        central  = clean_noise(central)
        ## second filter
        ambiente = clean_noise(ambiente)
        lateral  = clean_noise(lateral)
        central  = clean_noise(central)

        ambiente = ambiente[-2:]
        lateral  = lateral[-2:]
        central  = central[-2:]

        ## calcular ACH ###################    
        ach, f = ACH(ambiente, lateral, central, dt)

        ## guardar CO2 reescalado #########
        file = open('scaled.txt', 'w')
        c_lat = lateral[1]['value'] - f
        c_cen = central[1]['value'] - f
        file.write('{}\n'.format(c_lat))
        file.write('{}\n'.format(c_cen))
        file.write('{}'.format(ach))
        file.close()


    elif len(sensores[0]['series']) > 2:    

        ## remove noise ##################
        for i in range(len(central)):
            ambiente[i] = ambiente[i]['value']
            lateral[i] = lateral[i]['value']
            central[i] = central[i]['value']        

        ambiente = clean_noise(ambiente)
        lateral  = clean_noise(lateral)
        central  = clean_noise(central)

        ambiente = ambiente[-2:]
        lateral  = lateral[-2:]
        central  = central[-2:]

        ## leer CO2 reescalado ############
        file = open('scaled.txt', 'r')
        scale = file.read().split('\n')
        lateral[0] = scale[0]
        central[0] = scale[1]
        ach_mean = scale[2]
        file.close()

        ## calcular ACH ###################
        ach, f = ACH(ambiente, lateral, central, dt)

        ## guardar CO2 reescalado #########
        file = open('scaled.txt', 'w')
        c_lat = lateral[1] - f
        c_cen = central[1] - f
        ach_mean = float(ach_mean) + ach
        file.write('{}\n'.format(c_lat))
        file.write('{}\n'.format(c_cen))
        file.write('{}'.format(ach_mean))
        file.close()
        
    return ach_mean/num_m