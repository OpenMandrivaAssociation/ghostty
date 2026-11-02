Name:		ghostty
Version:	1.4.0
Release:	2
Summary:	Cross-platform terminal emulator
# The application is MIT. The terminal core also includes wuffs
# (MIT and Apache-2.0), pixels (CC0-1.0), and uucode (MIT).
License:	MIT and Apache-2.0 and CC0-1.0
Url:		https://ghostty.org/
Group:		Graphical desktop/Other
Source0:	https://release.files.ghostty.org/%{version}/ghostty-%{version}.tar.gz
# Extracted zig packages, named by the bare hash. zig --system rejects tarballs.
Source1:	ghostty-%{version}-zig-packages.tar.xz
Patch0:		om-theme.patch
# zig 0.17 ships a broken amxtf32intrin.h. Skip it while compiling wuffs.
Patch1:		ghostty-%{version}-zig-amx-tf32.patch
# ImGui 1.92 already defines IMGUI_HAS_DOCK, and it hits the same header.
Patch2:		ghostty-%{version}-zig-imgui.patch
BuildRequires:	gettext
BuildRequires:	ncurses
BuildRequires:	pkgconfig(blueprint-compiler)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(fontconfig)
BuildRequires:	pkgconfig(freetype2)
BuildRequires:	pkgconfig(glib-2.0)
BuildRequires:	pkgconfig(gtk4) >= 4.18
BuildRequires:	pkgconfig(gtk4-layer-shell-0) >= 1.0.4
BuildRequires:	pkgconfig(harfbuzz)
BuildRequires:	pkgconfig(harfbuzz-gobject)
BuildRequires:	pkgconfig(libadwaita-1) >= 1.7
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(oniguruma)
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:	pkgconfig(x11)
BuildRequires:	pkgconfig(zlib)
BuildRequires:	zig >= 0.17.0

%description
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

%prep
%autosetup -p1 -n ghostty-%{version} -a 1
cp -a LICENSE LICENSE.ghostty
cp -a p/N-V-__8AAP5JWgCGP_AD0teWpa4krRvE9VPZzvviGdbmN4jI/LICENSE LICENSE.wuffs
cp -a p/N-V-__8AADYiAAB_80AWnH1AxXC0tql9thT-R-DYO1gBqTLc/LICENSE LICENSE.pixels
cp -a p/uucode-0.2.0-ZZjBPoGFVgCiflJNFc6Io8xzC67B6PA5bUkk4LT0kCxg/LICENSE.md LICENSE.uucode

%install
# SIMD stays off: zig 0.17 cannot compile the bundled simdutf and highway.
# Leave the binary unstripped so rpm can split debuginfo.
# The app build also installs libghostty-vt. That library is the
# separate libghostty package, and this binary does not link it.
DESTDIR="%{buildroot}" \
ZIG_GLOBAL_CACHE_DIR="%{_builddir}/zig-global-cache" \
zig build \
	--cache-dir "%{_builddir}/zig-local-cache" \
	--system "$PWD/p" \
	--build-id=sha1 \
	-Dsimd=false \
	-Demit-docs=false \
	-Demit-terminfo=true \
	-Doptimize=ReleaseFast \
	-Dstrip=false \
	-Dcpu=baseline \
	-Dversion-string=%{version} \
	--prefix %{_prefix} \
	--prefix-lib-dir %{_lib}
rm -rf %{buildroot}%{_includedir}/ghostty \
	%{buildroot}%{_libdir}/libghostty-vt.* \
	%{buildroot}%{_datadir}/pkgconfig/libghostty-vt.pc \
	%{buildroot}%{_datadir}/pkgconfig/libghostty-vt-static.pc
%find_lang com.mitchellh.ghostty

%files -f com.mitchellh.ghostty.lang
%license LICENSE.ghostty LICENSE.wuffs LICENSE.pixels LICENSE.uucode
%{_bindir}/ghostty
%{_datadir}/applications/com.mitchellh.ghostty.desktop
%{_datadir}/bash-completion/completions/ghostty.bash
%{_datadir}/bat/syntaxes/ghostty.sublime-syntax
%{_datadir}/dbus-1/services/com.mitchellh.ghostty.service
%{_datadir}/fish/vendor_completions.d/ghostty.fish
%{_datadir}/ghostty
%{_datadir}/icons/hicolor/*/apps/com.mitchellh.ghostty.png
%{_datadir}/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_datadir}/metainfo/com.mitchellh.ghostty.metainfo.xml
%{_datadir}/nautilus-python/extensions/ghostty.py
%{_datadir}/nvim/site/compiler/ghostty.vim
%{_datadir}/nvim/site/ftdetect/ghostty.vim
%{_datadir}/nvim/site/ftplugin/ghostty.vim
%{_datadir}/nvim/site/syntax/ghostty.vim
%{_datadir}/terminfo/g/ghostty
%{_datadir}/terminfo/ghostty.terminfo
%{_datadir}/terminfo/x/xterm-ghostty
%{_datadir}/vim/vimfiles/compiler/ghostty.vim
%{_datadir}/vim/vimfiles/ftdetect/ghostty.vim
%{_datadir}/vim/vimfiles/ftplugin/ghostty.vim
%{_datadir}/vim/vimfiles/syntax/ghostty.vim
%{_datadir}/zsh/site-functions/_ghostty
%{_userunitdir}/app-com.mitchellh.ghostty.service
