#
# spec file for package SFEre2c
#

%include Solaris.inc
%include packagenamemacros.inc
%define cc_is_gcc 1
%define _gpp g++
%include base.inc

Name:		SFEre2c
IPS_Package_Name:	developer/lexer/re2c
Summary:	A tool for writing very fast and very flexible scanners
Group:		Development/Other Languages
URL:		http://re2c.org/
Version:	0.13.5
Source:		%{sf_download}/re2c/re2c-%{version}.tar.gz

SUNW_Copyright:		 re2c.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires: SFEgcc
Requires:      SFEgccruntime

%include default-depend.inc

%prep
%setup -q -n re2c-%version

%build

export CC=gcc
export CXX=g++
export CFLAGS="%optflags -I%{gnu_inc} %{gnu_lib_path}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc} %{gnu_lib_path}"
export LDFLAGS="%_ldflags %gnu_lib_path"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


gmake

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT
#in case old pkgbuild does not automaticly place %doc files there
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README CHANGELOG
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Mon Jan  7 2013 - TAKI,Yasushi <taki@justplayer.com>
- revert about using gcc-45 when Solaris 11
* Sun Jan  6 2013 - TAKI,Yasushi <taki@justplayer.com>
- merge jposug fork version.
- When using Solaris 11, use gcc-45.
* Wed Jun 13 2012 - Osamu Tabata <cantimerny.g@gmail.com>
- Support for Solaris11
* Mon Jul 25 2011 - N.B.Prashanth
- Add SUNW_Copyright
* Thr Aug 06 2009  - Thomas Wagner
- switch to gcc4 - sunstudio spits "parser.y", line 98: Error: Cannot cast from std::pair<unsigned, re2c::RuleOp*> to std::pair<int, re2c::RegExp*>.
- spamassassin now works with re2c (old re2c version did hang forever)
* Sat Mar 12 2009  - Thomas Wagner
- bump to 0.13.5
* Sat May 12 2007  - Thomas Wagner
- Initial spec
