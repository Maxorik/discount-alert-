# https://docs.google.com/spreadsheets/d/18I0IZJbCrAehSGw6Zq1KDyv9aHVJwIoBHlH0hufc-a8/edit?gid=391999805#gid=391999805

import gspread
import re
from google.oauth2.service_account import Credentials
from datetime import datetime
from market_parser import parse_market

def start_update():
    # json с доступом к sheets
    SERVICE_ACCOUNT_FILE = 'credentials/google_sheet.json'

    # куда доступ
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]

    # авторизация
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)

    # открытие таблицы по названию и выбор вкладки
    spreadsheet = client.open_by_key("18I0IZJbCrAehSGw6Zq1KDyv9aHVJwIoBHlH0hufc-a8")
    worksheet = spreadsheet.worksheet("parsed_components")

    # чтение всех значений
    data = worksheet.get_all_values()
    data.pop(0)

    # обновление цен
    for i in range(len(data)):
        try:
            get_current_price = parse_market(data[i][1])
            sheet_data = re.sub(r"[^0-9]", '', get_current_price)
            worksheet.update(f'G{i+2}', [[sheet_data]])
            print(f'price from {data[i][0]} is {get_current_price}')
        except Exception as e:
            worksheet.update(f'G{i+2}', [['error']])
            print('error', e)

    now = datetime.now()
    formatted_datetime = now.strftime("%d.%m.%y, %H:%M")
    worksheet.update('F2', [[formatted_datetime]])
