import urllib2, os
def testclean(fname):
    if os.path.exists(fname): os.remove(fname) 
testclean("package.json")
testclean("gulpfile.js")

LAUNCHER_VERSION = "0.0.1"
JQ_VERSION = "1.3"
BASE_LOCAL_DIR = "$HOME/.gulp-launcher"

package_json = """\
{{
  "name": "YOUR_PROJECT_NAME",
  "version": "0.0.0",
  "description": "YOUR PROJECT DESCRIPTION",
  "devDependencies": {{
    "gulp": "{DEFAULT_GULP_VERSION}"
  }},
  "engines": {{
    "node": "{DEFAULT_NODE_VERSION}",
    "npm": "{DEFAULT_NPM_VERSION}"
  }}
}}
""".format(
        DEFAULT_NODE_VERSION = "0.10.33",
        DEFAULT_NPM_VERSION = "1.4.12",
        DEFAULT_GULP_VERSION = "3.8.10")

gulpfile_js = """\
var gulp = require('gulp');

gulp.task('default', function() {
  // place code for your default task here
});
"""

def ensure_file_exists(filename, newfile):
    if not os.path.exists(filename):
        print("You need to run gulp in a directory containing a " + filename + " file.")
        response = raw_input("Should one be created for you? [yes] ")
        if response == "" or response.startswith('y') or response.startswith('Y'):
            file(filename, 'w').write(newfile)
        else:
            print("No " + filename + " found. Aborting.")

ensure_file_exists("package.json", package_json)
ensure_file_exists("gulpfile.js", gulpfile_js)

