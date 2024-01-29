import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime
import os

# Read the HTML file
file_path = '/Users/kumar/Downloads/splitwise_1.html'
with open(file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse the HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the div with id "expenses"
outer_div = soup.find('div', id='expenses')

# Check if the "expenses" div is found
if outer_div:
    month_divider_div = outer_div.find('div', class_='month-divider')
    data = []
    if month_divider_div:
    # Extract and print the text content of the span inside "month-divider"
        span_text = month_divider_div.find('span').get_text()
        print("month = ",span_text)
        expense_divs = outer_div.find_all('div', class_='expense', id=True)
        for expense_div in expense_divs:
            print("expense_div id= ", expense_div['id'])
            data_date_value = expense_div['data-date']
            datetime_object = datetime.strptime(data_date_value, "%Y-%m-%dT%H:%M:%SZ")
            formatted_date = datetime_object.strftime("%d-%m-%Y")
            summary_div = expense_div.find('div', class_='summary')
            if summary_div:
                data_involved_div = summary_div.find_next('div', {'data-involved': True})
                if data_involved_div:
                    data_involved = data_involved_div['data-involved']
                    main_block_div = data_involved_div.find('div', class_='main-block')
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
                                group_name = ""
                            else:
                                title = ""
                                group_name = ""
                        else:
                            print("No description header div found.")
                    else:
                        print("No main-block div found.") 
                    cost_div = data_involved_div.find('div', class_='cost')
                    if cost_div:
                        paid_by = cost_div.get_text(strip=True, separator='\n').split()[0]
                        total_amount = cost_div.find('span', class_='number').get_text(strip=True)
                    else:
                        print("No cost div found.")
                    you_div = data_involved_div.find('div', class_='you')
                    if you_div:
                        # print("you_div = ", you_div)
                        share_amount = cost_div.find('span').get_text(strip=True)
                        # print("you_div.attrs = ", you_div.attrs)
                        # you_class = cost_div.find('span').attrs
                        # print("you_class = ", you_class)
                        print("share_amount = ", share_amount)
                        
                    else:
                        print("No you div found.")
                else:
                    print("No next div with data-involved found.")

                
                
            else:
                print("No element with class 'summary' found.")
            data.append({
                'ROW_ID': expense_div['id'],
                'TRANSACTION_DATE': formatted_date,
                "DATA_INVOLVED": data_involved,
                'TITLE': title,
                'GROUP_NAME': group_name,
                'PAID_BY': paid_by,
                'TOTAL_AMOUNT': total_amount,
                'SHARE_AMOUNT': share_amount
            })

        df = pd.DataFrame(data)
        main_folder = "/Users/kumar/personal_finance/"
        month = "jan_2024"
        current_folder = main_folder + month + "/"
        file_path = current_folder + 'splitwise_data.csv'
        df.to_csv(file_path, index=False)

        print("df = ", df)
    else:
        print("No element with class 'month-divider' found.")
else:
    print("No element with class 'month-divider' found.")
