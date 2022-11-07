import openpyxl as xl
import twstock_dashboard as td

filename='twstock_dashboard.xlsx'      
stocks = ['0050', '0056', '2317', '2330', '2302', '2454', '2303', '1303', '2301', '2324', '2367', '3008',
          '2409', '3481', '3049', '2002', '3105', '2603', '2609', '2615', '2618', '2610','2344']
token='zTwPX9x9iEXIDbymJDhLkCyVk9DMkV3MtDkU6XgPGrG'   
td.create_dashboard(filename, stocks, token)  

wb=xl.load_workbook('twstock_dashboard.xlsx')   # 開啟工作簿檔案
ws=wb.active   # 取得目前工作表
td.update_dashboard(ws)  # 更新股票看板 (爬聚財網 + Line Notify 推播)
wb.save('twstock_dashboard.xlsx')  # 將工作簿存檔

 
   