#! /usr/bin/python

# # Amanzi: The Multi-Process HPC Simulator
# #   https://github.com/amanzi/amanzi

# # David Moulton   DGL LANL/T-5  moulton@lanl.gov  505 665 4712
# # Daniel Topa     LANL/CCS-2    dantopa@lanl.gov  505 667 0817

# # imports
import datetime             # timestamps
import os                   # opeating system
import sys                  # python version
from pathlib import Path    # rename file
import xlsxwriter           # API for Excel
# home brew
# tools
import tools_debug
import tools_xl             # spreadsheet authoring tools

#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #

if __name__ == "__main__":

    print(os.environ)
    print( "os.environ[ 'HOSTNAME' ] = %s" % os.environ[ 'HOSTNAME' ] )
    # create xl notebook for results
    workbook = tools_xl.xl_new_workbook( "output.xlsx" )
    # worksheets for debugging
    # tools_debug.xl_dramatis_personae( workbook, book )
    #tools_debug.xl_numbered_lines( workbook, book.source.col_lines )


    # write workbook
    workbook.close( )
    print( "\n", datetime.datetime.now( ) )
    print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "python version %s" % sys.version )
