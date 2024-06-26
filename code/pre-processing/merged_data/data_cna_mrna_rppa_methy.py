import os
import pandas as pd


def concatena_csv(input_csv, output_csv, directory_path):
    input_df = pd.read_csv(input_csv, delimiter=';')

    # Cerca sottodirectory con lo stesso nome del file 'data_cna.csv' nella directory principale
    main_directory = os.path.abspath(directory_path)
    subdirectories = [dir for dir in os.listdir(main_directory) if os.path.isdir(os.path.join(main_directory, dir))]

    # Inizializza il DataFrame concatenato con il DataFrame di input
    merged_df = input_df.copy()
    i = 2

    # Itera sulle sottodirectory
    for subdirectory in subdirectories:
        subdirectory_path = os.path.join(main_directory, subdirectory)
        sub_file_path = os.path.join(subdirectory_path, 'data_mrna_v2_seq_rsem_' + str(i) + '.csv')
        print(subdirectory_path)
        print(sub_file_path)
        print("\n")
        i += 1

        # Se trova un file 'data_cna.csv' nella sottodirectory, leggi e verifica le righe
        if os.path.exists(sub_file_path) and os.path.isfile(sub_file_path):
            sub_df = pd.read_csv(sub_file_path, delimiter=';')

            # Concatena i dataframe
            merged_df = pd.concat([merged_df, sub_df])

            # Elimina i duplicati in base alla prima cella e al nome dell'header dalla seconda colonna in poi
            merged_df = merged_df.drop_duplicates(subset=["Hugo_Symbol"] + list(merged_df.columns[1:]))

    print('Fatto')
    # Effettua la fusione (aggregazione) delle righe con lo stesso valore sulla prima colonna
    merged_df = merged_df.sort_values(by="Hugo_Symbol")
    merged_df = merged_df.groupby('Hugo_Symbol', as_index=False).first().fillna(method='ffill')

    merged_df.to_csv(output_csv, index=False, sep=';')


input_csv = '/home/alberto/Scrivania/1/data_mrna_v2_seq_rsem_1.csv'
output_csv = '/home/alberto/Scrivania/output.csv'
directory_path = '/home/alberto/Scrivania/prova'
concatena_csv(input_csv, output_csv, directory_path)
