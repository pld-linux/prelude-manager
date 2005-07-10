Summary:	A Network Intrusion Detection System
Name:		prelude-manager
%define	_rc	rc6
Version:	0.9.0
Release:	0.%{_rc}.1
License:	GPL
Group:		Applications
Source0:	http://www.prelude-ids.org/download/releases/%{name}-%{version}-%{_rc}.tar.gz
# Source0-md5:	91fe6e6468b0762fb8df8b42c259d14c
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://www.prelude-ids.org/
BuildRequires:	libprelude-devel >= 0.9.0
BuildRequires:	libpreludedb-devel >= 0.9.0
BuildRequires:	libxml2-devel
BuildRequires:	gnutls-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Prelude LML analyze log files and transmit to prelude some
informations. Prelude LML also use syslog to listen for some others
applications, like NTSyslog.

%package devel
Summary:	Header files and develpment documentation for prelude-manager
Group:		Development/Libraries
Requires:	%{name}-libs = %{epoch}:%{version}-%{release}

%description devel
Header files and develpment documentation for prelude-manager.

%prep
%setup -q -n %{name}-%{version}-%{_rc}

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
