import pandas as pd

def read_from_cash_csv(file,file_path):
    column_mapping = {'DATE': 'DATE', 'DESCRIPTION': 'DESCRIPTION', 'AMOUNT': 'AMOUNT', 'TYPE': 'TYPE'}
    columns = column_mapping.keys()
    df = pd.read_csv(file_path)
    df = df[columns]
    df['TRANSACTION_ID'] = ''
    df['AMOUNT'] = df['AMOUNT'].astype(float)
    # Add S_NO column
    df.insert(0, 'S_NO', range(1, len(df) + 1))
    df['ACCOUNT'] = file
    df['ACCOUNT_TYPE'] = 'BANK'
    df["REMARKS"] = ""
    df["IS_TRANSFER"] = ""
    return df