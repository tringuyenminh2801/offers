from datetime import datetime, timedelta
import polars as pl

class Solver():
    def __init__(self, filePath: str, checkinDate: str, valid_range: int):
        self.filePath = filePath
        self.checkinDate = datetime.strptime(checkinDate, '%Y-%m-%d')
        self.valid_range = valid_range
        self.__loadFileToDF()
    
    def __loadRawFileToDF(self):
        with open(file=self.filePath, mode="rb") as f:
            self.df = pl.read_json(source=f.read())
        return self
    
    def __loadFileToDF(self):
        self.__loadRawFileToDF()\
            .__json_normalize()
        return self
    
    def __json_normalize(self):
        self.df = self.df.explode("offers")\
                         .unnest("offers")\
                         .explode("merchants")\
                         .rename({
                             "id" : "offer_id"
                         })\
                         .unnest("merchants")\
                         .cast({
                             "valid_to" : pl.Date
                         })
        return self
    
    def saveResultToFile(self):
        if not hasattr(self, "resultDf"):
            self._solve()
        merchantCols = ["id", "name", "distance"]
        resultDf = pl.DataFrame(data={
            "offers" : [
                self.resultDf.with_columns(pl.struct(pl.col(merchantCols)).alias("merchants"))\
                             .select(pl.exclude(merchantCols))\
                             .rename({"offer_id" : "id"})\
                             .to_dicts()
            ]
        })
        resultDf.write_json(file="output.json",
                            pretty=True,
                            row_oriented=True)
        return self
    
    def _solve(self):
        if not hasattr(self, "df"):
            self.__loadFileToDF()
        filteredCategory = [1, 2, 4]
        self.resultDf = self.df.filter(pl.col("category").is_in(filteredCategory),
                                       pl.col("valid_to") >= self.checkinDate + timedelta(days=self.valid_range))\
                               .filter(pl.col("distance") == pl.col("distance").min().over("category"))\
                               .filter(pl.col("name") == pl.col("name").min().over("category"))\
                               .sort(by=["distance", "valid_to"], descending=[False, True])\
                               .head(2)
        return self
        
    def getInputDf(self):
        if not hasattr(self, "df"):
            self.__loadFileToDF()
        return self.df

    def getOutputDf(self):
        if not hasattr(self, "resultDf"):
            self._solve()
        return self.resultDf