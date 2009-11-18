%define		_modname	gnupg
%define		_status		stable
Summary:	%{_modname} - wrapper around the gpgme library
Summary(pl.UTF-8):	%{_modname} - wrapper biblioteki gpgme
Name:		php-pecl-%{_modname}
Version:	1.3.1
Release:	2
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{_modname}-%{version}.tgz
# Source0-md5:	75881c633d7a53065d281e8a4a9a2cdf
URL:		http://pecl.php.net/package/gnupg/
BuildRequires:	gpgme-devel
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	re2c
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	gpgme >= 1.1.4-2
Requires:	php-common >= 4:5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides methods to interact with gnupg. So you can
sign, encrypt, verify directly from PHP.

In PECL status of this extension is: %{_status}.

%description -l pl.UTF-8
To rozszerzenie dostarcza metody współpracy z gnupg. Umożliwia to
podpisywanie, szyfrowanie oraz weryfikację danych z poziomu PHP.

To rozszerzenie ma w PECL status: %{_status}.

%prep
%setup -q -c

%build
CFLAGS="%{rpmcflags} -D_FILE_OFFSET_BITS=64" ; export CFLAGS
cd %{_modname}-%{version}
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install %{_modname}-%{version}/modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc %{_modname}-%{version}/{EXPERIMENTAL,README}
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
