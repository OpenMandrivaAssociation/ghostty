Name:           ghostty
Version:        1.1.4+git.1067cd3
Release:        1
Summary:        Cross-platform terminal emulator
License:        MIT
URL:            https://ghostty.org/
Source0:        https://github.com/ghostty-org/ghostty/releases/download/tip/ghostty-source.tar.gz
Source1:        zig-cache.tar.gz

BuildRequires: gettext
BuildRequires: pkgconfig
BuildRequires: pkgconfig(blueprint-compiler)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(gtk4)
BuildRequires: pkgconfig(gtk4-layer-shell-0)
BuildRequires: pkgconfig(harfbuzz)
BuildRequires: pkgconfig(harfbuzz-gobject)
BuildRequires: pkgconfig(libadwaita-1)
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(oniguruma)
BuildRequires: pkgconfig(pixman-1)
BuildRequires: zig >= 0.14.0

%description
Ghostty is a fast, feature-rich, and cross-platform terminal
emulator that uses platform-native UI and GPU acceleration.

%prep
%autosetup -a 1 -n ghostty-1.1.4-main+1067cd3

%build
# Run `./nix/build-support/fetch-zig-cache.sh` locally to
# prep deps for offline install 

# Docs require pandoc which is not available

zig build \
    --verbose \
    --summary all \
    --prefix "%{buildroot}%{_prefix}" \
    --system "$(pwd)/zig-cache/p" \
    -Dversion-string=%{version}-%{release} \
    -Doptimize=ReleaseFast \
    -Dcpu=baseline \
    -Dpie=true \
    -Demit-docs=false

%files
%license LICENSE
%{_bindir}/ghostty
%{_prefix}/share/applications/com.mitchellh.ghostty.desktop
%{_prefix}/share/bash-completion/completions/ghostty.bash
%{_prefix}/share/bat/syntaxes/ghostty.sublime-syntax
%{_prefix}/share/fish/vendor_completions.d/ghostty.fish
%{_prefix}/share/ghostty
%{_prefix}/share/icons/hicolor/1024x1024/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/128x128@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/16x16@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/256x256@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/32x32@2/apps/com.mitchellh.ghostty.png
%{_prefix}/share/icons/hicolor/512x512/apps/com.mitchellh.ghostty.png
%{_prefix}/share/kio/servicemenus/com.mitchellh.ghostty.desktop
%{_prefix}/share/locale/de_DE.UTF-8/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/locale/nb_NO.UTF-8/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/locale/pl_PL.UTF-8/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/locale/uk_UA.UTF-8/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/locale/zh_CN.UTF-8/LC_MESSAGES/com.mitchellh.ghostty.mo
%{_prefix}/share/nautilus-python/extensions/ghostty.py
%{_prefix}/share/nvim/site/compiler/ghostty.vim
%{_prefix}/share/nvim/site/ftdetect/ghostty.vim
%{_prefix}/share/nvim/site/ftplugin/ghostty.vim
%{_prefix}/share/nvim/site/syntax/ghostty.vim
%{_prefix}/share/terminfo/g/ghostty
%{_prefix}/share/terminfo/x/xterm-ghostty
%{_prefix}/share/vim/vimfiles/compiler/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftdetect/ghostty.vim
%{_prefix}/share/vim/vimfiles/ftplugin/ghostty.vim
%{_prefix}/share/vim/vimfiles/syntax/ghostty.vim
%{_prefix}/share/zsh/site-functions/_ghostty
