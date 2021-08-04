import pyodbc
import azure_config

driver = azure_config.driver
server = azure_config.server
database = azure_config.database
username = azure_config.username
password = azure_config.password

with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*)'rows',COUNT(DISTINCT Player_Name) 'Players' FROM dbo.PlayerRank")
        row = cursor.fetchone()
        while row:
            print(row)
            row = cursor.fetchone()