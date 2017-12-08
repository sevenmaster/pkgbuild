#
# spec file for package SFEpython-pycrypto
#
# includes module(s): pycrypto
#
%include Solaris.inc
%include osdistro.inc
%include pkg-renamed.inc

%define _use_internal_dependency_generator 0

%define  src_name   pycrypto

Name:                    SFEpython27-pycrypto
IPS_Package_Name:	 library/python/pycrypto-27
Summary:                 Cryptographic library for the Python Programming Language
URL:                     http://www.pycrypto.org
Version:                 2.6.1
Source:                  http://ftp.dlitz.net/pub/dlitz/crypto/pycrypto/pycrypto-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-pycrypto
IPS_Package_Name:	 library/python/pycrypto
Summary:                 %{summary}
Requires:	         SFEpython27-pycrypto

%description
pycrypto
This is a collection of both secure hash functions (such as SHA256 and RIPEMD160), and various encryption algorithms (AES, DES, RSA, ElGamal, etc.). 

%if %{solaris11}%{solaris12}%{oihipster}
%package -n %{name}-noinst-1
Summary:                %{summay} - automatic renamed-to-package to uninstall python-crypto package and install pycrypto
IPS_Package_Name:	/library/python/python-crypto
%define renamed_from_oldname      library/python/python-crypto
%define renamed_to_newnameversion library/python/pycrypto = *
%include pkg-renamed-package.inc

%package -n %{name}-noinst-2
Summary:                %{summay} - automatic renamed-to-package to uninstall python-crypto package and install pycrypto
IPS_Package_Name:	/library/python/python-crypto-27
%define renamed_from_oldname      library/python/python-crypto-27
%define renamed_to_newnameversion library/python/pycrypto-27 = *
%include pkg-renamed-package.inc

%actions -n %{name}-noinst-1
depend fmri=library/python/python-crypto@%{ips_version_release_renamedbranch} type=optional

%actions -n %{name}-noinst-2
depend fmri=library/python/python-crypto-27@%{ips_version_release_renamedbranch} type=optional

%endif #%{solaris11}%{solaris12}%{oihipster}

%prep
%setup -q -n pycrypto-%version

%if %{omnios}
gsed -e '/std=c99/ s/^/#/' < setup.py
%endif

%build
%if %( expr %{solaris11} '=' 1 '|' %{solaris12} '=' 1 )
export CC=cc
%else
export CC=gcc
%endif

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
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Thu Dec  7 2017 - Thomas Wagner
- rename from library/python/python-crypto-27 to library/python/pycrypto-27
- add unversioned alias package library/python/pycrypto
- add renamed-to as old name library/python/python-crypto-27 needs to uninstall for library/python/pycrypto-27
* Sun Jul 31 2016 - Thomas Wagner
- bump to version 2.6.1, copy to separate files to get python-version specific packages
- add IPS_Package_name
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec file
