import os
import pandas as pd

main_folder = "/Users/kumar/personal_finance/"
month_folder = "jan_2024"

def get_kotak_csv_file_path():
    current_folder = main_folder + month_folder + "/"
    kotak_folder = current_folder + "kotak/"
    files_in_folder = os.listdir(kotak_folder)
    filtered_files_in_folder = [file for file in files_in_folder if file.endswith(".csv")]
    file_path = kotak_folder + filtered_files_in_folder[0]
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("KOTAK File not found")
        return
    print("kotak file_path ->", file_path)
    return file_path

def read_from_kotak_csv():
    file_path = get_kotak_csv_file_path()
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
    print("credit_data ------> ")
    print(credit_data)
    debit_data = df_filtered[df_filtered['TYPE'] == 'DEBIT']
    print("debit_data ------> ")
    print(debit_data)

    total_income = credit_data['AMOUNT'].sum()
    print("total_income ------> ", total_income)
    total_expenses = debit_data['AMOUNT'].sum()
    print("total_expenses ------> ", total_expenses)
    

def process_kotak_data():
    print("process_kotak_data started ...")
    read_from_kotak_csv()
    

process_kotak_data()