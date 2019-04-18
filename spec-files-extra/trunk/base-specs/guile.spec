
Name:                guile
Summary:             Embeddable Scheme implementation written in C
#Version:             5.16.2
#this can be set at compile with, see SFEguile.spec
Version:             %{version}
Source:              http://ftp.gnu.org/pub/gnu/guile/guile-%{version}.tar.gz
Patch1:              guile-01-autoconf.diff
Patch2:              guile-02-1.8.8-dd_fd-d_fd.diff
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build


%prep
#%setup -q -c -n guile-%version
%setup -q -n guile-%version
%patch1 -p1


#do we have d_fd or dd_fd?
#was needed one day for OpenIndiana or OmniOS
#note: [tab blank]
#note2: this grep doesn't help on S11.4, needs __USE_LEGACY_PROTOTYPES__ be defined in CDFLAGS
grep "int.*[	 ]dd_fd" /usr/include/dirent.h || {
%patch2 -p1
}

%build
CPUS=$(psrinfo | gawk '$2=="on-line"{cpus++}END{print (cpus==0)?1:cpus}')

export CFLAGS="%optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export ACLOCAL_FLAGS="-I . -I m4"
%if %{s110400}
# we get dd_fd defined with __USE_LEGACY_PROTOTYPES__
export CFLAGS="${CFLAGS} -D__USE_LEGACY_PROTOTYPES__"
%endif

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

gmake install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
[ -d ${RPM_BUILD_ROOT}%{_datadir}/info/dir ] && rm ${RPM_BUILD_ROOT}%{_datadir}/info/dir



%clean
rm -rf $RPM_BUILD_ROOT



%changelog
* Fri Apr 12 2019 - Thomas Wagner
- need __USE_LEGACY_PROTOTYPES__ to get dd_fd defined on (S11.4 / S12)
* Sun Jul 31 2016 - Thomas Wagner
- make it 32/64-bit
- apply patch2 guile-02-1.8.8-dd_fd-d_fd.diff only, if the OS doesn't have dd_fd (d_fd instead)
