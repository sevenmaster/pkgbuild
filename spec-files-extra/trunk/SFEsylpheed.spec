#
# spec file for package SUNWsylpheed
#

%include Solaris.inc
%include packagenamemacros.inc

%define src_name        sylpheed
#%define src_version 3.3.0
#%define src_version 3.4.0beta4
%define src_version 3.6.0
#(echo 3.4.0; echo 3.4.0beta4) | sed regex-here) -> 3.4 or 3.4beta
#%define src_url_dir     %( echo src_version |  sed -e 's/^\([0-9]*\.[0-9]*\)\.[0-9]*/\1/'  -e 's/^\([0-9]*\.[0-9]*\)\(beta\).*/\1\2/' )
# 3.6.0beta1 > 3.6beta
# (echo 3.6.1; echo 3.6.0beta1 ) | sed -e 's?beta.*?beta?' -e 's?\.[0-9]$??' -e 's?\.[0-9]*beta?beta?'
%define src_url_dir     %( echo v%{src_version} | sed -e 's?beta.*?beta?' -e 's?\.[0-9]$??' -e 's?\.[0-9]*beta?beta?' )
%define src_url         http://sylpheed.sraoss.jp/sylpheed/%{src_url_dir}


Name:                     SFEsylpheed
IPS_Package_Name:  	  mail/sylpheed
Summary:                  A GTK+ based, lightweight, and fast e-mail client
Version:                  %{src_version}
#make betas 3.4.0.0.<beta-n> and release 3.4.0.1.0
# ( echo "3.4.0"; echo "3.5.0beta1" )  |  sed -e 's/beta/.0./' -e '/^[0-9]*\.[0-9]*\.[0-9]*$/ s/$/.1.0/'
#3.4.0.1.0
#3.5.0.0.1
IPS_component_version: %( echo %{version} | sed -e 's/beta/.0./' -e '/^[0-9]*\.[0-9]*\.[0-9]*$/ s/$/.1.0/' )
Group:		          Applications/Internet
Source:                   %{src_url}/%{src_name}-%{version}.tar.bz2
License:                  GPLv2+ with openSSL exception
URL:                      http://sylpheed.sraoss.jp/
SUNW_BaseDir:             %{_basedir}
BuildRoot:                %{_tmppath}/%{name}-%{version}-build
SUNW_Copyright:		  sylpheed.copyright
%include default-depend.inc

#BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: %{pnm_buildrequires_SUNWopenssl}
BuildRequires: %{pnm_buildrequires_SUNWlibms}
BuildRequires: %{pnm_buildrequires_library_desktop_gtkspell}
BuildRequires: %{pnm_buildrequires_SUNWgnupg_devel}
Requires:      %{pnm_requires_SUNWlibms}
Requires:      SUNWgnome-base-libs
Requires:      %{pnm_requires_SUNWopenssl}
Requires:      %{pnm_requires_library_desktop_gtkspell}
Requires:      %{pnm_requires_SUNWgnupg}

#descriton taken from original sylpheed.spec file:
%description
Sylpheed is an e-mail client (and news reader) based on GTK+, running on
X Window System, and aiming for
 * Quick response
 * Simple, graceful, and well-polished interface
 * Easy configuration
 * Intuitive operation
 * Abundant features
The appearance and interface are similar to some popular e-mail clients for
Windows, such as Outlook Express, Becky!, and Datula. The interface is also
designed to emulate the mailers on Emacsen, and almost all commands are
accessible with the keyboard.

The messages are managed by MH format, and you'll be able to use it together
with another mailer based on MH format (like Mew). You can also utilize
fetchmail or/and procmail, and external programs on receiving (like inc or
imget).

%if %build_l10n
%package l10n
Summary:	%{summary} - l10n files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}
%endif

%prep
%setup -q -n %{src_name}-%{version}


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}          \
            --bindir=%{_bindir}         \
            --mandir=%{_mandir}         \
            --libdir=%{_libdir}         \
            --datadir=%{_datadir}       \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared             \
            --disable-static


make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=${RPM_BUILD_ROOT} install
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
#install -m 644 *.png ${RPM_BUILD_ROOT}%{_datadir}/pixmaps

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean 
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc AUTHORS COPYING COPYING.LIB ChangeLog ChangeLog.ja ChangeLog-1.0 ChangeLog-1.0.ja README README.es README.ja INSTALL INSTALL.ja NEWS NEWS-1.0 NEWS-2.0 LICENSE TODO TODO.ja
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/%{src_name}
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/%{src_name}/faq/*/*
%{_datadir}/%{src_name}/manual/*/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*.png
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Jul 25 2017 - Thomas Wagner
- bump to 3.6.0
- fix (Build)Requires to more pnm_macros
- fix version number calculation for old pkgbuild version
* Sun Aug 11 2013 - Thomas Wagner
- bump to 3.4.0beta4
- make IPS_Component_Version "beta4" aware, make src_url_dir "beta" aware
- fix permissions for %{_docdir}
- change to (Build)Requires to %{pnm_buildrequires_SUNWopenssl}, %include packagenamacros.inc
* Fri Jan 04 2013 - Ken Mays <kmays2000@gmail.com>
- bump to 3.3.0
- Added GnuPG and GTKspell
* Sat Aug 25 2012 - Ken Mays <kmays2000@gmail.com>
- bump to 3.2.0
* Tue Sep 14 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 3.1.2
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Mon Jun 6 2011 - Ken Mays <kmays2000@gmail.com>
- bump to 3.1.1
* Sat Apr 16 2011 - Alex Viskovatoff
- bump to 3.1.0
* Thu Oct 16 2009 - Dick Hoogendijk
- update to 2.7.1 stable
* Thu Jan 1 2009 - Dick Hoogendijk
- update to the stable 2.6 release
* Thu Jul 3 2008 - Dick Hoogendijk
- update to the stable 2.5 release
* Mon May 12 2008 - Thomas Wagner
- inital spec including base-specs/syhlpeed.spec from the tarball
