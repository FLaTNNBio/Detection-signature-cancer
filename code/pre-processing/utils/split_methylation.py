import os
import pandas as pd


def separa_duplica_valori(file_path):
    # Carica il file CSV
    df = pd.read_csv(file_path, delimiter=';')

    # Elimina le righe con valori vuoti o 'NA' nella prima colonna
    df = df.dropna(subset=['Hugo_Symbol'])

    # Separa i valori nella prima colonna
    df['Hugo_Symbol'] = df['Hugo_Symbol'].str.split(',')

    # Duplica le righe
    df = df.explode('Hugo_Symbol')

    # Salva il risultato nel file originale
    df.to_csv(file_path, index=False, sep=';')


def elabora_cartella(cartella):
    for root, dirs, files in os.walk(cartella):
        for file in files:
            if file.startswith('data_methylation_hm27_hm450_merged') and file.endswith('.csv'):
                file_path = os.path.join(root, file)
                separa_duplica_valori(file_path)
                print(file_path)


# Sostituisci 'percorso_della_cartella' con il percorso effettivo della tua cartella principale
elabora_cartella('/home/musimathicslab/Desktop/Dataset (completo)')