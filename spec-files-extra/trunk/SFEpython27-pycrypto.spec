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
Source2:                 python-switch-to-env-CC.py
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

#make renamed-to-package for all OSDISTRO %if %{solaris11}%{solaris12}%{oihipster}
%package -n %{name}-noinst-1
Summary:                %{summay} - automatic renamed-to-package to uninstall python-crypto package and install pycrypto
IPS_Package_Name:	library/python/python-crypto
%define renamed_from_oldname      library/python/python-crypto
%define renamed_to_newnameversion library/python/pycrypto = *
%include pkg-renamed-package.inc

%package -n %{name}-noinst-2
Summary:                %{summay} - automatic renamed-to-package to uninstall python-crypto package and install pycrypto
IPS_Package_Name:	library/python/python-crypto-27
%define renamed_from_oldname      library/python/python-crypto-27
%define renamed_to_newnameversion library/python/pycrypto-27 = *
%include pkg-renamed-package.inc


%actions
depend fmri=library/python/python-crypto@%{ips_version_release_renamedbranch} type=optional
depend fmri=library/python/python-crypto-27@%{ips_version_release_renamedbranch} type=optional


%prep
%setup -q -n pycrypto-%version

%if %{omnios}
gsed -e '/std=c99/ s/^/#/' < setup.py
%endif

#hipster
cp -p %{SOURCE2} .

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

%if %{oihipster}
#unfortunatly oihipster has a complete path to "gcc" in the python 2.7 core. That makes it impossible to
#got with the sfe-gcc compiler.
#this is a workaroud to change compiler ar build time
#CC='/usr/gcc-sfe/4.9/bin/gcc -m32 -O3  -fPIC -DPIC -std=c99 -D_XOPEN_SOURCE=600' LDSHARED='/usr/gcc-sfe/4.9/bin/gcc -m32 -O3  -fPIC -DPIC -std=c99 -D_XOPEN_SOURCE=600 -shared -m32 -fPIC -DPIC -R/usr/gnu/lib -L/usr/gnu/lib' ${PYTHON_BINARY_OFFSET}/python2.7 setup.py  build_ext 

${PYTHON_BINARY_OFFSET}/python%{python_version} python-switch-to-env-CC.py  > python_env.source
. python_env.source
export CC CXX LDSHARED
%endif

#if set, use the variables from environment CC CXX LDSHARED (OIH)
#needs build_ext
${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build_ext

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
* Thu Mar 15 2018 - Thomas Wagner
- add workaround to python 2.7 core pointing with full path to /usr/gcc/bin/gcc, we want our /usr/gcc-sfe/bin/gcc (OIH)
- remove leading "/" from IPS names in renamed-to packages, fix assigment of %action
* Sat Dec  9 2017 - Thomas Wagner
- fix osdistro switch for renamed-to-package (S11, S12, OIH)
* Thu Dec  7 2017 - Thomas Wagner
- rename from library/python/python-crypto-27 to library/python/pycrypto-27
- add unversioned alias package library/python/pycrypto
- add renamed-to as old name library/python/python-crypto-27 needs to uninstall for library/python/pycrypto-27
* Sun Jul 31 2016 - Thomas Wagner
- bump to version 2.6.1, copy to separate files to get python-version specific packages
- add IPS_Package_name
* Sat Oct 06 2007 - ananth@sun.com
- Initial spec file
