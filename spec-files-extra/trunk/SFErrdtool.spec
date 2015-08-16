#
# spec file for package SFErrdtool
#

#TODO# python might love a subdirectory "rrdtool" under site-packages:  lib/python2.4/site-packages/rrdtoolmodule.so

##TODO## 32-/64-bit Version might have different binary database file contents - check and build both
#maybe a mediator could switch 32/64-bit modes?


%include Solaris.inc
%include usr-gnu.inc
%include base.inc

%include packagenamemacros.inc

%define src_name rrdtool

%define _std_prefix %{_basedir}

#below compare with perl-modules SFEperl-*
##TODO##%define perl_version 5.8.4

##TODO##%ifarch sparc
##TODO##%define perl_dir sun4-solaris-64int
##TODO##%else
##TODO##%define perl_dir i86pc-solaris-64int 
##TODO##%endif

##TODO##%define SUNWruby18u    %(/usr/bin/pkginfo -q SUNWruby18u && echo 1 || echo 0)
##TODO##%define SUNWPython     %(/usr/bin/pkginfo -q SUNWPython && echo 1 || echo 0)



Name:                    SFErrdtool-gnu
IPS_Package_Name:	 image/gnu/rrdtool
Summary:                 rrdtool - data logging and graphing system for time series data. (/usr/gnu)
URL:                     http://oss.oetiker.ch/rrdtool/
Version:                 1.4.8
##TODO##License:		
Source:                  http://oss.oetiker.ch/rrdtool/pub/rrdtool-%{version}.tar.gz

##TODO##PATCHFILES += 0002-Always-link-local-libs-first-during-Perl-module.patch
# Make sure to link against libperl.so to make shared libraries self-contained.
##TODO##PATCHFILES += 0003-Always-link-against-libperl.so.patch
# Do not pass LDFLAGS during pysetup or -L/opt/csw/lib will appear too early during
# linking which results in the system installed librrd.so is linked against instead
# of the newly build one
##TODO##PATCHFILES += 0004-Do-not-pass-LDFLAGS-to-pysetup-or-the-system-lib-is-.patch



SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

BuildRequires:	%{pnm_buildrequires_perl_default}
Requires:	%{pnm_requires_perl_default}
##TODO##     Libraries: -lxml2 -lglib-2.0 -lcairo -lcairo -lcairo -lm  -lsocket -lcairo -lpng12   -lpangocairo-1.0 -lpango-1.0 -lcairo -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lpthread -lglib-2.0

##TODO###use if they are installed
##TODO###ruby
##TODO##%if %SUNWruby18u
##TODO##BuildRequires: SUNWruby18u
##TODO###user decides at runtime
##TODO###Requires: SUNWruby18u
##TODO##%else
##TODO##%endif

##TODO###python 2.4 (or what rrdtool delivers)
##TODO##%if %SUNWPython
##TODO##BuildRequires: SUNWPython-devel
##TODO##Requires: SUNWPython-devel
##TODO###user decides at runtime
##TODO###Requires: SUNWPython
##TODO##%else
##TODO##%endif

##TODO###want perl modules, right.
##TODO##Requires:                SUNWperl584core
##TODO##BuildRequires:           SUNWperl584core

##TODO###bug and lacks perl modules (, ruby, python too)
##TODO##Conflicts: SUNWrrdtool

%include default-depend.inc

%include perl-depend.inc


%prep
%setup -q -n rrdtool-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi


