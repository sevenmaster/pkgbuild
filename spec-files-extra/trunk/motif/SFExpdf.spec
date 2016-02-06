#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define src_version	3.04

Name:		SFExpdf
IPS_Package_Name:	desktop/motif/pdf-viewer/xpdf
Summary:	X PDF document viewer
Group:		X11/Applications
Version:	3.4
Source:		ftp://ftp.foolabs.com/pub/xpdf/xpdf-%{src_version}.tar.gz
URL:		http://foolabs.com/xpdf/
License:	GPLv2+
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %{name}-root
BuildRequires: library/motif

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/


%prep
%setup -q -n xpdf-%src_version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir}	\
	--with-freetype2-includes=/usr/include/freetype2	\
	--enable-a4-paper	\
	--enable-cmyk		\
	--enable-opi		\
	--enable-wordlist

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
cd %buildroot%_bindir
# These files are delivered by desktop/pdf-viewer/evince
rm pdffonts  pdfimages  pdfinfo  pdftoppm  pdftops  pdftotext

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%attr (-, root, bin) %{_sysconfdir}/xpdfrc

%changelog
* Wed Dec 16 2015 - Alex Viskovatoff
- bump to 3.4; do not deliver executables supplied by desktop/pdf-viewer/evince
* Sat Oct 29 2011 - Milan Jurik
- Initial spec
