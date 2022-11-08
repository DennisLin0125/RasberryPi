from openpyxl import Workbook
import requests
import openpyxl 
url = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json'
wb=Workbook()
ws=wb.create_sheet('Ubike',0)

arr=[]
if __name__ == "__main__":
    response  = requests.get(url)
    a = response.json()
    b=a['retVal'].keys()
    c=a['retVal']['0001'].keys()

    for x in b:
        for j in c:
            arr+=[a['retVal'][x][j]]
        ws.append(arr)
        arr=[]
wb.save('台北市Ubike即時資料.xlsx')