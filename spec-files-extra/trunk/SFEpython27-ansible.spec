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

IPS_Component_version:   2.5.5.0.0.0
#Version:                 2.4.0.0-0.2.beta2
#Version:                 2.4.2.0
Version:                 2.5.5.0

#Source:			http://releases.ansible.com/ansible/ansible-2.4.1.0-0.2.beta2.tar.gz
Source:			http://releases.ansible.com/ansible/ansible-%{version}.tar.gz
SUNW_BaseDir:            /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%if %{omnios}
#with this package, the following IPS package names can be resolved by pkgtool/pkgbuild automatically.
#the packages provide python modules which are normally in OSDISTRO, but OmniOS/OmniOSce is a bit too slim :)
BuildRequires:          SFEpython27-omnios-bundle
Requires:               SFEpython27-omnios-bundle
%endif

#get pycrypto either by requesting SFEpython27-pycrypto or from the OSdistro
BuildRequires:		library/python/pycrypto-27
Requires:		library/python/pycrypto-27
BuildRequires:		library/python/cffi-27
Requires:		library/python/cffi-27
BuildRequires:		library/python/jinja2-27
Requires:		library/python/jinja2-27
BuildRequires:		library/python/pyyaml-27
Requires:		library/python/pyyaml-27
BuildRequires:		library/python/paramiko-27
Requires:		library/python/paramiko-27
BuildRequires:		library/python/pyasn1-27
Requires:		library/python/pyasn1-27
BuildRequires:		library/python/cryptography-27
Requires:		library/python/cryptography-27
BuildRequires:		library/python/six-27
Requires:		library/python/six-27
BuildRequires:		library/python/pycparser-27
Requires:		library/python/pycparser-27

#only fun BuildRequires:		text/cowsay
#only fun Requires:		text/cowsay

#BuildRequires:		library/python/setuptools
#Requires:		library/python/setuptools
#we need >= 1.0 and not 0.9.x unfortunately. We patch ansible to use the binary call to
BuildRequires:		SFEpython27-setuptools
Requires:		SFEpython27-setuptools
#BuildRequires:		library/python/ipaddress
#Requires:		library/python/ipaddress
#NOTE: on S12 and on S11 from 1.0.16-0.175.3.14.0.2.0 and up, we have OS library/python/ipaddress - this gets auto-replaced through "renamed" flag in SFEpython27-ipaddress.spec-own-library/python/ipaddress@1.0.16-0.175.3.14.0.2.0 - so the OS library/python/ipaddress is the result
BuildRequires:		SFEpython27-ipaddress
Requires:		SFEpython27-ipaddress

%define python_version  2.7

%package -n SFEansible
IPS_package_name:	system/management/ansible
Summary:		ansible automation
BuildRequires:		SFEpython27-ansible
Requires:		SFEpython27-ansible


%description
Ansible automation

Verify your ansible install with:
ansible -m ping localhost

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

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ansible

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ansible*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}
%dir %attr(-, root, sys) %{_sysconfdir}
%dir %attr(-, root, sys) %{_sysconfdir}/ansible/

%changelog
* Fri Jun 22 2018 - Thomas Wagner
- bump to 2.5.5
* Fri Dec  8 2017 - Thomas Wagner
- add empty %{_sysconfdir}/ansible (check if that directory gets removed on pkg uninstall ansible if files are in it)
- rename (Build)Requires from python-crypto to python/pycryptro
- add helper package to pull in modules (Build)Requires SFEpython27-omnios-bundle (OM only).
* Tue Dec  5 2017 - Thomas Wagner
- bump to 2.4.2
* Sat Oct  7 2017 - Thomas Wagner
- Initial spec file version 2.4.0.0
