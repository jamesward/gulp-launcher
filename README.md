Gulp Launcher
=============

Automates the install of [gulp](http://gulpjs.com/) and its dependencies (Node, NPM, etc).  Like this (with nothing pre-installed):
```
$ ./gulp
Downloading jq 1.3 for x86_64 MAC
Downloading Node 0.10.33 for x86_64 MAC
... npm install output ...
[09:13:25] Using gulpfile ~/projects/gulp-starter/gulpfile.js
[09:13:25] Starting 'default'...
[09:13:25] Finished 'default' after 7.28 μs
```


Downloads
---------

Grab the latest `gulp` (Linux, Mac, and Cygwin) or `gulp.exe` (Windows) from [Releases](https://github.com/jamesward/gulp-launcher/releases).

Or if you don't have an existing gulp build, grab the [gulp-starter](https://github.com/jamesward/gulp-starter) project.


Usage
-----

Just run `gulp` and the launcher will download everything it needs and then run your Gulp build.  If run `gulp` in a directory that does not contain a `package.json` and `gulpfile.js` then you will be prompted to create them.

Windows Launcher Specifics
* Set a `GULP_LAUNCHER_TRACE` env var to enable trace output
* Set a `GULP_LAUNCHER_CLEANUP` env var to remove the downloaded files before running gulp (causing them to be re-downloaded)


Developer Info
--------------

[![Linux Build Status](https://travis-ci.com/jamesward/gulp-launcher.svg?branch=master)](https://travis-ci.com/jamesward/gulp-launcher)

[![Windows Build status](https://ci.appveyor.com/api/projects/status/0yui49am31q2i91i?svg=true)](https://ci.appveyor.com/project/jamesward/gulp-launcher)

Bash Version (Linux, Mac, and Cygwin)
* [Source](bash/gulp)
* No compile / build needed
* Run the tests: `cd tests; ./tests.sh ../../bash/gulp`

Python Version (Windows only right now)
* [Source](python/gulp.py)
* Compile on Windows with: `cd python; build.bat`
* Run the tests: `cd tests & bash tests.sh ../../python/dist/gulp.exe`

CI & Releases
* [AppVeyor](http://www.appveyor.com) builds the exe, runs the tests for both the bash (Cygwin) and the native launcher
* [Travis](https://travis-ci.org/) runs the tests for the bash launcher on Linux
