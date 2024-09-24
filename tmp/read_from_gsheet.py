import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

# Define the scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

# Add your JSON key file name here
creds = ServiceAccountCredentials.from_json_keyfile_name('/Users/kumar/sideprojects/gcp_credentials/eastern-amp-436415-b9-8a4db89f99b3.json', scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the spreadsheet by name or URL
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/17Ag0AUQY_yl6IgbKPhIVDTGgw4s8x2zzgRu5_ivY4VQ/edit?gid=0#gid=0')

# Select the first sheet
worksheet = spreadsheet.sheet1
print("worksheet.title = ",worksheet.title)

# Get all records as a list of dictionaries
data = worksheet.get_all_records()

# Print the data
# for record in data:
#     print(record)



# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Print the first few rows of the DataFrame
print(df.head())

# Print DataFrame info (column names, data types, non-null counts)
print(df.info())