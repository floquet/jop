# # imports
import os           # probe, change directories
import sys          # python version
import datetime     # https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python

import pandas as pd
import h5py

# provenance
print( "\n", datetime.datetime.now( ) )
print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
print( "python version %s" % sys.version )

dataSource = "c:/Users/topad/python/xl/NATO/NATO Spreadsheet.xlsx"
dataSource = "c:/Users/topad/python/xl/NATO/test.xlsx"
dataSource = "../sample.xlsx"

nameSheet = "charlie"

print( "\nreading %s with pandas" % dataSource )
print( "\nreading sheet '%s' with pandas" % nameSheet )

# read by default 1st sheet of an excel file
# dataframe1 = pd.read_excel( io = dataSource, sheet_name = nameSheet )['B']
dataframe1 = pd.read_excel( io = dataSource, sheet_name = nameSheet, usecols = "B:C", header = 2, engine='openpyxl' )
dataframe1.to_hdf()

print( "\ndataframe" )
print ( dataframe1 )

print( "\ntype dataframe" )
print ( type( dataframe1 ) )


print( "\ndataframe shape" )
print ( dataframe1.shape )

# dantopa@Xiuhcoatl.local:demo $ python dataframe.py

#  2022-12-30 10:08:11.325389
# source: /Volumes/repos/github/jop/python/catalog/demo/dataframe.py
# python version 3.10.9 (main, Dec 11 2022, 07:43:52) [Clang 14.0.0 (clang-1400.0.29.202)]

# reading ../sample.xlsx with pandas

# reading sheet 'charlie' with pandas

# dataframe
#         Marking  Unnamed: 2
# 0        SECRET         NaN
# 1       unclass         NaN
# 2  unclassified         NaN
# 3             U         NaN

# type dataframe
# <class 'pandas.core.frame.DataFrame'>

# dataframe shape
# (4, 2)
