%define rname mpg123

%define flavor emacs xemacs

Summary:	A front-end program to mpg123 under Emacs/XEmacs
Name:		emacs-%{rname}
Version:	1.50
Release:	%mkrel 2
Source0:	http://www.gentei.org/~yuuji/software/mpg123el/%{rname}.el
Source1:	%{name}-autostart.el
License:	Freeware
Group:		Editors
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	%{flavor}
BuildRequires:	perl
BuildRequires:	emacs-bin
Requires:	%{rname}
BuildArch:	noarch
URL:		http://www.gentei.org/~yuuji/software/mpg123el/

%description
A front-end program to mpg123 under Emacs/XEmacs.

%prep
iconv -f EUC-JP -t UTF-8 %{SOURCE0} > %{rname}.el
sed -i -e 's,euc-jp,utf-8,g' %{rname}.el
#install -m 644 %{SOURCE0} %{rname}.el

%build
for i in %{flavor};do
$i -batch -q -no-site-file -f batch-byte-compile %{rname}.el 
mv %{rname}.elc $i-%{rname}.elc
done

#Maybe need adjust
perl -n -e 'last if /^\(/;last if /^;;; Code/; print' < %{SOURCE0} > DOCUMENTATION

%install
rm -rf %{buildroot}

for i in %{flavor};do
install -D -m644 $i-%{rname}.elc %{buildroot}%{_datadir}/$i/site-lisp/$i-%{rname}.elc
[[ $i = emacs ]] && install -D -m644 %{rname}.el %{buildroot}%{_datadir}/emacs/site-lisp/%{rname}.el
done

install -d %buildroot%{_sysconfdir}/emacs/site-start.d
cat << EOF > %buildroot%{_sysconfdir}/emacs/site-start.d/%{name}.el
%{expand:%(%__cat %{SOURCE1})}
EOF


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc DOCUMENTATION
%config(noreplace) /etc/emacs/site-start.d/%{name}.el
%{_datadir}/*/site-lisp/*el*

