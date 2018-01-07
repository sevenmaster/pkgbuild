##TODO## copy experimental/make_perl_cpan_settings.pl and make a generator for python modules - any volunteers please?
## :4,$ s/@@PACKAGENAME@@/_place_name_here_/gc
## :5,$ s/@@VERSION@@/_1.2.3.4_/gc
## /##FILLIN##


#
# spec file for package SFEpython27-feedgenerator
#
# includes module(s): feedgenerator
#
%include Solaris.inc
%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#below:
##TODO##                   record open tasks or invesitgations here


#https://github.com/getpelican/feedgenerator/commit/6582cd4bb3949aad2d1aa7d96c2c90c1ba9cf954
%define commit 6582cd4bb3949aad2d1aa7d96c2c90c1ba9cf954
#remember to increast the counter below for every update of %{commit}!
%define increment_version_helper 1
#e.g. cb721f0
%define shortcommit %(c=%{commit}; echo ${c:0:7})
%define src_name        feedgenerator
%define githubowner1    getpelican
%define githubproject1  %{src_name}
%define versiontag 	1.7.0.0
#put additional digits to the version to have a change to get packages updated with new git commit versions
#increase first the last number, in case you need to roll back, only then increase the second last and reset the last digit
#new         pervious version
#upgrade:
#1.7.0.0.0 -->> 1.7.0.0.1   
#rollback, downgrade example (rolled back to older git commit)
#               1.7.0.0.1 -->> 1.7.0.1.0 
#again, now a fresh upgrade
#                              1.7.0.1.0 > 1.7.0.1.1 

%define     targetdirname feedgenerator
#set to blank if not text part like ".RC2" is in the version string. IPS can't handle non-numeric version strings


Name:                    SFEpython27-feedgenerator
IPS_Package_Name:	 library/python/feedgenerator-27
Summary:		Standalone version of django.utils.feedgenerator
URL:                     https://github.com/getpelican/feedgenerator
Version:                 %{versiontag}.%{increment_version_helper}
                        #https://github.com/getpelican/feedgenerator/archive/6582cd4bb3949aad2d1aa7d96c2c90c1ba9cf954.zip ? and add readable and verison_ed filename
Source:                  http://github.com/%{githubowner1}/%{githubproject1}/archive/%{commit}.zip?%{src_name}-%{version}-%{shortcommit}.zip
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
#License: BSD
License:		Django

%include default-depend.inc
BuildRequires:           runtime/python-27
Requires:                runtime/python-27

%define python_version  2.7


%package -n SFEpython-feedgenerator
IPS_Package_Name:	 library/python/feedgenerator
Summary:                 %{summary}
Requires:	         SFEpython27-feedgenerator

%description
feedgenerator ##FILLIN##

%prep
%setup -q -n %{githubproject1}-%{commit}

#%if %{omnios}
#gsed -e '/std=c99/ s/^/#/' < setup.py
#%endif

%build
%if %( expr %{solaris11} '=' 1 '|' %{solaris12} '=' 1 )
export CC=cc
%else
export CC=gcc
%endif

%if %( /usr/bin/python%{python_version}-config --cflags  | grep -- -m64 >/dev/null && echo 1 || echo 0 )
BITS=64
export CFLAGS="-m64 -I%{gnu_inc}"
export LDFLAGS="-L%{gnu_lib}/%{_arch64} -R%{gnu_lib}/%{_arch64}"
export PYTHON_BINARY_OFFSET="/usr/bin/%{_arch64}"
%else
BITS=32
export CFLAGS="-I%{gnu_inc}"
export LDFLAGS="-L%{gnu_lib} -R%{gnu_lib}"
export PYTHON_BINARY_OFFSET="/usr/bin"
%endif
echo "compiling for ${BITS}-bit python!"


${PYTHON_BINARY_OFFSET}/python%{python_version} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
python%{python_version} setup.py install --root=$RPM_BUILD_ROOT --prefix=%{_prefix} --no-compile

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{python_version}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
#%dir %attr (0755, root, bin) %{_bindir}
#%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{python_version}


%changelog
* Sun Jan  7 2018 - Thomas Wagner
- reworked, change to github source commit 
* Tue Jan 13 2015 - Ian Johnson <ianj@tsundoku.ne.jp>
- Initial spec 1.7

