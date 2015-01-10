#/tmp/pkgbuild.out.*: No such file or directory
#
#ERROR: failed to update IPS packages: Error 1: 
#pkg install: The following packages all deliver file actions to usr/gnu/share/info/dir:
#
#  pkg://localhosts11/compress/gnu/lzip@1.16,5.11-0.0.175.0.0.0.2.0:20150109T014918Z
#  pkg://localhosts11/sfe/library/gmp@5.1.3,5.11-0.0.175.0.0.0.2.0:20131101T095425Z



#
# spec file for package SFElzip
#
# includes module(s): lzip
#

%include Solaris.inc
%define cc_is_gcc 1
%include usr-gnu.inc
%include base.inc

%include arch64.inc
%use lzip_64 = lzip.spec
%include base.inc
%use lzip = lzip.spec


Name:                    %{lzip.name}
IPS_Package_Name:	compress/gnu/lzip
Summary:    	         %{lzip.summary} (/usr/gnu)
Version:                 %{lzip.version}
URL:			 %{lzip.url}
Source:         http://download.savannah.gnu.org/releases/lzip/lzip-%{version}.tar.gz
#SUNW_Copyright: lzip-utils.copyright
Group:		Applications/Archivers
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc


%description
Lzip is a lossless data compressor with a user interface similar to the one of gzip or bzip2. Lzip is about as fast as gzip, compresses most files more than bzip2, and is better than both from a data recovery perspective. Lzip is a clean implementation of the LZMA algorithm.

%prep
rm -rf %{name}-%{version}
mkdir -p %{name}-%{version}/%_arch64
%lzip_64.prep -d %{name}-%{version}/%_arch64


%build
%lzip_64.build -d %{name}-%{version}/%_arch64


%install
rm -rf %{buildroot}
%lzip_64.install -d %{name}-%{version}/%_arch64

#want 64-bit binary in bin/amd64 and in bin
ln %{buildroot}%{_bindir}/%{_arch64}/lzip %{buildroot}%{_bindir}/lzip

[ -r ${RPM_BUILD_ROOT}%{_datadir}/info/dir ] && rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(0755, root, bin)
%{_bindir}/%{_arch64}/lzip
%hard %{_bindir}/lzip
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/info/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man*/*


%changelog
* Sat Jan 10 2015 - Thomas Wagner
- remove conflicting file share/info/dir
* Fri Jan  1 2014 - Thomas Wagner
- initial spec
- derived from SFExz-gnu.spec
- build 64-bit only, bindir is /usr/gnu/bin/
- fix build for 64-bit only
- rename to SFElzip-gnu.spec
