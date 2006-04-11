Summary:	A Network Intrusion Detection System
Summary(pl):	System do wykrywania intruzów w sieci
Name:		prelude-manager
Version:	0.9.4.1
Release:	0.1
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}.tar.gz
# Source0-md5:	4641da26473496b2bc43647753ff0499
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	gnutls-devel
BuildRequires:	libprelude-devel >= 0.9.0
BuildRequires:	libpreludedb-devel >= 0.9.0
BuildRequires:	libxml2-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Prelude-Manager is a high-availability server which collects and
normalizes events from distributed sensors.

%description -l pl
Prelude-Manager to serwer o wysokiej dostêpno¶ci zbieraj±cy i
normalizuj±cy zdarzenia od rozproszonych czujników.

%package devel
Summary:	Header files for prelude-manager
Summary(pl):	Pliki nag³ówkowe dla prelude-managera
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for prelude-manager.

%description devel -l pl
Pliki nag³ówkowe dla prelude-managera.

%prep
%setup -q -n %{name}-%{version}

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/etc/{rc.d/init.d,sysconfig}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add prelude-manager
if [ -f /var/lock/subsys/prelude-manager ]; then
        /etc/rc.d/init.d/prelude-manager restart 1>&2
else
        echo "Run \"/etc/rc.d/init.d/prelude-manager start\" to start Prelude Manager."
fi

%preun
if [ "$1" = "0" ]; then
        if [ -f /var/lock/subsys/prelude-manager ]; then
                /etc/rc.d/init.d/prelude-manager stop 1>&2
        fi
        /sbin/chkconfig --del prelude-manager
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%dir %{_sysconfdir}/%{name}
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/%{name}/*.*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%attr(755,root,root) %{_bindir}/%{name}
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/*
%attr(755,root,root) %{_libdir}/%{name}/*/*.so
%{_libdir}/%{name}/*/*.la
%{_datadir}/%{name}
%{_var}/run/%{name}
%{_var}/spool/%{name}

%files devel
%defattr(644,root,root,755)
%{_includedir}/%{name}
