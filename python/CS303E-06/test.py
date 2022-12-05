# File: Project1.py
# Student: Daniel Topa
# UT EID: dat3244
# Course Name: CS303E
#
# Date: 10/09/2022
# Description of Program:


HW_ERROR_MESSAGE    = "  Grade must be in range [0..10]. Try again."
PR_EX_ERROR_MESSAGE = "  Grade must be in range [0..100]. Try again."

def computeHomeworkAvg():
    print( "HOMEWORKS:" )
    hw1 = int( input( "  Enter Hw1 grade: " ))
    if ( hw1 < 0 or hw1 > 10 ):
        print( HW_ERROR_MESSAGE )
        int( input( "  Enter Hw1 grade: " ))
    hw2 = int( input( "  Enter Hw2 grade: " ))
    if ( hw2 < 0 or hw2 > 10 ):
        print( HW_ERROR_MESSAGE )
        int( input( "  Enter Hw2 grade: " ))
    hw3 = int( input( "  Enter Hw3 grade: " ))
    if ( hw3 < 0 or hw3 > 10 ):
        print( HW_ERROR_MESSAGE )
        int( input( "  Enter Hw3 grade: " ))
    hwAvg = (((hw1 + hw2 + hw3) / 30.00) * 100)
    return (hwAvg)
    computeHomeworkAvg()

print(" ")

def computeProjectAvg():
    print( "PROJECTS:" )
    prj1 = int( input( "  Enter Pr1 grade: " ))
    if ( prj1 < 0 or prj1 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        int( input( "  Enter Pr1 grade: " ))
    prj2 = int( input( "  Enter Pr2 grade: " ))
    if ( prj2 < 0 or prj2 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        int( input( "  Enter Pr1 grade: " ))
    prjAvg = ((prj1 + prj2) / 30.0)
    return (prjAvg)
    computeProjectAvg()

print(" ")

def computeExamAvg():
    print( "EXAMS:" )
    ex1 = int( input( "  Enter Ex1 grade: "))
    if ( ex1 < 0 or ex1 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        int( input( "  Enter Ex1 grade: "))
    ex2 = int( input( "  Enter Ex2 grade: "))
    if ( ex2 < 0 or ex2 > 100 ):
        print( PR_EX_ERROR_MESSAGE )
        int( input( "  Enter Ex2 grade: "))
    exAvg = ((ex1 + ex2) / 40.0)
    return (exAvg)
    computeExamAvg()

print(" ")

def computeStudentGradeReport():
    hwAvg = computeHomeworkAvg()
    prjAvg = computeProjectAvg()
    exAvg = computeExamAvg()
    courseAvg = ( hwAvg + prjAvg + exAvg ) / 3
    courseScore = courseAvg
    if courseScore >= 90: return "A"
    elif courseScore >= 80: return "B"
    elif courseScore >= 70: return "C"
    elif courseScore >= 60: return "D"
    else:
        return "F"
    computeStudentGradeReport

def printGradeReport():
    print( "Grade report for:", name)
    print( "  Homework average (30% of grade):", hwAvg )
    print( "  Project average (30% of grade):", prjAvg )
    print( "  Exam average (40% of grade):", exAvg )
    print( "  Student course average:", courseAvg )
    print( "  Courseg grade (CS303E: Fall, 2022):", courseScore)

def main():
    name = input( "Enter the student's name (or 'stop'): " )
    print(" ")
    if str( name ) == "stop":
        print ( "Thanks for using the grade calculator! Goodbye." )
    exAvg = computeHomeworkAvg()


main()
print(" ")
computeHomeworkAvg()
print(" ")
computeProjectAvg()
print(" ")
computeExamAvg()
print(" ")
computeStudentGradeReport()
print(" ")
printGradeReport()
