python -c "import urllib2; get_pip = urllib2.urlopen('https://bootstrap.pypa.io/get-pip.py').read(); file('get_pip.py', 'w').write(get_pip)"
python get_pip.py
C:\Python27\Scripts\pip install -r requirements.txt
C:\Python27\Scripts\pyinstaller --onefile gulp.py
del get_pip.py
