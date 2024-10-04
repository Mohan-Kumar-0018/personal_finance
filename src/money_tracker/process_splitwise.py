import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

main_folder = os.environ.get('MAIN_FOLDER')
month_folder = os.environ.get('YEAR_MONTH')


def read_from_splitwise_html(file,file_path):
    expense_boxes, transaction_boxes, errors = extract_valid_expense_and_transaction_boxes(file_path)
    print("expense_boxes length= ", len(expense_boxes))
    print("transaction_boxes length= ", len(transaction_boxes))
    print("errors length= ", len(errors))
    expense_data = extract_data_from_expense_boxes(expense_boxes)
    # Sort the expense data by date
    expense_data.sort(key=lambda x: datetime.strptime(x['DATE'], '%d-%m-%Y'))
    expense_df = pd.DataFrame(expense_data)
    expense_df.insert(0, 'S_NO', range(1, len(expense_df) + 1))
    expense_df['ACCOUNT'] = file
    expense_df['ACCOUNT_TYPE'] = 'SHARED_EXPENSE'
    expense_df["REMARKS"] = ""
    
    # print("TOTAL EXPENSES = ", expense_df['EXPENSE_AMOUNT'].sum())
    transaction_data = extract_data_from_transaction_boxes(transaction_boxes)
    # Sort the transaction data by date
    transaction_data.sort(key=lambda x: datetime.strptime(x['DATE'], '%d-%m-%Y'))
    transaction_df = pd.DataFrame(transaction_data)
    transaction_df.insert(0, 'S_NO', range(1, len(transaction_df) + 1))
    transaction_df['ACCOUNT'] = file
    transaction_df['ACCOUNT_TYPE'] = 'SHARED_EXPENSE'
    transaction_df["REMARKS"] = ""
    return expense_df, transaction_df


def extract_data_from_expense_boxes(expense_boxes):
    data = []
    for expense_box in expense_boxes:
        datetime_object = datetime.strptime(expense_box['data-date'], "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = datetime_object.strftime("%d-%m-%Y")
        main_block_div = expense_box.find('div', class_='main-block')
        spend_receivable = 0
        if main_block_div:
            main_block_header_div = main_block_div.find('div', class_='header')
            if main_block_header_div:
                a_tags = main_block_header_div.find_all('a')
                a_tags_length = len(a_tags)            
                if a_tags_length >= 2:
                    title = a_tags[0].get_text(strip=True)
                    group_name = a_tags[1].get_text(strip=True)
                elif a_tags_length == 1:
                    title = a_tags[0].get_text(strip=True)
                    group_name = "N/A"
                else:
                    title = "N/A"
                    group_name = "N/A"
                if title == "Settle all balances":
                    # Skip splitwise automated settlements
                    continue
            else:
                print("No description main-block div found.")
        else:
            print("No main-block header div found.")
        
        cost_div = expense_box.find('div', class_='cost')
        if cost_div:
            paid_by = cost_div.get_text(strip=True, separator='\n').split()[0]
            total_amount = cost_div.find('span', class_='number').get_text(strip=True)
            total_amount = float(total_amount.replace('₹', ''))
        else:
            print("No cost div found.")
        you_div = expense_box.find('div', class_='you')
        if you_div:
            you_span_div = you_div.find_next('span')
            share_amount = you_span_div.get_text(strip=True)
            share_amount = float(share_amount.replace('₹', ''))
            if paid_by == "you":
                expense_amount = total_amount - share_amount
                spend_receivable = total_amount - expense_amount
            else:
                expense_amount = share_amount
        else:
            print("No you div found.")    
        data.append({
            'DATE': formatted_date,
            'TITLE': title,
            'GROUP_NAME': group_name,
            'PAID_BY': paid_by,
            'TOTAL_AMOUNT': round(total_amount,2),
            'SHARE_AMOUNT': round(share_amount,2),
            'EXPENSE_AMOUNT': round(expense_amount,2),
            "SPEND_RECEIVABLE": round(spend_receivable,2),
        })
        
    return data

def extract_data_from_transaction_boxes(transaction_boxes):
    data = []
    for transaction_box in transaction_boxes:
        datetime_object = datetime.strptime(transaction_box['data-date'], "%Y-%m-%dT%H:%M:%SZ")
        formatted_date = datetime_object.strftime("%d-%m-%Y")
        main_block_div = transaction_box.find('div', class_='main-block')
        if main_block_div:
            main_block_header_div = main_block_div.find('div', class_='header')
            if main_block_header_div:
                a_tag = main_block_header_div.find_next('a')
                full_text = a_tag.get_text().replace('\n', '').strip()
                paid_by = full_text.split("paid")[0].strip()
                start_index = full_text.find("paid")
                end_index = full_text.find("₹", start_index + len("paid"))
                group_name = full_text[start_index + len("paid"):end_index]
            else:
                print("No description main-block div found.")
        else:
            print("No main-block header div found.")
        cost_div = transaction_box.find('div', class_='cost')
        if cost_div:
            paid_by_text = cost_div.get_text().replace('\n', '').strip()
            if paid_by_text == "you paid":
                transaction_type = "DEBIT"
            else:
                transaction_type = "CREDIT"
        else:
            print("No cost div found.")
        you_div = transaction_box.find('div', class_='you')
        if you_div:
            you_span_div = you_div.find_next('span')
            total_amount = you_span_div.get_text(strip=True)
            total_amount = float(total_amount.replace('₹', ''))
        else:
            print("No you div found.")
        data.append({
            'DATE': formatted_date,
            'TYPE': transaction_type,
            'PAID_BY': paid_by,
            'GROUP_NAME': group_name,
            'AMOUNT': total_amount,
        })
    return data
    
def extract_valid_expense_and_transaction_boxes(file_path):
    expenses_list_div = get_expenses_list_table_element(file_path)
    errors = []
    expense_boxes = []
    transaction_boxes = []
    if expenses_list_div:
        expense_divs = expenses_list_div.find_all('div', class_='expense', id=True)
        for expense_div in expense_divs:
            data_date_value = expense_div['data-date']
            datetime_object = datetime.strptime(data_date_value, "%Y-%m-%dT%H:%M:%SZ")
            target_dt_obj = datetime.strptime(month_folder, "%b_%Y")
            if datetime_object.month != target_dt_obj.month or datetime_object.year != target_dt_obj.year:
                continue
            summary_div = expense_div.find('div', class_='summary')
            if summary_div:
                expense_summary_div = summary_div.find_next('div')
                if expense_summary_div:
                    if expense_summary_div.has_attr('data-involved'):
                        if expense_summary_div['data-involved'] == "true":
                            expense_boxes.append(expense_summary_div)
                    else:
                        if "involved" in expense_summary_div.attrs['class']:
                            transaction_boxes.append(expense_summary_div)
                else:
                    errors.append("expense_summart_not_found"+expense_div['id'])
            else:
                errors.append("summary_div_not_found"+expense_div['id'])
    else:
        errors.append("expenses_list_div_not_found")
    return expense_boxes, transaction_boxes, errors

def get_expenses_list_table_element(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    # Find the div with id "expenses_list"
    expenses_list_div = soup.find('div', id='expenses_list')
    if expenses_list_div:
       return expenses_list_div
    else:
        print("expense div not found")
    

def get_start_month(expense_div):
    month_divider_div = expense_div.find('div', class_='month-divider')
    if month_divider_div:
        # Extract and print the text content of the span inside "month-divider"
        month = month_divider_div.find('span').get_text()
        return month
