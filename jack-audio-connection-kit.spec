Summary: The Jack Audio Connection Kit
Name: jack-audio-connection-kit
Version: 0.103.0
Release: 1%{?dist}
License: GPL/LGPL
Group: System Environment/Daemons
Source0: http://dl.sourceforge.net/sourceforge/jackit/%{name}-%{version}.tar.gz
Source1: %{name}-README.Fedora
URL: http://www.jackaudio.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: alsa-lib-devel
BuildRequires: libsndfile-devel >= 1.0.0
BuildRequires: pkgconfig
BuildRequires: doxygen
BuildRequires: readline-devel, ncurses-devel
BuildRequires: autoconf >= 2.59, automake >= 1.9.3, libtool
BuildRequires: libfreebob-devel >= 1.0.0

%define gid 334
%define groupname jackuser

Requires(pre): /usr/sbin/groupadd
Requires(post): /sbin/ldconfig

%description
JACK is a low-latency audio server, written primarily for the Linux
operating system. It can connect a number of different applications to
an audio device, as well as allowing them to share audio between
themselves. Its clients can run in their own processes (ie. as a
normal application), or can they can run within a JACK server (ie. a
"plugin").

JACK is different from other audio server efforts in that it has been
designed from the ground up to be suitable for professional audio
work. This means that it focuses on two key areas: synchronous
execution of all clients, and low latency operation.

%package devel
Summary: Header files for Jack
Group: Development/Libraries
Requires: %{name} = %{version}
Requires: pkgconfig

%description devel
Header files for the Jack Audio Connection Kit.

%package example-clients
Summary: Example clients that use Jack 
Group: Applications/Multimedia
Requires: %{name} = %{version}

%description example-clients
Small example clients that use the Jack Audio Connection Kit.

%prep
%setup -q

%build
# x86_64 issue reported by Rudolf Kastl (not checked, but not bad).
autoreconf --force --install

%configure \
    --with-html-dir=%{_docdir} \
    --enable-freebob \
    --disable-oss \
    --disable-portaudio \
    --with-default-tmpdir=/dev/shm
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# can't use the makeinstall macro, jack needs DESTDIR and prefix gets
# added to it and messes up part of the install
make install DESTDIR=$RPM_BUILD_ROOT

# prepare README.Fedora for documentation including
install -p -m644 %{SOURCE1} README.Fedora

# remove extra install of the documentation
rm -fr $RPM_BUILD_ROOT%{_docdir}

# remove *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/jack/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%pre
/usr/sbin/groupadd -g %gid -r %groupname &>/dev/null || :

%post
/sbin/ldconfig

# Add default limits for jackuser group
grep -q jackuser /etc/security/limits.conf || cat >> /etc/security/limits.conf << EOF

## Automatically appended by jack-audio-connection-kit
@jackuser - rtprio 20
@jackuser - memlock 4194304
EOF

%postun -p /sbin/ldconfig

%files 
%defattr(-,root,root)
%doc AUTHORS TODO COPYING*
%doc README.Fedora
%{_bindir}/jackd
%{_bindir}/jack_load
%{_bindir}/jack_unload
%{_bindir}/jack_bufsize
%{_bindir}/jack_freewheel
%{_libdir}/jack/
%{_mandir}/man1/jack*.1*
%{_libdir}/libjack.so.*

%files devel
%defattr(-,root,root)
%doc doc/reference
%{_includedir}/jack/
%{_libdir}/libjack.so
%{_libdir}/pkgconfig/jack.pc

%files example-clients
%defattr(-,root,root)
%{_bindir}/jackrec
%{_bindir}/jack_connect
%{_bindir}/jack_disconnect
%{_bindir}/jack_impulse_grabber
%{_bindir}/jack_lsp
%{_bindir}/jack_metro
%{_bindir}/jack_showtime
%{_bindir}/jack_monitor_client
%{_bindir}/jack_simple_client
%{_bindir}/jack_midiseq
%{_bindir}/jack_midisine

%changelog
* Wed May 23 2007 Andy Shevchenko <andy@smile.org.ua> 0.103.0-1
- update to the last official release
- append defaults to the limits.conf (#221785, #235624)

* Wed Mar 07 2007 Andy Shevchenko <andy@smile.org.ua> 0.102.20-4
- drop libtermcap-devel build requirement (#231203)
- create special jackuser group (#221785)

* Sat Oct 28 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-3
- fix BuildRequires: libfreebob -> libfreebob-devel

* Tue Oct 24 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-2.1
- rebuild with libfreebob (should closed #211751)

* Wed Oct 11 2006 Andy Shevchenko <andy@smile.org.ua> 0.102.20-2.0
- update to 0.102.20
- drop patch0 (already in mainstream)
- no pack jack_transport (build error)
- pack new JACK MIDI files

* Tue Aug 29 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-13
- http://fedoraproject.org/wiki/Extras/Schedule/FC6MassRebuild

* Tue Aug 01 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-12
- use install instead of cp (#200835)

* Tue Jul 04 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-11
- update URL
- add BR: libtool

* Tue Jun 20 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-10
- add BRs: autoconf, automake
  (http://fedoraproject.org/wiki/QA/FixBuildRequires)

* Sat May 27 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-9
- remove --enable-stripped-jackd and --enable-optimize (use default flags)

* Fri May 19 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-8
- uniform directories items at %files section

* Wed May 17 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-7
- change License tag to GPL/LGPL
- remove --enable-shared (it should be default)
- add a -p flag to the line that copies README.Fedora

* Wed May 10 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-6
- apply clock fix for AMD X2 CPUs (please, refer to
  http://sourceforge.net/mailarchive/forum.php?thread_id=8085535&forum_id=3040)

* Wed May 03 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-5
- adjust spec after reviewing

* Thu Apr 27 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-4
- reformatting README.Fedora to 72 symbols width

* Wed Apr 26 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-3
- add README.Fedora
- remove useless BRs

* Mon Apr 24 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-2
- disable oss and portaudio engines
- use /dev/shm as jack tmpdir
- remove capabilities stuff

* Tue Apr 04 2006 Andy Shevchenko <andriy@asplinux.com.ua> 0.101.1-1
- update to 0.101.1

* Mon Mar 27 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- update to 0.100.7 (#183912)
- adjust BR (add versions)
- replace files between examples and main packages
- own jack tmpdir

* Fri Mar 17 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- no libs subpackage
- From Fernando Lopez-Lezcano <nando@ccrma.stanford.edu>:
  - added configuration variable to build with/without capabilities
  - added --enable-optimize flag to configure script
  - disabled sse/mmx instructions in i386 build
  - create temporary directory as /var/lib/jack/tmp
  - create and erase tmp directory at install or uninstall
  - try to umount the temporary directory before uninstalling the package

* Fri Mar 03 2006 Andy Shevchenko <andriy@asplinux.com.ua>
- fix spec for extras injection

* Fri Nov 18 2005 Andy Shevchenko <andriy@asplinux.ru>
- exclude *.la files
- use dist tag

* Fri Oct 14 2005 Andy Shevchenko <andriy@asplinux.ru>
- 0.100.0
- no optimization

* Tue Sep 28 2004 Andy Shevchenko <andriy@asplinux.ru>
- 0.99.1

* Fri Aug 20 2004 Andy Shevchenko <andriy@asplinux.ru>
- rebuild from Mandrake
