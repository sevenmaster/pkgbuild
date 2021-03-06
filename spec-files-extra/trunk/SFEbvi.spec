#
# spec file for package SFEbvi
#

%include Solaris.inc
%include usr-gnu.inc

Name:                    SFEbvi-gnu
IPS_Package_Name:	 sfe/editor/gnu/bvi
Group:			 Development/Editors
Summary:                 bvi - display-oriented editor for binary files (vi like) (/usr/gnu)
URL:			 http://bvi.sourceforge.net/
Version:                 1.4.0
Source:                  %{sf_download}/bvi/bvi-%{version}.src.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
The bvi is a display-oriented editor for binary files, based on the vi 
texteditor. If you are familiar with vi, just start the editor and 
begin to edit! A bmore program is also included in the package.


%prep
%setup -q -n bvi-%version

%build

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc CHANGES COPYING CREDITS README
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr (0755, root, bin) %{_libdir}
#%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/bvi/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Mon Oct 10 2016 - Thomas Wagner
- change IPS_package_name to avoid stupid consolidation/sfw/sfw-incorporation preventing the install
* Tue Feb 16 2016 - Thomas Wagner
- relocate to /usr/gnu, OI is in the way
* Tue Mar  3 2015 - Thomas Wagner
- add IPS_Package_Name, fix %files
* Thr Feb 26 2015 - Thomas Wagner
- bump to 1.4.0
* Sun Jan 25 2009 - Thomas Wagner
- adjust %doc and %files permissions
* Wed Jan 07 2009  - Thomas Wagner
- Initial spec inspired by a tweet from davetong
