! 3456789 123456789 223456789 323456789 423456789 523456789 623456789 723456789 823456789 923456789 023456789 123456789 223456789 32
program least_squares

    use, intrinsic :: iso_fortran_env,  only : REAL64

    implicit none

    integer, parameter :: rp = selected_real_kind ( REAL64 ),  m = 9, n = 2

        ! rank one
        real ( kind = rp ), parameter :: one ( 1 : m ) = [ 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp, 1.0_rp ]
        real ( kind = rp ), parameter :: x   ( 1 : m ) = [ 1.0_rp, 2.0_rp, 3.0_rp, 4.0_rp, 5.0_rp, 6.0_rp, 7.0_rp, 8.0_rp, 9.0_rp ]
        real ( kind = rp ), parameter :: T   ( 1 : m ) = [ 15.6_rp, 17.5_rp, 36.6_rp, 43.8_rp, 58.2_rp, 61.6_rp, 64.2_rp, 70.4_rp, &
                                                           98.8_rp ]
        ! scalars
        real ( kind = rp ) :: a = 0.0_rp, b = 0.0_rp, c = 0.0_rp, d = 0.0_rp, e = 0.0_rp, det = 0.0_rp, a0 = 0.0_rp, a1 = 0.0_rp

            ! inner products
            a = dot_product ( one, one )
            b = dot_product ( one, x )
            c = dot_product ( x,   x )
            d = dot_product ( one, T )
            e = dot_product ( x,   T )
            ! determinant of Gram matrix
            det = a * c - b**2

            ! equations 10.26
            a0 = ( d * c - b * e ) / det
            a1 = ( a * e - b * d ) / det

            write ( * , * ) "particular least squares solution"
            write ( * , * ) "intercept a0 = ", a0
            write ( * , * ) "slope     a1 = ", a1

        stop 'Successful termination for "least_squares.f08".'

end program least_squares
