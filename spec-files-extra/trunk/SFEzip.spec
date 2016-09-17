#
# spec file for package SFEzip
#
# includes module: zip
#
## TODO ##
# Probably make 64bit version

# Note: this is required on Openindiana only AFAIK ebcause OI has too old a version of zip for Libreoffice

%include Solaris.inc
%include usr-gnu.inc
%define cc_is_gcc 1
%include base.inc
%include packagenamemacros.inc
#%define _use_internal_dependency_generator 0


%define src_name zip

Name:			SFEzip-gnu
IPS_Package_Name:	sfe/compress/gnu/zip
Summary:		The Info-Zip (zip) compression utility
Group:			System/Libraries
URL:			http://www.info-zip.org/Zip.html
Version:		3.0
License:		BSD
#SUNW_Copyright:	%{license}.copyright
Source:			ftp://ftp.info-zip.org/pub/infozip/src/zip30.tgz
Patch1:			zip-01-configure.patch
Patch2:			zip-02-zipnote.patch
SUNW_BaseDir:		%_basedir
BuildRoot:		%_tmppath/%name-%version-build

%include default-depend.inc

##TODO## BuildRequires:	SFEgcc
##TODO## Requires:	SFEgccruntime

# (Build)Requires bzip2
BuildRequires:	%{pnm_buildrequires_SUNWbzip_devel}
Requires:	%{pnm_requires_SUNWbzip}

%description
Zip is a compression and file packaging/archive utility. Although highly compatible both with PKWARE's PKZIP and PKUNZIP utilities for MS-DOS and with Info-ZIP's own UnZip, our primary objectives have been portability and other-than-MSDOS functionality.


%prep
#%setup -q -n %src_name-%version
%setup -q -n zip30
%patch1 -p1
%patch2 -p1

# Change prefix to /usr/gnu
cp -p unix/Makefile unix/Makefile.orig
gsed -i -e 's|prefix = /usr/local|prefix = $(DESTDIR)%{_prefix}|' \
	-e 's|MANDIR = $(prefix)/man/man$(MANEXT)|MANDIR = $(prefix)/share/man/man$(MANEXT)|'	\
	unix/Makefile	\
	;

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CC=gcc
export CFLAGS="%optflags -I/usr/gnu/include"
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"


#make -j$CPUS
make -f unix/Makefile generic_gcc


%install
rm -rf $RPM_BUILD_ROOT
make -f unix/Makefile install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/zip*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/zip*

%changelog
* Sun Aug 16 2015 - pjama
- initial spec to provide updated info-zip for OI 151a9 required by Libreoffice
