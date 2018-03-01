
# modeled after https://github.com/oracle/solaris-userland/tree/master/components/sg3_utils


#
# spec file for package SFEsg3_utils
#
#
# you will need FUSE see: http://www.opensolaris.org/os/project/fuse

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name sg3_utils

#avoid detection of osdistro delivered fuse / libfuse package
%define _use_internal_dependency_generator 0

Name:                    SFEsg3utils
Summary:                 sg3_utils - send SCSI commands
Version:                 1.42
IPS_package_name:	utility/sg3utils
#License:                 
Source:			http://sg.danny.cz/sg/p/sg3_utils-%{version}.tgz
Source2:		sg3_utils-exec_attr
Source3:		sg3_utils-prof_attr
Patch1:                  sg3_utils-solaris-build.patch
Patch2:                  patches/sg3_utils-solaris-build.patch-_XOPEN_SOURCE
Url:                    http://sg.danny.cz/sg/sg3_utils.html
SUNW_BaseDir:           /
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


%description
sg3_utils

%prep
%setup -q -n %{src_name}-%{version}
%if %cc_is_gcc
#only remove _XOPEN_SOURCE
%patch2 -p1
%else
%patch1 -p1
%endif

cp -p %{SOURCE2} .
cp -p %{SOURCE3} .

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')
export CC=gcc
export CXX=g++

export CFLAGS="%{optflags}"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
	    --disable-static			\

gsed -i.bak  \
     -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
     -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
     libtool
 

gmake V=2 -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

##TODO##
# copy profile files to /etc/security

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%{_libdir}/*
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man*
%{_mandir}/man*/*


%changelog
* Wed Mar  1 2018 - Thomas Wagner
- Initial spec version 1.42
