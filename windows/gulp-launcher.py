# gulp-laucher for windows: run build.bat to turn into a standalone .exe file
import urllib2, os, sys, platform, json

ARCHITECTURE = platform.architecture()[0] # 64bit or 32bit

#def testclean(fname):
#    if os.path.exists(fname): os.remove(fname)
#testclean("package.json")
#testclean("gulpfile.js")

LAUNCHER_VERSION = "0.0.1"
BASE_LOCAL_DIR = "{HOME}\\gulp-launcher".format(HOME=os.getenv("APPDATA"))
print(BASE_LOCAL_DIR)

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

def answer_is_yes(prompt):
    response = raw_input(prompt + " [yes] ")
    return response == "" or response.startswith('y') or response.startswith('Y')

def ensure_file_exists(filename, newfile):
    if not os.path.exists(filename):
        print("You need to run gulp in a directory containing a " + filename + " file.")
        if answer_is_yes("Should one be created for you?"):
            file(filename, 'w').write(newfile)
        else:
            print("No " + filename + " found. Aborting.")

ensure_file_exists("package.json", package_json)
ensure_file_exists("gulpfile.js", gulpfile_js)

def get_raw_node_version():
    package = json.load(file("package.json"))
    return package['engines']['node']

print get_raw_node_version()

def get_node_version():
    if "NODE_VERSION" in globals(): return NODE_VERSION
    if get_raw_node_version() == "null":
        print("The Node version was not specified.")
        if answer_is_yes("Should the latest be used?"):
            NODE_VERSION=$(curl -s https://semver.io/node/stable)
    # else:
    #     # does the raw version need to be resolved because it contains: ^ x ~ < >
    #     if [ "${NODE_RAW_VERSION#*x}" != "$NODE_RAW_VERSION" ] ||
    #        [ "${NODE_RAW_VERSION#*~}" != "$NODE_RAW_VERSION" ] ||
    #        [ "${NODE_RAW_VERSION#*>}" != "$NODE_RAW_VERSION" ] ||
    #        [ "${NODE_RAW_VERSION#*<}" != "$NODE_RAW_VERSION" ] ||
    #        [ "${NODE_RAW_VERSION#*^}" != "$NODE_RAW_VERSION" ]:
    #           readonly NODE_VERSION=$(curl -m 10 -s https://semver.io/node/resolve/$NODE_RAW_VERSION)
    #     else:
    #        readonly NODE_VERSION=$NODE_RAW_VERSION

    # if [ -z $NODE_VERSION ]:
    #     print("Exiting because the Node version could not be determined.")
    #     print("Set a specific node version in the package.json file.")
    #     sys.exit()

