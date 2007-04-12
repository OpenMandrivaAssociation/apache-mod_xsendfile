#Module-Specific definitions
%define apache_version 2.2.0
%define mod_name mod_xsendfile
%define mod_conf A58_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Process X-SENDFILE header cgi/scripts may set
Name:		apache-%{mod_name}
Version:	0.9
Release:	%mkrel 2
Group:		System/Servers
License:	Apache License
URL:		http://celebnamer.celebworld.ws/stuff/mod_xsendfile/
Source0:	http://celebnamer.celebworld.ws/stuff/mod_xsendfile/mod_xsendfile-%{version}.tar.gz
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler. If it encounters the presence of such
a header, it will discard all output and send the file specified by that header
instead, using Apache internals including all optimizations like caching-headers
and sendfile or mmap if configured. It is useful for processing script output of
PHP, Perl, or other CGI programs.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build

%{_sbindir}/apxs -c %{mod_name}.c

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

install -d %{buildroot}%{_var}/www/html/addon-modules
ln -s ../../../..%{_docdir}/%{name}-%{version} %{buildroot}%{_var}/www/html/addon-modules/%{name}-%{version}

%post
if [ -f %{_var}/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart 1>&2;
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f %{_var}/lock/subsys/httpd ]; then
        %{_initrddir}/httpd restart 1>&2
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Readme.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}
%{_var}/www/html/addon-modules/*


