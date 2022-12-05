def computeHomeworkAvg(hw1, hw2, hw3):
    HW_ERROR_MESSAGE = "Grade must be in range [0..10]. Try again."
    print()
    print( "HOMEWORKS:" )
    while True:
        hw1 = int( input( "  Enter HW1 grade =  ", hw1 ) )
        if ( hw1 < 0 or hw1 > 10 ):
            print( "Error on HW1 grade" )
            print( HW_ERROR_MESSAGE )
            return;
        else:
            while True:
                hw2 = int( input( "  Enter HW2 grade = ", hw2 ) )
                if ( hw2 < 0 or hw2 > 10 ):
                    print( "Error on HW2 grade" )
                    print( HW_ERROR_MESSAGE )
                    return;
#                else:
#                    while True:
#                        hw3 = int( input( "  Enter HW3 grade: " ) )
#                        if ( hw3 < 0 or hw3 > 10 ):
#                            print( "Error on HW3 grade = ", hw3 )
#                            print( HW_ERROR_MESSAGE )
#                            return;
    print( "all three grades were valid" )
    return;

computeHomeworkAvg(hw1=1, hw2=2, hw3=3)
