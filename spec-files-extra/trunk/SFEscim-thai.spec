#
# spec file for package SFEscim-thai
#
# includes module(s): scim-thai
#
%include Solaris.inc

%define	src_name scim-thai
%define	src_url	ftp://linux.thai.net/pub/thailinux/software/libthai

Name:                SFEscim-thai
Summary:             SCIM Thai language support
Version:             0.1.0
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEscim-devel
Requires: SFEscim
BuildRequires: SFElibdatrie-devel
Requires: SFElibdatrie

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal -I m4
automake -a -f
autoconf -f -I autoconf
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    --disable-static		\
	    --enable-shared

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/scim

%changelog
* Thu Jul 26 2007 - dougs@truemail.co.th
- Initial spec
