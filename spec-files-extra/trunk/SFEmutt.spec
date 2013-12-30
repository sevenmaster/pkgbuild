#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%include packagenamemacros.inc


Name:                SFEmutt
Summary:             The mutt e-mail client
Version:             1.5.22
Source:              ftp://ftp.mutt.org/mutt/devel/mutt-%{version}.tar.gz
Patch1:              mutt-01-makefile.diff
Patch2:              mutt-02-configure-gssapi-krb5.diff

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: %{name}-root

BuildRequires: %{pnm_buildrequires_SUNWgnu_dbm}
Requires:      %{pnm_requires_SUNWgnu_dbm}

BuildRequires: SUNWslang
Requires: SUNWslang

BuildRequires: SFElibiconv-devel
Requires: SFElibiconv

#headers for sasl in SUNWhea/
Requires: SUNWlibsasl

BuildRequires: %{pnm_buildrequires_SUNWgnu_idn}
Requires:      %{pnm_buildrequires_SUNWgnu_idn}

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n mutt-%version
%patch1 -p0
%patch2 -p0

sed -i -e 's,#! */bin/sh,#! /usr/bin/bash,' configure 


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export EXTRAINCLUDES="-I/usr/include/sasl"

#export CFLAGS="%optflags -I/usr/include/idn"
export CFLAGS="%{optflags} $EXTRAINCLUDES -I%{gnu_inc}"
export LDFLAGS="%{_ldflags} %{gnu_lib_path} -lgss"
export CPPFLAGS="$EXTRAINCLUDES -I/usr/sfw/include"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \
            --sysconfdir=%{_sysconfdir} \
	    --with-docdir=%{_docdir}/mutt \
	    --disable-nls \
	    --with-slang=/usr/lib \
	    --with-ssl=/usr/sfw \
	    --enable-pop \
	    --enable-imap \
            --enable-hcache \
            --with-idn=/usr/gnu \
            --with-libiconv-prefix=/usr/gnu \
            --enable-smtp \
            --with-sasl   \
            --without-qdbm \
            --with-gss

#            --with-idn \
#  --without-wc-funcs      Do not use the system's wchar_t functions

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

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
* Fri Oct 25 2013 - Thomas Wagner
- change (Build)Requires to %{pnm_buildrequires_SUNWgnu_dbm}
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
