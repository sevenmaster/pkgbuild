##TODO##
##TODO## Import scripts
##TODO##
##TODO## doesn't recognize HOME-dir, so SMF startup fails
##TODO##

##TODO## wrapper script to run "newtask -p mediatomb" and then run mediatomb
##TODO## resource control, choose the number of shared it should get
##TODO## cat /etc/project 
##TODO## mediatomb:1003:mediatomb with trancoding:mediatomb::project.cpu-shares=(privileged,200,none)
##TODO##
 
#CONFIGURATION SUMMARY ----
#
#sqlite3               : yes
#mysql                 : missing
#libjs                 : yes
#libmagic              : yes
#inotify               : missing
#libexif               : yes
#id3lib                : disabled
#taglib                : yes
#FLAC                  : yes
#libmp4v2              : yes
#ffmpeg                : yes
#ffmpegthumbnailer     : missing
#lastfmlib             : missing
#external transcoding  : yes
#curl                  : yes
#YouTube               : yes
#libextractor          : disabled
#db-autocreate         : yes

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
Summary:             UPnP AV MediaServer / DLNA Server / transcoding
Version:             0.12.1
URL:                 http://mediatomb.cc
Source:              %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
Source2:             mediatomb.xml
Source3:             mediatomb.sh
Patch1:              mediatomb-01-0.12.1-gcc46.patch.diff
Patch2:              mediatomb-02-libav_0.7_support.patch.diff
Patch3:              mediatomb-03-AVMetadataTag_not_defined.diff
Patch4:              mediatomb-04-have-gnu-libiconv-remove-cast-const-char.diff
Patch5:              mediatomb-05-remove-solaris-check-nullpointer-to-prtinf.diff
Patch6:              mediatomb-06-libmp4v2_191_p479.diff
#imported from http://pkgs.fedoraproject.org/cgit/mediatomb.git/plain
Patch11:             mediatomb-11-0.12.1.fixogg.patch
Patch12:             mediatomb-12-0.12.1.fixbufferoverrun.patch
#our patch1 Patch13:             mediatomb-13-0.12.1.fixbuild.patch
Patch14:             mediatomb-14-0.12.1.tonewjs.patch
Patch15:             mediatomb-15-0.12.1-jsparse.patch
Patch16:             mediatomb-16-0.12.1.ps3_timeseekrange.patch
Patch17:             mediatomb-17-0.12.1.flacart.patch
Patch18:             mediatomb-18-0.12.1.flacart.config.patch
Patch19:             mediatomb-19-0.12.1.fixyoutube.patch
Patch20:             mediatomb-20-0.12.1-samsung_video_subtitles.patch
Patch21:             mediatomb-21-0.12.1-transcode-segfault.patch


SUNW_BaseDir:        /

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
# flac
# lastfm


%description
This server might open access to your local files if not confiured and firewalled
propperly. Be warned.

AV Media Server
DNLA

can even serve your LAN connected TV set, tables, smartphone.

config file is in in /etc/mediatomb/.mediatomb/config.xml (can be changed in SMF)

svcadm enable mediatomb

make your media-files readable for group "nogroup" or user "mediatomb"
(running userid/group can be changed in SMF, mind chmod -R /etc/mediatomb
as well!)

read the fine online documentation, e.g.:
http://mediatomb.cc/pages/documentation

google "mediatomb transcoding" if you want turning local large files
into small bandwidth streams to the net

on android you may use "UPnPlay" and the like to find your mediatomb server,
play video e.g. with vlc including pause / seek

on the webbrowser configure mediatomb to include the directories you want to serve.

initial results are quick, configuring transcoding is a nightmare but it is the
coolest feature!


%prep
%setup -q -n %{src_name}-%version

# Fix build error with GCC 4.6 
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%patch11 -p1
%patch12 -p1
#our patch1 %patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p0
%patch17 -p0
%patch18 -p1
%patch19 -p1
%patch20 -p0
%patch21 -p0

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
##TODO## temp fix  -L/usr/lib/mps -R/usr/lib/mps
#may go away once spidermonkey libmozjs185.so has the rpath /usr/lib/mps to find libnspr4.so itself
#libmozjs.so -> /usr/lib/mps/libnspr4.so
export LDFLAGS="%{_ldflags}  -L/usr/g++/lib -R/usr/g++/lib -L/usr/gnu/lib -R/usr/gnu/lib -L/usr/lib/mps -R/usr/lib/mps -liconv -lFLAC -lm"

##TODO## "file" - point configure to new sfe file
autoconf -i -f
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
            --with-js-h=/usr/include/js \
            --disable-static            \


#osdistro flac is too old, enable again once g++ compiled new flac is available
            #--enable-FLAC               \
#note: id3lib might not be needed, see mediatomb doc/website
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

##TODO## enhance SMF manifest to know more parameters - enables easy multi-instance setups
mkdir -p ${RPM_BUILD_ROOT}/var/svc/manifest/network/media/
cp -p %{SOURCE2} ${RPM_BUILD_ROOT}/var/svc/manifest/network/media/

#with write permissions for %{daemonuser} %{daemongroup}
mkdir -p $RPM_BUILD_ROOT/%{_localstatedir}/%{src_name}

mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{src_name}
cp -p %{SOURCE3} ${RPM_BUILD_ROOT}/%{_sysconfdir}/%{src_name}/

%clean
rm -rf $RPM_BUILD_ROOT


#IPS
%actions 
user ftpuser=false gcos-field="%{daemongcosfield}" username="%{daemonuser}" uid=%{daemonuid} password=NP group="%{daemongroup}" home-dir="%{_sysconfdir}/%{src_name}" login-shell="/bin/false"
%if %( expr %{daemongid} '!=' 65534 )
#not needed _if_ group is nogroup  (65534)
group groupname="%{daemongroup}" gid="%{daemongid}"
%endif


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0700, %{daemonuser}, %{daemongroup}) %{_sysconfdir}/%{src_name}
%attr (0700, %{daemonuser}, %{daemongroup}) %{_sysconfdir}/%{src_name}/mediatomb.sh
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}
%{_datadir}/mediatomb
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/%{src_name}
%config %attr(0444, root, sys)/var/svc/manifest/network/media/mediatomb.xml

%changelog
* Mon Aug 17 2015 - Thomas Wagner
- import patches 11-21 from fedora, rework patch mediatomb-18-0.12.1.flacart.config.patch
- relocate SMF manifest, add add startup helper script /etc/mediatomb/mediatomb.sh, fix %files
- find spidermonkey headers --with-js-h=/usr/include/js, temp add -L|-R/usr/lib/mps and needs final fix in SFEspidermonkey.spec to find libnspr4.so
* Sun Aug 16 2015 - Thomas Wagner
- copy SMF manifest to /var/svc/manifest/network/media/
- create %{_sysconfdir}/%{src_name}, set user's homedir to this location
  config file is in /etc/mediatomb/.mediatomb/config.xml (can be changed)
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

