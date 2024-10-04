import os
import pandas as pd
from process_kotak import read_from_kotak_csv
from process_pluxee import read_from_pluxee_csv
from process_pnb import read_from_pnb_csv
from process_splitwise import read_from_splitwise_html

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')


def process_all_data():
	current_folder = main_folder + month_folder + "/"

	source_folder = current_folder + "source/"
	files_in_folder = os.listdir(source_folder)

	banks_df, splitwise_expense_df, splitwise_transaction_df, pluxee_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
	
	for file in files_in_folder:
		print(file)
		file_path = source_folder + file
		file_name = file.split(".")[0]		
		match file:
			case _ if file.endswith("kotak.csv"):
				print("processing kotak")
				banks_df = pd.concat([banks_df, read_from_kotak_csv(file_name, file_path)], ignore_index=True)
			case _ if file.endswith("splitwise.html"):
				print("processing splitwise")
				expense_df, transaction_df = read_from_splitwise_html(file_name, file_path)
				splitwise_expense_df = pd.concat([splitwise_expense_df, expense_df], ignore_index=True)
				splitwise_transaction_df = pd.concat([splitwise_transaction_df, transaction_df], ignore_index=True)
			case _ if file.endswith("pluxee.csv"):
				print("processing pluxee")
				pluxee_df = pd.concat([pluxee_df, read_from_pluxee_csv(file_name, file_path)], ignore_index=True)
			case _ if file.endswith("pnb.csv"):
				print("processing pnb")
				banks_df = pd.concat([banks_df, read_from_pnb_csv(file_name, file_path)], ignore_index=True)
			case _:
				print("unknown file type")
				pass

	# Merge all DataFrames
	print("Banks DataFrame:")
	print(banks_df)
	output_file_path = current_folder + "result/" + 'banks' + '.csv'
	banks_df.to_csv(output_file_path, index=False)
	print("\nSplitwise Expense DataFrame:")
	print(splitwise_expense_df)
	print("\nSplitwise Transaction DataFrame:")
	print(splitwise_transaction_df)
	print("\nPluxee DataFrame:")
	print(pluxee_df)
	banks_df = mark_transfers(banks_df)
    # Print rows where IS_TRANSFER is YES
	print("Transfers:")
	print(banks_df[banks_df['IS_TRANSFER'] == 'YES'])
	output_file_path = current_folder + "result/" + file + '.csv'
	banks_df.to_csv(output_file_path, index=False)
   
	
def mark_transfers(banks_df):
    # Find matching rows with the same non-empty TRANSACTION_ID
    matching_transactions = banks_df[(banks_df['TRANSACTION_ID'] != '') & (banks_df['TRANSACTION_ID'].notna() & banks_df['TRANSACTION_ID'].duplicated(keep=False))]
    # Sort matching_transactions by DATE, TRANSACTION_ID
    matching_transactions = matching_transactions.sort_values(by=['DATE', 'TRANSACTION_ID'])
    print("Matching transactions:")
    print(matching_transactions)
    current_folder = main_folder + month_folder + "/"
    output_file_path = current_folder + "result/" + 'matching_transactions' + '.csv'
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

process_all_data()