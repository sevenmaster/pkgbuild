#
# spec file for package SFEldns.spec
#
# includes module(s): ldns
#

Name:		ldns
URL:		http://www.nlnetlabs.nl/projects/ldns/
Summary:	ldns library for DNS programming
Version:	1.6.17
Group:		System/Libraries
License:	BSD
Source:		http://www.nlnetlabs.nl/downloads/%{name}/%{name}-%{version}.tar.gz 
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir} \
	--bindir=%{_bindir} \
	--includedir=%{_includedir} \
	--libdir=%{_libdir} \
	--mandir=%{_mandir} \
	--disable-static \
	--disable-ecdsa \
	--disable-gost \
	--with-drill

make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Sun May 04 2014 - Milan Jurik
- bump to 1.6.17, add multiarch support
* Mon Sep 09 2013 - Milan Jurik
- bump to 1.6.16
* Sun Jul 29 2012 - Milan Jurik
- bump to 1.6.13
* Tue May 15 2012 - Milan Jurik
- bump to 1.6.12
* Fri Nov 25 2011 - Milan Jurik
- bump to 1.6.11
* Sun Jul 24 2011 - Guido Berhoerster <gber@openindiana.org>
- added License and SUNW_Copyright tags
* Thu Jun 30 2011 - Milan Juril
- bump to 1.6.10
* Fri Mar 25 2011 - Milan Jurik
- bump to 1.6.9
* Mon Jan 24 2011 - Milan Jurik
- bump to 1.6.8
* Mon Nov 08 2010 - Milan Jurik
- bump to 1.6.7
- disable GOST because of old OpenSSL
* Thu Sep 23 2010 - Milan Jurik
- bump to 1.6.6
* Wed Jun 09 2010 - Milan Jurik
- Initial version
