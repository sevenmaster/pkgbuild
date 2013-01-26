#
# spec file for package SFEjxplorer
#


##TODO## fix gnome menu icon

%include Solaris.inc
%include osdistro.inc

%define src_name  jxplorer
%define subdir    jxplorer
%define platform  default
%ifarch amd64 i386
%define platform  intel
%endif
%ifarch sparcv9
%define platform  sparc
%endif


Name:                    SFEjxplorer
Summary:                 jxplorer - LDAP Directory Editor (Java based, X-Windows)
URL:                     http://www.jxplorer.org
Version:                 3.3.02
#3.3b2 -> 3.3.0.0.2,  3.3 -> 3.3.0.1.0,  3.3.1 -> 3.3.1.0.1.0,   3.3.1b7 -> 3.3.1.0.0.7, 3.3.02 -> 3.3.2.0.1.0
#(echo 3.3b2; echo 3.3; echo 3.3.1; echo 3.3.1b7; echo 3.3.02) | gsed -e 's/\([0-9]*\.[0-9]*\)$/\1.0.1.0/' -e 's/\([0-9]\)b\(.*\)/\1.0.0.\2/' -e 's/\.0*\([0-9]\)/.\1/g'
#note: to keep the order with non-beta being numbered higher then beta version,
# this adds one more ".greater_then_zero_number.0" (.1.0 here) or translate the
# letter "b" (beta) into ".0.nuber_from_beta" (.0.<n> here)
IPS_component_version: $( echo %{version} | gsed -e 's/\([0-9]*\.[0-9]*\)$/\1.0.1.0/' -e 's/\([0-9]\)b\(.*\)/\1.0.0.\2/' -e 's/\.0*\([0-9]\)/.\1/g' )

# (echo "3.3b3"; echo 3.3.2) | sed -e 's,\(.*[0-9]*\.[0-9]*\)$,version \1,'   -e 's,\(.*[0-9]\)b\(.*\),version \1 (beta \2),'
#%define download_version_string %( echo %{version} | sed -e 's,\(.*[0-9]*\.[0-9]*\)$,version \1,' -e 's,\(.*[0-9]\)b\(.*\),version\x20\1%%\x20\\\x28beta%%\x20\2\\\x29,' )
#%define download_version_string %( echo %{version} | gsed -e 's,\(.*[0-9]*\.[0-9]*\)$,version \1,' -e 's,\(.*[0-9]\)b\(.*\),version \1 (beta \2),' )
#%define dl_version_string_escaped %( echo %{download_version_string} |  gsed -e 's, ,\x2520,g' -e 's,\x28,\x2528,g' -e 's,\x29,\x2528,g' )

%define download_version_string %( echo %{version} | gsed -e 's,\(.*[0-9]*\.[0-9]*\)$,version \1,' -e 's,\(.*[0-9]\)b\(.*\),version:\1:beta:\2,' -e 's,version:,version\x25\x2520,' -e 's,:beta:\(.*[0-9]*\),\x25\x2520\\\x28beta\x25\x2520\1\\\x29,' -e 's, ,\x25\x2520,g' )

#http://netcologne.dl.sourceforge.net/project/jxplorer/jxplorer/version%203.3%20%28beta%203%29/jxplorer-3.3b3-solaris-intel-installer.run
#http://netcologne.dl.sourceforge.net/project/jxplorer/jxplorer/version%203.3%20%28beta%203%29/jxplorer-3.3b3-solaris-intel-installer.run
#Resolving netcologne.dl.sourcef
Source1:                  %{sf_download}/project/jxplorer/jxplorer/%{download_version_string}/jxplorer-%{version}-solaris-%{platform}-installer.run
#Source1:                  %{sf_download}/project/jxplorer/jxplorer/%{dl_version_string_escaped}/jxplorer-%{version}-solaris-%{platform}-installer.run


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build


%include default-depend.inc

%description
Java based LDAP Editor


%prep
%setup -c -T -n %{src_name}-%version
cp -p %{SOURCE1} .
chmod +x `basename ./%{SOURCE1}`


%build
#nothing to do

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p             $RPM_BUILD_ROOT%{_libdir}/%{subdir}/

./`basename %{SOURCE1}` --prefix $RPM_BUILD_ROOT%{_libdir}/%{subdir}/ << --EOF---





y


n

--EOF---


%if %{SXCE}
gsed -i -e 's,#! */bin/sh,#! /bin/bash,' $RPM_BUILD_ROOT%{_libdir}/%{subdir}/jxplorer.sh
%endif

gsed -i -e 's?-cp "\.:jars/\*:jasper/lib/\*"?-cp "%{_libdir}/%{subdir}/jars/*"?' $RPM_BUILD_ROOT%{_libdir}/%{subdir}/jxplorer.sh

mkdir -p $RPM_BUILD_ROOT%{_bindir}/
#ln -s $RPM_BUILD_ROOT%{_libdir}/%{subdir}/%{src_name}.sh ../bin/%{src_name}
ln -s ../lib/%{subdir}/%{src_name}.sh $RPM_BUILD_ROOT%{_bindir}/%{src_name} 

gsed -i -e 's?'$RPM_BUILD_ROOT'??' $RPM_BUILD_ROOT%{_libdir}/%{subdir}/*desktop

#ln -s $RPM_BUILD_ROOT%{_libdir}/%{subdir}/*desktop 
#../packages/PKGS/SFEjxplorer/reloc/lib/jxplorer/JXplorer.desktop /var/tmp/pkgbuild-tom/SFEjxplorer-3.3.02-build

# ... and desktop menu
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_libdir}/%{subdir}/JXplorer.desktop


#workaround pkgbuild/pkgtool not taking spaces in filenames:
mv "$RPM_BUILD_ROOT%{_libdir}/%{subdir}/Uninstall JXplorer.desktop" "$RPM_BUILD_ROOT%{_libdir}/%{subdir}/Uninstall_JXplorer.desktop"

%post
%restart_fmri desktop-mime-cache

%postun
%restart_fmri desktop-mime-cache


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}/%{subdir}/
%{_libdir}/%{subdir}/*
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
#%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*


%changelog
* Fri Jan 25 2013 - Thomas Wagner
- bump to 3.3.02 (IPS 3.3.2.0.1.0)
- include %isdistro.inc, for older OS edit /bin/sh -> /bin/bash
* Sat May 19 2012 - Thomas Wagner
- bump to 3.3b3  (IPS 3.3.0.0.2)
* Sat Oct  8 2011 - Thomas Wagner
- Initial spec
