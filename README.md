# personal_finance

System Pre-requisite:
    python3

Setup:
 - Run command `make setup` for packages installation

Steps:
Pre-requisite:
1. Configure MAIN_FOLDER from Makefile in local.
2. Configure YEAR_MONTH from Makefile in local.
3. Add OPENAI_API_KEY env variable in makefile. (bash export not working in local. Need to check)
4. Create month folder under main folder in format - mmm_YYYY (Eg: feb_2024)

Splitise Data extraction:
1. Create folders for spliwise under month folder
    - https://secure.splitwise.com/#/all
    - Open spliwise all expenses link and load more data if needed for entire month that needs calculation
    - Save as html file from browser and add to corresponding month splitwise folder
    - Save file with name ending with *splitwise.html
2. Run Command `make splitwise` for data extraction

Kotak Data Extraction:
1. Create kotak folder under month folder
    - Download transactions data for the mont in csv file format from kokat net banking
    - Save file with name ending with *kotak.csv
2. Run Command `make kotak` for data extraction

Expense cateorization
1. Run Command `make local` for expense categorization - currenly configured for splitwise
2. Prompts added in code for now (move to folder - pending
3. Categorized Files will be generated inside corresponding folders.

Pending:
2. Kotak - Add filter based on YEAR_MONTH
3. Expense category and sub-category - finalise
4. Have global prompt and monthly prompt - Read from files - to use in chatgpt
5. Ignore invalid expenses using prompts.
6. Combine splitwise and bank transactions - for expense categorization



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
4. Utiltity payments - Basic needs
5. Petrol and toll - Travel
6.  -->