#
# spec file for package SFEmediainfo
#

# Don't bother with the GUI for now.  (wxWidgets don't get found.)
#
# NOTE: The sections dealing with the GUI have been deleted from the spec.
#	The spec on which this spec is based can be found in the source tree:
#	MediaInfo/Project/GNU/mediainfo.spec

%include Solaris.inc
%define cc_is_gcc 1
%include base.inc
%define download_loc	http://mediaarea.net/download/source/
%define srcname		mediainfo
%define mediainfo_version           0.7.67
%define libmediainfo_version        0.7.67
%define libzen_version              0.4.29

Name:           SFEmediainfo
IPS_package_name: media/mediainfo
Version:        %{mediainfo_version}
Summary:        Most relevant technical and tag data for video and audio files
Group:          Applications/Sound and Video
License:        BSD-2-Clause
URL:            http://MediaArea.net/MediaInfo
Packager:       MediaArea.net SARL <info@mediaarea.net>
Source0:	%download_loc%srcname/%version/%{srcname}_%version.tar.bz2

# BuildRequires:  gcc-c++
# BuildRequires:  pkgconfig
# BuildRequires:  libmediainfo-devel >= %{libmediainfo_version}
BuildRequires:	SFElibmediainfo-devel
# BuildRequires:  libzen-devel >= %{libzen_version}
# BuildRequires:  pkgconfig
# BuildRequires:  wxGTK-devel
# BuildRequires:  zlib-devel
# BuildRequires:  libtool
# BuildRequires:  automake
# BuildRequires:  autoconf

#BuildRequires: SFEwxwidgets-gpp-devel

%description
MediaInfo is a convenient unified display of the most relevant technical
and tag data for video and audio files.

What information can I get from MediaInfo?
• General: title, author, director, album, track number, date, duration...
• Video: codec, aspect, fps, bitrate...
• Audio: codec, sample rate, channels, language, bitrate...
• Text: language of subtitle
• Chapters: number of chapters, list of chapters

DivX, XviD, H263, H.263, H264, x264, ASP, AVC, iTunes, MPEG-1,
MPEG1, MPEG-2, MPEG2, MPEG-4, MPEG4, MP4, M4A, M4V, QuickTime,
RealVideo, RealAudio, RA, RM, MSMPEG4v1, MSMPEG4v2, MSMPEG4v3,
VOB, DVD, WMA, VMW, ASF, 3GP, 3GPP, 3GP2

What format (container) does MediaInfo support?
• Video: MKV, OGM, AVI, DivX, WMV, QuickTime, Real, MPEG-1,
  MPEG-2, MPEG-4, DVD (VOB) (Codecs: DivX, XviD, MSMPEG4, ASP,
  H.264, AVC...)
• Audio: OGG, MP3, WAV, RA, AC3, DTS, AAC, M4A, AU, AIFF
• Subtitles: SRT, SSA, ASS, SAMI


%prep
%setup -q -n MediaInfo
sed -i 's/.$//' *.txt *.html Release/*.txt

find Source -type f -exec chmod 644 {} ';'
chmod 644 *.html *.txt Release/*.txt

pushd Project/GNU/CLI
    autoreconf -i
popd


%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%optflags"
# # The /usr/g++ paths are for wxWidgets
# export CXXFLAGS="%optflags -I/usr/g++/include"
# export LDFLAGS="%_ldflags -L/usr/g++/lib -R/usr/g++/lib"

# build CLI
pushd Project/GNU/CLI
    %configure
    make
popd


%install
pushd Project/GNU/CLI
    make install DESTDIR=%{buildroot}
popd

%clean
rm -rf %buildroot


%files
%defattr(-,root,bin,-)
%doc Release/ReadMe_CLI_Linux.txt License.html History_CLI.txt
%{_bindir}/mediainfo


%changelog
* Mon Feb 10 2014 - Alex Viskovatoff
- import spec into SFE
* Tue Jan 01 2009 MediaArea.net SARL <info@mediaarea.net> - 0.7.67
- See History.txt for more info and real dates
- Previous packages made by Toni Graffy <toni@links2linux.de>
- Fedora style made by Vasiliy N. Glazov <vascom2@gmail.com>
