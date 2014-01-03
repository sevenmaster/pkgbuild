



Summary:	A little color management system (/usr/gnu)
Version:	%{version}
Source:		http://www.littlecms.com/%{src_name}-%{version}.tar.gz



%prep
%setup -q -n %{src_name}-%{version}


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --mandir=%{_mandir} \
            --docdir=%{_docdir} \
            --disable-static \

gmake -j$CPUS

%install
make DESTDIR=%{buildroot} install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/*.a


%changelog
* Wed Jan 01 2014 - Thomas Wagner
- add 32/64-bit support
