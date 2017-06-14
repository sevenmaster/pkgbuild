#
# spec file for package SFEharfbuzz-gpp
#

##info for osdistro:
##currently not used on oihipster, we use odistro (harfbuzz 0.9.39 in userland)
##all other osdistro: use SFEharfbuzz.spec

%include Solaris.inc
%define cc_is_gcc 1
%include usr-g++.inc
%include base.inc
%include packagenamemacros.inc
#until we recorded the dependencies manually
%define _use_internal_dependency_generator 1

%define	src_name	harfbuzz

#imported from OI userland, thanks much!

Name:			SFEharfbuzz-gpp
IPS_Package_Name:	library/g++/harfbuzz
Summary:		harfbuzz - text shaping engine (/usr/g++)
Group:			System/Libraries
#available: 0.9.42 and 1.0.1
#Version:		1.0.6
Version:		1.4.6
URL:			http://www.freedesktop.org/wiki/Software/HarfBuzz
License:		MIT
SUNW_Copyright:		%{src_name}.copyright
Source:			http://www.freedesktop.org/software/harfbuzz/release/harfbuzz-%{version}.tar.bz2
#fixed upstream
#Patch1:			harfbuzz-01-cast-double-scalbn.diff
#Patch2:			harfbuzz-02-cast-double-lround.diff

SUNW_BaseDir:		%_basedir

%include default-depend.inc

BuildRequires:	SFEgraphite2-gpp-devel
Requires:	SFEgraphite2-gpp

BuildRequires:  %{pnm_buildrequires_SUNWfreetype2}
Requires:       %{pnm_buildrequires_SUNWfreetype2}

BuildRequires:  SFEicu-gpp-devel
Requires:       SFEicu-gpp


%description
HarfBuzz is an OpenType text shaping engine.


%package devel
Summary:        %summary - development files
SUNW_BaseDir:   %_basedir
%include default-depend.inc
Requires: %name


%prep
%setup -q -n %{src_name}-%{version}

#%patch1 -p1
#%patch2 -p1

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export PKG_CONFIG_PATH=/usr/g++/lib/pkgconfig:/usr/lib/pkgconfig

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I/usr/g++/include"
export CXXFLAGS="%cxx_optflags -I/usr/g++/include"
export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"
# The following line was suggested by graphite2-02-examples-libstdc++.patch,
# the purpose of which is to remove the same error that is produced by the
# harfbuzz build if glib is not disabled
export GRAPHITE2_LIBS="-lgraphite2 -lstdc++"

#same options as in OI userland

./configure     \
        --prefix=%{_prefix}     \
        --enable-shared         \
        --disable-static        \
        --with-graphite2=yes    \
        --with-freetype=yes     \
		--with-glib=no			\
        ;

gmake V=2 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %_bindir

%dir %attr (0755, root, bin) %_libdir
%_libdir/*.so*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/%{src_name}*.pc
%dir %attr (0755, root, bin) %_includedir
%dir %_includedir/%src_name
%_includedir/%src_name/*

%changelog
* Wed Jun 14 2017 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.4.6
* Tue Nov 22 2016 - Ian Johnson <ianj@tsundoku.ne.jp>
- bump to 1.3.3
* Sat Apr 23 2016 - Thomas Wagner
- bump to 1.0.6
- add patch1 harfbuzz-01-cast-double-scalbn.diff, patch2 harfbuzz-02-cast-double-lround.diff  (cast argument to scalbn and lround)
* Tue Dec 29 2015 - Alex Viskovatoff <herzen@imap.cc>
- enable glib; change SVr4 name to maintain consistency with IPS name
* Sun Oct 25 2015 - Thomas Wagner
- %include usr-g++.inc
* Wed 19 Aug 2015 - Thomas Wagner
- init ENV in %install (else might catch wrong compiler)
* Mon Aug 10 2015 - Thomas Wagner
- initial spec 0.9.38, more fresh versions untested. Note: LibreOffice4 uses harfbuzz
##TODO## make a 32/64 bit package
