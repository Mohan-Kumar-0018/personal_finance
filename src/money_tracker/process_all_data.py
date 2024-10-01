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

	kotak_df, splitwise_expense_df, splitwise_transaction_df, pluxee_df, pnb_df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
	for file in files_in_folder:
		print(file)
		file_path = source_folder + file
		file_name = file.split(".")[0]
		# Initialize empty DataFrames for each type
		
		match file:
			case _ if file.endswith("kotak.csv"):
				print("processing kotak")
				kotak_df = pd.concat([kotak_df, read_from_kotak_csv(file_name, file_path)])
				print("Kotak DataFrame:")
				print(kotak_df)
			case _ if file.endswith("splitwise.html"):
				print("processing splitwise")
				expense_df, transaction_df = read_from_splitwise_html(file_name, file_path)
				splitwise_expense_df = pd.concat([splitwise_expense_df, expense_df])
				splitwise_transaction_df = pd.concat([splitwise_transaction_df, transaction_df])
				print("Splitwise Expense DataFrame:")
				print(splitwise_expense_df)
				print("Splitwise Transaction DataFrame:")
				print(splitwise_transaction_df)
			case _ if file.endswith("pluxee.csv"):
				print("processing pluxee")
				pluxee_df = pd.concat([pluxee_df, read_from_pluxee_csv(file_name, file_path)])
				print("Pluxee DataFrame:")
				print(pluxee_df)
			case _ if file.endswith("pnb.csv"):
				print("processing pnb")
				pnb_df = pd.concat([pnb_df, read_from_pnb_csv(file_name, file_path)])
				print("PNB DataFrame:")
				print(pnb_df)
			case _:
				print("unknown file type")
				pass

	# Merge all DataFrames
	print("Kotak DataFrame:")
	print(kotak_df)
	print("\nSplitwise Expense DataFrame:")
	print(splitwise_expense_df)
	print("\nSplitwise Transaction DataFrame:")
	print(splitwise_transaction_df)
	print("\nPluxee DataFrame:")
	print(pluxee_df)
	print("\nPNB DataFrame:")
	print(pnb_df)

process_all_data()