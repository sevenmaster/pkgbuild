#
# spec file for package blasc
#
# includes module(s): blas
#

Name:		blas
Summary:	BLAS - Basic Linear Algebra Subprograms
# In fact there is no version , we give it
Version:	1.1
Source:		http://www.netlib.org/blas/blas.tgz
#Source1:	blas.Makefile
Group:		Math
URL:		http://www.netlib.org/blas/
Patch1:		blas-01-shared.diff

Requires: SUNWcsl
Requires: SUNWlibms

%prep
%setup -q -c -n %{name}
%patch1

%build
cd BLAS
if $( echo "%{_libdir}" | /usr/xpg4/bin/grep -q %{_arch64} ) ; then
  make CC=cc CXX=CC F77=f77 FORTRAN=f77 LOADER=f77 PLAT="" OPTS="-03 -m64"
else
  make F77=gfortran FORTRAN=gfortran LOADER=gfortran PLAT="" OPTS="-O3 -fPIC"
fi

%install
cd BLAS
mv blas.a libblas.a
install -d -m 0755 $RPM_BUILD_ROOT/%{_libdir}
install -m 0755 libblas.a $RPM_BUILD_ROOT%{_libdir}
install -m 0755 libblas.so $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun Apr 29 2012 - Pavel Heimlich
- added shared library
* Tue Jan 17 2012 - James Choi
- specify fPIC 
* Sat Jul 30 2011 - Alex Viskovatoff
- "-03" is not a gcc option
* Tue May 25 2010 - Milan Jurik
- disable multiarch support, not stable with Sun studio Fortran and unsupported with gfortran yet
* Mon May 24 2010 - Milan Jurik
- multiarch support
* Wed Dec 10 2008 - dauphin@enst.fr
- Initial version
