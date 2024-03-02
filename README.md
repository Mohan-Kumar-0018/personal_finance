# Expense Management System

## System Requirements
- Python 3

## Setup Instructions
Run the following command to install necessary packages:
    `make setup`


## Configuration Steps

### Pre-requisites
1. **Configure Main Folder**: Set the `MAIN_FOLDER` variable in the Makefile to match your local directory structure.
2. **Set Year and Month**: Adjust `YEAR_MONTH` in the Makefile to reflect the current period of interest.
3. **Environment Variable for API Key**: Add your `OPENAI_API_KEY` to your bash or zsh profile. This is necessary for expense categorization.
4. **Monthly Folder Creation**: Under the main folder, create a new directory for the month in the format `mmm_YYYY` (e.g., `feb_2024`).

### Splitwise Data Extraction
1. **Folder Setup**: Inside the monthly folder, create a new subfolder named `splitwise`.
2. **Data Download**:
    - Visit the [Splitwise All Expenses page](https://secure.splitwise.com/#/all).
    - Load the data for the entire month. Ensure all relevant data is displayed.
    - Save the webpage as an HTML file within the `splitwise` folder.
    - The file should be named with a suffix `*splitwise.html`.
3. **Run Extraction**: Execute the following command to start the data extraction process:
    `make splitwise`


### Kotak Data Extraction
1. **Folder Setup**: Inside the monthly folder, create a new subfolder named `kotak`.
2. **Data Download**:
 - Log in to your Kotak net banking and download the transaction data for the month in CSV format.
 - Save the CSV file in the `kotak` folder with a suffix `*kotak.csv`.
3. **Run Extraction**: To extract data from the Kotak CSV file, run:
    `make kotak`


### Expense Categorization
1. **Run Categorization**: Execute the command below to categorize expenses. This is currently configured for Splitwise data.
    `make local`
2. **Prompt Configuration**: Prompts for categorization are currently hardcoded in the code.
3. **Output**: Categorized files will be generated inside their respective folders.

---


<!-- Pending:
2. Kotak - Add filter based on YEAR_MONTH
3. Expense category and sub-category - finalise
4. Have global prompt and monthly prompt - Read from files - to use in chatgpt
5. Ignore invalid expenses using prompts.
6. Combine splitwise and bank transactions - for expense categorization -->



<!-- Expenses and sub-categories:
1. Travel
2. Food and groceries
3. Entertainment and lifestyle
    - Movie, trips
4. Basic needs
    - includes Rent, maintenance
    - Utility payments like groceries, food, mobile recharge, wifi, electricity
    - 
5. Shopping

Sub Category - Category
1. Food - Basic needs
2. Groceries - Basic needs
3. Rent - Basic needs
4. Utility payments - Basic needs
5. Petrol and toll - Travel
6. Shopping - Lifestyle
7. Entertainment - Lifestyle
8. Drinks - Party
9. Petty Expenses - Basic needs -->
