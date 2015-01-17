#!/usr/bin/python

from datetime import datetime
import pandas as pd
from pandas import DataFrame

def timbratura_piu_recente(timb):
#     print timb
    # riordina dal piu recente (in testa) al piu vecchio
    timbrature_ordinate = timb.sort('data_timbratura')
    return timbrature_ordinate[['persona','data_no_ora','ore_lavorate']].values[0]

def converti_data(data):

    #  legge data in ingresso 
    date_object = datetime.strptime(data, '%B %d, %Y at %I:%M%p')

    # converte la data in epoch 
    # http://it.wikipedia.org/wiki/Tempo_(Unix)
    return date_object

# dato un oggetto data, calcola il numer do ore 
def restituisci_ore(data):
    return float(data.seconds/3600)

# leggi la tabella excel  modifica Piero
foglio = pd.read_excel('calendar.xlsx')

# array dove mettere le ore lavorate
ore_lavorate = []
for indice, riga in foglio.iterrows():
    ore = converti_data(riga.uscita)-converti_data(riga.ingresso)
    ore_lavorate.append(ore)
    
# aggiungi la colonna ore alla tabella 
foglio['ore_lavorate'] = ore_lavorate


data_no_ora=[]
# elimina l ora dalla data del giorno lavorato
for indice, riga in foglio.iterrows():
    data_no_ora.append(str(converti_data(riga.ingresso).day)  +'/'+\
                       str(converti_data(riga.ingresso).month)+'/'+\
                       str(converti_data(riga.ingresso).year))
    
# aggiungi la colonna data_no_ora alla tabella 
foglio['data_no_ora'] = data_no_ora

# trova il nome delle persone uniche 
persone = foglio.persona.unique()

date = []
person = []
hours = [] 

linee = 0 
#  per ogni persona unica 
for p in persone :
    print p
    # trova i giorni lavorati dalla persona p 
    # elimina le date duplicate con unique()
    giorni_lavorati =  foglio[foglio['persona']== p].data_no_ora.unique()
    # per ogni giorno lavorato, trova la timbratura piu recente 
    for g in giorni_lavorati:
#         print g 
        # trova tutte le timbrature per ogni giorno g lavorato dalla persona p 
        timbrature = foglio[ (foglio['persona'] == p) &  (foglio['data_no_ora'] ==g)]
        # seleziona la piu recente
        timbratura_da_stampare = timbratura_piu_recente(timbrature)
        # metti in colonna le persone, le date e le ore 
        person.append(timbratura_da_stampare[0])
        date.append(timbratura_da_stampare[1])
        # prendi il numero di ore 
        ore = restituisci_ore(timbratura_da_stampare[2]) 
        hours.append(ore)
        linee += 1


# scrivi la tabella in un file di uscita 
# definisci le colonne 
columns =[ 'date', 'person','hours']
# crea la tabella
df_ = pd.DataFrame(columns=columns)

# copia le colonne nella tabella 
df_['date']= date 
df_['person']= person 
df_['hours']= hours
# modifica  da csv a excel  Piero
df_.to_excel('out.xlsx')
df_.sort(['person'])
