import os
import pandas as pd

main_folder = "/Users/kumar/personal_finance/"
month = "jan_2024"

def read_from_kotak_csv():
    current_folder = main_folder + month + "/"
    kotak_folder = current_folder + "kotak/"
    print("kotak_folder ------> ", kotak_folder)
    files_in_folder = os.listdir(kotak_folder)
    print("files_in_folder ------> ", files_in_folder)
    file_path = kotak_folder + files_in_folder[0]
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("KOTAK File not found")
        return

    column_mapping = {'Sl. No.': 'S_NO', 'Transaction Date': 'DATE', 'Description': 'DESCRIPTION', 'Chq / Ref No.': 'TRANSACTION_ID', 'Amount': 'AMOUNT', 'Dr / Cr': 'TYPE', 'Balance': 'BALANCE'}
    columns = column_mapping.keys()
    data_df = pd.read_csv(file_path, skiprows=13, on_bad_lines='warn')
    df_filtered = data_df[pd.to_numeric(data_df.iloc[:, 0], errors='coerce').notna()][columns]
    df_filtered = df_filtered.rename(columns=column_mapping)
    df_filtered['TYPE'] = df_filtered['TYPE'].map({'DR': 'DEBIT', 'CR': 'CREDIT'})
    df_filtered['AMOUNT'] = df_filtered['AMOUNT'].str.replace(',', '').astype(float)
    df_filtered['BALANCE'] = df_filtered['BALANCE'].str.replace(',', '').astype(float)
    print("df_filtered ------> ", df_filtered)
    credit_data = df_filtered[df_filtered['TYPE'] == 'CREDIT']
    print("credit_data ------> ", credit_data)
    debit_data = df_filtered[df_filtered['TYPE'] == 'DEBIT']
    print("debit_data ------> ", debit_data)

    total_income = credit_data['AMOUNT'].sum()
    print("total_income ------> ", total_income)
    total_expenses = debit_data['AMOUNT'].sum()
    print("total_expenses ------> ", total_expenses)

    # for index, row in df_filtered.iterrows():
    #     print("index ------> ", index)
    #     print("row ------> ", row)
    

def process_kotak_data():
    print("process_kotak_data started ...")
    read_from_kotak_csv()
    

process_kotak_data()