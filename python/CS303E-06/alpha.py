# File: Project1.py
# Student: Daniel Topa
# UT EID: dat3244
# Course Name: CS303E
#
# Date: 10/09/2022
# Description of Program: compute weighted average of homework, projects and tests

def computeHomeworkAvg():
    HW_ERROR_MESSAGE    = "  Grade must be in range [0..10]. Try again."
    print( "HOMEWORKS:" )
    hw1 = int( input( "  Enter Hw1 grade: " ))
    if ( hw1 < 0 or hw1 > 10 ):
        print( HW_ERROR_MESSAGE )
        hw1 = int( input( "  Enter Hw1 grade: " ))
    hw2 = int( input( "  Enter Hw1 grade: " ))
    if ( hw2 < 0 or hw2 > 10 ):
        print( HW_ERROR_MESSAGE )
        hw2 = int( input( "  Enter Hw2 grade: " ))
    hw3 = int( input( "  Enter Hw1 grade: " ))
    if ( hw3 < 0 or hw3 > 10 ):
        print( HW_ERROR_MESSAGE )
        hw3 = int( input( "  Enter Hw3 grade: " ))
    hwAvg = (hw1 + hw2 + hw3) / 3
    return (hwAvg)

def computeProjectAvg():
    PR_EX_ERROR_MESSAGE = "  Grade must be in range [0..100]. Try again."
    print( "PROJECTS:" )

    prj1 = int( input( "  Enter Pr1 grade: " ))
    if ( prj1 < 0 or prj1 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        prj1 = int( input( "  Enter Pr1 grade: " ))

    prj2 = int( input( "  Enter Pr2 grade: " ))
    if ( prj2 < 0 or prj2 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        prj2 = int( input( "  Enter Pr1 grade: " ))

    prjAvg = (prj1 + prj2) / 2
    return (prjAvg)

def main():
    GOODBYE_MESSAGE = "Thanks for using the grade calculator! Goodbye."
    name = input( "Enter the student's name (or 'stop'): " )
    print(" ")
    if str( name ) == "stop":
        print ( GOODBYE_MESSAGE )
        quit()

    # homework average: routine takes keyboard input for hw1, h2, hw3 and returns the average
    exAvg = computeHomeworkAvg()
    # diagnostic message to verify correct return
    print( "\nDebug: homework average = ", exAvg )

    # project average: routine takes keyboard input for prj1, prj2 and returns the average
    prjAvg = computeProjectAvg()
    # diagnostic message to verify correct return
    print( "\nDebug: project average = ", prjAvg )

    # all tasks completed
    print ( GOODBYE_MESSAGE )
    quit()


if __name__ == "__main__":
    main()
