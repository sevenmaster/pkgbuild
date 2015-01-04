#
# spec file for package SFEmediatomb
#
# includes module(s): mediatomb
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

%define	src_name mediatomb

Name:                SFEmediatomb
IPS_Package_Name:    media/mediatomb
Summary:             UPnP AV MediaServer
Version:             0.12.1
URL:                 http://mediatomb.cc
Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Patch1:              mediatomb-01-0.12.1-gcc46.patch.diff
Patch2:              mediatomb-02-libav_0.7_support.patch.diff
Patch3:              mediatomb-03-AVMetadataTag_not_defined.diff
Patch4:              mediatomb-04-have-gnu-libiconv-remove-cast-const-char.diff
Patch5:              mediatomb-05-remove-solaris-check-nullpointer-to-prtinf.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:     SUNWlibexif-devel
Requires:          SUNWlibexif
BuildRequires:     SFEtaglib-gpp-devel
Requires:          SFEtaglib-gpp
BuildRequires:     %{pnm_buildrequires_SUNWsqlite3}
Requires:          %{pnm_requires_SUNWsqlite3}
#get fresh file type assignments/detection
BuildRequires:     SFEfile
Requires:          SFEfile
BuildRequires:     %{pnm_buildrequires_image_library_libexif}
Requires:          %{pnm_requires_image_library_libexif}
BuildRequires:     %{pnm_buildrequires_SUNWcurl}
Requires:          %{pnm_requires_SUNWcurl}
BuildRequires:     SFEspidermonkey
Requires:          SFEspidermonkey

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

# Fix build error with GCC 4.6 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#paused export PATH=/usr/gnu/bin:$PATH
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export CPPFLAGS="-I/usr/g++/include -I/usr/gnu/include"
export LDFLAGS="%{_ldflags}  -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib -liconv"

##TODO## "file" passenden Pfad hier angeben, damit neue Version benutzt wird
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_includedir} \
            --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
            --enable-taglib             \
            --with-taglib-h=/usr/g++/include   \
            --with-taglib-libs=/usr/g++/lib    \
            --disable-id3lib            \
            --enable-curl               \
            --with-libmagic-h=/usr/gnu/include \
            --with-libmagic-libs=/usr/gnu/lib  \

            #--with-id3lib-h=/usr/g++/include   \
            #--with-id3lib-libs=/usr/g++/lib    \

gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/mediatomb

%changelog
* Thu Jan  1 2015 - Thomas Wagner
- bump to 0.12.1, use standard sf_download -URL
- add patch1 patch2 patch3 patch4 for 0.12.1, remove solaris check with patch5
  (older Solaris would need LDFLAGS="/usr/lib/0@0.so.1 ...")
- change (Build)Requires to %{pnm_buildrequires_SUNWsqlite3}, libexif, %include packagenamemacros.inc
- change (Build)Requires SFElibmagic to SFEfile in /usr/gnu/
- add SFEspidermonkey, enable/add SUNWcurl
- use SFEtaglib-gnu and remove SFEid3lib-gnu
- officially use gcc, add IPS_Package_Name, standardize CFLAGS/CXXFLAGS/LDFLAGS
* Tue Jul 17 2007 - dougs@truemail.co.th
- Initial spec

