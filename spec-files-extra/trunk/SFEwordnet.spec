#
# spec file for package SFEwordnet.spec
#
# includes module(s): wordnet
#
%include Solaris.inc

%define src_name	WordNet
%define src_url		http://wordnetcode.princeton.edu/
%define base_version    3.0

Name:                   SFEwordnet
IPS_Package_Name:	text/wordnet
Summary:                lexical database for the English language
Version:                3.1
Source:                 %{src_url}/%{base_version}/%{src_name}-%{base_version}.tar.bz2
Source2:                %{src_url}/wn%{version}.dict.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{base_version}
tar xzf %{SOURCE2}
gsed -i -e 's/%{base_version}/%{version}/g' configure lib/wnglobal.c

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


export PATH=$PATH:/usr/sfw/bin
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc
mv $RPM_BUILD_ROOT/usr/doc $RPM_BUILD_ROOT%{_datadir}/doc/WordNet
mkdir -p $RPM_BUILD_ROOT%{_datadir}/lib
mv $RPM_BUILD_ROOT/usr/dict $RPM_BUILD_ROOT%{_datadir}/lib/dict

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755,root,sys) %{_datadir}/lib
%dir %attr (0755,root,other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/lib/*
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}
%{_libdir}

%changelog
* Mon Mar 11 2013 - Logan Bruns <logan@gedanken.org>
- Updated to 3.1
* Sat Mar 10 2012 - Logan Bruns <logan@gedanken.org>
- Updated download url and added ips package name.
* Sun Mar  6 2007 - dougs@truemail.co.th
- Initial version
