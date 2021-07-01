import pandas as pd
from sqlalchemy import create_engine
import os

cwd = os.getcwd()

already_installed = []

data = []
def create_df(all_files):
    for i in range (len(all_files)):
        if all_files[i] in already_installed:
            pass
        else:
            filename = cwd + "\\Stats\\" + all_files[i]
            df = pd.read_excel(filename, sheet_name='Match Coordinates Statistics')
            for index, rows in df.iterrows():
                # Select the wanted columns to fetch from the spreadsheets!!!!
                my_lis = [rows["timestamp"], rows["playerId"], rows["posX.1"], rows["posY.1"]]
                data.append(my_lis)
            already_installed.append(all_files[i])
    print(already_installed)


def sendToDB(downloaded_spreadsheets):
    create_df(downloaded_spreadsheets)
    # Select the wanted columns to create the dataframe that will be sent to the DB!!!!
    df2 = pd.DataFrame(data=data, columns=["timestamp", "playerId", "PosX", "PosY"])
    engine = create_engine("mysql+mysqlconnector://root:root@127.0.0.1/gengee")
    df2.to_sql(name="data",con=engine,if_exists='replace',index=False, chunksize=1000)