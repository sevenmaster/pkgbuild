
Name:                autogen
Summary:             Templatized program/text generation system
URL:                 http://autogen.sourceforge.net/
#Version:             5.16.2
Version:             5.16.2
#beware of IPS once sub-micro version is removed, IPS would not upgrade if simply removed
#needs guile 2.x Version:             5.18.5.029
IPS_Component_Version: %( echo %{version} | sed -e 's?\.0*?.?g' )
#5.16.2 comes from SF
#https://sourceforge.net/projects/autogen/files/AutoGen/AutoGen-5.16.2/autogen-5.16.2.tar.xz/download
Source:              http://sourceforge.net/projects/autogen/files/AutoGen/AutoGen-%{version}/autogen-%{version}.tar.xz
#Source:              %{sf_download}/autogen/autogen-%{version}.tar.bz2
#5.18.5.029 come from other URL
#Source:              http://autogen.sourceforge.net/data/autogen-%{version}.tar.xz
Source2:             guile-config_remove_compiler_defines_pthreads
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build


%prep
#don't unpack please
%setup -q -c -T -n autogen-%version

xz -dc %SOURCE0 | (cd ..; tar xf -)

mkdir bin
cp %{SOURCE2} bin/guile-config
chmod 0755 bin/guile-config

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

#run our guild-config to remove -pthreads and -D.... from the "guile-config link" output
#or get LD complaining about "hreads" not a valid option
export PATH=`pwd`/bin:$PATH

export CFLAGS="%optflags -I/usr/include/gmp"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --bindir=%{_bindir}  \
            --libdir=%{_libdir}  \
            --libexecdir=%{_libexecdir}  \
            --mandir=%{_mandir}    \
            --datadir=%{_datadir}  \
            --infodir=%{_datadir}/info  \
            --enable-static=no

gmake -j$CPUS

%install
#rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
[ -d ${RPM_BUILD_ROOT}%{_datadir}/info/dir ] && rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir

#/usr/share/pkgconfig/autoopts.pc
mv ${RPM_BUILD_ROOT}%{_datadir}/pkgconfig ${RPM_BUILD_ROOT}%{_libdir}/


%clean
rm -rf $RPM_BUILD_ROOT



%changelog
* Sun Jul 31 2016 - Thomas Wagner
- check if infodir exists before trying to delete it (OM)
* Tue May 24 2016 - Thomas Wagner
- go back to version 5.16.2
- fix build with wrapper around guile-config (remove -pthreads)
* Thu Apr 14 2016 - Thomas Wagner
- set IPS_Package_Name to sfe/developer/build/autogen to escape the consolidation/userland/userland-incorporation version-dictatroship
- make spec 32/64-bit
* Wed Apr 13 2016 - Thomas Wagner
- bump to 5.18.5.029 (beware of IPS once sub-micro version is removed, IPS would not upgrade then)
* Sun Jan 18 2009 - halton.huo@sun.com
- Bump to 5.9.7
* Wed Aug 20 2008 - nonsea@users.sourceforge.net
- Bump to 5.9.5
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Bump to 5.9.4
* Mon Sep 10 2007 - nonsea@users.sourceforge.net
- Bump to 5.9.2
* Sun May 13 2007 - nonsea@users.sourceforge.net
- Bump to 5.9.1
* Thu Mar 22 2007 - nonsea@users.sourceforge.net
- Bump to 5.9
- Add Requires/BuildRequries after check-deps.pl run.
* Tue Mar 20 2007 - daymobrew@users.sourceforge.net
- Use single thread make so as not to break build.
* Mon Jan 15 2007 - daymobrew@users.sourceforge.net
- Add SUNWtexi dependency. Add %post/%preun to update the info dir file.
* Wed Dec 20 2006 - Eric Boutilier
- Initial spec
