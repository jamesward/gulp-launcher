# gulp-laucher for windows: run build.bat to turn into a standalone .exe file
# before changing to config dictionary
import urllib2, os, sys, shutil, platform, json, argparse, tarfile

DEFAULT_NODE_VERSION = "0.10.33"
DEFAULT_NPM_VERSION = "1.4.12"
DEFAULT_GULP_VERSION = "3.8.10"
ARCHITECTURE = platform.architecture()[0] # 64bit or 32bit
LAUNCHER_VERSION = "0.0.1"
BASE_LOCAL_DIR = "{HOME}\\gulp-launcher".format(HOME=os.getenv("APPDATA"))

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--clean", action='store_true', help="Remove all artifacts and exit")
parser.add_argument("-t", "--trace", action='store_true', help="Display trace information")
args = parser.parse_args()

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
    DEFAULT_NODE_VERSION = DEFAULT_NODE_VERSION,
    DEFAULT_NPM_VERSION = DEFAULT_NPM_VERSION,
    DEFAULT_GULP_VERSION = DEFAULT_GULP_VERSION)

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

# Clean up all effects of running this program:
if args.clean:
    print "Cleaning up artifacts ...",
    def removeFile(fname):
        if os.path.exists(fname): os.remove(fname)
    removeFile("package.json")
    removeFile("gulpfile.js")
    if os.path.exists(BASE_LOCAL_DIR):
        shutil.rmtree(BASE_LOCAL_DIR, ignore_errors = True)
    print "done"
    sys.exit()

ensure_file_exists("package.json", package_json)
ensure_file_exists("gulpfile.js", gulpfile_js)

def get_raw_node_version():
    package = json.load(file("package.json"))
    if package.has_key('engines') and package.has_key('node'):
        return package['engines']['node']
    return None

if args.trace:
    print get_raw_node_version()

def get_node_version():
    if "NODE_VERSION" in globals():
        return NODE_VERSION
    if not get_raw_node_version():
        print("The Node version was not specified.")
        if answer_is_yes("Should the latest be used?"):
            NODE_VERSION = urllib2.urlopen("https://semver.io/node/stable").read()
        else:
            print("Exiting because the Node version could not be determined.")
            print("Set a specific node version in the package.json file.")
            sys.exit()
    else:
        nrv = get_raw_node_version()
        if any([c in nrv for c in "^x~<>"]):
            NODE_VERSION = urllib2.urlopen("https://semver.io/node/resolve/" + nrv).read()
        else:
            NODE_VERSION = get_raw_node_version()

    if "NODE_VERSION" not in globals():
        NODE_VERSION = urllib2.urlopen("https://semver.io/node/stable").read()

    return NODE_VERSION


def download_node_binary():
    NODE_VERSION = get_node_version()
    NODE_DIR = BASE_LOCAL_DIR + "\\tools\\node-" + NODE_VERSION

    if platform.system() == "Windows":
        NODE_BIN = NODE_DIR + "\\node.exe"
        NPM_BIN="{NODE_DIR}\\node_modules\\npm\\cli.js".format(NODE_BIN=NODE_BIN, NODE_DIR=NODE_DIR)
        if ARCHITECTURE == "32bit":
            # I assume this is the right one for 32bit. There's also node-v0.10.33-x86.msi
            NODE_DOWNLOAD_PATH = "/dist/v{NODE_VERSION}/node.exe".format(NODE_VERSION=NODE_VERSION)
        if ARCHITECTURE == "64bit":
            # There's also https://nodejs.org/dist/v0.10.33/x64/node-v0.10.33-x64.msi
            NODE_DOWNLOAD_PATH = "/dist/v{NODE_VERSION}/x64/node.exe".format(NODE_VERSION=NODE_VERSION)

    if args.trace:
        print "NODE_VERSION:", NODE_VERSION
        print "NODE_DIR:", NODE_DIR
        print "NODE_BIN:", NODE_BIN
        print "NODE_DOWNLOAD_PATH:", NODE_DOWNLOAD_PATH
        print "NPM_BIN:", NPM_BIN

    NODE_HOST="nodejs.org"

    if not os.path.exists(NODE_BIN):
        if not os.path.exists(NODE_DIR):
            os.makedirs(NODE_DIR)

        if platform.system() == "Windows":
            print("Downloading Node {NODE_VERSION} for {ARCHITECTURE} {OS}".format(
                NODE_VERSION=NODE_VERSION, ARCHITECTURE=ARCHITECTURE, OS=platform.system()))
            #$(curl -s -o $NODE_BIN https://$NODE_HOST$NODE_DOWNLOAD_PATH)
            url = "https://{NODE_HOST}{NODE_DOWNLOAD_PATH}".format(
                    NODE_HOST=NODE_HOST, NODE_DOWNLOAD_PATH=NODE_DOWNLOAD_PATH)
            if args.trace:
                print url
            file(NODE_BIN, 'wb').write(urllib2.urlopen(url).read())

    if not os.path.exists(NPM_BIN):
        if not os.path.exists(NODE_DIR):
            os.makedirs(NODE_DIR)

        if platform.system() == "Windows":
            print("Downloading npm {DEFAULT_NPM_VERSION} for {ARCHITECTURE} {OS}".format(
                DEFAULT_NPM_VERSION=DEFAULT_NPM_VERSION, ARCHITECTURE=ARCHITECTURE, OS=platform.system()))
            url = "http://{NODE_HOST}/dist/npm/npm-{DEFAULT_NPM_VERSION}.tgz".format(
                      NODE_HOST=NODE_HOST, DEFAULT_NPM_VERSION=DEFAULT_NPM_VERSION)
            if args.trace:
                print url
            file(NODE_DIR + "\\npm.tgz", 'wb').write(urllib2.urlopen(url).read())
            tarfile.open(NODE_DIR + "\\npm.tgz", "r:gz").extractall(os.path.join(NODE_DIR, "node_modules"))
            # $(rm $NODE_DIR/npm.tgz) # This is a small file so I'm leaving it for now

download_node_binary()
