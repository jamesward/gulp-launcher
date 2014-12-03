cd /d %~dp0
python -c "import urllib2; get_pip = urllib2.urlopen('https://bootstrap.pypa.io/get-pip.py').read(); file('get_pip.py', 'w').write(get_pip)"
python get_pip.py
C:\Python27\Scripts\pip install -r requirements.txt
pyinstaller --onefile gulp-launcher.py
