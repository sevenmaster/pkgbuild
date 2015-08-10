##TODO##
##TODO## Import scripts
##TODO##
##TODO##
##TODO##





#
# spec file for package SFEmediatomb
#
# includes module(s): mediatomb
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%include packagenamemacros.inc

%define _use_internal_dependency_generator 0

#http://slackbuilds.org/uid_gid.txt would say 241:241
%define  daemonuser  mediatomb
%define  daemonuid   65583
%define  daemongcosfield mediatomb Reserved UID

##TODO## check if this should be nogroup or nobody group
##TODO## make this configurable at compile time with --define 'daemongroup nogroup' --define 'daemongid 65534'
#if you change the number, then you change as well the text and the group will be created, else nogroup with 65534 is used
#nogroup = 65534
%define  daemongroup nogroup
%define  daemongid   65534

#config file can be centrally located
#default would be to look for $HOME/.mediatomb/config.xml
#for initial user experience, #we deliver a default 
#confi file in /etc/mediatomb/config.xml
#and create a cache / database directory in /var/mediatomb
#with write permissions for %{daemonuser} %{daemongroup}
%define	 configfile /etc/mediatomb/config.xml

%define	src_name mediatomb

Name:                SFEmediatomb
IPS_Package_Name:    media/mediatomb
Summary:             UPnP AV MediaServer
Version:             0.12.1
URL:                 http://mediatomb.cc
Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Source2:             mediatomb.xml
Patch1:              mediatomb-01-0.12.1-gcc46.patch.diff
Patch2:              mediatomb-02-libav_0.7_support.patch.diff
Patch3:              mediatomb-03-AVMetadataTag_not_defined.diff
Patch4:              mediatomb-04-have-gnu-libiconv-remove-cast-const-char.diff
Patch5:              mediatomb-05-remove-solaris-check-nullpointer-to-prtinf.diff
Patch6:              mediatomb-06-libmp4v2_191_p479.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
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
BuildRequires:     SFElibmp4v2
Requires:          SFElibmp4v2

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
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#paused export PATH=/usr/gnu/bin:$PATH
export CC=gcc
export CXX=g++
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags} -fpermissive"
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
            --with-taglib-cfg=/usr/g++/bin/taglib-config \
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

%if %( expr %{daemongid} '!=' 65534 )
# <method_credential user="mediatomb" group="nogroup"/>
gsed -i -e '/method_credential user=/ s?mediatomb?%{daemonuser}?g'  \
        -e '/method_credential .*group=/ s?nogroup?%{daemongroup}?g'  \
        %{SOURCE2}
%endif

#with write permissions for %{daemonuser} %{daemongroup}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT


#IPS
%actions 
user ftpuser=false gcos-field="%{daemongcosfield}" username="%{daemonuser}" uid=%{daemonuid} password=NP group="%{daemongroup}"
%if %( expr %{daemongid} '!=' 65534 )
#not needed _if_ group is nogroup  (65534)
group groupname="%{daemongroup}" gid="%{daemongid}"
%endif


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/mediatomb
#%class config
#%volatile ...
%{_localstatedir}/%{src_name}

%changelog
* Wed Mar  4 2015 - Thomas Wagner
- remove (Build)Requires SUNWlibexif (use pnm_requires_image_library_libexif)
* Sat Feb 15 2015 - Thomas Wagner
- add SMF manifest mediatomb.xml
- add userid/groupid
* Fri Feb  6 2015 - Thomas Wagner
- taglib not found, use --with-taglib-cfg=path (S12, ..)
* Thu Feb  5 2015 - Thomas Wagner
- add -fpermissive (S12/gcc-4.8.4)
- add patch6 mediatomb-06-libmp4v2_191_p479.diff
* Fri Jan  9 2015 - Thomas Wagner
- switch off pkgdepend. doesn't to the right thing: find the other taglib package and add false dependencies
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

