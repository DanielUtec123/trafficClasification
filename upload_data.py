import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name('/home/daniel/Documents/Utec/7to ciclo/Redes y Comunicaciones/Proyecto/scripts/client_secret.json', scope)
client = gspread.authorize(credentials)


def add_record(values):
    spreadsheet = client.open('training_dataset')
    ws = spreadsheet.get_worksheet(0)
    ws.append_row(values)

