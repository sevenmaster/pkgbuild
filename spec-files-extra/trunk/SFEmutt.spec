#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

##TODO## verify that TLS 1.1 TLS 1.2 works/is compiled in

%include Solaris.inc
%include packagenamemacros.inc


Name:                SFEmutt
IPS_Package_Name:    sfe/mail/mutt
Summary:             The mutt e-mail client
Version:             1.7.1
#Source:              ftp://ftp.mutt.org/mutt/devel/mutt-%{version}.tar.gz
Source:              ftp://ftp.mutt.org/pub/mutt/mutt-%{version}.tar.gz
#Source:              %{sf_download}/mutt/mutt-%{version}.tar.gz  
Patch2:              mutt-02-configure-gssapi-krb5.diff
Patch3:              mutt-03-configure-unquoted-test.diff
##TODO## remove once CVE-2014-9116 included in next version (past 1.5.23)
#Patch4:              mutt-04-CVE-2014-9116-ticket-3716-stable.patch.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %{name}-root

##TODO## openssl libraries!
#check dependencies on e.g. S11 or OI151a8, add new deps here

BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
Requires:      %{pnm_requires_SUNWgnu_dbm}

BuildRequires: %{pnm_buildrequires_SUNWslang}
Requires:      %{pnm_buildrequires_SUNWslang}

BuildRequires: SFElibiconv-devel
Requires: SFElibiconv

BuildRequires: %{pnm_buildrequires_SUNWgnu_idn}
Requires:      %{pnm_requires_SUNWgnu_idn}

#headers for sasl in SUNWhea/
#  dependency discovered: system/library/security/libsasl@0.5.11-0.175.0.0.0.2.1
BuildRequires: SUNWlibsasl
Requires:      SUNWlibsasl

#  dependency discovered: library/security/openssl@1.0.0.5-0.175.0.0.0.2.537
BuildRequires: %{pnm_buildrequires_SUNWopenssl_devel}
Requires:      %{pnm_requires_SUNWopenssl}

#  dependency discovered: system/library/security/gss@0.5.11-0.175.0.0.0.2.1
BuildRequires: SUNWgss
Requires:      SUNWgss

#smime_keys wants perl, so pkgdepend finds the actual perl as dependency
# dependency discovered: runtime/perl-512@5.12.3-0.175.0.0.0.2.537

%description

1.6.0 contains a few new features, along with a slew of bug fixes.
Please take the time to read the UPDATING file, and review the sample
gpg.rc and smime.rc files for changed and added options.  We have
started a wiki page at https://dev.mutt.org/trac/wiki/UpgradingTips
and encourage the community to contribute tips and suggestions.


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n mutt-%version
%patch2 -p0
%patch3 -p0
##TODO## remove once CVE-2014-9116 included in next version (past 1.5.23)
#%patch4 -p1

#if you dont have $PATH in your compile environment prefixed with /usr/gnu/bin then you get an error :)
sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%if %( echo  %{pnm_buildrequires_SUNWgnu_idn} | grep -i sfe >/dev/null && echo 1 || echo 0 )
CONFIGURE_WITH_IDN="--with-idn=/usr/gnu"
EXTRAINCLUDES="$EXTRAINCLUDES -I/usr/gnu/include/idn"
%else
CONFIGURE_WITH_IDN="--with-idn"
EXTRAINCLUDES="$EXTRAINCLUDES -I/usr/include/idn"
%endif
echo "DEB: CONFIGURE_WITH_IDN $CONFIGURE_WITH_IDN"
echo "DEB: EXTRAINCLUDES  $EXTRAINCLUDES"


export EXTRAINCLUDES="$EXTRAINCLUDES -I/usr/include/sasl"

export CFLAGS="%{optflags} $EXTRAINCLUDES -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} -lgss"
export CPPFLAGS="$EXTRAINCLUDES -I/usr/sfw/include"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
	    --with-docdir=%{_docdir}/mutt \
	    --disable-nls \
	    --with-slang=/usr/lib \
	    --with-ssl \
	    --enable-pop \
	    --enable-imap \
            --enable-hcache \
            $CONFIGURE_WITH_IDN \
            --with-libiconv-prefix=/usr/gnu \
            --enable-smtp \
            --with-sasl   \
            --without-qdbm \
            --enable-debug \
            --with-gdbm \
            --with-gss

