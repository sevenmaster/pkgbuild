#
# spec file for package SFEbinwalk
#
# includes module(s): binwalk
#
%include Solaris.inc
%include osdistro.inc

%define  src_name   binwalk

Name:                    SFEbinwalk
IPS_Package_Name:	 developer/binwalk
Summary:                 binwalk through firmware binaries
URL:                     https://github.com/devttys0/binwalk 
Version:                 2.1.1
Source:                  http://github.com/devttys0/binwalk/archive/v%{version}.tar.gz?binwalk-%{version}.tar.gz

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
#BuildRequires:           runtime/python-27
#Requires:                runtime/python-27
##TODO## adjust for different python majorminor versions
BuildRequires:		SFEpython27-lzma
Requires:		SFEpython27-lzma

%define python_version  2.7

%prep
%setup -q -n binwalk-%version

#%if %{omnios}
#gsed -e '/std=c99/ s/^/#/' < setup.py
#%endif

%build
export CC=gcc
%if %( /usr/bin/python%{python_version}-config --cflags  | grep -- -m64 >/dev/null && echo 1 || echo 0 )
BITS=64
export CFLAGS="-m64 -I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib/%{_arch64} -R%gnu_lib/%{_arch64}"
export PYTHON_BINARY_OFFSET="/usr/bin/%{_arch64}"
%else
BITS=32
export CFLAGS="-I%{gnu_inc}"
export LDFLAGS="-L%gnu_lib -R%gnu_lib"
export PYTHON_BINARY_OFFSET="/usr/bin"
%endif
echo "compiling for ${BITS}-bit python!"


${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Fri Feb 10 2017 - Thomas Wagner
- Initial spec file version 2.1.1
