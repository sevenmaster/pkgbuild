#
# spec file for package SFEpython27-ansible
#
# includes module(s): ansible
#
%include Solaris.inc
%include osdistro.inc

%define  src_name   ansible

#Note: This spec file creates another package called "system/management/ansible" to create a nice install experience

Name:                    SFEpython27-ansible
IPS_Package_Name:	 library/python/ansible-27
Summary:                 ansible automation
License:		GPLv3+
URL:                     https://www.ansible.com/
#                                  .0. release or a beta
#2.4.0.0 .0. 0  release
#    .
#2.4.1.0 .0. 2  beta2
#    .  
#2.4.1.0 .1. 0  release 2.4.1.0 if we have a previous a beta2
#

IPS_Component_version:   2.4.0.0.0.0
#Version:                 2.4.0.0-0.2.beta2
Version:                 2.4.0.0

#Source:			http://releases.ansible.com/ansible/ansible-2.4.1.0-0.2.beta2.tar.gz
Source:			http://releases.ansible.com/ansible/ansible-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

#get pycrypto
BuildRequires:		SFEpython27-crypto
Requires:		SFEpython27-crypto

BuildRequires:		library/python/cffi
Requires:		library/python/cffi
BuildRequires:		library/python/jinja2
Requires:		library/python/jinja2
BuildRequires:		library/python/pyyaml
Requires:		library/python/pyyaml
BuildRequires:		library/python/paramiko
Requires:		library/python/paramiko
#BuildRequires:		library/python/setuptools
#Requires:		library/python/setuptools
#we need >= 1.0 and not 0.9.x unfortunately. We patch ansible to use the binary call to
BuildRequires:		SFEpython27-setuptools
Requires:		SFEpython27-setuptools
BuildRequires:		library/python/pyasn1
Requires:		library/python/pyasn1
BuildRequires:		library/python/cryptography
Requires:		library/python/cryptography
BuildRequires:		library/python/six
Requires:		library/python/six
#BuildRequires:		library/python/ipaddress
#Requires:		library/python/ipaddress
#NOTE: on S12 and on S11 from 1.0.16-0.175.3.14.0.2.0 and up, we have OS library/python/ipaddress - this gets auto-replaced through "renamed" flag in SFEpython27-ipaddress.spec-own-library/python/ipaddress@1.0.16-0.175.3.14.0.2.0 - so the OS library/python/ipaddress is the result
BuildRequires:		SFEpython27-ipaddress
Requires:		SFEpython27-ipaddress
BuildRequires:		library/python/pycparser
Requires:		library/python/pycparser

%define python_version  2.7

%package -n SFEansible
IPS_package_name:	system/management/ansible
Summary:		ansible automation
BuildRequires:		SFEpython27-ansible
Requires:		SFEpython27-ansible


%description
Ansible automation

Verify your ansible install with:
ansible -m ping yourlocalmachinename

%prep
%setup -q -n ansible-%version

#%if %{omnios}
#gsed -e '/std=c99/ s/^/#/' < setup.py
#%endif

#need to use *our* setuptools version >= 1.0 because Solaris Python 2.7 only has a 0.9 version
#we change the call to our extra easy_install-2.7-sfe
gsed -i -e '/candidate_easy_inst_basenames = ..easy_install/ s?easy_install?easy_install-2.7-sfe?' \
    lib/ansible/modules/packaging/language/easy_install.py


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
#python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix}

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ansible*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}

%changelog
* Sat Oct  7 2017 - Thomas Wagner
- Initial spec file version 2.4.0.0
