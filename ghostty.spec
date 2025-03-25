%global common_build_flags --system %{_builddir}/%{name}-%{version}/vendor/zig/p -Doptimize=ReleaseFast -Dcpu=baseline -Dpie=true -Dstrip=false -Dversion-string=%{version} %{?_smp_mflags}

%bcond_without  standalone_terminfo

Name:           ghostty
Version:        1.1.1
Release:        0
Summary:        Cross-platform terminal emulator
License:        MIT
URL:            https://github.com/ghostty-org/ghostty
# can be verified with:
# minisign -V -P 'RWQlAjJC23149WL2sEpT/l0QKy7hMIFhYdQOFy0Z7z7PbneUgvlsnYcV' -m ghostty-%{version}.tar.gz
Source0:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
Source2:        https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz.minisig
Source1:        vendor.tar.zst
Source98:       series
Source99:       vendor.sh
BuildRequires:  gobject-introspection
BuildRequires:  hicolor-icon-theme
BuildRequires:  pandoc
BuildRequires:  pkgconfig
BuildRequires:  zig = 0.13.0
BuildRequires:  zstd
BuildRequires:  pkgconfig(bash-completion)
#
# In theory it should be able to use those as well but the build is not picking them up
#
# BuildRequires:  cmake(glslang)
# BuildRequires:  pkgconfig(spirv-cross-c-shared)
#
BuildRequires:  pkgconfig(bzip2)
BuildRequires:  python-nautilus-common-files
BuildRequires:  python3-gobject
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
Requires:       terminfo-ghostty = %{version}
%else
BuildRequires:  terminfo
Requires:       terminfo >= %{terminfo_with_ghostty_version}
%endif

%description
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

%prep
%autosetup -p1 -a1

%build
# Run `./nix/build-support/fetch-zig-cache.sh` locally to
# prep deps for offline install
zig build %{common_build_flags}

%install
export DESTDIR=%{buildroot}
zig build %{common_build_flags} --prefix %{_prefix}
%if %{without standalone_terminfo}
rm -rv %{buildroot}%{_datadir}/terminfo/
%endif

%files
%license LICENSE
%{_bindir}/%{name}
