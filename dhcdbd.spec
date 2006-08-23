#
# TODO:
# - move header file to -devel
# - split an -init  (what for? --radek)
#
Summary:	DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS, stores and presents DHCP options
Summary(pl):	Demon DHCP D-BUS (dhcdbd) - sterowanie sesjami dhclient przy u¿yciu D-BUS, przechowywanie opcji DHCP
Name:		dhcdbd
Version:	1.14
Release:	0.2
License:	GPL
Group:		Networking/Daemons
Source0:	http://people.redhat.com/~jvdias/dhcdbd/%{name}-%{version}.tar.gz
# Source0-md5:	1180dee7a51a4384d55768650634cf93
Source1:	%{name}.init
Patch0:		%{name}-dbus.patch
URL:		http://people.redhat.com/~jvdias/dhcdbd/
BuildRequires:	dbus-devel >= 0.33
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus >= 0.33
Requires:	dhcp-client >= 3:3.0.3-3
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS,
stores and presents DHCP options.

%description -l pl
Demon DHCP D-BUS (dhcdbd) steruje sesjami dhclient przy u¿yciu D-BUS,
a tak¿e przechowuje i przedstawia opcje DHCP.

%prep
%setup -q
%patch0 -p1

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I%{_libdir}/dbus-1.0/include" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/rc.d/init.d,%{_sbindir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

mv $RPM_BUILD_ROOT{/sbin/dhcdbd,%{_sbindir}}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/dhcdbd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dhcdbd
%service dhcdbd restart "DHCP D-BUS daemon"
if [ -f /var/lock/subsys/dhcdbd ]; then
	echo "You will probably also need \"/sbin/service messagebus restart\""
	echo "to reload the *.service database."
fi

%preun
if [ "$1" = "0" ]; then
	%service dhcdbd stop
	/sbin/chkconfig --del dhcdbd
fi

%files
%defattr(644,root,root,755)
%doc README LICENSE
%attr(755,root,root) %{_sbindir}/dhcdbd
%attr(754,root,root) /etc/rc.d/init.d/dhcdbd
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/dbus-1/system.d/dhcdbd.conf
%{_datadir}/dbus-1/services/dhcdbd.service
