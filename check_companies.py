import pandas as pd

# Read the Excel files
daily_reports_df = pd.read_excel('Daily Reports.xlsx')
applicants_df = pd.read_excel('Applicant Stages.xlsx')

print("\nCompanies in Daily Reports:")
print(daily_reports_df['companyName'].unique())

print("\nCompanies in Applicant Stages:")
print(applicants_df['company'].unique()) 