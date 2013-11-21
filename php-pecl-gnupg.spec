%define		php_name	php%{?php_suffix}
%define		modname	gnupg
%define		status		stable
Summary:	%{modname} - wrapper around the gpgme library
Summary(pl.UTF-8):	%{modname} - wrapper biblioteki gpgme
Name:		%{php_name}-pecl-%{modname}
Version:	1.3.3
Release:	1
License:	BSD, revised
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	00033067dbe0af126c838498a98886ea
URL:		http://pecl.php.net/package/gnupg/
BuildRequires:	%{php_name}-devel >= 3:5.0.0
BuildRequires:	gpgme-devel
BuildRequires:	re2c
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Requires:	gpgme >= 1.1.4-2
Requires:	php(core) >= 5.0.4
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides methods to interact with gnupg. So you can
sign, encrypt, verify directly from PHP.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
To rozszerzenie dostarcza metody współpracy z gnupg. Umożliwia to
podpisywanie, szyfrowanie oraz weryfikację danych z poziomu PHP.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
export CFLAGS="%{rpmcflags} -D_FILE_OFFSET_BITS=64"
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install -p modules/%{modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
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
%doc EXPERIMENTAL README
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
