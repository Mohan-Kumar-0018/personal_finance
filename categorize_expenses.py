import tiktoken
import json
from openai import OpenAI
from process_splitwise_html import save_splitwise_csv
from process_kotak import save_kotak_csv
import pandas as pd
from unused import num_tokens_from_messages 
import os
client = OpenAI()
main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')

def categorize_expenses():
    print("Categorising expenses now ...")
    


def categorize_splitwise_expenses():
    print("Categorising splitwise expenses now ...")
    splitwise_expenses_file = main_folder + month_folder + "/" + "splitwise/" + "expense_data.csv"
    if not splitwise_expenses_file:
        print("Splitwise File not found")
        return
    print("splitwise file_path ->", splitwise_expenses_file)
    df = pd.read_csv(splitwise_expenses_file)
    df = df[df["EXPENSE_AMOUNT"] > 10]
    df["GPT_CATEGORY"] = ""
    print("df = ", df)
    for index, row in df.iterrows():
        print("row ----->", row)
        category = classify_expense(row["TITLE"], row["GROUP_NAME"])
        df.at[index, 'GPT_CATEGORY'] = category

    print("final df = ", df)
    save_splitwise_csv(df, "expense_data_categorized")

def get_all_categories():
    return ["Food", "Groceries", "Rent", "Utility payments", "Petrol and toll", "Shopping", "Entertainment", "Drinks","Petty Expenses"]

def classify_expense(title, group_name):
    pre_prompts = pre_requisites_prompts()
    current_prompt =  (f"Based on these keywords, categorize the following expense.\n"
              f"Title: {title}\n"
              f"Group Name: {group_name}\n"
              f"Categories: {get_all_categories()}\n"
              f"If not able to categorize, categorize as 'Others'\n")
    prompt = pre_prompts + current_prompt

    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=60
    )
    print("response = ", response)
    return response.choices[0].text.strip()

def pre_requisites_prompts():
    rule1 = (f"Here are the keywords for categorization:\n"
              f"- 'movie': Entertainment and Lifestyle\n"
              f"- 'poonkuzhali marriage': Travel\n"
              f"- 'lunch, dinner,kakatiya ': Food \n"
              f"- if not able to categorize, categorize as 'Others'")

    return rule1

def get_kotak_prompts():
    category_constrain = (f"Here are the keywords for categorization:\n"
            f"- 'movie': Entertainment\n"
            f"- 'CHANNAHALLI RAJ, DD': Drinks\n"
            f"- 'Blinkit, Grofers ': Groceries\n"
            f"- 'WATTAPP TECHNOL': Petrol and toll\n"
            f"- 'Mygate': Rent\n"
            f"- 'mohankumaarrr@o': Petty Expenses\n"
            f"- 'Amazon, Flipkart': Shopping\n"
            f"- 'lunch, dinner, kakatiya': Food \n")
    is_expense_constrain = (f"Here are rules to determine if given transaction is an expense or not:\n"
             f"- If the description starts with MB: it's a trasfer \n"
             f"- Transfers are usually not an expense\n"
             f"- Rent is paid through transfer, it is an expense\n"
             f"- Transfer to Niroop, SMK, Ramya, Mom, Jeevarathinam are not expenses\n"
             f"- If not an expense, category needs to be empty string\n"
    )
    format_constrain = "Note: The output must strictly follow the dict or JSON format: {'category': '{type: string}', 'is_expense': '{type: string}' ." + f"category must be a one of the following: {get_all_categories()} and is_expense must be either 'Yes' or 'No' "
    return category_constrain + is_expense_constrain + format_constrain

def classify_kotak_expense(description):
    pre_prompts = get_kotak_prompts()
    prompt = pre_prompts + (f"Based on these keywords, categorize the following expense.\n") + f"Description: {description}\n"
    print("prompt = ", prompt)
    tokens_count = count_tokens(prompt,'cl100k_base')
    print("tokens_count = ", tokens_count)
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.3,
        max_tokens=400
    )
    print("response = ", response)
    response_text = response.choices[0].text.strip()
    response_text = response_text.replace("'", '"')
    json_data = json.loads(response_text)
    print("json_data = ", json_data)
    category = json_data['category']
    is_expense = json_data['is_expense']
    print(f"Category: {category}, Is Expense: {is_expense}")
    token_used = response.usage.total_tokens
    print("token_used = ", token_used)
    
    # print("completion_tokens = ", completion_tokens, "prompt_tokens = ", prompt_tokens)
    return category, is_expense, token_used

def categorize_kotak_expenses():
    print("Categorising kotak expenses now ...")
    kotak_expenses_file = main_folder + month_folder + "/" + "kotak/" + "debit_data.csv"
    if not kotak_expenses_file:
        print("Kotak File not found")
        return
    print("kotak file_path ->", kotak_expenses_file)
    df = pd.read_csv(kotak_expenses_file)
    df["IS_EXPENSE"] = ""
    df["GPT_CATEGORY"] = ""
    df["TOKENS_USED"] = ""
    print("df = ", df)
    for index, row in df.iterrows():
        print("row ----->", row)
        category, expense, tokens_used = classify_kotak_expense(row["DESCRIPTION"])
        df.at[index, 'GPT_CATEGORY'] = category
        df.at[index, 'IS_EXPENSE'] = expense
        df.at[index, 'TOKENS_USED'] = tokens_used
    
    print("final df = ", df)
    total_tokens_used = df['TOKENS_USED'].sum()
    print("total_tokens_used = ", total_tokens_used)
    save_kotak_csv(df, "expense_data_categorized")

def experiment_code():
    print("Experimenting now ...")
    classify_kotak_expense("UPI/mohankumaarrr@o/440295538741/UPI")
    
def count_tokens(string: str, encoding_name: str) -> int:
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

# experiment_code()
# categorize_splitwise_expenses()
categorize_kotak_expenses()