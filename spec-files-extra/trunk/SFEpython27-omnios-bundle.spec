#
# spec file for package SFEpython27-pyasn1
#
# includes module(s): pyasn1
#
%include Solaris.inc
%include osdistro.inc

%define _use_internal_dependency_generator 0


%if %{omnios}

Name:                    SFEpython27-omnios-bundle
IPS_Package_Name:	 library/python/omnios-bundle
Summary:                 bundle package to add common python modules
Version:                 0.0.1
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7

BuildRequires: SFEpython27-pycparser
Requires:      SFEpython27-pycparser
BuildRequires: SFEpython27-six
Requires:      SFEpython27-six
BuildRequires: SFEpython27-cffi
Requires:      SFEpython27-cffi
BuildRequires: SFEpython27-pyyaml
Requires:      SFEpython27-pyyaml
BuildRequires: SFEpython27-pyasn1
Requires:      SFEpython27-pyasn1
BuildRequires: SFEpython27-cryptography
Requires:      SFEpython27-cryptography
#paused BuildRequires: SFEpython27-pelican
#paused Requires:      SFEpython27-pelican
BuildRequires: SFEpython27-pycrypto
Requires:      SFEpython27-pycrypto
BuildRequires: SFEpython27-markupsafe
Requires:      SFEpython27-markupsafe
BuildRequires: SFEpython27-jinja2
Requires:      SFEpython27-jinja2
BuildRequires: SFEpython27-paramiko
Requires:      SFEpython27-paramiko



%description
Add common python modules that are not present in OSDISTRO OmniOS. 
Downstream (Build)Requires are then propperly resolved by specifying the IPS package name in spec files (this a term from the development of these packages).


%endif
##END omnios

%changelog
* Fri  8 Dec 2017 - Thomas Wagner
- Initial spec file version 0.0.1
