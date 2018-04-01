
%include Solaris.inc

Name:                SFEpdftk
IPS_package_name:    image/pdftk
Summary:             manipulating PDF on the command line (merge, split, watermark, ...)
License:             GPLv2
SUNW_Copyright:	     %{license}.copyright
Version:             2.02
IPS_component_version: 2.2
URL:                 http://www.pdflabs.com
Source:		     https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/pdftk-%{version}-src.zip
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#currently needs gcc 4.9 with gcj / ecj
#mind updating >4.9< in variables in %build
BuildRequires:	SFEgcc-49
Requires:	SFEgccruntime-49

%prep
%setup -q -n pdftk-%{version}-dist


%build

CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"


cd pdftk
#gmake V=2 -j$CPUS -f Makefile.Solaris TOOLPATH=/usr/gcc-sfe/4.9/bin CXXFLAGS="-Wall -Wextra -O2 -std=c++11 -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/gcc-sfe/4.9/lib -R/usr/gcc-sfe/4.9/lib" LDLIBS= -lgcj -lsocket -L/usr/gnu/lib -R/usr/gnu/lib -liconv
#run twice, might be a dependency problem. Second run succeeds.
gmake V=2 -j$CPUS -f Makefile.Solaris CXXFLAGS="-Wall -Wextra -O2 -std=c++11 -L/usr/gnu/lib -R/usr/gnu/lib" LIBGCJ="/usr/gcc-sfe/4.9/lib/libgcj.so:/usr/gcc-sfe/lib/libgcj.so" \
   || gmake V=2 -j$CPUS -f Makefile.Solaris CXXFLAGS="-Wall -Wextra -O2 -std=c++11 -L/usr/gnu/lib -R/usr/gnu/lib" LIBGCJ="/usr/gcc-sfe/4.9/lib/libgcj.so:/usr/gcc-sfe/lib/libgcj.so" \
 

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/pdftk

ginstall -m755 pdftk/pdftk ${RPM_BUILD_ROOT}%{_bindir}
ginstall -m644 pdftk.1 ${RPM_BUILD_ROOT}%{_mandir}/man1
ginstall -m644 pdftk.1.txt ${RPM_BUILD_ROOT}%{_docdir}/pdftk
ginstall -m644 pdftk.1.html ${RPM_BUILD_ROOT}%{_docdir}/pdftk

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pdftk
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/pdftk
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*


%changelog
* Sun Apr  1 2018 - Thomas Wagner
- initial version 2.02 (2.2)
- fix %files
