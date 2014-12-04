# gulp-laucher for windows: run build.bat to turn into a standalone .exe file
# before changing to config dictionary
import urllib2, os, sys, shutil, platform, json, argparse, tarfile, pprint

cf = dict( # Configuration dictionary
    NODE_VERSION = None,
    NODE_BIN = None,
    NPM_BIN = None,
    NODE_DOWNLOAD_PATH = None,
    NODE_HOST="nodejs.org",
    DEFAULT_NODE_VERSION = "0.10.33",
    DEFAULT_NPM_VERSION = "1.4.12",
    DEFAULT_GULP_VERSION = "3.8.10",
    OS = platform.system(),
    ARCHITECTURE = platform.architecture()[0], # 64bit or 32bit
    LAUNCHER_VERSION = "0.0.1",
    BASE_LOCAL_DIR = "{HOME}\\gulp-launcher".format(HOME=os.getenv("APPDATA")),
)

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
""".format(**cf)

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
    if os.path.exists(cf["BASE_LOCAL_DIR"]):
        shutil.rmtree(cf["BASE_LOCAL_DIR"], ignore_errors = True)
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
    if cf["NODE_VERSION"]:
        return cf["NODE_VERSION"]
    if not get_raw_node_version():
        print("The Node version was not specified.")
        if answer_is_yes("Should the latest be used?"):
            cf["NODE_VERSION"] = urllib2.urlopen("https://semver.io/node/stable").read()
        else:
            print("Exiting because the Node version could not be determined.")
            print("Set a specific node version in the package.json file.")
            sys.exit()
    else:
        nrv = get_raw_node_version()
        if any([c in nrv for c in "^x~<>"]):
            cf["NODE_VERSION"] = urllib2.urlopen("https://semver.io/node/resolve/" + nrv).read()
        else:
            cf["NODE_VERSION"] = get_raw_node_version()

    if cf["NODE_VERSION"]:
        cf["NODE_VERSION"] = urllib2.urlopen("https://semver.io/node/stable").read()

    return cf["NODE_VERSION"]


def download_node_binary():
    cf["NODE_VERSION"] = get_node_version()
    cf["NODE_DIR"] = cf["BASE_LOCAL_DIR"] + "\\tools\\node-" + cf["NODE_VERSION"]

    if platform.system() == "Windows":
        cf["NODE_BIN"] = cf["NODE_DIR"] + "\\node.exe"
        cf["NPM_BIN"]="{NODE_DIR}\\node_modules\\npm\\cli.js".format(**cf)
        if cf["ARCHITECTURE"] == "32bit":
            # I assume this is the right one for 32bit. There's also node-v0.10.33-x86.msi
            cf["NODE_DOWNLOAD_PATH"] = "/dist/v{NODE_VERSION}/node.exe".format(**cf)
        if cf["ARCHITECTURE"] == "64bit":
            # There's also https://nodejs.org/dist/v0.10.33/x64/node-v0.10.33-x64.msi
            cf["NODE_DOWNLOAD_PATH"] = "/dist/v{NODE_VERSION}/x64/node.exe".format(**cf)

    if args.trace:
        pprint.pprint(cf)

    if not os.path.exists(cf["NODE_BIN"]):
        if not os.path.exists(cf["NODE_DIR"]):
            os.makedirs(cf["NODE_DIR"])

        if platform.system() == "Windows":
            print("Downloading Node {NODE_VERSION} for {ARCHITECTURE} {OS}".format(**cf))
            #$(curl -s -o $NODE_BIN https://$NODE_HOST$NODE_DOWNLOAD_PATH)
            url = "https://{NODE_HOST}{NODE_DOWNLOAD_PATH}".format(**cf)
            if args.trace:
                print url
            file(cf["NODE_BIN"], 'wb').write(urllib2.urlopen(url).read())

    if not os.path.exists(cf["NPM_BIN"]):
        if not os.path.exists(cf["NODE_DIR"]):
            os.makedirs(cf["NODE_DIR"])

        if platform.system() == "Windows":
            print("Downloading npm {DEFAULT_NPM_VERSION} for {ARCHITECTURE} {OS}".format(**cf))
            url = "http://{NODE_HOST}/dist/npm/npm-{DEFAULT_NPM_VERSION}.tgz".format(**cf)
            if args.trace:
                print url
            file(cf["NODE_DIR"] + "\\npm.tgz", 'wb').write(urllib2.urlopen(url).read())
            tarfile.open(cf["NODE_DIR"] + "\\npm.tgz", "r:gz").extractall(os.path.join(cf["NODE_DIR"], "node_modules"))

download_node_binary()
