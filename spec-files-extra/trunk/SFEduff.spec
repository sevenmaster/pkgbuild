#
# spec file for package SFEduff
#

%include Solaris.inc

Name:                    SFEduff
IPS_Package_Name:	 file/duff
Group:                   Applications/System Utilities
Summary:                 duff - Unix command-line utility for quickly finding duplicates in a given set of files.
URL:                     http://duff.dreda.org
Version:                 0.5.2
#construct unique filename for storing in source directory
#Source:                  http://github.com/elmindreda/duff/archive/%{version}.tar.gz?duff-%{version}.tar.gz
#  https://sourceforge.net/projects/duff/files/duff/0.5.2/duff-0.5.2.tar.bz2/download
Source:                  %{sf_download}/duff/duff-%{version}.tar.bz2
License:		 zlib/libpng
SUNW_Copyright:		 duff.copyright

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

#Requires: file/gnu-coreutils

%description
"duff" only finds the identical files and prints them,
but doesn't change them.
You can manually take approriate actions based in the results.

Or use the script /usr/bin/join-duplicates.sh /thisdirectory
to let it run duff and find the duplicate files. The script
then unlinks the duplicate files and creates links for them.

Use with care! (e.g. snapshot all filesystems before, run it,
then do a verification before destroying the snapshots to 
actually get the free disk space. Depending on your other
snapshots present, the new snapshot might then show the
saved disk space which is eventually freed if it is removed)
(or claimend by another snapshot lingering around)


%prep

%setup -q -n duff-%version
##don't unpack please
#%setup -q -c -T -n duff-%version
#gzip -d < %SOURCE0 | (cd ${RPM_BUILD_DIR}; tar xf -)

%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

#from README
#`gettextize' and then `autoreconf
#gettextize
#autoreconf -i

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}  \


gmake -j$CPUS

#use bash
#use gnu touch
#use gnu mktemp
#surround $file with " and as well the output of dirname
gsed -i \
  -e 's,#! */bin/sh,#! /usr/bin/bash,' \
  -e 's,touch,/usr/gnu/bin/touch,' \
  -e 's,mktemp,/usr/gnu/bin/mktemp,' \
  -e '/mktemp/ s,\$file,"\$file",' \
  -e '/mktemp/ s,mktemp -p ,mktemp -p ",' -e '/mktemp/ s,.$,"\`,' \
  join-duplicates.sh


%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT/%{_datadir}/duff/join-duplicates.sh $RPM_BUILD_ROOT/%{_bindir}/
chmod a+rx $RPM_BUILD_ROOT/%{_bindir}/join-duplicates.sh
rmdir $RPM_BUILD_ROOT/%{_datadir}/duff


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/duff/*
%attr (-, root, other) %{_datadir}/locale

%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*



%changelog
* Sun Oct 23 2016 - Thomas Wagner
- use /usr/gnu/bin/mktemp and /usr/gnu/bin/touch which knows --reference=<file> option
- escape names with spaces in join-duplicates.sh, chmod a+rx
* Sat Oct 22 2016 - Thomas Wagner
- initial spec version 0.5.2
