import pandas as pd


def read_from_pnb_csv(file,file_path):
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
    
    # Convert CREDIT and DEBIT columns to float, handling potential string values
    df['CREDIT'] = df['CREDIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.strip() else 0)
    df['DEBIT'] = df['DEBIT'].apply(lambda x: float(x.replace(',', '')) if isinstance(x, str) and x.strip() else 0)
    
    # Determine TYPE and AMOUNT
    df['TYPE'] = df.apply(lambda row: 'CREDIT' if row['CREDIT'] > 0 else 'DEBIT', axis=1)
    df['AMOUNT'] = df.apply(lambda row: row['CREDIT'] if row['TYPE'] == 'CREDIT' else row['DEBIT'], axis=1)
    
    # Drop unnecessary columns
    df = df.drop(['CREDIT', 'DEBIT'], axis=1)
    # Convert DATE to datetime and format it to DD-MM-YYYY
    df['DATE'] = pd.to_datetime(df['DATE'], format='%d/%m/%Y')
    df = df.sort_values('DATE')
    df['DATE'] = df['DATE'].dt.strftime('%d-%m-%Y')
    # Add S_NO column
    df.insert(0, 'S_NO', range(1, len(df) + 1))
    # Reorder columns
    df = df[['S_NO', 'DATE', 'DESCRIPTION', 'AMOUNT', 'TYPE']]
    df['ACCOUNT'] = file
    df['ACCOUNT_TYPE'] = 'BANK'
    df["REMARKS"] = ""
    df["IS_TRANSFER"] = ""
    
    # Reset index after all operations
    df = df.reset_index(drop=True)
    return df