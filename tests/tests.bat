:: Test the Windows Gulp Launcher
@echo OFF

set BASEDIR=%~dp0
cd /d %BASEDIR%

set "GULP=..\..\windows\dist\gulp-launcher.exe"

::
:: Tests
::

:: Node 0.10.x with a gulpfile
set "TEST=node_0.10.x"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"


goto End


:: Runs a test
::
:: Usage:
:: call :run_test base_dir expected_output [stdin] [cleanup]
::
:run_test
  setlocal EnableDelayedExpansion
  set "DIR=%~1"
  set "EXPECTED=%~2"
  set "IN=%~3"
  set "CLEANUP=%~4"

  echo Running the gulp launcher in %DIR%
  echo IN: %IN%

  :: start fresh
  rmdir /s /q %APPDATA%\gulp-launcher >nul 2>&1
  rmdir /s /q %DIR%\node_modules >nul 2>&1

  cd %DIR%

  echo Expected:
  echo.
  echo %EXPECTED%
  echo.

  echo OUTPUT:
  echo.

  set FAILED=true

  if not defined IN (
    set "GULP_CMD=%GULP%"
  ) else (
    set "GULP_CMD=%GULP% ^< %IN%"
  )

  echo Running: %GULP_CMD%

  for /f "delims=" %%a in ('%GULP_CMD% ^| FIND "%EXPECTED%"') do (
    set FAILED=false
  )

  echo.

  if defined CLEANUP (
    call %CLEANUP%
  )

  cd ..

  if %FAILED% == true (
    echo Test failed!
    exit /b 1
  ) else (
    echo Test passed!
  )

  exit /b
:: end of run_test

:End