import pandas as pd
from datetime import datetime, timedelta
import table_prices

def write_data():

    # logger.info("csv started interval")
    print("csv started interval", file=open('logs.txt', 'a'))
    now = datetime.now()

    df, df1, df2 = table_prices.main()
    df.loc[-1] = str(now)  # adding a row
    df.index = df.index + 1  # shifting index
    df.sort_index(inplace=True)

    df.to_csv('data.csv')

    df1.to_csv('park.csv')
    df2.to_csv('top_sto.csv')

    # logger.info("csv written interval")
    print("csv written interval", file=open('logs.txt', 'a'))
    # logger.debug(now)
    print(now, file=open('logs.txt', 'a'))

write_data()