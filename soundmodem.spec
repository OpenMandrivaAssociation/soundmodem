# FIXME: temporarily disable to get package to build (wally 10/2010)
%define Werror_cflags %nil

Summary:	Driver and diagnostic utility for Usermode SoundModem
Name:		soundmodem
Version:	0.18
Release:	2
License:	GPLv2+
Group:		Communications
Url:		http://www.baycom.org/~tom/ham/soundmodem/
Source0:	http://www.baycom.org/~tom/ham/soundmodem/%{name}-%{version}.tar.gz
BuildRequires:	alsa-oss-devel
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	gtk2-devel
BuildRequires:	audiofile-devel
BuildRequires:	hamlib-devel
Requires(post):		rpm-helper
Requires(preun):	rpm-helper

%description
This package contains the driver and the diagnostic utility for
user-space SoundModem. It allows you to use sound-cards supported
by OSS/Free as Amateur Packet Radio modems.

%package devel

Summary:	Development files for %{name}
Group:		Development/Other
Requires:	%{name} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q

%build
%configure2_5x \
%ifarch %ix86
	--enable-mmx \
%endif
	--disable-rpath
%make

%install
%makeinstall_std

# init script
install -Dpm 0755 soundmodem.initscript %{buildroot}%{_initrddir}/soundmodem

# config file
install -dm 0755 -d %{buildroot}%{_sysconfdir}/ax25
touch %{buildroot}%{_sysconfdir}/ax25/%{name}.conf

#move devel files to better location
install -dm 0755 %{buildroot}%{_includedir}/%{name}
mv %{buildroot}%{_includedir}/*.h %{buildroot}%{_includedir}/%{name}

%find_lang %{name}

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README newqpsk/README.newqpsk
%{_sbindir}/soundmodem
%{_bindir}/soundmodemconfig
%{_mandir}/man8/soundmodem*
%config(noreplace) %{_sysconfdir}/ax25/%{name}.conf
%{_initrddir}/soundmodem

%files devel
%{_includedir}/%{name}

