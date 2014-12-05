Gulp Launcher
=============

Automates the install of gulp and its dependencies.

Downloads
---------

TODO


Usage
-----

Just run `gulp` and the launcher will download everything it needs and then run your Gulp build.  If run `gulp` in a directory that does not contain a `package.json` and `gulpfile.js` then you will be prompted to create them.

Windows Launcher Specifics
* Set a `GULP_LAUNCHER_TRACE` env var to enable trace output
* Set a `GULP_LAUNCHER_CLEANUP` env var to remove the downloaded files before running gulp (causing them to be re-downloaded)


Developer Info
--------------

[![Linux Build Status](https://travis-ci.org/jamesward/gulp-launcher.svg?branch=master)](https://travis-ci.org/jamesward/gulp-launcher)

[![Windows Build status](https://ci.appveyor.com/api/projects/status/0yui49am31q2i91i?svg=true)](https://ci.appveyor.com/project/jamesward/gulp-launcher)

Bash Version (Linux, Mac, and Cygwin)
* [Source](bash/gulp)
* No compile / build needed
* Run the tests: `tests/tests.sh`

Python Version (Windows only right now)
* [Source](python/gulp.py)
* Compile on Windows with: `cd python; build.bat`
* Run the tests: `tests\tests.bat`

CI & Releases
* [AppVeyor](http://www.appveyor.com) builds the exe, runs the tests for both the bash (Cygwin) and the native launcher
* [Travis](https://travis-ci.org/) runs the tests for the bash launcher on Linux
