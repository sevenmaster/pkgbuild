#
# spec file for package SFEstellarium
#
# includes module(s): stellarium
#

%include Solaris.inc
%include packagenamemacros.inc

%define cc_is_gcc 1
%include base.inc

%define srcname stellarium
%define _pkg_docdir %{_docdir}/%{srcname}

Name:		SFEstellarium
IPS_Package_Name:	image/stellarium
#version 0.13.x 0.14.x need Qt5
#Version:	0.12.4
Version:	0.12.6
#Version:	0.13.3
#Version:	0.14.2
Summary:	Photo-realistic night sky renderer
Group:		Scientific/Astronomy
License:	GPLv2+
SUNW_Copyright:	GPLv2.copyright
URL:		http://stellarium.free.fr/
Source:		%{sf_download}/%{srcname}/%{srcname}-%{version}.tar.gz
Patch2:		stellarium-02-gcc-name-conflict.diff

SUNW_BaseDir:	%{_basedir}
%include default-depend.inc

#BuildRequires: SFEsdl-mixer-devel
#Requires: SFEsdl-mixer
##TODO## make a pnm_macro for sdl-mixer / SFEsdl-mixer
BuildRequires: library/audio/sdl-mixer
Requires:      library/audio/sdl-mixer
BuildRequires: %{pnm_buildrequires_SUNWimagick_devel}
Requires:      %{pnm_buildrequires_SUNWimagick}
BuildRequires: SFEcmake
##TODO## update stellarium to 0.13.x 0.14.x once SFEqt5-gpp is available!
BuildRequires: SFEqt-gpp-devel
Requires:      SFEqt-gpp

%description
Stellarium is a real-time 3D photo-realistic nightsky renderer. It can
generate images of the sky as seen through the Earth's atmosphere with
more than one hundred thousand stars from the Hipparcos Catalogue,
constellations, planets, major satellites and nebulas.

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n stellarium-%{version}

%patch2 -p1

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

# pod2man
export CC=gcc
export CXX=g++
export PATH=/usr/g++/bin:$PATH:/usr/perl5/bin
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags -D__C99FEATURES__"
export LDFLAGS="%_ldflags"
export QMAKESPEC=solaris-g++

mkdir -p builds/unix
cd builds/unix

cmake -DCMAKE_BUILD_TYPE=Release -DCMAKE_INSTALL_PREFIX:PATH=%{_prefix} -DCMAKE_C_COMPILER=$CC -DCMAKE_CXX_COMPILER=$CXX -DCMAKE_LIBRARY_PATH=/usr/g++/lib:/usr/gnu/lib ../..
make VERBOSE=1 -j$CPUS
cd ../..
convert -size 32x32 data/icon.bmp stellarium.png


%install
rm -rf %{buildroot}
cd builds/unix
make install DESTDIR=%{buildroot} INSTALL="%{_bindir}/ginstall -c -p"
cd ../..

# Setting CMAKE_LIBRARY_PATH does not do any good
/usr/bin/elfedit -e 'dyn:runpath /usr/g++/lib:/usr/gnu/lib' %buildroot/%_bindir/stellarium

mkdir -p %{buildroot}%{_datadir}/pixmaps/
install -m 0644 -p stellarium.png %{buildroot}%{_datadir}/pixmaps/stellarium.png

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf %{buildroot}%{_datadir}/locale
%endif


%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc AUTHORS ChangeLog CHANGES-FROM-TRUNK.txt README
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{srcname}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/stellarium.1
%defattr (-, root, other)
%{_datadir}/applications/%{srcname}.desktop
%{_datadir}/pixmaps/%{srcname}*
%{_datadir}/icons

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 22 2016 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWimagick_devel}
* Sun Feb 14 2016 - Thomas Wagner
- bump to 0.12.6 (last version working on Qt4)
* Sun Feb  7 2016 - Thomas Wagner
- merge with local workspace
- temporarily use IPS name for sdl-mixer
* Thu Oct 31 2013 - Alex Viskovatoff
- update to 0.12.4; undo unexplained move to archive/
- change oder for runpath in stellarium (g++ first, then gnu, then default)
* Thu Aug 16 2012 - Thomas Wagner
- bump to 0.11.3
- add IPS_package_name
* Wed Apr 11 2012 - Thomas Wagner
- bump to 0.11.2
* Sun Jan 1 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 0.11.1
* Wed Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 0.11.0
* Fri Jul 29 2011 - Alex Viskovatoff
- add SUNW_Copyright
* Sat Jul 02 2011 - Alex Viskovatoff
- fork new spec using gcc to build off SFEstellarium.spec
* Mon Mar 07 2011 - Alex Viskovatoff
- use SFEcmake; boost is not a dependency
* Tue Feb 08 2011 - Milan Jurik
- initial spec
