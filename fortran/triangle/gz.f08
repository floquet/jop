! 3456789 123456789 223456789 323456789 423456789 523456789 623456789 723456789 823456789 923456789 023456789 123456789 223456789 32
program ground_zero

    use, intrinsic :: iso_fortran_env,  only : REAL64, compiler_options, compiler_version

    implicit none

    character ( len = * ), parameter :: fmt_datecom = '( /, " - - - - - - - - -", //, I5, 2 ( "-", I2.2 ), I3, 2 ( ":", I2.2 ), / )'

    integer, parameter :: rp = selected_real_kind ( REAL64 ),  m = 3, n = 2

    ! rank one
    real ( kind = rp ), parameter :: x     ( 1 : m ) = [  1.0_rp, 20.0_rp, 50.0_rp ], &
                                     y     ( 1 : m ) = [ 66.0_rp, 15.0_rp, -3.0_rp ], &
                                     theta ( 1 : m ) = [  1.0_rp,  0.74_rp, 0.43_rp ]

    real ( kind = rp ), parameter :: machineEpsilon = epsilon ( 1.0_rp )
    real ( kind = rp ), parameter :: mmX  = 117.97723925949964161745199905235647691501049017468_rp, &
                                     mmY  = 135.24677447077613795832279777569468400355063639720_rp, &
                                     mmSx =  18.698052680295699237828157411268853967898756424020_rp, &
                                     mmSy =  20.860166494699188800182633692615600495039424579191_rp

    ! rank two
    real ( kind = rp ) :: A    ( 1 : m, 1 : n ) = 0.0_rp
    real ( kind = rp ) :: Winv ( 1 : n, 1 : n ) = 0.0_rp

    ! rank one : m vectors
    real ( kind = rp ) :: c        ( 1 : m ) = 0.0_rp, s   ( 1 : m ) = 0.0_rp, b ( 1 : m ) = 0.0_rp, &
                          xi       ( 1 : m ) = 0.0_rp, eta ( 1 : m ) = 0.0_rp, &
                          residual ( 1 : m ) = 0.0_rp
    ! rank one : n vectors
    real ( kind = rp ) :: gz       ( 1 : n ) = 0.0_rp, &
                          sigma    ( 1 : n ) = 0.0_rp, &
                          atb      ( 1 : n ) = 0.0_rp

    ! scalars
    real ( kind = rp ) :: cc = 0.0_rp, cs = 0.0_rp, ss = 0.0_rp, det = 0.0_rp, &
                          cb = 0.0_rp, sb = 0.0_rp, &
                          t2 = 0.0_rp, psd = 0.0_rp

    ! containers for date and time
    integer :: dt_values ( 1 : 8 ) = 0

            ! construct vectors
            c = cos ( theta )
            s = sin ( theta )
            xi  = x * c
            eta = y * s

            ! linear system
            A = reshape ( [ c, -s ], [ m, n ] )
            b = xi - eta

            ! inner products
            cc = dot_product ( c, c )
            cs = dot_product ( c, s )
            ss = dot_product ( s, s )
            cb = dot_product ( c, b )
            sb = dot_product ( s, b )

            ! determinant of Gram matrix
            det = cc * ss - cs ** 2

            ! Fortran is COLUMN major
            ! construct inverse, do not compute inverse
            Winv = reshape ( [ [ ss, cs ], [ cs, cc ] ], [ n, n ] ) / det
            atb = matmul ( transpose ( A ), b )

            ! least squares solution via normal equations
            gz = matmul ( Winv, atb )

            residual = matmul ( A, gz ) - b
            t2 = dot_product ( residual, residual )

            ! parent standard deviation, equation 6.19
            psd = t2 / real ( m - n, kind = rp )
            ! Bevington equations 6-21, 22
            sigma = sqrt( psd * [ ss, cc ] / det )

            ! compare to values in table 6-1, p. 93
            write ( * , * ) "particular least squares solution for ground zero"
            write ( * , * ) "x0 = ", gz( 1 ), " +/- ", sigma( 1 )
            write ( * , * ) "y0 = ", gz( 2 ), " +/- ", sigma( 2 )

            ! compare to values in table 6-1, p. 93
            write ( * , * )
            write ( * , * ) "Errors in machine epsilon = ", machineEpsilon
            write ( * , * ) "x0 = ", ( gz( 1 ) - mmX ) / machineEpsilon, " +/- ", ( sigma( 1 ) - mmSx ) / machineEpsilon
            write ( * , * ) "y0 = ", ( gz( 2 ) - mmY ) / machineEpsilon, " +/- ", ( sigma( 2 ) - mmSy ) / machineEpsilon

        ! execution complete - tag output
        call date_and_time ( VALUES = dt_values )
            write ( * , fmt_datecom ) dt_values ( 1 : 3 ), dt_values ( 5 : 7 )

        write ( * , '( "compiler version: ", g0, "."    )' ) compiler_version ( )
        write ( * , '( "compiler options: ", g0, ".", / )' ) compiler_options ( )

        stop 'Successful termination for "ground_zero.f08".'

end program ground_zero

! dantopa@Xiuhcoatl.local:triangle $ gfortran -Wall -o gz gz.f08

! dantopa@Xiuhcoatl.local:triangle $ ./gz
!  particular least squares solution for ground zero
!  x0 =    117.97723925949958       +/-    18.698052680295692
!  y0 =    135.24677447077607       +/-    20.860166494699182
!
!  - - - - - - - - -
!
!  2023-01-05 17:41:04
!
! compiler version: GCC version 12.2.0.
! compiler options: -fPIC -mmacosx-version-min=13.0.0 -mtune=core2 -Wall.
!
! STOP Successful termination for "ground_zero.f08".
