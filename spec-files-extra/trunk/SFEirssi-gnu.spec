#
# spec file for package SFEirssi
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%include usr-gnu.inc

#perl -V:cc -> gcc? then set cc_is_gcc 1
%define cc_is_gcc %( %{_basedir}/perl%{perl_major_version}/%{perl_version}/bin/perl -V:cc | egrep "cc='gcc';|cc='.*/gcc';" >/dev/null && echo 1 || echo 0 )
%include base.inc
%if %( expr %{omnios} '|' %{s110400} )
#perl is 64-bit
%include arch64.inc
%endif

Name:                SFEirssi-gnu
IPS_Package_Name:    network/chat/gnu/irssi
Summary:             irssi - a terminal based IRC client (/usr/gnu)
Version:             1.1.1
#Source:              http://www.irssi.org/files/irssi-%{version}.tar.gz
Source:              http://github.com/irssi/irssi/releases/download/%{version}/irssi-%{version}.tar.gz

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

BuildRequires: %{pnm_buildrequires_perl_default}
Requires:      %{pnm_requires_perl_default}

BuildRequires: SFEperl-encode-locale
Requires:      SFEperl-encode-locale
BuildRequires: SFEperl-try-tiny
Requires:      SFEperl-try-tiny
BuildRequires: SFEperl-lwp
Requires:      SFEperl-lwp

%description
irssi is a terminal based IRC client and installs into /usr/gnu/bin/irssi path.
Please remmeber this if you have the OSDISTRO provided /usr/bin/irssi installed as well.

You can extend the client by perl scripts. To show perl support run this:
/load perl   
/load   
/help script    
Examples for scripts: Auto-Identify your nich at your irc network with with "nickserv.pl".
Several hundreds of scripts to be found here: https://scripts.irssi.org . 
Place your scripts from the above link into $HOME/.irssi/scripts/ directory, then run /load perl, then run /script load name_of_script.pl .


%prep
%setup -q -n irssi-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
%endif

export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"


./configure --prefix=%{_prefix}                 \
             --bindir=%{_bindir}                 \
             --sysconfdir=%{_sysconfdir}         \
             --includedir=%{_includedir}         \
             --mandir=%{_mandir}                 \
             --libdir=%{_libdir}                 \
             --with-perl=module                  \
             --with-perl-lib=%{_basedir}/%{perl_path_vendor_perl_version} \
             --with-gnu-ld=no \


%if %( echo %{_libdir} | grep "%{_arch64}" >/dev/null && echo 1 || echo 0 )
#well, calculation of GLIB_CFLAGS fails badly as it doesn't take into account the %{_arch64} directory offset.
#this ends in wrong type of variable, ending in core dumps as it tries to allocate 2^32 = 4294967296 bytes of memory in g_logv:
#wrong:   -I/usr/lib/glib-2.0/include (glibconfig.h)
#correct: -I/usr/lib/%{_arch64}/glib-2.0/include (glibconfig.h)
sed -i.bak.glib.arch64 -e 's?I/usr/lib/glib-2.0/include?I/usr/lib/%{_arch64}/glib-2.0/include?' `find . -name Makefile`
%endif

make V=2 -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f ${RPM_BUILD_ROOT}%{_libdir}/irssi/modules/*.la \
         ${RPM_BUILD_ROOT}%{_libdir}/irssi/modules/*.a \
         ${RPM_BUILD_ROOT}%{_basedir}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/Irssi/.packlist \
         ${RPM_BUILD_ROOT}%{_basedir}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/auto/Irssi/*/.packlist \
         ${RPM_BUILD_ROOT}%{_basedir}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/perllocal.pod \
         ${RPM_BUILD_ROOT}/etc/irssi.conf
rm -rf ${RPM_BUILD_ROOT}%{_docdir} \
        ${RPM_BUILD_ROOT}%{_includedir}
rmdir $RPM_BUILD_ROOT/etc

%if %{omnios}
ln -s %{_arch64}/irssi ${RPM_BUILD_ROOT}%{_prefix}/bin
%endif

