import os
import re
import pandas as pd

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')


def mark_bank_transfers(banks_df):
    # Find matching rows with the same non-empty TRANSACTION_ID
    matching_transactions = banks_df[(banks_df['TRANSACTION_ID'] != '') & (banks_df['TRANSACTION_ID'].notna() & banks_df['TRANSACTION_ID'].duplicated(keep=False))]
    # Sort matching_transactions by DATE, TRANSACTION_ID
    matching_transactions = matching_transactions.sort_values(by=['DATE', 'TRANSACTION_ID'])
    print("Matching transactions:")
    print(matching_transactions)
    
    # Mark IS_TRANSFER as 'YES' for matching transactions
    for transaction_id, group in matching_transactions.groupby('TRANSACTION_ID'):
        # Ensure that there are at least two matching transactions to mark as transfers
        if len(group) == 2:
            first_row_index = group.index[0]
            second_row_index = group.index[1]
            banks_df.at[first_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[second_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[first_row_index, 'REMARKS'] = f"{second_row_index + 1} - {banks_df.at[second_row_index, 'ACCOUNT']}"
            banks_df.at[second_row_index, 'REMARKS'] = f"{first_row_index + 1} - {banks_df.at[first_row_index, 'ACCOUNT']}"
    return banks_df, matching_transactions

def mark_pnb_transfers(banks_df):
    # Extract transaction IDs from DESCRIPTION for PNB transactions
    pnb_transactions = banks_df[banks_df['ACCOUNT_TYPE'] == 'BANK' & banks_df['ACCOUNT'].str.contains('PNB')]
    pnb_transactions['TRANSACTION_ID'] = pnb_transactions['DESCRIPTION'].apply(lambda x: re.search(r'KKBKH\d+', x).group() if re.search(r'KKBKH\d+', x) else None)

    # Find matching rows with the same non-empty TRANSACTION_ID
    matching_transactions = pnb_transactions[(pnb_transactions['TRANSACTION_ID'] != '') & (pnb_transactions['TRANSACTION_ID'].notna() & pnb_transactions['TRANSACTION_ID'].duplicated(keep=False))]
    # Sort matching_transactions by DATE, TRANSACTION_ID
    matching_transactions = matching_transactions.sort_values(by=['DATE', 'TRANSACTION_ID'])
    print("Matching transactions for PNB:")
    print(matching_transactions)
    current_folder = main_folder + month_folder + "/"
    output_file_path = current_folder + "result/" + 'pnb_matching_transactions' + '.csv'
    matching_transactions.to_csv(output_file_path, index=False)

    # Mark IS_TRANSFER as 'YES' for matching transactions
    for transaction_id, group in matching_transactions.groupby('TRANSACTION_ID'):
        # Ensure that there are at least two matching transactions to mark as transfers
        if len(group) == 2:
            first_row_index = group.index[0]
            second_row_index = group.index[1]
            banks_df.at[first_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[second_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[first_row_index, 'REMARKS'] = f"{second_row_index + 1} - {banks_df.at[second_row_index, 'ACCOUNT']}"
            banks_df.at[second_row_index, 'REMARKS'] = f"{first_row_index + 1} - {banks_df.at[first_row_index, 'ACCOUNT']}"
    return banks_df