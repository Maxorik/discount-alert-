import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# Путь к JSON-файлу
SERVICE_ACCOUNT_FILE = 'service_account.json'

# Определение областей доступа
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Авторизация
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# Открытие таблицы по названию
spreadsheet = client.open_by_key("18I0IZJbCrAehSGw6Zq1KDyv9aHVJwIoBHlH0hufc-a8")

# Выбор нужной вкладки (листа)
worksheet = spreadsheet.worksheet("parsed_components")

# Чтение всех значений
data = worksheet.get_all_values()
for row in data:
    print(row)

now = datetime.now()
formatted_datetime = now.strftime("%d.%m.%y, %H:%M")
worksheet.update('G2', [[formatted_datetime]])

# Пример: массовое обновление диапазона
worksheet.update('B2:F2', [[0, 0, 0, 0, 0]])