%clean
rm -rf $RPM_BUILD_ROOT

# The following shorthand works fine...

%files
%defattr (-, root, bin)
%{_prefix}/bin/*
%{_libdir}/irssi/
%{_basedir}/perl5/vendor_perl/%{perl_version}/%{perl_dir}/*
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/irssi/

# Here's the "longhand" version:
# %files
# %defattr (-, root, bin)
# %dir %attr (0755, root, bin) %{_bindir}
# %{_bindir}/*
# %dir %attr (0755, root, bin) %{_libdir}/irssi
# %dir %attr (0755, root, bin) %{_libdir}/irssi/modules
# %{_libdir}/irssi/modules/*
# %{perl_archlib}/Irssi.pm
# %dir %attr (0755, root, bin) %{perl_archlib}/Irssi
# %{perl_archlib}/Irssi/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi
# %{perl_archlib}/auto/Irssi/Irssi.bs
# %{perl_archlib}/auto/Irssi/Irssi.so
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/Irc
# %{perl_archlib}/auto/Irssi/Irc/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/TextUI
# %{perl_archlib}/auto/Irssi/TextUI/*
# %dir %attr (0755, root, bin) %{perl_archlib}/auto/Irssi/UI
# %{perl_archlib}/auto/Irssi/UI/*
# %dir %attr (0755, root, other) %{_datadir}/irssi
# %dir %attr(0755, root, bin) %{_datadir}/irssi/*
# %{_datadir}/irssi/*/*
# %dir %attr(0755, root, bin) %{_mandir}
# %dir %attr(0755, root, bin) %{_mandir}/*
# %{_mandir}/*/*
# %{_sysconfdir}/irssi.conf
# In order to include /etc/irssi.conf, is a root
# package required (which in this case would contain one file)?

%changelog
* Sun Aug 19 2018 - Thomas Wagner
- add test on what compiler is used in perl -V:cc ... if gcc then set cc_is_gcc 1 else 0 - compiler options from gcc to irssi perl module would make StudioCC complain (S11.3)
- use build-env default compiler Studio (S11.3) or gcc, but fix compile on Studio based build environments
* Sun Aug  5 2018 - Thomas Wagner
- fix wrong %{_arch64} include of glib glibconfig.h, resulting in allocating 2^32 bytes memory causing a core dump (OM)
  open: is Solaris 11.4 affected as well?
- --with-gnu-ld=no or run into "--export-dynamic" not available in SunOS ld
- make /run scriptassist work, add (Build)Requires: SFEperl-try-tiny SFEperl-lwp
* Mon Jun 25 2018 - Thomas Wagner
- irssi with perl support on Solaris 11.4 (S11.4), compiles in 64-bit for perl-64
* Sat May 12 2018 - Thomas Wagner
- irssi with perl support on OmniOSce (OM), compiles in 64-bit for perl-64
- compile with cc_is_gcc 1 (all)
* Fri Feb 16 2018 - Thomas Wagner
- bump to 1.1.1 IRSSI-SA-2018-02 Irssi Security Advisory: CVE-2018-7054, CVE-2018-7053, CVE-2018-7050, CVE-2018-7052, CVE-2018-7051
* Mon Jan 16 2018 - Thomas Wagner
- bump to 1.1.0
* Sun Jun 26 2016 - Thomas Wagner
- bump to 0.8.19
- rename spec file, add IPS_Package_Name
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Sun Apr  5 2015 - Thomas Wagner
- bump to 0.8.17
* Wed Jul 25 2012 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_perl_default}, %include packagenamemacros.inc
* Wed Jul 25 2012 - Thomas Wagner
- bump to 0.8.15
* Fri Oct 09 2007 - Petr Sobotka sobotkap@centrum.cz
- bump to 0.8.12
* Sun Apr 08 2007 - Thomas Wagner
- bump to 0.8.11-rc1, removed tarball_version (re-add if ever needed)
* 
* Fri Sep 01 2006 - Eric Boutilier
- Initial spec
