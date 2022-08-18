
from google_play_scraper import app
from urllib import response

import xlsxwriter
import requests
import os 


def parse_single(package):
    return app(package)

def filter_single(parsed):
    return [parsed['appId'], parsed['title'], parsed['genre'],  parsed['installs'], parsed['released']]

def get_app_folder(parsed):
    app_folder='apps_content/'+parsed['title']
    if not os.path.exists(app_folder):
        os.mkdir(app_folder)
    return app_folder

def request_ico(parsed):
    response = requests.get(parsed['icon'])
    app_folder=get_app_folder(parsed)
    path=app_folder+'/icon.png'
    open(path,'wb').write(response.content)

def request_screenshots(parsed):
    app_folder=get_app_folder(parsed)
    links=parsed['screenshots']
    sceenshot_amount=3
    if len(links)<sceenshot_amount:
        sceenshot_amount=len(links)
    for index in range(sceenshot_amount):
        response=requests.get(links[index])
        path=(app_folder+'/screenshot{}.png').format(index)
        open(path,'wb').write(response.content)

def get_bold_format(workbook):
    return workbook.add_format({'bold': True})

def write_headers(workbook):
    headers=['App ID', "Title", "Genre", "Installs", "Release Date"]
    for i in range(len(headers)):
        workbook.write(0,i,headers[i],get_bold_format(workbook))



def write_to_xlsx(rows):
    file_name='apps.xlsx'
    if os.path.exists(file_name):
        os.remove(file_name)

    print(rows)
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet("Apps")
    write_headers(workbook)
    row=1
    col=1
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            worksheet.write(row+i,col+j,rows[i][j])        
        row=i+1
    workbook.close()


def main():
    parsed=parse_single('co.urmobi.casual.larrysfishing')
    filtred=filter_single(parsed)
    request_ico(parsed)
    request_screenshots(parsed)
    write_to_xlsx([filtred,])
    print(filtred)

if __name__ == "__main__":
    main()

