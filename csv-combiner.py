import argparse
import sys
from csv_manager import csvObj

'''
Handle command line arguments
'''
parser = argparse.ArgumentParser(prog='csv-combiner.py',
                                 description='Combine csv files. ')
parser.add_argument('filename', 
                    metavar='files', 
                    type=argparse.FileType('r'), 
                    nargs='+')
args = parser.parse_args()


# Files into Objects
fileList = [csvObj(file.name) for file in args.filename]

'''
Check column names
'''
for file in fileList:
    file.set_columns()

name_of_column = ""
try:
    name_of_column = fileList[0].get_columns()
    for file in fileList:
        if name_of_column != file.get_columns():
            raise ValueError("Unmatched column name", 
                              name_of_column, 
                              file.get_columns(),
                              file.get_name())
except ValueError as err:
    print(err.args)
    sys.exit("Make sure csv files have matching columns.")

'''
New csv file output to stdout
'''
# Initialize column names for output file
sys.stdout.write(name_of_column.strip() 
                 + ',\"filename\"\n')

# Append each csv file to the output file
for file in fileList:
    file.write_to_file()