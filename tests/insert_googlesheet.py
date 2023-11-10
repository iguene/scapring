import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(creds)
spreadsheet = client.open('TEST')

worksheet = spreadsheet.sheet1

values = [['Donnée1', 'Donnée2', 'Donnée3'], ['Donnée4', 'Donnée5', 'Donnée6']]
worksheet.insert_rows(values, row=1)

print("Données insérées avec succès.")