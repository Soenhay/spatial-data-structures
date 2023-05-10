import pandas as pd
from pathlib import Path

class MyDataframeManager:
    def __init__(self, timeInfos, absolutePathAndFilename, pandasColumns, indexCols = None):
        self.timeInfos = timeInfos
        self.df = pd.read_csv(absolutePathAndFilename, usecols = pandasColumns)
        self.columns = pandasColumns

        #create an index on the dataframe for flightId column to make things faster.
        if indexCols is not None:
            self.df = self.df.set_index(indexCols)
        

    # def oneFileToRuleThemAll():
    #     df = None
    #     fname = input_data_folder / 'flightTelemAll.csv'

    #     if not Path.isfile(fname):
    #         dfs = []
    #         #Relative paths are relative to current working directory. Since this project is in a sub folder the path needs to include it.
    #         dfs.append(pd.read_csv(input_data_folder / 'flightAdsb.csv', usecols = columns))
    #         dfs.append(pd.read_csv(input_data_folder / 'flightTelem.csv', usecols = columns))
    #         dfs.append(pd.read_csv(input_data_folder / 'flightTelem2.csv', usecols = columns))
    #         df = pd.concat(dfs, ignore_index=True)
    #         df.to_csv(fname, encoding='utf-8', index=False, columns = columns)
    #     else:
    #         df = pd.read_csv(fname, usecols = columns)
    #     return df


    def dfSpecs(self):
        #print(f'Row count: {len(df.index)}')
        print(f'Row count: {self.df.shape[0]}')
        #print(f'Row count: {ddf[df.columns[0]].count()}')
        print(f'Column count: {len(self.df.columns)}')
        print(f'Memory usage: \n{self.df.memory_usage()}')

    
    def getPoints(self):
        return []
    