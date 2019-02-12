# python　v3.6.3 インストール
```
wget 'https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz';
```
# 事前に必要となるパッケージをインストール
```
sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel;
sudo yum -y install epel-release;
```

# Pythonをインストール
```
tar zxvf Python-3.6.3.tgz;
cd Python-3.6.3;
./configure --prefix=/usr/local/python;
make && make install;
```

# シンボリックリンクを作成
```
ln -f -s /usr/local/python/bin/python3 /usr/local/bin/python;
ln -f -s /usr/local/python/bin/pip3.6 /usr/local/bin/pip;
```

# chromedriverインストール
```
sudo yum -y install chromedriver;
```

# Xvfb のインストール(ヘッドレス (GUI 無し) に実行)
```
sudo yum -y install Xvfb;
sudo yum -y install xorg-x11-server-Xvfb;
```

# python用 selenium、xvfbwrapper、Pillow (PIL) のインストール
```
pip install selenium;
pip install pillow;
pip install xvfbwrapper;
```

# CentOSの場合
```
pip install pyvirtualdisplay;
```

# Xvfbサービス作成
```
cat <<EOF > /usr/lib/systemd/system/Xvfb.service
[Unit]
Description=Virtual Framebuffer X server for X Version 11

[Service]
Type=simple
EnvironmentFile=-/etc/sysconfig/Xvfb
ExecStart=/usr/bin/Xvfb $OPTION
ExecReload=/bin/kill -HUP ${MAINPID}

[Install]
WantedBy=multi-user.target
EOF
```

# Xvfb環境変数設定ファイル作成
```
cat <<EOF > /etc/sysconfig/Xvfb
# Xvfb Enviroment File
OPTION=":1 -screen 0 1366x768x24"
EOF
```

# Chromeリポジトリファイル作成
## 手動で行ったほうが確実
```
cat <<EOF > /etc/yum.repos.d/google-chrome.repo
[google-chrome]
name=google-chrome
baseurl=http://dl.google.com/linux/chrome/rpm/stable/$basearch
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub
EOF
```

# Google Chromeのインストール
```
yum -y install google-chrome-stable;
```

# 日本語フォントインストール
```
yum -y install ipa-pgothic-fonts.noarch;
```

# Xvfbサービス起動
```
systemctl enable Xvfb;
systemctl restart Xvfb;
```
