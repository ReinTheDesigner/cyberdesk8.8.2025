Name:       cyberdesk
Version:    1.4.1
Release:    0
Summary:    RPM package
License:    GPL-3.0
URL:        https://cyberdesk.com
Vendor:     cyberdesk <info@cyberdesk.com>
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

# %global __python %{__python3}

%install

mkdir -p "%{buildroot}/usr/share/cyberdesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/cyberdesk"
mkdir -p "%{buildroot}/usr/bin"
install -Dm 644 $HBB/res/cyberdesk.service -t "%{buildroot}/usr/share/cyberdesk/files"
install -Dm 644 $HBB/res/cyberdesk.desktop -t "%{buildroot}/usr/share/cyberdesk/files"
install -Dm 644 $HBB/res/cyberdesk-link.desktop -t "%{buildroot}/usr/share/cyberdesk/files"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/cyberdesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/cyberdesk.svg"

%files
/usr/share/cyberdesk/*
/usr/share/cyberdesk/files/cyberdesk.service
/usr/share/icons/hicolor/256x256/apps/cyberdesk.png
/usr/share/icons/hicolor/scalable/apps/cyberdesk.svg
/usr/share/cyberdesk/files/cyberdesk.desktop
/usr/share/cyberdesk/files/cyberdesk-link.desktop

%changelog
# let's skip this for now

%pre
# can do something for centos7
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop cyberdesk || true
  ;;
esac

%post
cp /usr/share/cyberdesk/files/cyberdesk.service /etc/systemd/system/cyberdesk.service
cp /usr/share/cyberdesk/files/cyberdesk.desktop /usr/share/applications/
cp /usr/share/cyberdesk/files/cyberdesk-link.desktop /usr/share/applications/
ln -sf /usr/share/cyberdesk/cyberdesk /usr/bin/cyberdesk
systemctl daemon-reload
systemctl enable cyberdesk
systemctl start cyberdesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop cyberdesk || true
    systemctl disable cyberdesk || true
    rm /etc/systemd/system/cyberdesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/cyberdesk || true
    rmdir /usr/lib/cyberdesk || true
    rmdir /usr/local/cyberdesk || true
    rmdir /usr/share/cyberdesk || true
    rm /usr/share/applications/cyberdesk.desktop || true
    rm /usr/share/applications/cyberdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
    rmdir /usr/lib/cyberdesk || true
    rmdir /usr/local/cyberdesk || true
  ;;
esac
