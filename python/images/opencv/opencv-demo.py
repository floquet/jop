#! /opt/local/bin/python

import datetime             # timestamps
import os                   # opeating system
import platform				# uname
import pwd
import sys                  # python version

from pathlib import Path

import cv2 as cv

# define modules
def image_box_bounding( image ):
    clr       = ( 0, 0, 255 )
    start_red = ( 0, 0 ) 
    end_red   = ( image.shape[ 1 ], image.shape[ 0 ] ) 
    thickness = 5 
    out = cv.rectangle( image, start_red, end_red, clr, thickness )
    return out


# define modules
def image_box_semi( image ):
    clr    = ( 255, 0, 0 )
    height = image.shape[ 0 ]
    width  = image.shape[ 1 ]
    start_blue = ( round( width / 4    ), round( height / 4     ) ) 
    end_blue   = ( round( width / 4 * 3), round( height / 4 * 3 ) ) 
    thickness  = 8 
    out = cv.rectangle( image, start_blue, end_blue, clr, thickness )
    return out


# define modules
def image_bisect( image ):
    clr    = ( 0, 255, 0 )
    height = image.shape[ 0 ]
    width  = image.shape[ 1 ]
    start_vert = ( round( width / 2 ), 0 ) 
    end_vert   = ( round( width / 2 ), height ) 
    start_horz = (     0,              round( height / 2 ) )
    end_horz   = ( width,              round( height / 2 ) ) 
    thickness  = 4 
    cv.line( image, start_vert, end_vert, clr, thickness )
    cv.line( image, start_horz, end_horz, clr, thickness )
    return image


def image_show( image, delay, fileIn, fileOut ):
    cv.imshow( winname = fileIn, mat = image )
    k = cv.waitKey( delay ) # miliseconds

    if k == 27:
        sys.exit( "escape key causes exit" )
    elif k == ord( "s" ):
    	print( "writing to file ", fileOut )
    	cv.imwrite( fileOut, image )
    return


def image_tag( image, fileIn, fileSizeBits ):
    # label image with fundamental data
    loc = [ 20, 40 ] # start point for text
    inc = [  0, 40 ] # next line of text

    font = cv.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    thickness = 2
    clr = ( 128, 128, 128 )

    cv.putText( image, fileIn, loc, font, fontScale, clr, thickness )

    new = tuple( map( lambda x, y: x + y, loc, inc ) )
    cv.putText( image, str( image.shape ), new, font, fontScale, clr, thickness )

    new = tuple( map( lambda x, y: x + y, new, inc ) )
    cv.putText( image, str( image.dtype ), new, font, fontScale, clr, thickness )

    new = tuple( map( lambda x, y: x + y, new, inc ) )
    cv.putText( image, str( fileSizeBits ), new, font, fontScale, clr, thickness )	

    return image


def write_file_descriptor( fileIn, dir_images ):
    stem = Path( fileIn ).stem
    nameOut = stem + '.txt'
    fullNameIn = os.path.join( dir_images, fileIn )
    print( f"{os.path.getsize( fullNameIn )/(1<<20):,.0f} MB" )
    with open( nameOut, 'w' ) as f:
        f.writelines( 'file name = {fileIn}\n' )
        f.writelines( 'file path = {dir_images}\n' )
        f.writelines( 'file size, bits = {fsize}\n' )
        f.writelines( 'file size, MBytes = {fsize}\n' )
    f.close( )
    return


def check_file_size( fileIn, dir_images ):
    fullNameIn = os.path.join( dir_images, fileIn )
    fsize      = os.path.getsize( fullNameIn )
    if fsize <= 0:
    	print( 'file size in bits = {fsize}' )
    	print( 'file size must be > 0' )
    	print( 'file name: {fileIn}' )
    	print( 'path     : {dir_images}' )
    	sys.exit( "exit caused by empty or corrupt image file" )
    return fsize


def write_provenance():
    print( "\n", datetime.datetime.now( ) )
    print( "source:  %s/%s" % ( os.getcwd( ), os.path.basename( __file__ ) ) )
    print( "user id:", pwd.getpwuid( os.getuid( ) ).pw_name )
    print( "platform info:")
    print( "    platform: ", platform.platform() )
    print( "    uname:    ", platform.uname() )
    #print( "    node:     ", platform.node( ) )
    #print( os.environ )
    print( "version info:")
    print( "    python:   %s" % sys.version )
    print( "    opencv:  ", cv.__version__ )
    print( "    platform:", platform.__version__ )


#  ==   ==   == ==   ==   == ==   ==   == ==   ==   ==  #


if __name__ == "__main__":

    dir_images = f'/Volumes/T7-Touch/repos/github/jop/python/images/opencv/'
    fileIn     = f'moon.png'
    fileIn     = f'fireball2.jpeg'

    print( "dir_images = ", dir_images )

    fullNameIn = os.path.join( dir_images, fileIn )
    img = cv.imread( fullNameIn )

    #if img is None:
    #	sys.exit( "could not read image ", dir_images)
    # check: is file extant?
    assert img is not None, sys.exit( "could not read image '", fileIn, "'\nfrom directory ", dir_images )

    # check: verify file not empty
    file_size_bits = check_file_size( fileIn = fileIn, dir_images = dir_images )
    height, width, layers = img.shape
    print( "img.shape = ", img.shape )
    print( "file_size_bits = ", file_size_bits )
   
    # draw rectangles
    img = image_box_bounding ( image = img )
    img = image_box_semi     ( image = img )
    img = image_bisect       ( image = img )
    img = image_tag          ( image = img, fileIn = fileIn, fileSizeBits = file_size_bits )

    # preview image: "s" to save, "esc" to exit
    stem = Path( fileIn ).stem
    fileOut = "out-" + stem + ".png"
    fullNameOut = os.path.join( dir_images, fileOut )
    image_show( image = img, delay = 2000, fileIn = fileIn, fileOut = fullNameOut )

    # write query file
    write_file_descriptor( fileIn, dir_images )

    # shut down with provenance
    write_provenance( )

# https://www.geeksforgeeks.org/python-opencv-cv2-rectangle-method/
# https://www.geeksforgeeks.org/python-opencv-cv2-puttext-method/
# https://stackoverflow.com/questions/497885/python-element-wise-tuple-operations-like-sum
# https://docs.opencv.org/3.4/d7/d4d/tutorial_py_thresholding.html
# https://stackoverflow.com/questions/14639077/how-to-use-sys-exit-in-python
# https://stackoverflow.com/questions/7132861/how-can-i-create-a-full-path-to-a-file-from-parts-e-g-path-to-the-folder-name
# https://stackoverflow.com/questions/5194057/better-way-to-convert-file-sizes-in-python
# https://www.pythontutorial.net/python-basics/python-write-text-file/
# https://stackoverflow.com/questions/541390/extracting-extension-from-filename-in-python
# https://stackoverflow.com/questions/842059/is-there-a-portable-way-to-get-the-current-username-in-python
# https://stackoverflow.com/questions/4271740/how-can-i-use-python-to-get-the-system-hostname
