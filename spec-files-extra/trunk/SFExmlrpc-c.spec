#
# spec file for package SFExmlrpc-c
#
# includes module(s): xmlrpc-c
#
%include Solaris.inc
%include usr-gnu.inc
%include base.inc


##TODO## make this 32/64 bit

%use xmlrpc_c = xmlrpc-c.spec

Name:                   SFExmlrpc-c
IPS_Package_Name:	library/gnu/xmlrpc-c
Summary:                A lightweight RPC library based on XML and HTTP (/usr/gnu)
Group:                  System/Libraries
Version:                %{xmlrpc_c.version}
IPS_component_version:	%{xmlrpc_c.ips_component_version}
SUNW_Copyright:         %{name}.copyright
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
XML-RPC is a quick-and-easy way to make procedure calls over the Internet. 
It converts the procedure call into XML document, sends it to a remote
server using HTTP, and gets back the response as XML. This library pro-
vides a modular implementation of XML-RPC for C.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%xmlrpc_c.prep -d %name-%version
cd %{_builddir}/%name-%version

%build
export CFLAGS="%optflags -xc99"
export CFLAGS_PERSONAL="%optflags"
export LDFLAGS="%_ldflags"
%xmlrpc_c.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%xmlrpc_c.install -d %name-%version
find $RPM_BUILD_ROOT -name '*.la' -exec rm {} \; -o -name '*.a'  -exec rm {} \;

#no manpages there
rm -r $RPM_BUILD_ROOT%{_mandir}
rmdir $RPM_BUILD_ROOT%{_datadir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*
# %dir %attr(0755, root, bin) %{_mandir}
# %dir %attr(0755, root, bin) %{_mandir}/man1
# %{_mandir}/man1/*


%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Thu Jan  1 2015 - Thomas Wagner
- bump to 1.33.15
* Sun Oct 13 2013 - Thomas Wagner
- bump to 1.25.26
- IPS bring back IPS_component_version to regular format (needs manual 
  removal of version 1.632 IPS Packages from repo and system)
- add -std=c99
- relocate to /usr/gnu (S11 has own xmlrpc-c), add IPS_Package_Name
* Sat Mar 31 2012 - tropikhajma@gmail.com>
- fix ips version
* Tue Jun 24 2008 - trisk@acm.jhu.edu
- Rename to SFExmlrpc-c since we don't distribute C++ libs
- Add CFLAGS_PERSONAL for Studio
* Sat May 24 2008 - trisk@acm.jhu.edu
- Initial spec
