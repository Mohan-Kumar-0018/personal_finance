import pandas as pd

def read_from_kotak_csv(file,file_path):
    column_mapping = {'Sl. No.': 'S_NO', 'Value Date': 'DATE', 'Description': 'DESCRIPTION', 'Chq / Ref No.': 'TRANSACTION_ID', 'Amount': 'AMOUNT', 'Dr / Cr': 'TYPE'}
    columns = column_mapping.keys()
    df = pd.read_csv(file_path, skiprows=13, on_bad_lines='warn')
    df = df[pd.to_numeric(df.iloc[:, 0], errors='coerce').notna()][columns]
    df = df.rename(columns=column_mapping)    
    df['TYPE'] = df['TYPE'].map({'DR': 'DEBIT', 'CR': 'CREDIT'})
    df['AMOUNT'] = df['AMOUNT'].str.replace(',', '').astype(float)
    df['ACCOUNT'] = file
    df['ACCOUNT_TYPE'] = 'BANK'
    df["REMARKS"] = ""
    print("Kotak extracted data --->")
    print(df)