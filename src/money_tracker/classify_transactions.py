import re
import pandas as pd


def classify_credit_transactions(banks_credits_df):
  banks_credits_df['IS_INCOME'] = ''
  for index, row in banks_credits_df.iterrows():
    # NACH-DB is a transaction from Stocks Dividends
    if str(row['DESCRIPTION']).startswith('NACH-') & str(row['TRANSACTION_ID']).startswith('NACHDB'):
      banks_credits_df.at[index, 'IS_INCOME'] = 'YES'
      continue
      
    # Kotak Savings Account Interest
    kotak_interest_pattern = r"^Int\.Pd:(\d+):(\d{2}-\d{2}-\d{4}) to (\d{2}-\d{2}-\d{4})$"
    match = re.match(kotak_interest_pattern, str(row['DESCRIPTION']))
    if match and (pd.isna(row['TRANSACTION_ID']) or row['TRANSACTION_ID'] == '') and 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
      banks_credits_df.at[index, 'IS_INCOME'] = 'YES'
      continue

    # Kotak Salary:
    salary_pattern = r"^NEFT.*SHOPUP INDIA TECHNOLOGIES.*$"
    match = re.match(salary_pattern, str(row['DESCRIPTION']))
    if match and 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
      banks_credits_df.at[index, 'IS_INCOME'] = 'YES'
      continue

    # PNB Savings Account Interest
    pnb_interest_pattern = r"^(\d+):Int\.Pd:(\d{2}-\d{2}-\d{4}) to (\d{2}-\d{2}-\d{4})$"
    match = re.match(pnb_interest_pattern, str(row['DESCRIPTION']))
    if match and (pd.isna(row['TRANSACTION_ID']) or row['TRANSACTION_ID'] == '') and 'PNB'.lower() in str(row['ACCOUNT']).lower():
      banks_credits_df.at[index, 'IS_INCOME'] = 'YES'
      continue

  return banks_credits_df

def classify_debit_transactions(banks_debits_df):
  banks_debits_df['IS_INVESTMENT'] = ''
  banks_debits_df['IS_EXPENSE'] = ''
  for index, row in banks_debits_df.iterrows():
      # SVV GOLD Plan
      svv_gold_plan_pattern = r".*SRI VALLI VILAS.*"
      match = re.match(svv_gold_plan_pattern, str(row['DESCRIPTION']))
      if match:
        banks_debits_df.at[index, 'IS_INVESTMENT'] = 'YES'
        continue

      if 'KOTAK'.lower() in str(row['ACCOUNT']).lower():
        # Kotak INDMoney
        indmoney_pattern = r".*INDMoney.*"
        match = re.match(indmoney_pattern, str(row['DESCRIPTION']))
        if match:
          banks_debits_df.at[index, 'IS_INVESTMENT'] = 'YES'
          continue

        # Zerodha
        zerodha_pattern = r".*Zerodha Broking.*"
        match = re.match(zerodha_pattern, str(row['DESCRIPTION']))
        if match:
          banks_debits_df.at[index, 'IS_INVESTMENT'] = 'YES'
          continue

      

  return banks_debits_df