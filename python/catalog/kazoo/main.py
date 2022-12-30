#! /usr/bin/python

# # catalog reader
# #   sweep an Excel file, harvesting information about a catalog

# # Daniel Topa     DTRIAC

# # provenance
import datetime             # timestamps
import os                   # opeating system
import sys                  # python version

# # computation
import pandas as pd
import h5py

# # toolkits
import xl_toolkit      # spreadsheet authoring tools


#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #

if __name__ == "__main__":

# 1. read data from the XL file
# 2. assemble data structure
# 3. produce ideal data file
# 4. census

    # specify spreadsheets
    dataPath = "/Volumes/repos/github/jop/python/catalog"
    dataURL = "https://docs.google.com/spreadsheets/d/1Y1dBWR9Rv03XKIBeKFXbKjMA2KXztbZ5fy6iiFHHGQQ/edit#gid=0"
    dataName = "sample.xlsx"
    sheetNames = [ "alpha", "bravo", "charlie" ]

    # diagnostic
    print( "\ndiagnostic print for data source" )
    print( "looking in directory '%s' for file '%s'" % ( dataPath, dataName ) )
    for name in sheetNames:
        print( "expecting sheet name '%s'" % name )

    #df = pd.read_excel( "../" + dataName, sheet_name = None, index_col = 0 )
    df = pd.read_excel( "../" + dataNamec )
    print( "df" )
    print( df )
    print( "df done\n" )

    # df = pd.read_excel( "../" + dataName, sheet_name = sheetNames, engine='openpyxl', header = 2 )
    # print(df.columns.ravel())

    # https://pbpython.com/pandas-excel-tabs.html
    #first_df = pd.read_excel( "../" + dataName, sheet_name='sheetNames[0]' )
    # print( "df = \n" % df )
    # print( "printing datafield" )
    # print( df )

    df.to_hdf( 'data.h5', key='df', mode='w' )

    # fundamental object: a catalog
    #book        = cls_Book.Book( )     # instantiate book
    #book.source = cls_Source.Source( ) # instantiate source

#   farewell with provenance
    print( "\n", datetime.datetime.now( ) )
    print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "python version %s" % sys.version )

# dantopa@Xiuhcoatl.local:kazoo $ python main.py
#
# diagnostic print for data source
# looking in directory '/Volumes/repos/github/jop/python/catalog' for file 'sample.xlsx'
# expecting sheet name 'alpha'
# expecting sheet name 'bravo'
# expecting sheet name 'charlie'
# {'alpha':          INUM      Marking  Unnamed: 2                                             Title  Unnamed: 4  Unnamed: 5  Unnamed: 6  page count euro             notes
# 0       12345  SECRET//FRD         NaN                        Lorem ipsum dolor sit amet         NaN         NaN         NaN          12   NC               NaN
# 1  DAN 87 234   SECRET-FRD         NaN                         quis nostrud exercitation         NaN         NaN         NaN          22   NC     releasable to
# 2      no num      Unclass         NaN  laboris nisi ut aliquip ex ea commodo consequat.         NaN         NaN         NaN          15   NU  could not locate
# 3      no num            U         NaN                           Excepteur sint occaecat         NaN         NaN         NaN          67   NR           no euro, 'bravo':      INUM       Marking  Unnamed: 2                        Title  Unnamed: 4  Unnamed: 5  Unnamed: 6  page count euro           notes
# 0     234        SECRET         NaN  voluptate velit esse cillum         NaN         NaN         NaN        1222   NC             NaN
# 1     435  Confidential         NaN        fugiat nulla pariatur         NaN         NaN         NaN          44   NC   releasable to
# 2  no num  confidential         NaN              Duis aute irure         NaN         NaN         NaN           6   NU  could not find
# 3  no num             U         NaN      Ut enim ad minim veniam         NaN         NaN         NaN          78   NR       not found, 'charlie':    INUM       Marking  Unnamed: 2                                              Title  Unnamed: 4  Unnamed: 5  Unnamed: 6  page count           euro           notes
# 0  2341        SECRET         NaN                 Vehicula ipsum a arcu cursus vitae         NaN         NaN         NaN          22  NC-AtomThings             NaN
# 1    56       unclass         NaN                         Volutpat est velit egestas         NaN         NaN         NaN          65             NC   releasable to
# 2        unclassified         NaN              Mauris ultrices eros in cursus turpis         NaN         NaN         NaN         667             NU  could not find
# 3   NaN             U         NaN  Amet venenatis urna cursus eget nunc scelerisq...         NaN         NaN         NaN         123             NR       not found}
#
#  2022-12-30 10:14:33.398661
# source: /Volumes/repos/github/jop/python/catalog/kazoo/main.py
# python version 3.10.9 (main, Dec 11 2022, 07:43:52) [Clang 14.0.0 (clang-1400.0.29.202)]


# Air-to-Air Missiles
# Kangaroo
# Karen
# Kayak
# Kazoo
# Kedge
# Kegler
# Kelt
# Kennel
# Kent
# Kerry
# Kickback
# Killjoy
# Kilter
# Kingbolt
# Kingfish
# Kipper
# Kitchen
# Koala
# Kodiak
# Krypton
# Kyle
