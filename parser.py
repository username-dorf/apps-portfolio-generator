from google_play_scraper import app
from urllib import response

import xlsxwriter
import requests
import os

PACKAGES = [
    'games.urmobi.dotsmatch3',
    'games.urmobi.found.it'
    #'co.urmobi.CountAndLoop'
]

SETUP = [
    ("Icon", 10, False),  # text, width, wrap
    ('App ID', 40, False),
    ("Title", 40, False),
    ("Genre", 10, False),
    ("Installs", 15, False),
    ("Release Date", 15, False),
    ("Url", 15, True),
]

def parse_single(package):
    return app(package, lang='en', country='us')


def filter_single(parsed):
    return [parsed['appId'], parsed['title'], parsed['genre'], parsed['installs'], parsed['released'], parsed['url']]


def get_app_folder(parsed):
    app_folder = 'apps_content/' + parsed['title']
    if not os.path.exists(app_folder):
        os.mkdir(app_folder)
    return app_folder


def request_ico(parsed):
    response = requests.get(parsed['icon'])
    app_folder = get_app_folder(parsed)
    path = app_folder + '/icon.png'
    open(path, 'wb').write(response.content)
    return path


def request_screenshots(parsed):
    app_folder = get_app_folder(parsed)
    links = parsed['screenshots']
    screenshot_amount = 3
    screenshot_list = []
    if len(links) < screenshot_amount:
        screenshot_amount = len(links)
    for index in range(screenshot_amount):
        response = requests.get(links[index])
        path = (app_folder + '/screenshot{}.png').format(index)
        open(path, 'wb').write(response.content)
        screenshot_list.append(path)
    return screenshot_list


def get_bold_format(workbook):
    return workbook.add_format({'bold': True})


def get_wrap_format(workbook):
    return workbook.add_format({'text_wrap': True})


def format_column(worksheet):
    for i in range(len(SETUP)):
        worksheet.set_column(i, i, SETUP[i][1])


def write_headers(workbook, worksheet):
    headers = [item[0] for item in SETUP]
    for i in range(len(headers)):
        worksheet.write(0, i, headers[i], get_bold_format(workbook))


def write_to_xlsx(icon_path, rows, workbook, worksheet, row):
    text_format = workbook.add_format({'text_wrap': True})
    write_headers(workbook, worksheet)
    col = 1
    for i in range(len(rows)):
        worksheet.insert_image(row + i, col-1, icon_path, {"x_scale": 0.1, "y_scale": 0.1})
        for j in range(len(rows[i])):
            worksheet.write(row + i, col + j, rows[i][j], text_format)


def write_screenshots(screenshots_path_array, rows, worksheet, row):
    col = 1
    for i in range(len(rows)):
        for j in range(len(screenshots_path_array)):
            worksheet.insert_image(row + i, col + len(rows[i])+j*2, screenshots_path_array[j],
                                   {"x_scale": 0.4, "y_scale": 0.4})

def create_workbook(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
    workbook = xlsxwriter.Workbook(file_name)
    return workbook


def create_worksheet(workbook):
    worksheet = workbook.add_worksheet("Apps")
    return worksheet


def create_record(package, workbook, worksheet, package_index):
    parsed = parse_single(package)
    filtered = filter_single(parsed)
    icon_path = request_ico(parsed)
    screenshot_paths = request_screenshots(parsed)
    row = package_index+1
    worksheet.set_row(row, 160) # +1 to offset headers
    write_to_xlsx(icon_path, [filtered, ], workbook, worksheet, row)
    write_screenshots(screenshot_paths, [filtered, ], worksheet, row)
    print(filtered)


def main():
    file_name = 'apps.xlsx'
    workbook = create_workbook(file_name)
    worksheet = create_worksheet(workbook)
    format_column(worksheet)
    for index, package in enumerate(PACKAGES):
        create_record(package, workbook, worksheet, index)

    workbook.close()

if __name__ == "__main__":
    main()
