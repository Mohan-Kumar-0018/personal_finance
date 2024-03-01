
YEAR_MONTH = feb_2024
MAIN_FOLDER = /Users/kumar/personal_finance/

export YEAR_MONTH
export MAIN_FOLDER
export OPENAI_API_KEY

setup:
	pip install -r requirements.txt

kotak:
	python3 process_kotak.py

splitwise:
	python3 process_splitwise_html.py

local:
	python3 categorize_expenses.py