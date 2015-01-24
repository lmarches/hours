#!/usr/bin/python

from datetime import datetime
import pandas as pd
from pandas import DataFrame, Series

# -----------------------------------------------------------------------------------
def _sum(x):
    if len(x) == 0: return 0
    else: return sum(x)

#  plotTimeSeries(df_local, label_,resamplig_freq):
# -----------------------------------------------------------------------------------
# DESCRIPTION : plots a time series into the range
#               '2/01/2014' - '3/31/2014'
# USAGE
#
# df_local       : pandas dataframe with at least two columns
#                 one of them MUST  be 'timestamp_epoch'
#
# label_         : name of the column to print into a time series
# resamplig_freq : sampling rate for aggregating temporal data
#
# Example
def plotTimeSeries(df_local, label_,resamplig_freq, delete_before,delete_after):

    dates=[]
    for f in df_local[label_].values:
        print f
        dates.append(datetime.fromtimestamp(int(float(f))))

    dates.sort(reverse=False)
    s = Series(ones(len(dates)),index=dates)
    s_tr = s.truncate(before=delete_before, after=delete_after)
    s_tr = s_tr.resample(resamplig_freq, how=_sum)

#     plt.figure()
#     plt.plot(s_tr.index,s_tr.values,label=label_)
#     xticks(rotation=60)
#     plt.title('Volume')
#     legend(loc=2)

#     plt.figure()
#     plt.plot(s_tr.index,s_tr.cumsum(),label=label_)
#     xticks(rotation=60)
#     plt.title('Cumulative')
#     legend(loc=2)

    return s_tr


def timbratura_piu_recente(timb):
#     print timb
    # riordina dal piu recente (in testa) al piu vecchio
    timbrature_ordinate = timb.sort('data_timbratura',ascending=False)
    return timbrature_ordinate[['persona','data_no_ora','ore_lavorate','ingresso']].values[0]

def converti_data(data):

    #  legge data in ingresso 
    date_object = datetime.strptime(data, '%B %d, %Y at %I:%M%p')

    # converte la data in epoch 
    # http://it.wikipedia.org/wiki/Tempo_(Unix)
    return date_object

# dato un oggetto data, calcola il numer do ore 
def restituisci_ore(data):
    return float(data.seconds/3600)

# leggi la tabella
foglio = pd.read_csv('time_robert_brady.csv')
foglio

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
 
date = []
person = []
hours = [] 
date_obj = []

linee = 0 
#  per ogni persona unica 
for p in foglio.persona.unique():
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
        # prendi le date in formato object 
        date_obj.append(converti_data(timbratura_da_stampare[3]) )
        hours.append(ore)
        linee += 1


# scrivi la tabella in un file di uscita 
# definisci le colonne 
columns =[ 'date', 'person','hours','date_obj']
# crea la tabella
df_ = pd.DataFrame(columns=columns)

# copia le colonne nella tabella 
df_['date']= date 
df_['person']= person
# lowercase since sometimes the lads are not indicating work correctly
df_['person'] = df_['person'].str.lower()
df_['hours']= hours
df_.to_csv('out.csv')
df_['date_obj']=date_obj

print df_[['person','hours']].groupby('person').sum()
# df_.sort(['person'])



for p in df_['person'].unique():
    df_person = df_[df_['person'] == p]
    date_obj_dti=pd.DatetimeIndex(df_person['date_obj'].values)
    s = Series(df_person['hours'].values,index=date_obj_dti)
    s_rs = s.resample('W', how=_sum)
    print s_rs