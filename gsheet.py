import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

client = gspread.authorize(creds)
spreadsheet = client.open('TEST')

worksheet = spreadsheet.sheet1

def insert_lines(values: list, row: int):
    """INSERER un tableau de lignes dans le Google Sheet
    Exemple: values = [['Donnée1', 'Donnée2', 'Donnée3'], ['Donnée4', 'Donnée5', 'Donnée6']]"""
    worksheet.insert_rows(values, row)
    print(values, "inséré(s) à la colonne", row, '.')


def read_gsheet(spreadsheet, range_name):
    worksheet = spreadsheet.sheet1

    # Récupérer les valeurs dans la plage spécifiée
    values = worksheet.get(range_name).execute().get("values", [])

    # Transposer les valeurs pour obtenir une liste par colonne
    columns = list(map(list, zip(*values)))

    return columns

if __name__ == "__main__":
    insert_lines([['test', 'test2', 'test3']], 1)