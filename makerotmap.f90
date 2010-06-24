program makerotmap
  use emissmod, only: extinct
  use wfitsutils, only: fitswrite
  use cuberotate, only: rotate, &
       & interpolation, interpolation_nearest, interpolation_linear
  implicit none
  integer :: i, j, k, nx=0, ny, nz, nxx, nyy, nzz
  real, dimension(:), allocatable :: tau
  real, dimension(:,:), allocatable :: map
  real, dimension(:,:,:), allocatable :: e, d ! original datacubes
  real :: theta, phi
  real, dimension(:,:,:), allocatable :: ee, dd ! rotated datacubes
  character(len=128) :: prefix
  character(len=6) :: emtype
  integer :: itime
  character(len=4) :: ctime
  character(len=13) :: rotid
  real :: extinct_sigma, zsize, dzz

  ! options are nearest/linear
  interpolation = interpolation_linear

  print *, 'File prefix?'
  read '(a)', prefix

  print *, 'Save time?'
  read *, itime
  write(ctime, '(i4.4)') itime
  
  print *, 'Emissivity type?'
  read '(a)', emtype

  ! dust extinction cross-section
  extinct_sigma = extinct(emtype)

  print *, 'Cube extent in z-direction (parsec)?'
  read *, zsize

  print *, 'Rotation theta, phi?'
  read *, theta, phi
  write(rotid, '(a,2(sp,i4.3),a)') '-rot', int(theta), int(phi), '-'

  call read_cube(d, 'dd')
  print '("Original grid size: ",i0,"x",i0,"x",i0)', shape(d)
  d = d/(1.3*1.67262158e-24)    ! convert to cm^-3
  dzz = zsize*3.085677582e18/real(nz) ! physical pixel scale

  ! WJH 04 Mar 2009
  ! Pre-allocate output cube to prevent truncation along zz axis
  nxx = nx
  nyy = ny
  nzz = int(sqrt(real(nx**2 + ny**2 + nz**2))) ! longest diagonal possible
  allocate(dd(nxx,nyy,nzz))
  call rotate(d, theta, phi, dd)
  deallocate(d)
!   nxx = size(dd, 1) !! No longer needed
!   nyy = size(dd, 2)
!   nzz = size(dd, 3)
  print '("Rotated grid size: ",i0,"x",i0,"x",i0)', nxx, nyy, nzz

  call read_cube(e, 'e-'//emtype)
  ! Pre-allocate this one too
  allocate(ee(nxx,nyy,nzz))
  call rotate(e, theta, phi, ee)
  deallocate(e)

  ! integration is along the new zz-axis
  allocate(map(nxx, nyy), tau(nzz) )

  call domap

  call fitswrite(map, trim(prefix)//'map'//rotid//emtype//ctime//'.fits')

contains

  subroutine read_cube(var, id)
    use wfitsutils, only: fitsread, fitscube
    real, intent(inout), dimension(:,:,:), allocatable :: var
    character(len=*), intent(in) :: id
    call fitsread(trim(prefix)//'-'//id//ctime//'.fits')
    if (nx==0) then
       nx = size(fitscube, 1)
       ny = size(fitscube, 2)
       nz = size(fitscube, 3)
    end if
    allocate(var(nx,ny,nz))
    var = fitscube
    deallocate(fitscube)
  end subroutine read_cube

  subroutine domap
    do i = 1, nx
       do j = 1, ny
          tau(1) = 0.0
          do k = 2, nz
             tau(k) = tau(k-1) + dd(i,j,k) 
          end do
          tau = tau*dzz*extinct_sigma
          map(i, j) = sum(ee(i,j,:)*exp(-tau))
       end do
    end do
  end subroutine domap

end program makerotmap
