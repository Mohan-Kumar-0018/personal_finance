
YEAR_MONTH = sep_2024
MAIN_FOLDER = /Users/kumar/personal_finance/

export YEAR_MONTH
export MAIN_FOLDER
export OPENAI_API_KEY

setup:
	pip3 install -r requirements.txt

kotak:
	python3 src/process_kotak.py

splitwise:
	python3 src/process_splitwise_html.py

pluxee:
	python3 src/process_pluxee.py

local:
	python3 src/categorize_expenses.py