program cubedenstats
  ! calculates mean densities for the data cubes
  use wfitsutils, only: fitsread, fitscube
  implicit none
  real, parameter :: boltzmann_k = 1.3806503e-16, mp = 1.67262158e-24, mu = 1.3
  real, dimension(:,:,:), allocatable :: d, x, r
  logical, dimension(:,:,:), allocatable :: ion_mask, m
  character(len=128) :: prefix, fitsfilename
  integer :: it1, it2, it, itstep
  integer :: nx, ny, nz, i, j, k
  real :: dmean_tot, dmean_nn, dmean_ii
  real :: dmean_n, dmean_i, d2mean_tot, d2mean_n, d2mean_i, d3mean_i
  real :: rmax
  character(len=1), parameter :: TAB = achar(9)
  character(len=15) :: itstring
  real, parameter :: pi = 3.14159265358979, cubesize = 4.0*3.086e18

  print *, 'Run prefix (e.g., 30112005_c)?'
  read '(a)', prefix

  print *, 'First and last time index, and step?'
  read *, it1, it2, itstep

  write(itstring,'(3("-",i4.4))') it1, it2, itstep

  open(1, file=trim(prefix)//itstring//'.dstats', action='write')
  write(1, '("# ",10(a,"'//TAB//'"))') 'Time', &
       & 'Dmean_tot', 'Dmean_nn', 'Dmean_ii', &
       & 'Dmean_n', 'Dmean_i', 'D2mean_tot', 'D2mean_n', 'D2mean_i', 'D3mean_i'

  do it = it1, it2, itstep

     write(fitsfilename, '(2a,i4.4,a)') trim(prefix), '-dd', it, '.fits'
     call fitsread(trim(fitsfilename))
     if (it == it1) then
        ! first time setup
        nx = size(fitscube, 1)
        ny = size(fitscube, 2)
        nz = size(fitscube, 3)
        allocate( d(nx, ny, nz), x(nx, ny, nz), ion_mask(nx, ny, nz) )
        allocate( r(nx, ny, nz), m(nx, ny, nz) )
     end if
     d = fitscube/mp/mu

     write(fitsfilename, '(2a,i4.4,a)') trim(prefix), '-xi', it, '.fits'
     call fitsread(trim(fitsfilename))
     x = fitscube

     forall(i=1:nx, j=1:ny, k=1:nz)
        ! radial distance from center in grid units
        r(i, j, k) = &
             & sqrt( &
             &        (real(i) - 0.5*real(nx+1))**2 &
             &      + (real(j) - 0.5*real(ny+1))**2 &
             &      + (real(k) - 0.5*real(nz+1))**2 &
             &     )
     end forall

     ! For early times, we have some partially ionized material
     ! around the edges of the grid, which is skewing our statistics.
     ! We cut it out by only considering a sphere of radius 1 pc. 
     rmax = (1.0 + real(it)/50.0)*0.25*real(nx)
     m = r < rmax

     ion_mask = x>0.5

     dmean_tot = sum(d)/real(nx*ny*nz)
     d2mean_tot = sum(d*d)/real(nx*ny*nz)

     ! version 1: consider i-front as discontinuity at x=0.5
     dmean_nn = sum(d, mask=.not.ion_mask)/count(.not.ion_mask)
     if (count(ion_mask) > 0) then 
        dmean_ii = sum(d, mask=ion_mask)/count(ion_mask)
     else
        dmean_ii = 0.0
     end if

     ! version 2: weight by the ion fraction
     dmean_n = sum(d*(1.-x))/sum(1.-x)
     dmean_i = sum(d*x, mask=m)/sum(x, mask=m)

     ! mean of density-squared
     d2mean_n = sum(d*d*(1.-x))/sum(1.-x)
     d2mean_i = sum(d*d*x, mask=m)/sum(x, mask=m)

     ! mean of density-cubed
     d3mean_i = sum(d*d*d*x, mask=m)/sum(x, mask=m)

     if (mod(it,10)==0) print *, 'Done timestep: ', it

     write(1, '(i4.4,"'//TAB//'",9(es11.3,"'//TAB//'")))') it, &
          & dmean_tot, dmean_nn, dmean_ii, &
          & dmean_n, dmean_i, d2mean_tot, d2mean_n, d2mean_i, d3mean_i

  end do

end program cubedenstats
