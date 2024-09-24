import os
import pandas as pd

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')

def get_pluxee_csv_file_path():
    current_folder = main_folder + month_folder + "/"
    pluxee_folder = current_folder + "pluxee/"
    files_in_folder = os.listdir(pluxee_folder)
    filtered_files_in_folder = [file for file in files_in_folder if file.endswith("pluxee.csv")]
    file_path = pluxee_folder + filtered_files_in_folder[0]
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("Pluxee File not found")
        return
    print("pluxee file_path ->", file_path)
    return file_path

def read_from_pluxee_csv():
    file_path = get_pluxee_csv_file_path()
    # Define column mapping
    column_mapping = {
      'Date & Time of Balance': 'DATE',
      'Transaction ID': 'TRANSACTION_ID',
      'Transaction Details': 'DESCRIPTION',
      'Credit(in Rs.)': 'CREDIT',
      'Debit(in Rs.)': 'DEBIT'
    }
    # Read CSV file
    df = pd.read_csv(file_path)
    # Select and rename columns
    df = df[column_mapping.keys()].rename(columns=column_mapping)
    # Add S_NO column
    df.insert(0, 'S_NO', range(1, len(df) + 1))
    # Convert CREDIT and DEBIT columns to float, handling potential string values
    df['CREDIT'] = df['CREDIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
    df['DEBIT'] = df['DEBIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) else x)
    # Determine TYPE and AMOUNT
    df['TYPE'] = df.apply(lambda row: 'CREDIT' if pd.notnull(row['CREDIT']) and row['CREDIT'] > 0 else 'DEBIT', axis=1)
    df['AMOUNT'] = df.apply(lambda row: row['CREDIT'] if row['TYPE'] == 'CREDIT' else row['DEBIT'], axis=1)
    # Drop unnecessary columns
    df = df.drop(['CREDIT', 'DEBIT'], axis=1)
    # Reorder columns
    df = df[['S_NO', 'DATE', 'DESCRIPTION', 'TRANSACTION_ID', 'AMOUNT', 'TYPE']]
    # Convert DATE to datetime and format it to DD-MM-YYYY
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y %H:%M:%S').dt.strftime('%d-%m-%Y')
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['AMOUNT'] = df['AMOUNT'].astype(float)
    # Add REMARKS column
    df["REMARKS"] = ""

    # Save all data
    save_pluxee_csv(df, "all_data")
    
    # Save credit data
    credit_data = df[df['TYPE'] == 'CREDIT']
    save_pluxee_csv(credit_data, "credit_data")
    
    # Save debit data
    debit_data = df[df['TYPE'] == 'DEBIT']
    save_pluxee_csv(debit_data, "debit_data")

def save_pluxee_csv(data_frame, file_name):
    current_folder = main_folder + month_folder + "/pluxee/"
    output_file_path = current_folder + file_name + '.csv'
    print("output_file_path = ", output_file_path)
    data_frame.to_csv(output_file_path, index=False)
    

def process_pluxee_data():
    print("process_pluxee_data started ...")
    read_from_pluxee_csv()

process_pluxee_data()
