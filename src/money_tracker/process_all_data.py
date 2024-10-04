import os
import re
import pandas as pd
from process_kotak import read_from_kotak_csv
from process_pluxee import read_from_pluxee_csv
from process_pnb import read_from_pnb_csv
from process_splitwise import read_from_splitwise_html
from analyse_transfers import mark_bank_transfers
main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')
current_folder = main_folder + month_folder + "/"


def process_all_data():
	banks_df, splitwise_expense_df, splitwise_transaction_df, pluxee_df = read_all_data()
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
	banks_df, matching_transactions = mark_bank_transfers(banks_df)
	save_result(matching_transactions, 'matching_transactions')
	transfers_df = banks_df[banks_df['IS_TRANSFER'] == 'YES']
	save_result(transfers_df, 'transfers')
   
def save_result(df, file_name):
	print("File:", file_name, '\n', df)
	output_file_path = current_folder + "result/" + file_name + '.csv'
	df.to_csv(output_file_path, index=False)
	
def read_all_data():
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
	return banks_df, splitwise_expense_df, splitwise_transaction_df, pluxee_df

process_all_data()