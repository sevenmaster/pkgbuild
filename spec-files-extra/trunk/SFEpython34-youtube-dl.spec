#
# spec file for package SFEpython34-youtube-dl
#

%include Solaris.inc
%define srcname youtube-dl

Name:		SFEpython34-%srcname
IPS_Package_Name:	video/youtube-dl
Summary:	A small command-line program to download videos from YouTube.com and a few more sites
URL:		http://rg3.github.io/%srcname/
Version:	2016.1.29
%define srcver	2016.01.29
Source:		http://yt-dl.org/downloads/%srcver/%srcname-%srcver.tar.gz

BuildRequires:	runtime/python-34
Requires:	runtime/python-34

%include default-depend.inc

%define python_version	3.4

%prep
%setup -q -n %srcname

%build
python%python_version setup.py build

%install
rm -rf %buildroot

python%python_version setup.py install --root=%buildroot --prefix=%_prefix

# move to vendor-packages
mkdir -p %buildroot%_libdir/python%python_version/vendor-packages
mv %buildroot%_libdir/python%python_version/site-packages/* \
   %buildroot%_libdir/python%python_version/vendor-packages/
rmdir %buildroot%_libdir/python%python_version/site-packages

# do not bother with these conveniences for now, especially since no such
# directories (bash_completion.d and fish) exist on Solaris
rm -r %buildroot%_basedir/etc

%clean
rm -rf %buildroot

%files
%defattr (-, root, bin)
%_bindir/%srcname
%_libdir/python%python_version/vendor-packages
%dir %attr (0755, root, sys) %_datadir
%_mandir/man1/%srcname.1
%dir %attr (0755, root, other) %_docdir
%_docdir/youtube_dl/README.txt

%changelog
* Sat 30 Jan 2016 - Alex Viskovatoff <herzen@imap.cc>
- Initial spec
