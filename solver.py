import json
import polars as pl
from datetime import datetime, timedelta



class Solver():
    def __init__(self, filePath: str, checkinDate: str, valid_range: int):
        self.filePath = filePath
        self.checkinDate = datetime.strptime(checkinDate, '%Y-%m-%d')
        self.valid_range = valid_range
    
    def __loadRawFileToDF(self):
        """Load the JSON file to the `DataFrame` without any processing

        Returns:
            _type_: _description_
        """
        with open(file=self.filePath, mode="rb") as f:
            self.df = pl.read_json(source=f.read())
        return self
    
    def __loadFileToDF(self):
        """Load the JSON file to the `DataFrame` in table-like structure

        Returns:
            _type_: _description_
        """
        self.__loadRawFileToDF()\
            .__json_normalize()
        return self
    
    def __json_normalize(self):
        """Decompose json-like structure of raw file
        into readable table-like structure of the dataframe

        Returns:
            
        """
        self.df = self.df.explode("offers")\
                         .unnest("offers")\
                         .explode("merchants")\
                         .rename({
                             "id" : "offer_id" # RENAME TO AVOID CONFUSION WITH MERCHANT ID
                         })\
                         .unnest("merchants")\
                         .cast({
                             "valid_to" : pl.Date
                         })
        return self
    
    def saveResultToFile(self):
        """Save result `DataFrame` to output.json file

        Returns:
        """
        if not hasattr(self, "resultDf"): # ENSURE RESULT DATAFRAME IS INIT
            self._solve()
        merchantCols = ["id", "name", "distance"] # MERCHANTS-RELATED COLUMN NAME
        # CONVERT THE DATAFRAME TABLE-LIKE STRUCTURE
        # TO JSON-LIKE STRUCTURE
        resultDf = pl.DataFrame(data={
            "offers" : [
                self.resultDf.with_columns(pl.struct(pl.col(merchantCols)).alias("merchants")) # CREATE NEW COLUMN AS GROUP OF MERCHANTS-RELATED COLS
                             .select(pl.exclude(merchantCols)) # REMOVE OLD MERCHANTS COLs
                             .rename({"offer_id" : "id"}) # RENAME TO FIT WITH OUTPUT FORMAT
                             .cast({"valid_to" : str}) # CAST VALID_TO DATATYPE FROM DATE TO STRING 
                             .to_dicts() # CONVERT TO list[dict[str, any]] TYPE TO FIT WITH OUTPUT FORMAT
            ]
        })
        # WRITE TO output.json FILE
        with open("output.json", "w") as f:
            output = ",\n".join(json.dumps(x, indent=2) for x in resultDf.to_dicts()) # CONVERT PY OBJECT TO JSON STR
            f.write(output)
        return self
    
    def _solve(self):
        """Filter out the offers in 5 steps
        1.  Filter out offers that are not valid within check-in date + 5 days and not in the required category.
        2.  Find the offer with the closest merchants for every category.
        3.  There might be case that more than one offers has same closest merchants, so choose the first one order by their name.
        4.  Sort the offers by distance from closest to furthest.
        5.  Choose the best 2 offers.

        Returns:
            _type_: _description_
        """
        if not hasattr(self, "df"): # ENSURE INPUT DATAFRAME IS INIT
            self.__loadFileToDF()
        filteredCategory = [1, 2, 4] # ONLY CHOOSE OFFERS FROM THESE CATEGORY (Restaurant, Retail, Activity)
        self.resultDf = self.df.filter(pl.col("category").is_in(filteredCategory),
                                       pl.col("valid_to") >= self.checkinDate + timedelta(days=self.valid_range))\
                               .filter(pl.col("distance") == pl.col("distance").min().over("category"))\
                               .filter(pl.col("name") == pl.col("name").min().over("category"))\
                               .sort(by="distance", descending=False)\
                               .head(2)
        return self
        
    def getInputDf(self) -> pl.DataFrame:
        """Get input `DataFrame`

        Returns:
            `pl.DataFrame`: Input `DataFrame` in table structure
        """
        if not hasattr(self, "df"):
            self.__loadFileToDF()
        return self.df

    def getOutputDf(self) -> pl.DataFrame:
        """Get output `DataFrame`

        Returns:
            `pl.DataFrame`: Output `DataFrame` in table structure
        """
        if not hasattr(self, "resultDf"):
            self._solve()
        return self.resultDf