import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(creds)
spreadsheet = client.open('TEST')

worksheet = spreadsheet.get_worksheet(1)

def insert_lines(values: list, row: int):
    """INSERER un tableau de lignes dans le Google Sheet
    Exemple: values = [['Donnée1', 'Donnée2', 'Donnée3'], ['Donnée4', 'Donnée5', 'Donnée6']]"""
    worksheet.insert_rows(values, row)
    print(values, "inséré(s) à la colonne", row, '.')

def get_lines():
    """Récupere les lignes et renvoie un tableau de lignes."""
    cells = worksheet.get_all_values()
    return cells

def clear_sheet():
    worksheet.clear()

def update_cells(row, col, value):
    worksheet.update_cell(row, col, value)

if __name__ == "__main__":
    #insert_lines([['test', 'test2', 'test3']], 1)

    worksheet.update_cell(1, 1, "test")
