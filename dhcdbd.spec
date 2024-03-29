#
# TODO:
# - move header file to -devel
# - split an -init  (what for? --radek)
#
Summary:	DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS, stores and presents DHCP options
Summary(pl.UTF-8):	Demon DHCP D-BUS (dhcdbd) - sterowanie sesjami dhclient przy użyciu D-BUS, przechowywanie opcji DHCP
Name:		dhcdbd
Version:	3.0
Release:	2
License:	GPL
Group:		Networking/Daemons
Source0:	http://dcantrel.fedorapeople.org/dhcdbd/%{name}-%{version}.tar.bz2
# Source0-md5:	5316b1a0b3a3d53e972374627546d0bf
Source1:	%{name}.init
URL:		http://dcantrel.fedorapeople.org/dhcdbd/
BuildRequires:	dbus-devel >= 0.33
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	dbus >= 0.33
Requires:	dhcp-client >= 4:3.0.5-1
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
DHCP D-BUS daemon (dhcdbd) controls dhclient sessions with D-BUS,
stores and presents DHCP options.

%description -l pl.UTF-8
Demon DHCP D-BUS (dhcdbd) steruje sesjami dhclient przy użyciu D-BUS,
a także przechowuje i przedstawia opcje DHCP.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -I../include -DDHCLIENT_EXTENDED_OPTION_ENVIRONMENT=0"
	LDFLAGS="%{rpmldflags}"

%{__sed} -i -e"s@Exec=.*@Exec=%{_sbindir}/dhcdbd@" dhcdbd.service

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
%doc README
%attr(755,root,root) %{_sbindir}/dhcdbd
%attr(754,root,root) /etc/rc.d/init.d/dhcdbd
%config(noreplace) %verify(not md5 mtime size) /etc/dbus-1/system.d/dhcdbd.conf
%{_datadir}/dbus-1/services/dhcdbd.service
