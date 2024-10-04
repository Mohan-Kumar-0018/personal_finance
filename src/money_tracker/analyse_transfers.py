import os
import re
import pandas as pd

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')
import logging

def mark_bank_transfers(banks_df):
    # Find matching rows with the same non-empty TRANSACTION_ID
    matching_transactions = banks_df[(banks_df['TRANSACTION_ID'] != '') & (banks_df['TRANSACTION_ID'].notna() & banks_df['TRANSACTION_ID'].duplicated(keep=False))]    
    # Mark IS_TRANSFER as 'YES' for matching transactions
    for transaction_id, group in matching_transactions.groupby('TRANSACTION_ID'):
        # Ensure that there are at least two matching transactions to mark as transfers
        if len(group) == 2:
            first_row_index = group.index[0]
            second_row_index = group.index[1]
            banks_df.at[first_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[second_row_index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[first_row_index, 'REMARKS'] = f"{banks_df.at[second_row_index, 'S_NO']} - {banks_df.at[second_row_index, 'ACCOUNT']}"
            banks_df.at[second_row_index, 'REMARKS'] = f"{banks_df.at[first_row_index, 'S_NO']} - {banks_df.at[first_row_index, 'ACCOUNT']}"
    return banks_df

def mark_pnb_transfers(banks_df):
    # Extract transaction IDs from DESCRIPTION for PNB transactions
    pnb_transactions = banks_df[(banks_df['ACCOUNT_TYPE'] == 'BANK') & (banks_df['ACCOUNT'].str.upper().str.contains('PNB'))]
    for index, row in pnb_transactions.iterrows():
        opposite_type = 'CREDIT' if row['TYPE'] == 'DEBIT' else 'DEBIT'
        matching_row = banks_df[
            (banks_df['IS_TRANSFER'] != 'YES') &
            (banks_df['TRANSACTION_ID'].notna()) &
            (banks_df['TRANSACTION_ID'] != '') &
            (banks_df['ACCOUNT'] != row['ACCOUNT']) &
            (banks_df['TYPE'] == opposite_type) &
            (banks_df['AMOUNT'] == row['AMOUNT']) &
            (banks_df['DATE'] == row['DATE']) &
            (banks_df['TRANSACTION_ID'].apply(lambda x: str(x).lower() in row['DESCRIPTION'].lower()))
        ].first_valid_index()
        if matching_row is not None:
            banks_df.at[matching_row, 'IS_TRANSFER'] = 'YES'
            banks_df.at[matching_row, 'REMARKS'] = f"{banks_df.at[index, 'S_NO']} - {banks_df.at[index, 'ACCOUNT']}"
            banks_df.at[index, 'IS_TRANSFER'] = 'YES'
            banks_df.at[index, 'REMARKS'] = f"{banks_df.at[matching_row, 'S_NO']} - {banks_df.at[matching_row, 'ACCOUNT']}"
            logging.info(f"Marked transfer: Bank transaction at index {banks_df.at[matching_row, 'S_NO']} matches PNB transaction {row['S_NO']}")
        else:
            logging.debug(f"No matching bank transaction found for PNB transaction {row['S_NO']}")
    return banks_df

def mark_splitwise_transfers(banks_df, splitwise_transaction_df):
    for index, row in splitwise_transaction_df.iterrows():
        # Find matching row in banks_df
        matching_row = banks_df[
            (banks_df['IS_TRANSFER'] != 'YES') &
            (banks_df['TYPE'] == row['TYPE']) &
            (banks_df['AMOUNT'].between(row['AMOUNT'] - 5, row['AMOUNT'] + 5, inclusive='both')) &
            (banks_df['DATE'] == row['DATE'])
        ].first_valid_index()

        if matching_row is not None:
            # Mark the matching row as a transfer
            banks_df.at[matching_row, 'IS_TRANSFER'] = 'YES'
            banks_df.at[matching_row, 'REMARKS'] = f"Splitwise transaction ID: {row['S_NO']}"
            splitwise_transaction_df.at[index, 'REMARKS'] = f"Bank transaction ID: {banks_df.at[matching_row, 'S_NO']}"
            logging.info(f"Marked transfer: Bank transaction at index {banks_df.at[matching_row, 'S_NO']} matches Splitwise transaction {row['S_NO']}")
        else:
            logging.debug(f"No matching bank transaction found for Splitwise transaction {row['S_NO']}")
    return banks_df, splitwise_transaction_df

def mark_splitwise_expenses(banks_df, splitwise_expense_df):
	paid_expenses = splitwise_expense_df[splitwise_expense_df['PAID_BY'] == 'you']
	for index, row in paid_expenses.iterrows():
		matching_row = banks_df[
			(banks_df['IS_TRANSFER'] != 'YES') &
			(banks_df['TYPE'] == 'DEBIT') &
			(banks_df['AMOUNT'].between(row['TOTAL_AMOUNT'] - 5, row['TOTAL_AMOUNT'] + 5, inclusive='both')) &
			(banks_df['DATE'] == row['DATE'])
		].first_valid_index()
		if matching_row is not None:
			banks_df.at[matching_row, 'IS_TRANSFER'] = 'YES'
			banks_df.at[matching_row, 'REMARKS'] = f"Splitwise Expense ID: {row['S_NO']}"
			splitwise_expense_df.at[index, 'REMARKS'] = f"Bank transaction ID: {banks_df.at[matching_row, 'S_NO']}"
			logging.info(f"Marked transfer: Bank transaction at index {banks_df.at[matching_row, 'S_NO']} matches Splitwise Expense {row['S_NO']}")
		else:
			logging.debug(f"No matching bank transaction found for Splitwise Expense {row['S_NO']}")
	return banks_df, splitwise_expense_df

