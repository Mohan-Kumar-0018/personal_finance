import pandas as pd

def read_from_pluxee_csv(file_path):
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
    df['AMOUNT'] = df['AMOUNT'].astype(float)
    # Add REMARKS column
    df["REMARKS"] = ""

    print("Pluxee extracted data --->")
    print(df)
    return df