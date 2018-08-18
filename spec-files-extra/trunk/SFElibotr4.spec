#
# spec file for package SFElibotr
#
# includes module(s): libotr
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%include packagenamemacros.inc
%include usr-gnu.inc
%include base.inc

%define srcname libotr

Name:                    SFElibotr4
IPS_Package_Name:	 library/security/gnu/libotr4
Summary:                 libotr - Off-the-Record Messaging Library and Toolkit (/usr/gnu)
Group:                   Utility
Version:                 4.1.1
URL:		         http://www.cypherpunks.ca/otr/
Source:		         http://www.cypherpunks.ca/otr/libotr-%version.tar.gz
License: 		 LGPLv2
SUNW_Copyright:          %{license}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:           %{pnm_buildrequires_SUNWlibgcrypt_devel}
Requires:                %{pnm_buildrequires_SUNWlibgcrypt}


%description
This is a library and toolkit which implements Off-the-Record (OTR) Messaging.

OTR allows you to have private conversations over IM by providing:
 - Encryption
   - No one else can read your instant messages.
 - Authentication
   - You are assured the correspondent is who you think it is.
 - Deniability
   - The messages you send do _not_ have digital signatures that are
     checkable by a third party.  Anyone can forge messages after a
     conversation to make them look like they came from you.  However,
     _during_ a conversation, your correspondent is assured the messages
     he sees are authentic and unmodified.
 - Perfect forward secrecy
   - If you lose control of your private keys, no previous conversation
     is compromised.

%prep
rm -rf %name-%version
%setup -q -n %srcname-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
# we don't need the utilities that are under GPL instead of LGPL (if
# we do they should be in a separate package.)
rm -rf $RPM_BUILD_ROOT/usr/share/man
rm -rf $RPM_BUILD_ROOT/usr/bin
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libotr.*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/libotr.pc
%dir %attr (0755, root, bin) %{_includedir}/libotr
%{_includedir}/libotr/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/libotr.m4


%changelog
* Sat Aug 18 2018 - Thomas Wagner
- bump to 4.1.1
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Mon Jan  5 2014 - Thomas Wagner
- bump to 4.1.0
* Sun Dec 16 2012 - Thomas Wagner
- move to /usr/gnu by %include usr-gnu.inc (interferes with files from solaris/communication/im/pidgin)
- change (Build)Requires to %{pnm_buildrequires_SUNWlibgcrypt_devel}, %include packagenamemacros.inc
- change IPS_Package_Name to library/security/gnu/libotr
- remove static files, add %{_bindir} and %{_mandir}/man1 to %files
* Sun Nov  5 2012 - Logan Bruns <logan@gedanken.org>
- Updated to 3.2.1.
* Tue Apr 17 2012 - Logan Bruns <logan@gedanken.org>
- Fixed some permissions.
* Thu Mar 1 2012- Logan Bruns <logan@gedanken.org>
- Initial spec.
