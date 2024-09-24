import os
import pandas as pd

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')

def get_kotak_csv_file_path():
    current_folder = main_folder + month_folder + "/"
    kotak_folder = current_folder + "kotak/"
    files_in_folder = os.listdir(kotak_folder)
    filtered_files_in_folder = [file for file in files_in_folder if file.endswith("kotak.csv")]
    file_path = kotak_folder + filtered_files_in_folder[0]
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("KOTAK File not found")
        return
    print("kotak file_path ->", file_path)
    return file_path

def read_from_kotak_csv():
    file_path = get_kotak_csv_file_path()
    column_mapping = {'Sl. No.': 'S_NO', 'Transaction Date': 'DATE', 'Description': 'DESCRIPTION', 'Chq / Ref No.': 'TRANSACTION_ID', 'Amount': 'AMOUNT', 'Dr / Cr': 'TYPE'}
    columns = column_mapping.keys()
    df = pd.read_csv(file_path, skiprows=13, on_bad_lines='warn')
    df = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()][columns]
    df = df.rename(columns=column_mapping)
    df['TYPE'] = df['TYPE'].map({'DR': 'DEBIT', 'CR': 'CREDIT'})
    df['AMOUNT'] = df['AMOUNT'].str.replace(',', '').astype(float)
    df["REMARKS"] = ""

    save_kotak_csv(df, "all_data")
    credit_data = df[df['TYPE'] == 'CREDIT']
    save_kotak_csv(credit_data, "credit_data")
    debit_data = df[df['TYPE'] == 'DEBIT']
    save_kotak_csv(debit_data, "debit_data")


def save_kotak_csv(data_frame, file_name):
    current_folder = main_folder + month_folder + "/kotak/"
    output_file_path = current_folder + file_name + '.csv'
    print("output_file_path = ", output_file_path)
    data_frame.to_csv(output_file_path, index=False)

def process_kotak_data():
    print("process_kotak_data started ...")
    read_from_kotak_csv()
    

process_kotak_data()