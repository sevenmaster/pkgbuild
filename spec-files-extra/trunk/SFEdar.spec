#
# spec file for package SFEdar
#

%define src_name dar
%define _pkg_docdir %_docdir/%src_name
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

Name:                    SFEdar
IPS_package_name:	 compress/dar
Group:			 Applications/System Utilities
Summary:                 Archiving and compression utility avoiding the drawbacks of tar
URL:                     http://dar.linux.free.fr/
Version:                 2.4.11
Source:                  %{sf_download}/dar/dar-%{version}.tar.gz
#Patch1:			dar-01-configure-detect-getopt-in-unistd.h.diff
License:		 GPLv2
SUNW_Copyright:		 GPLv2.copyright
SUNW_BaseDir:            %{_basedir}

BuildRequires: SFEgcc
BuildRequires: SUNWbzip
BuildRequires: SFElzo
Requires: SFEgccruntime
Requires:      %{pnm_requires_perl_default}
Requires: SUNWbash
Requires: SUNWbzip

%include default-depend.inc

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%description
dar (Disk ARchive) is a command-line archiving tool and a replacement for tar,
in the latter's capacity as an archiver as opposed to a distribution medium.
dar features:
● Support for slices — archives split over multiple files of a particular size
● The option of deleting files from the system that have been removed from the
archive
● Incremental backup
● Decremental backup
● Taking care of hard-linked inodes (hard-linked plain files, char devices,
block devices, hard-linked symlinks
● Takeing care of sparse files
● Taking care of POSIX Extended Attributes, which implies POSIX File ACL under
Linux and File forks under Mac OS X (not implemented for Solaris)
● Per-file compression with gzip, bzip2 or lzo (as opposed to compressing the
whole archive). The user can choose not to compress already compressed files,
based on their filename suffix
● Fast extracting of files from anywhere in the archive
● Fast listing of archive contents through saving the catalogue of files in the
archive
● Optional Blowfish, Twofish, AES, Serpent, Camellia encryption
● Live filesystem backup: dar detects when a file has been modified while it was
read for backup and can retry saving it up to a given maximum number of retries
● Live Database backup: a user command can be launched before and after saving
a particular set of files or directories — suitable for placing a database in a
consistent state during its backup
● A hash file (md5 or sha1) is generated for each slice: this hash can be used
to quickly check each slice's integrity


%prep
%setup -q -n %src_name-%version
#%patch1 -p1


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%{optflags} -I%{gnu_inc} -D__EXTENSIONS__ -DHAVE_GETOPT_IN_UNISTD_H=1"
export CXXFLAGS="%{cxx_optflags} -I%{gnu_inc} -D__EXTENSIONS__ -DHAVE_GETOPT_IN_UNISTD_H=1"

#export LD=ld-wrapper
export LDFLAGS="%_ldflags %picflags"

export CC=gcc
export CXX=g++

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-gnugetopt \
            --enable-examples    \
            --disable-dar-static \
            --disable-static

make -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*la

cd %buildroot/%_prefix
mkdir -p share/doc/%src_name/doc
mv share/dar/* share/doc/%src_name/doc
rmdir share/dar
mv etc/darrc share/doc/%src_name/doc/darrc.example
rmdir etc

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc ABOUT-NLS AUTHORS ChangeLog NEWS README THANKS TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %_docdir
%_pkg_docdir/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%if %build_l10n
%files l10n
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif


%changelog
* Fri Nov 15 2013 - Thomas Wagner
- change Requires to %{pnm_requires_perl_default}, SFElzo, %include packagenamemacros.inc
* Tue Nov  5 2013 - Alex Viskovatoff <herzen@imapmail.org>
- do not add %gnu_lib_path to LDFLAGS: dar does not use any libraries there
* Mon Nov  4 2013 - Alex Viskovatoff <herzen@imapmail.org>
- update to 2.4.11
* Sun Jun 07 2009 - Thomas Wagner
- C++ errors, switched to gcc(4.x) (no deep check why SunStudio C++ does not compile)
* Mon Jun 01 2009 - Thomas Wagner
- Initial spec