./configure --prefix=%{_prefix}  \
	    --bindir=%{_bindir}  \
            --mandir=%{_mandir}  \
            --libdir=%{_libdir}/%{src_name} \
            --datadir=%{_datadir}	    \
            --libexecdir=%{_libdir}/%{src_name}/bin \
            --sysconfdir=%{_sysconfdir}/%{src_name} \
            --with-perl-options="
    LIB=$RPM_BUILD_ROOT%{_std_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITELIB=$RPM_BUILD_ROOT%{_std_prefix}/%{perl_path_vendor_perl_version} \
    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_std_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_std_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
   INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
" \
            --disable-static


#    LIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
#    INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version} \
#    INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
#    INSTALLARCHLIB=$RPM_BUILD_ROOT%{_prefix}/%{perl_path_vendor_perl_version}/%{perl_dir} \
#    INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
#    INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 \
#    INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 \
#    INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3

#result:
##note##Config is DONE!
##note##
##note##          With MMAP IO: yes
##note##      Build rrd_getopt: no
##note##       Build rrd_graph: yes
##note##       Static programs: no
##note##          Perl Modules: perl_piped perl_shared
##note##           Perl Binary: /usr/bin/perl
##note##          Perl Version: 5.12.5
##note##          Perl Options:
##note##    LIB=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/perl5/vendor_perl/5.12     INSTALLSITELIB=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/perl5/vendor_perl/5.12     INSTALLSITEARCH=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/perl5/vendor_perl/5.12/i86pc-solaris-64int     INSTALLARCHLIB=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/perl5/vendor_perl/5.12/i86pc-solaris-64int     INSTALLSITEMAN1DIR=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/gnu/share/man/man1     INSTALLSITEMAN3DIR=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/gnu/share/man/man3     INSTALLMAN1DIR=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/gnu/share/man/man1    INSTALLMAN3DIR=/var/tmp/pkgbuild-tom/SFErrdtool-1.4.8-build/usr/gnu/share/man/man3
##note##          Ruby Modules:
##note##           Ruby Binary: no
##note##          Ruby Options: sitedir=/usr/gnu/lib/ruby
##note##    Build Lua Bindings: yes
##note##            Lua Binary: /usr/bin/lua
##note##           Lua Version: 5.1.4
##note##     Lua C-modules dir: /usr/gnu/lib/lua/5.1
##note##    Build Tcl Bindings: yes
##note## Build Python Bindings: yes
##note##          Build rrdcgi: yes
##note##       Build librrd MT: yes
##note##           Use gettext: yes
##note##           With libDBI: no
##note##          With libwrap: no
##note##
##note##             Libraries: -lxml2 -lglib-2.0 -lcairo -lcairo -lcairo -lm  -lsocket -lcairo -lpng12   -lpangocairo-1.0 -lpango-1.0 -lcairo -lgobject-2.0 -lgmodule-2.0 -lgthread-2.0 -lpthread -lglib-2.0
##note##
##note##Type 'make' to compile the software and use 'make install' to
##note##install everything to: /usr/gnu.
##note##

gmake -j$CPUS CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC || echo "try again!"
gmake -j$CPUS CC=$CC CCCDLFLAGS="%picflags" OPTIMIZE="%optflags" LD=$CC 


            #--with-perl-options="PREFIX=$RPM_BUILD_ROOT%{_prefix} INSTALLSITELIB=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version} INSTALLSITEARCH=$RPM_BUILD_ROOT%{_prefix}/perl5/vendor_perl/%{perl_version}/%{perl_dir} INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3 INSTALLMAN1DIR=$RPM_BUILD_ROOT%{_mandir}/man1 INSTALLMAN3DIR=$RPM_BUILD_ROOT%{_mandir}/man3" \

##make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT%{_std_prefix}/perl5/site_perl $RPM_BUILD_ROOT%{_std_prefix}/perl5/vendor_perl

find $RPM_BUILD_ROOT -name .packlist -exec %{__rm} {} \; -o -name perllocal.pod  -exec %{__rm} {} \;

rm -r $RPM_BUILD_ROOT%{_std_prefix}/perl%{perl_major_version}/%{perl_version}/lib

##TODO###in case old pkgbuild does not automaticly place %doc files there
##TODO##test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc README COPYING NEWS TODO THREADS
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
#%dir %attr(0755, root, bin) %{_prefix}/perl5
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl
#%dir %attr(0755, root, bin) %{_prefix}/perl5/vendor_perl/%{perl_version}
#%{_prefix}/perl5/vendor_perl/%{perl_version}/*
%dir %attr(0755, root, bin) %{_std_prefix}/perl5
%dir %attr(0755, root, bin) %{_std_prefix}/perl5/vendor_perl
%dir %attr(0755, root, bin) %{_std_prefix}/perl5/vendor_perl/%{perl_version}
%{_std_prefix}/perl5/vendor_perl/%{perl_version}/*

%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/*
#%{_libdir}/%{src_name}/*

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}/*
#%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}-%{version}/*
#%{_docdir}/%{name}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
#extra man directory for perl manpages 
%dir %attr(0755, root, bin) %{_std_prefix}/perl%{perl_major_version}/%{perl_version}
%dir %attr(0755, root, bin) %{_std_prefix}/perl%{perl_major_version}/%{perl_version}/man
%dir %attr(0755, root, bin) %{_std_prefix}/perl%{perl_major_version}/%{perl_version}/man/man3
%{_std_prefix}/perl%{perl_major_version}/%{perl_version}/man/man3/*


%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*



%changelog
* Sun Aug 16 2015 - Thomas Wagner
- fix order %include usr-g.*inc base.inc
* Thu Jun  5 2014 - Thomas Wagner
- bump to 1.4.8, rework spec file to meet new style
- relocate to /usr/gnu to co-exist with OS provided rrdtool (which misses RRDs.pm)
* Mon May 24 2010 - Milan Jurik
- bump to 1.4.3
* Thr Feb 27 2009  - Thomas Wagner
- Initial spec version 1.3.6
- include Perl-Support to "use RRDs/RRDp", ruby, python support
