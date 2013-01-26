# 
# spec file for package LibreOffice 
# 
# by Ken Mays
#
# LibreOffice is the free power-packed open source cross-platform personal
# productivity suite that gives you six feature-rich applications for
# all your document production and data processing needs:
# Writer, Calc, Impress, Draw, Math and Base.
# 

#%define src_name libreoffice
#%define src_url http://download.documentfoundation.org/libreoffice/src/
#%define         piece             base 

Name:           SFElibreoffice
Version:        4.0.0.2
Summary:        Full integrated office productivity suite
URL:            http://www.libreoffice.org
Source:         http://download.documentfoundation.org/libreoffice/src/4.0.0/libreoffice-%{version}.tar.xz
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

# Note: Requires compress/zip >= 3.0
# Note: Requires perl Archive::Zip::Archive 

Requires:  SFEhunspell
Requires:  SUNWperl-xml-parser
Requires:  SUNWdoxygen
Requires:  SUNWhea
Requires:  %{pnm_buildrequires_SFExz_gnu}
Requires:  SUNWgnu-gperf  
Requires:  SUNWbison
Requires:  SUNWflexlex
Requires:  SUNWant

%description
LibreOffice is the free power-packed Open Source cross-platform personal
productivity suite for that gives you six feature-rich applications for
all your document production and data processing needs:
Writer, Calc, Impress, Draw, Math and Base.

%prep
tar xJf %{SOURCE} 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export JAVA_HOME="/usr/java"
export CC="/usr/bin/gcc"
export CXX="/usr/bin/g++"
export CFLAGS="-g -Os -pipe -fopenmp -fno-omit-frame-pointer -I/usr/include -I%{xorg_inc} -I%{gnu_inc} -I%{sfw_inc} -Xlinker -i"
export LDFLAGS="-L/lib -R/lib -L/usr/lib -R/usr/lib %{xorg_lib_path} %{gnu_lib_path} %{sfw_lib_path}"
export LD=/usr/ccs/bin/ld

./configure \
	--without-junit \
	--with-system-curl \
 	--without-help \
 	--disable-cups \
 	--without-java \
 	--with-system-cairo \
 	--with-lang= \
 	--disable-gconf \
 	--enable-gio \
 	--disable-gnome-vfs \
 	--disable-gstreamer \
 	--without-fonts \
 	--with-system-dicts \
 	--disable-mozilla \
 	--without-system-mozilla \
 	--with-system-openssl


make -j$CPUS
  
%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
  
%files
%defattr (-, root, bin)
%_libdir/libreoffice
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_docdir
%_docdir
%_mandir
  
%changelog
* Sat Jan 26 2013 - Ken Mays <kmays2000@gmail.com>
- Initial spec 

