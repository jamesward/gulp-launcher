# -*- mode: python -*-
a = Analysis(['gulp.py'],
             pathex=['C:\\GitHub\\gulp-launcher\\python'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='gulp.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
