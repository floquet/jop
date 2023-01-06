! 3456789 123456789 223456789 323456789 423456789 523456789 623456789 723456789 823456789 923456789 023456789 123456789 223456789 32
program ground_zero

    use, intrinsic :: iso_fortran_env,  only : REAL64, compiler_options, compiler_version

    implicit none

    character ( len = * ), parameter :: fmt_datecom = '( /, " - - - - - - - - -", //, I5, 2 ( "-", I2.2 ), I3, 2 ( ":", I2.2 ), / )'

    integer, parameter :: rp = selected_real_kind ( REAL64 ),  m = 3, n = 2

    ! rank one
    real ( kind = rp ), parameter :: x     ( 1 : m ) = [  1.0_rp, 20.0_rp, 50.0_rp ]
    real ( kind = rp ), parameter :: y     ( 1 : m ) = [ 66.0_rp, 15.0_rp, -3.0_rp ]
    real ( kind = rp ), parameter :: theta ( 1 : m ) = [  1.0_rp,  0.74_rp, 0.43_rp ]

    ! rank two
    real ( kind = rp ) :: A    ( 1 : m, 1 : n ) = 0.0_rp
    real ( kind = rp ) :: Winv ( 1 : n, 1 : n ) = 0.0_rp

    ! rank one : m vectors
    real ( kind = rp ) :: c        ( 1 : m ) = 0.0_rp, s   ( 1 : m ) = 0.0_rp, b ( 1 : m ) = 0.0_rp
    real ( kind = rp ) :: xi       ( 1 : m ) = 0.0_rp, eta ( 1 : m ) = 0.0_rp
    real ( kind = rp ) :: residual ( 1 : m ) = 0.0_rp
    ! rank one : n vectors
    real ( kind = rp ) :: gz       ( 1 : n ) = 0.0_rp
    real ( kind = rp ) :: sigma    ( 1 : n ) = 0.0_rp
    real ( kind = rp ) :: atb      ( 1 : n ) = 0.0_rp

    ! scalars
    real ( kind = rp ) :: cc = 0.0_rp, cs = 0.0_rp, ss = 0.0_rp, det = 0.0_rp
    real ( kind = rp ) :: cb = 0.0_rp, sb = 0.0_rp
    real ( kind = rp ) :: t2 = 0.0_rp, psd = 0.0_rp

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

            write ( * , * ) "cc = ", cc
            write ( * , * ) "cs = ", cs
            write ( * , * ) "ss = ", ss
            write ( * , * ) "cb = ", cb
            write ( * , * ) "sb = ", sb
            write ( * , * ) "det = ", det
            write ( * , * ) "A = ", A
            write ( * , * ) "xi = ", xi
            write ( * , * ) "eta = ", eta
            write ( * , * ) "b = ", b

            ! Fortran is COLUMN major
            Winv = reshape ( [ [ ss, cs ], [ cs, cc ] ], [ n, n ] ) / det
            !Winv = [ [ ss, cs ], [ cs, cc ] ] / det
            atb = matmul ( transpose ( A ), b )
            write ( * , * ) "A^* = ", transpose( A )
            write ( * , * ) "Winv = ", Winv
            write ( * , * ) "atb = ", atb

            ! least squares solution via normal equations
            gz = matmul ( Winv, atb )

            residual = matmul ( A, gz ) - b
            t2 = dot_product ( residual, residual )

            ! parent standard deviation, equation 6.19
            psd = t2 / real ( m - n, kind = rp )
            ! equations 6-21, 22
            sigma = sqrt( psd * [ ss, cc ] / det )

            ! compare to values in table 6-1, p. 93
            write ( * , * ) "particular least squares solution for ground zero"
            write ( * , * ) "x0 = ", gz( 1 ), " +/- ", sigma( 1 )
            write ( * , * ) "y0 = ", gz( 2 ), " +/- ", sigma( 2 )

        ! execution complete - tag output
        call date_and_time ( VALUES = dt_values )
            write ( * , fmt_datecom ) dt_values ( 1 : 3 ), dt_values ( 5 : 7 )

        write ( * , '( "compiler version: ", g0, "."    )' ) compiler_version ( )
        write ( * , '( "compiler options: ", g0, ".", / )' ) compiler_options ( )

        stop 'Successful termination for "ground_zero.f08".'

end program ground_zero

! dantopa@Xiuhcoatl.local:triangle $ gfortran -Wall gz.f08
! dantopa@Xiuhcoatl.local:triangle $ ./a.out
!  particular least squares solution for ground zero
!  x0 =    53.131513333455359       +/-    70.217462895360043
! y0 =    60.908916382549272       +/-    78.336925875502942

! - - - - - - - - -

! 2023-01-05 17:19:48

! compiler version: GCC version 12.2.0.
! compiler options: -fPIC -mmacosx-version-min=13.0.0 -mtune=core2 -Wall.

! STOP Successful termination for "ground_zero.f08".
