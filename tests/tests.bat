:: Test the Windows Gulp Launcher
@echo OFF

set BASEDIR=%~dp0
cd /d %BASEDIR%

set GULP_LAUNCHER_TRACE=1
set "GULP=..\..\python\dist\gulp.exe"

::
:: Tests
::

:: Node 0.10.x with a gulpfile
set "TEST=node_0.10.x"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"
if errorlevel 1 goto :eof

:: Gulp dep isn't set and we tell the gulp launcher not to add it
set "TEST=no_gulp_dep"
set "EXP=No Gulp dependency was found"
set "STDIN=no"
call :run_test "%TEST%" "%EXP%" "%STDIN%"
if errorlevel 1 goto :eof

:: Gulp dep isn't set and we tell the gulp launcher to add it
set "TEST=no_gulp_dep"
set "EXP=Starting 'help'"
set "STDIN=yes"
set "CLEAN=git checkout package.json"
call :run_test "%TEST%" "%EXP%" "%STDIN%" "%CLEAN%"
if errorlevel 1 goto :eof

:: Node engine isn't set and we tell the gulp launcher not to add it
set "TEST=no_node"
set "EXP=Exiting because the Node version could not be determined."
set "STDIN=no"
call :run_test "%TEST%" "%EXP%" "%STDIN%"
if errorlevel 1 goto :eof

:: Node engine isn't set and we tell the gulp launcher to add it
set "TEST=no_node"
set "EXP=Starting 'help'"
set "STDIN=yes"
set "CLEAN=git checkout package.json"
call :run_test "%TEST%" "%EXP%" "%STDIN%" "%CLEAN%"
if errorlevel 1 goto :eof

:: Node 0.10.x without a gulpfile and auto-add one
set "TEST=node_0.10.x_without_gulpfile"
set "EXP=Starting 'default'"
set "STDIN=yes"
set "CLEAN=rm gulpfile.js"
call :run_test "%TEST%" "%EXP%" "%STDIN%" "%CLEAN%"
if errorlevel 1 goto :eof

:: Node 0.10.x without a gulpfile but don't auto-add one
set "TEST=node_0.10.x_without_gulpfile"
set "EXP=No gulpfile.js found"
set "STDIN=no"
call :run_test "%TEST%" "%EXP%" "%STDIN%"
if errorlevel 1 goto :eof

:: Node 0.10.x without a package.json and auto-add one
set "TEST=node_0.10.x_without_package_json"
set "EXP=Starting 'default'"
set "STDIN=yes"
set "CLEAN=rm package.json"
call :run_test "%TEST%" "%EXP%" "%STDIN%" "%CLEAN%"
if errorlevel 1 goto :eof

:: Node 0.10.x without a package.json but don't auto-add one
set "TEST=node_0.10.x_without_package_json"
set "EXP=No package.json found"
set "STDIN=no"
call :run_test "%TEST%" "%EXP%" "%STDIN%"
if errorlevel 1 goto :eof

:: Node 0.10.x with a gulpfile
set "TEST=node_0.10.x"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"
if errorlevel 1 goto :eof

:: Node ~0.10.33
set "TEST=node_tilde0.10.33"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"
if errorlevel 1 goto :eof

:: Node ^0.10.33
set "TEST=node_carret0.10.33"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"
if errorlevel 1 goto :eof

:: Node 0.10.33
set "TEST=node_0.10.33"
set "EXP=Starting 'help'"
call :run_test "%TEST%" "%EXP%"
if errorlevel 1 goto :eof

:: Node 0.10.33 with a specified task
set "TEST=node_0.10.33"
set "EXP=Task 'asdf' is not in your gulpfile"
set "STDIN="
set "CLEAN="
set "ARGS=asdf"
call :run_test "%TEST%" "%EXP%" "%STDIN%" "%CLEAN%" "%ARGS%"
if errorlevel 1 goto :eof


goto :eof


:: Runs a test
::
:: Usage:
:: call :run_test base_dir expected_output [stdin] [cleanup] [args]
::
:run_test
  setlocal EnableDelayedExpansion
  set "DIR=%~1"
  set "EXPECTED=%~2"
  set "IN=%~3"
  set "CLEANUP=%~4"
  set "ARGS=%~5"

  set FAILED=true

  cd %DIR%

  if not defined IN (
    set "GULP_CMD=%GULP% %ARGS%"
  ) else (
    set "GULP_CMD=echo %IN% ^| %GULP% %ARGS%"
  )

  echo Running the %GULP_CMD% in %DIR%
  echo STDIN: %IN%
  echo Expected: %EXPECTED%
  echo.
  echo OUTPUT:
  echo.

  :: Run it once to get the output
  for /f "delims=" %%a in ('%GULP_CMD%') do (
    echo %%a
  )

  echo.

  if defined CLEANUP (
    call %CLEANUP%
  )
  
  :: Run it again to see if it passed
  for /f "delims=" %%a in ('%GULP_CMD% ^| FIND "%EXPECTED%"') do (
    set FAILED=false
  )

  if defined CLEANUP (
    call %CLEANUP%
  )

  cd ..

  if %FAILED% == true (
    echo Test failed!
    echo.
    exit /b 1
  ) else (
    echo Test passed!
    echo.
  )

  exit /b
:: end of run_test
