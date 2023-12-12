import polars as pl
from solver import Solver
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--filePath", default="data/input.json")
parser.add_argument("--checkinDate", default="2019-12-25")
parser.add_argument("--dateRange", default=5, type=int)
args = parser.parse_args()

if __name__ == "__main__":
    solver = Solver(filePath=args.filePath, 
                    checkinDate=args.checkinDate,
                    valid_range=args.dateRange)
    print(f"Result data: {solver.getOutputDf()}")