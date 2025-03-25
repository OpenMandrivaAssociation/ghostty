%global common_build_flags --system %{_builddir}/%{name}-%{version}/offline-cache/p -Doptimize=ReleaseFast -Dcpu=baseline -Dpie=true -Dstrip=false -Dversion-string=%{version} %{?_smp_mflags}

%bcond_without  standalone_terminfo

Name:           ghostty
Version:        1.1.3
Release:        1
Summary:        Cross-platform terminal emulator
License:        MIT
URL:            https://ghostty.org
Source0:        https://github.com/ghostty-org/ghostty/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        vendor.tar.xz
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  hicolor-icon-theme
#BuildRequires:  pandoc
BuildRequires:  pkgconfig
BuildRequires:  zig >= 0.14.0
BuildRequires:  pkgconfig(libzstd)
BuildRequires:  pkgconfig(bash-completion)
#
# In theory it should be able to use those as well but the build is not picking them up
#
# BuildRequires:  cmake(glslang)
# BuildRequires:  pkgconfig(spirv-cross-c-shared)
#
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  pkgconfig(nautilus-python)
BuildRequires:  python-gobject3
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(freetype2)
BuildRequires:  pkgconfig(gtk4)
BuildRequires:  pkgconfig(libadwaita-1)
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(ncurses)
BuildRequires:  pkgconfig(oniguruma)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(zlib)
%if %{with standalone_terminfo}
#Requires:       terminfo-ghostty = %{version}
%else
BuildRequires:  terminfo
#Requires:       terminfo >= %{terminfo_with_ghostty_version}
%endif

%description
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

%prep
%autosetup -p1 -a1

%build
# Run `./nix/build-support/fetch-zig-cache.sh` locally to
# prep deps for offline install
zig build 
#{common_build_flags}

%install
export DESTDIR=%{buildroot}
zig build %{common_build_flags} --prefix %{_prefix}
%if %{without standalone_terminfo}
rm -rv %{buildroot}%{_datadir}/terminfo/
%endif

%files
%license LICENSE
%{_bindir}/%{name}
