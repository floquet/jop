#! /opt/local/bin/python

import datetime             # timestamps
import os                   # opeating system
import sys                  # python version

import cv2 as cv
print( "loaded opencv ", cv.__version__ )

#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #

if __name__ == "__main__":

    dir_images = f'/Volumes/T7-Touch/repos/github/jop/python/images/opencv/'
    print( "dir_images = ", dir_images )

    fileIn = f'moon.png'
    img = cv.imread( fileIn )

    if img is None:
    	sys.exit( "could not read image ", dir_images)

    cv.imshow( fileIn, img )
    k = cv.waitKey( 1000 ) # miliseconds

    if k == ord( "s" ):
    	fileOut = "output.png"
    	print( "writing to file ", fileOut )
    	cv.imwrite( fileOut, img )

    print( "\n", datetime.datetime.now( ) )
    print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "python version %s" % sys.version )
