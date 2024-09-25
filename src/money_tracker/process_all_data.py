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

  for file in files_in_folder:
    print(file)
    file_path = source_folder + file
    match file:
        case _ if file.endswith("kotak.csv"):
            print("processing kotak")
            read_from_kotak_csv(file_path)
        case _ if file.endswith("splitwise.html"):
            print("processing splitwise")
            read_from_splitwise_html(file_path)
        case _ if file.endswith("pluxee.csv"):
            print("processing pluxee")
            read_from_pluxee_csv(file_path)
        case _ if file.endswith("pnb.csv"):
            print("processing pnb")
            read_from_pnb_csv(file_path)
        case _:
            print("unknown file type")
            pass

process_all_data()