#
# spec file for package SFEtwolame
#
# includes module(s): twolame

# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=136040&atid=735435&aid=
#
%include Solaris.inc
%include packagenamemacros.inc


Name:		SFEtwolame
IPS_Package_Name:	audio/twolame
Summary:	twolame - MP3 Encoder
Version:	0.3.13
URL:		http://www.twolame.org/
Source:		http://downloads.sourceforge.net/twolame/twolame-%{version}.tar.gz
License:	LGPLv2.1+
SUNW_Copyright:	twolame.copyright
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	%{pnm_buildrequires_SFElibsndfile_devel}
Requires:	%{pnm_requires_SFElibsndfile}
BuildRequires:	%{pnm_buildrequires_SUNWgnome_common_devel}

Requires:	%{pnm_buildrequires_SUNWlibms}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n twolame-%version

#configure doesn't keep the order for -lsndfile
gsed -i.bak -e 's?-lsndfile?-R/usr/gnu/lib -L/usr/gnu/lib -lsndfile?' configure


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

%if %{cc_is_gcc}
export CFLAGS="%optflags -I%{gnu_inc}"
%else
export CFLAGS="%optflags -I%{gnu_inc} -xcrossfile=1"
%endif

export LDFLAGS="%{gnu_lib_path} %_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sun Nov 29 2015 - Thomas Wagner
- if cc_is_gcc, then remove CFLAG -xcrossfile=1
- Mon May 25 2015 - Thomas Wagner
- change (Build)Requires to pnm_buildrequires_SUNWgnome_common_devel
* Sun Dec  1 2013 - Thomas Wagner
- work around wrong order for -lsndfile in configure 
* Fri Jul  5 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SFElibsndfile_devel}, %include packagenamemacros.inc
* Mon Oct 10 2011 - Milan Jurik
- bump to 0.3.13, add IPS package name
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Sun Jul 05 2009 - Milan Jurik
- patch2 and patch3 to remove potential building problems
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
- removed BuildRequires: SFElibsndfiles-devel from package -devel
* Tue Sep 02 2008 - nonsea@users.sourceforge.net
- Add libtoolize/aclocal/autoheader/automake/autoconf before ./configure
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.12
- Remove patch crossfile_inline.diff and reorder
* Tue Feb 12 2008 - pradhap@gmail.com
- Fixed links
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.3.10.  Bump patch1 and patch2.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEtwolame
- delete -share subpkg
- update file attributes
- add missing dep
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Initial version
