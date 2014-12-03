:: Test the gulp.bat script
@echo OFF

set BASEDIR=%~dp0
cd /d %BASEDIR%

set GULP=..\..\gulp.bat

::
:: Tests
::

:: Node 0.10.x with a gulpfile
set TEST=node_0.10.x
set EXP=Starting 'help'
call :run_test %TEST% %EXP%
goto :eof


:: Runs a test
::
:: Usage:
:: call :run_test base_dir expected_output [stdin] [cleanup]
::
:run_test
  setlocal EnableDelayedExpansion
  set DIR=%1
  set EXPECTED=%2
  set IN=%3
  set CLEANUP=%4

  echo Running the gulp launcher in %DIR%
  echo IN: %IN%

  :: start fresh
  rmdir /s /q %APPDATA%\gulp-launcher >nul 2>&1
  rmdir /s /q %DIR%\node_modules >nul 2>&1

  cd %DIR%

  if not defined %IN% (
    for /f "delims=" %%a in ('%GULP%') do set OUTPUT=%%a
    exit /b
  ) else (
    for /f "delims=" %%a in ('%GULP% < %IN%') do set OUTPUT=%%a
    exit /b
  )

  cd ..

  if defined %CLEANUP% (
    %CLEANUP%
    exit /b
  )

  echo Output:
  echo.
  echo %OUTPUT%
  echo.

  echo Expected:
  echo.
  echo %EXPECTED%%
  echo.

  if /i not "!OUTPUT:%EXPECTED%=!" == "%OUTPUT%" (
    echo Test passed!
    exit /b
  ) else (
    echo Test failed!
    exit
  )

  exit /b
:: end of run_test
