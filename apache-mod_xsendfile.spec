#Module-Specific definitions
%define apache_version 2.2.0
%define mod_name mod_xsendfile
%define mod_conf A58_%{mod_name}.conf
%define mod_so %{mod_name}.so

Summary:	Process X-SENDFILE header cgi/scripts may set
Name:		apache-%{mod_name}
Version:	0.12
Release:	2
Group:		System/Servers
License:	Apache License
URL:		https://tn123.org/mod_xsendfile/
Source0:	https://tn123.org/mod_xsendfile/mod_xsendfile-%{version}.tar.bz2
Source1:	%{mod_conf}
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):  apache-conf >= %{apache_version}
Requires(pre):  apache >= %{apache_version}
Requires:	apache-conf >= %{apache_version}
Requires:	apache >= %{apache_version}
BuildRequires:  apache-devel >= %{apache_version}

%description
mod_xsendfile is a small Apache2 module that processes X-SENDFILE headers
registered by the original output handler. If it encounters the presence of
such a header, it will discard all output and send the file specified by that
header instead, using Apache internals including all optimizations like
caching- headers and sendfile or mmap if configured. It is useful for
processing script output of PHP, Perl, or other CGI programs.

%prep

%setup -q -n %{mod_name}-%{version}

cp %{SOURCE1} %{mod_conf}

%build

%{_bindir}/apxs -c %{mod_name}.c

%install

install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}%{_sysconfdir}/httpd/modules.d

install -m0755 .libs/*.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0644 %{mod_conf} %{buildroot}%{_sysconfdir}/httpd/modules.d/%{mod_conf}

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

%files
%doc docs/Readme.html
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/%{mod_conf}
%attr(0755,root,root) %{_libdir}/apache-extramodules/%{mod_so}


%changelog
* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 0.12-2mdv2011.0
+ Revision: 588106
- rebuild

* Sun Oct 17 2010 Oden Eriksson <oeriksson@mandriva.com> 0.12-1mdv2011.0
+ Revision: 586246
- 0.12

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 0.9-9mdv2010.1
+ Revision: 516282
- rebuilt for apache-2.2.15

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9-8mdv2010.0
+ Revision: 406689
- rebuild

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 0.9-7mdv2009.1
+ Revision: 326280
- rebuild

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9-6mdv2009.0
+ Revision: 235136
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9-5mdv2009.0
+ Revision: 215679
- fix rebuild
- fix buildroot

* Fri Mar 07 2008 Oden Eriksson <oeriksson@mandriva.com> 0.9-4mdv2008.1
+ Revision: 181989
- rebuild

  + Thierry Vignaud <tv@mandriva.org>
    - fix description-line-too-long
    - kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9-3mdv2008.0
+ Revision: 82708
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9-2mdv2007.1
+ Revision: 140781
- rebuild

* Sat Feb 10 2007 Oden Eriksson <oeriksson@mandriva.com> 0.9-1mdv2007.1
+ Revision: 118791
- 0.9

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 0.8-2mdv2007.1
+ Revision: 79565
- Import apache-mod_xsendfile

* Mon Aug 07 2006 Oden Eriksson <oeriksson@mandriva.com> 0.8-2mdv2007.0
- rebuild

* Mon Apr 03 2006 Oden Eriksson <oeriksson@mandriva.com> 0.8-1mdk
- initial Mandriva package