#  --without-wc-funcs      Do not use the system's wchar_t functions

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

#avoid installing the same file twice, $(sysconfdir)/mime.types conflicts with OSdistro
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/
touch $RPM_BUILD_ROOT%{_sysconfdir}/mime.types
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_sysconfdir}/mime.types

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*.1
%dir %attr (0755, root, bin) %{_mandir}/man5
%{_mandir}/man5/*.5
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Sat Oct  8 2016 - Thomas Wagner
- bump to 1.7.1
- remove workaround for M_CMD, M_READ
- rework patch mutt-02-configure-gssapi-krb5.diff, mutt-03-configure-unquoted-test.diff
- remove patch1 and replace it with a dummy file which gets removed after make install and doesn't get packaged
* Thu Aug 18 2016 - Thomas Wagner
- bump to 1.7.0
* Mon Apr  4 2016 - Thomas Wagner
- bump to 1.6.0
* Thu Dec 18 2014 - Thomas Wagner
- add patch4 ticket-3716, CVE-2014-9116, Debian Bug 771125
* Thu Dec 18 2014 - Thomas Wagner
- fix download URL (now: sourceforge)
* Wed Mar 12 2014 - Thomas Wagner
- bump to 1.5.23 - CVE-2014-0467
* Wed Jan  8 2014 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWslang}
* Tue Dec 31 2013 - Thomas Wagner
- add IPS_Package_Name
- add patch3 mutt-03-configure-unquoted-test.diff
- --enable-debug 
- adjust gnu-idn location
- add (Build)Requires %{pnm_buildrequires_SUNWopenssl_devel}, %{pnm_buildrequires_SUNWopenssl_devel}
- add (Build)Requires SUNWgss, SUNWlibsasl
* Mon Dec 30 2013 - Thomas Wagner
- adjust gnu-idn location
- change (Build)Requires to %{pnm_buildrequires_SUNWgnu_dbm}
- add --enable-debug by default
- bump to 1.5.22, bugfix release. Adds support for TLS 1.1/1.2. 
- add patch mutt-02-configure-gssapi-krb5.diff (thanks to Meths for patch)
* Fri Oct 25 2013 - Thomas Wagner
- change to (Build)Requires to %{pnm_buildrequires_SUNWSUNWgnu_idn}, %include packagenamacros.inc
*     Oct 20 2010 - Thomas Wagner
- bump to 1.5.21
- Require on old builds SFEgdbm or SUNWgnnu-dbm starting with osbuild number >= 114
- add missing (Build)Requires: SUNWgnu-idn
- --with-idn=/usr/include/idn , cleaned CFLAGS
* Fri Jun 20 2008 - river@wikimedia.org
- change SFEslang dependency to SUNWslang
* Sat May 17 2008 - river@wikimedia.org
- 1.5.18
* Wed May 14 2008 - river@wikimedia.org
- Add --enable-hcache to configure
- Depend on SFEgdbm(-devel)
* Tue Jan 01 2008 - Thomas Wagner
- bump to 1.5.17
* Sun Nov 25 2007 - Thomas Wagner
- PSARC 2007/167 "IDN" is found (new around build 73/74), add -I/usr/include/idn
* Sat May 26 2007 - dick@nagual.nl
- Corrected LDFLAGS setting
* Wed May 23 2007 - dick@nagual.nl
- Bump to v1.5.15 (devel)
* Mon May 21 2007 - dick@nagual.nl
- Added CPPFLAGS and LDFLAGS (/usr/sfw) to support openssl
  Without it ssl is not supported by mutt
- Added a patch for Makefile.in to change mime.types to mutt-mime.types
  to exclude a clash with a system mime.types in /etc
- Forced dependency from libcurses to slang
* Sun May 20 2007 - dick@nagual.nl
- Initial spec
