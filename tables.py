import pandas as pd
import time, datetime

def makeTable(results):
    df_table = pd.DataFrame( results )
    return df_table
    #print(df_table)
    #print(df.info())

def writeExcel(results , name ):

    tableName = name + "--" + datetime.date.today().strftime("%d.%m.%Y") + ".xlsx"
    df_table = makeTable(results)
    writer = pd.ExcelWriter( tableName  , engine='xlsxwriter')
    # Convert the dataframe to an XlsxWriter Excel object.
    df_table.to_excel(writer, sheet_name='Sheet1')
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

    print(tableName + " saved!!!")


