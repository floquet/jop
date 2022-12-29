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

    dict_df = pd.read_excel( "../" + dataName, sheet_name=sheetNames, header = 2 )

    # https://pbpython.com/pandas-excel-tabs.html
    #first_df = pd.read_excel( "../" + dataName, sheet_name='sheetNames[0]' )
    print( dict_df )

    # fundamental object: a catalog
    #book        = cls_Book.Book( )     # instantiate book
    #book.source = cls_Source.Source( ) # instantiate source

#   farewell with provenance
    print( "\n", datetime.datetime.now( ) )
    print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "python version %s" % sys.version )

#  2022-12-21 16:31:57.430372
# source: /Volumes/repos/github/jop/python/catalog/kazoo/main.py
# python version 3.10.8 (main, Nov 12 2022, 21:52:25) [Clang 14.0.0 (clang-1400.0.29.202)]


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
