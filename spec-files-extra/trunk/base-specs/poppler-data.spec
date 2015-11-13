#
#
Name:         poppler-data
License:      GPL
Group:        System/Libraries
Version:      0.4.7
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
Summary:      poppler-data - supporting library for poppler, the PDF Rendering Library
URL:          http://poppler.freedesktop.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}

BuildRequires: SFEpoppler-gpp
Requires:      SFEpoppler-gpp


%description
poppler-data is used by poppler, the PDF rendering library based on xpdf-3.0


%prep
#don't unpack please
%setup -q -c -T
echo %SOURCE0 | grep "gz$" && gzip -d < %SOURCE0 | (cd ..; tar xf -)


%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

gmake V=2 datadir=%{_datadir} prefix=%{_prefix}

cat poppler-data.pc

%install
gmake V=2 DESTDIR=$RPM_BUILD_ROOT datadir=%{_datadir} prefix=%{_prefix} install

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Thu Nov  5 2015 - Thomas Wagner
- initial spec
