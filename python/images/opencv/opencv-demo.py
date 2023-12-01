#! /opt/local/bin/python

import datetime             # timestamps
import os                   # opeating system
import sys                  # python version

import cv2 as cv
print( "loaded opencv ", cv.__version__ )

#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #

if __name__ == "__main__":

    dir_images = r'/Volumes/T7-Touch/repos/github/jop/python/images/opencv/'
    print( "dir_images = ", dir_images )

    fileIn = f'moon.png'
    img = cv.imread( fileIn )

    if img is None:
    	sys.exit( "could not read image ", dir_images)

    height, width, layers = img.shape

    #red box
    clr       = ( 0, 0, 255 )
    start_red = ( 0, 0 ) 
    end_red   = ( width, height ) 
    thickness = 8 
    cv.rectangle( img, start_red, end_red, clr, thickness )

    #blue box
    clr        = ( 255,   0,   0 )
    start_blue = ( round( width / 4    ), round( height / 4     ) ) 
    end_blue   = ( round( width / 4 * 3), round( height / 4 * 3 ) ) 
    thickness  = 5 
    cv.rectangle( img, start_blue, end_blue, clr, thickness )

    # image properties
    clr        = ( 200, 200, 200 )
    org = ( 10, 10 )
    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    cv.putText( img, str( "shape = {img.shape}" ), org, font, fontScale, clr )

    cv.imshow( fileIn, img )
    k = cv.waitKey( 2000 ) # miliseconds

    if k == ord( "s" ):
    	fileOut = "output.png"
    	print( "writing to file ", fileOut )
    	cv.imwrite( fileOut, img )

    print( "\n", datetime.datetime.now( ) )
    print( "source: %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "python version %s" % sys.version )

# https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
# https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
