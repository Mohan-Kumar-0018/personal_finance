from openai import OpenAI
from process_splitwise_html import save_splitwise_csv
from process_kotak import save_kotak_csv
import pandas as pd
import os
client = OpenAI()
main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')

def categorize_expenses():
    print("Categorising expenses now ...")

    spliwise_expense_file = "splitwise_expense.csv"


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
    return ["Travel", "Food and groceries", "Entertainment and lifestyle", "Basic needs"]

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
              f"- 'lunch, dinner,kakatiya ': Food and groceries\n")

    return rule1

def categorize_kotak_expenses():
    print("Categorising kotak expenses now ...")
    kotak_expenses_file = main_folder + month_folder + "/" + "kotak/" + "debit_data.csv"
    if not kotak_expenses_file:
        print("Kotak File not found")
        return
    print("kotak file_path ->", kotak_expenses_file)
    df = pd.read_csv(kotak_expenses_file)
    df["GPT_CATEGORY"] = ""
    print("df = ", df)
    for index, row in df.iterrows():
        print("row ----->", row)
        category = classify_expense(row["DESCRIPTION"], "")
        df.at[index, 'GPT_CATEGORY'] = category
    
    print("final df = ", df)
    save_kotak_csv(df, "expense_data_categorized")



# categorize_splitwise_expenses()
categorize_kotak_expenses()