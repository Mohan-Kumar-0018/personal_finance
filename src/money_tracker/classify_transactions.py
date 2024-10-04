import re
import pandas as pd


def classify_credit_transactions(banks_credits_df):
  banks_credits_df['IS_INCOME'] = ''
  for index, row in banks_credits_df.iterrows():
    if is_income(row):
      banks_credits_df.at[index, 'IS_INCOME'] = 'YES'
      continue
  
  return banks_credits_df

def classify_debit_transactions(banks_debits_df):
  banks_debits_df['IS_INVESTMENT'] = ''
  banks_debits_df['IS_EXPENSE'] = ''
  for index, row in banks_debits_df.iterrows():
    if is_investment(row):
      banks_debits_df.at[index, 'IS_INVESTMENT'] = 'YES'
      continue

  return banks_debits_df

def is_income(row):
  # NACH-DB is a transaction from Stocks Dividends
  if str(row['DESCRIPTION']).startswith('NACH-') and str(row['TRANSACTION_ID']).startswith('NACHDB'):
    return True
    
  # Kotak Savings Account Interest
  kotak_interest_pattern = r"^Int\.Pd:(\d+):(\d{2}-\d{2}-\d{4}) to (\d{2}-\d{2}-\d{4})$"
  if re.match(kotak_interest_pattern, str(row['DESCRIPTION'])) and (pd.isna(row['TRANSACTION_ID']) or row['TRANSACTION_ID'] == '') and 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
    return True

  # Kotak Salary
  salary_pattern = r"^NEFT.*SHOPUP INDIA TECHNOLOGIES.*$"
  if re.match(salary_pattern, str(row['DESCRIPTION'])) and 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
    return True

  # PNB Savings Account Interest
  pnb_interest_pattern = r"^(\d+):Int\.Pd:(\d{2}-\d{2}-\d{4}) to (\d{2}-\d{2}-\d{4})$"
  if re.match(pnb_interest_pattern, str(row['DESCRIPTION'])) and (pd.isna(row['TRANSACTION_ID']) or row['TRANSACTION_ID'] == '') and 'PNB'.lower() in str(row['ACCOUNT']).lower():
    return True

  return False


def is_investment(row):
  # SVV GOLD Plan
  svv_gold_plan_pattern = r".*SRI VALLI VILAS.*"
  if re.match(svv_gold_plan_pattern, str(row['DESCRIPTION'])):
    return True

  if 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
    # Kotak INDMoney
    indmoney_pattern = r".*INDMoney.*"
    if re.match(indmoney_pattern, str(row['DESCRIPTION'])):
      return True

    # Zerodha
    zerodha_pattern = r".*Zerodha Broking.*"
    if re.match(zerodha_pattern, str(row['DESCRIPTION'])):
      return True

  return False
