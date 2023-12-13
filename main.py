import polars as pl
from solver import Solver
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--filePath", default="input.json")
parser.add_argument("--checkinDate", default="2019-12-25")
parser.add_argument("--dateRange", default=5, type=int)
args = parser.parse_args()

if __name__ == "__main__":
    solver = Solver(filePath=f"data/{args.filePath}", 
                    checkinDate=args.checkinDate,
                    valid_range=args.dateRange) \
            .saveResultToFile()
    print(f"Init data: {solver.getInputDf()}")
    print(f"Result data: {solver.getOutputDf()}")