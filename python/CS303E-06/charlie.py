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

def computeExamAvg():
    print( "EXAMS:" )
    ex1 = int( input( "  Enter Ex1 grade: "))
    if ( ex1 < 0 or ex1 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        ex1 = int( input( "  Enter Ex1 grade: "))
    ex2 = int( input( "  Enter Ex2 grade: "))
    if ( ex2 < 0 or ex2 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        ex2 = int( input( "  Enter Ex2 grade: "))
    exAvg = (ex1 + ex2) / 2
    return (exAvg)

def computeStudentGradeReport(hwAvg, prjAvg, exAvg):
    courseScore = ( hwAvg * 30 + prjAvg * 30 + exAvg * 40 ) / 10
    print( "\nDebug: weighted average = ", courseScore )
    return (courseScore)

def computeStudentLetterGrade(courseScore):
    if courseScore >= 90: return "A"
    elif courseScore >= 80: return "B"
    elif courseScore >= 70: return "C"
    elif courseScore >= 60: return "D"
    else:
        return "F"

def printGradeBlock( name, hwAvg, prjAvg, courseAverage, letterGrade ):
        print( "Grade report for ", name)
        print( "   Homework average (30% of grade) : ", hwAvg )
        print( "   Project average (30% of grade) : ", prjAvg )
        print( "   Exam average (40% of grade) : ", exAvg )
        print( "   Student course average: : ", courseAverage )
        print( "   Course grade (CS303E: Fall, 2022) : ", letterGrade )
        return()

def main():
    GOODBYE_MESSAGE = "Thanks for using the grade calculator! Goodbye."
    name = input( "Enter the student's name (or 'stop'): " )
    print(" ")
    if str( name ) == "stop":
        print ( GOODBYE_MESSAGE )
        quit()

    # homework average: routine takes keyboard input for hw1, h2, hw3 and returns the average
    hwAvg = computeHomeworkAvg()
    # diagnostic message to verify correct return
    print( "\nDebug: homework average = ", hwAvg )

    # project average: routine takes keyboard input for prj1, prj2 and returns the average
    prjAvg = computeProjectAvg()
    # diagnostic message to verify correct return
    print( "\nDebug: project average = ", prjAvg )

    # exam average: routine takes keyboard input for ex1, ex2 and returns the average
    exAvg = computeExamAvg()
    # diagnostic message to verify correct return
    print( "\nDebug: exam average = ", exAvg )

    # compute weighted average of coursework
    courseAverage = computeStudentGradeReport(hwAvg, prjAvg, exAvg)
    print( "Your weighted average = ", courseAverage )
    letterGrade = computeStudentLetterGrade(courseAverage)
    print( "Your overall grade = ", letterGrade )

    # all tasks completed
    print ( GOODBYE_MESSAGE )
    quit()


if __name__ == "__main__":
    main()


Homework average (30% of grade) : 20.00
Project average (30% of grade): 15.00
Exam average (40% of grade): 16.50
Student course average: 17.10
Course grade (CS303E: Fall, 2022): F
