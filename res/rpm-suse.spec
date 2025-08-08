Name:       cyberdesk
Version:    1.1.9
Release:    0
Summary:    RPM package
License:    GPL-3.0
Requires:   gtk3 libxcb1 xdotool libXfixes3 alsa-utils libXtst6 libva2 pam gstreamer-plugins-base gstreamer-plugin-pipewire
Recommends: libayatana-appindicator3-1

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
The best open-source remote desktop client software, written in Rust.

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%global __python %{__python3}

%install
mkdir -p %{buildroot}/usr/bin/
mkdir -p %{buildroot}/usr/share/cyberdesk/
mkdir -p %{buildroot}/usr/share/cyberdesk/files/
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps/
mkdir -p %{buildroot}/usr/share/icons/hicolor/scalable/apps/
install -m 755 $HBB/target/release/cyberdesk %{buildroot}/usr/bin/cyberdesk
install $HBB/libsciter-gtk.so %{buildroot}/usr/share/cyberdesk/libsciter-gtk.so
install $HBB/res/cyberdesk.service %{buildroot}/usr/share/cyberdesk/files/
install $HBB/res/128x128@2x.png %{buildroot}/usr/share/icons/hicolor/256x256/apps/cyberdesk.png
install $HBB/res/scalable.svg %{buildroot}/usr/share/icons/hicolor/scalable/apps/cyberdesk.svg
install $HBB/res/cyberdesk.desktop %{buildroot}/usr/share/cyberdesk/files/
install $HBB/res/cyberdesk-link.desktop %{buildroot}/usr/share/cyberdesk/files/

%files
/usr/bin/cyberdesk
/usr/share/cyberdesk/libsciter-gtk.so
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
    rm /usr/share/applications/cyberdesk.desktop || true
    rm /usr/share/applications/cyberdesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
