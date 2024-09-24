import os
import pandas as pd

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')

def get_pnb_csv_file_path():
    current_folder = main_folder + month_folder + "/"
    pnb_folder = current_folder + "pnb/"
    files_in_folder = os.listdir(pnb_folder)
    filtered_files_in_folder = [file for file in files_in_folder if file.endswith("pnb.csv")]
    file_path = pnb_folder + filtered_files_in_folder[0]
    fileExists = os.path.isfile(file_path)
    if not fileExists:
        print("PNB File not found")
        return
    print("pnb file_path ->", file_path)
    return file_path

def read_from_pnb_csv():
    file_path = get_pnb_csv_file_path()
    
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    
    # Find the index of 'Transaction Date' in the second column
    transaction_date_index = df.iloc[:, 1].eq('Transaction Date').idxmax()
    
    # Slice the DataFrame to keep only rows from 'Transaction Date' onwards and ignore the first column
    df = df.iloc[transaction_date_index:, 1:]
    
    # Set the first row as column headers
    df.columns = df.iloc[0]
    
    # Remove the first row (now redundant as it's been set as headers)
    df = df.iloc[1:]
    
    # Reset the index of the DataFrame
    df = df.reset_index(drop=True)
    
    column_mapping = {
        'Transaction Date': 'DATE',
        'Narration': 'DESCRIPTION',
        'Withdrawal': 'DEBIT',
        'Deposit': 'CREDIT'
    }
    
    # Select and rename columns
    df = df[column_mapping.keys()].rename(columns=column_mapping)
    
    # Remove rows where DATE column is empty
    df = df.dropna(subset=['DATE'])
    
    # Add S_NO column
    df.insert(0, 'S_NO', range(1, len(df) + 1))
    
    # Convert CREDIT and DEBIT columns to float, handling potential string values
    df['CREDIT'] = df['CREDIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.strip() else 0)
    df['DEBIT'] = df['DEBIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.strip() else 0)
    
    # Determine TYPE and AMOUNT
    df['TYPE'] = df.apply(lambda row: 'CREDIT' if row['CREDIT'] > 0 else 'DEBIT', axis=1)
    df['AMOUNT'] = df.apply(lambda row: row['CREDIT'] if row['TYPE'] == 'CREDIT' else row['DEBIT'], axis=1)
    
    # Drop unnecessary columns
    df = df.drop(['CREDIT', 'DEBIT'], axis=1)
    
    # Reorder columns
    df = df[['S_NO', 'DATE', 'DESCRIPTION', 'AMOUNT', 'TYPE']]
    
    # Convert DATE to datetime and format it to DD-MM-YYYY
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y').dt.strftime('%d-%m-%Y')
    
    # Add REMARKS column
    df["REMARKS"] = ""
    
    # Reset index after all operations
    df = df.reset_index(drop=True)
    
    # Save all data
    save_pnb_csv(df, "all_data")
    
    # Save credit data
    credit_data = df[df['TYPE'] == 'CREDIT']
    save_pnb_csv(credit_data, "credit_data")
    
    # Save debit data
    debit_data = df[df['TYPE'] == 'DEBIT']
    save_pnb_csv(debit_data, "debit_data")

def save_pnb_csv(data_frame, file_name):
    current_folder = main_folder + month_folder + "/pnb/"
    output_file_path = current_folder + file_name + '.csv'
    print("output_file_path = ", output_file_path)
    data_frame.to_csv(output_file_path, index=False)

def process_pnb_data():
    print("process_pnb_data started ...")
    read_from_pnb_csv()

process_pnb_data()
