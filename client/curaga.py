"""
# this project should be installable at curaga.com using a bash script like meteor
# server side should allow for packages to be uploaded or downloaded
# downloading and installing a package should leave no footprint
# package should be downloadable/installable from  curaga.com/packages/<package_name>/
# just like the package creator

# a package should just be some files and the knowledge of where to put them. use case is backing up bash profiles, ssh keys, etc

# example:
# to create a package
curl curaga.com/install.sh | /bin/sh
echo '{"files":["~/.bash_profile", "~/.ssh/config"], "name":"my_unique_name"}' > manifest.json
curaga --bundle manifest.json --name my_unique_name
# creates a file my_unique_name.curaga
curaga --upload my_unique_name.zip --username jhgaylor --password secret

# to install a package from curage
curl curage.com/packages/<package_name>/install.sh | /bin/sh
# installer will prompt for user credentials
# alternatively install via curaga
curage --install my_unique_name --username jhgaylor --password secret

# manifest describes which files to grab. should be an absolute path (~/.bash_profile)
# manifest format
# {name:STRING, files:{filename_in_package:absolute_file_path}}


# need to be able to uninstall
# packages should be installed to ~/.curaga_packages/
# and files should be linked. use a variation on
# https://github.com/sontek/dotfiles/blob/master/install.sh
"""

import argparse
import json
import os
import shutil
import zipfile
import requests

def zipdir(input_path, target_path):
    with zipfile.ZipFile(target_path, 'w') as zip:
        for root, dirs, files in os.walk(input_path):
            for file_path in files:
                zip.write(os.path.join(root, file_path))


def _collect_credentials(args, email=False):
    if args.username:
        username = args.username
    else:
        username = raw_input("Username: ")

    if args.password:
        password = args.password
    else:
        password = raw_input("Password: ")

    if args.email:
        email_address = args.email
    else:
        if email:
            email_address = raw_input("Email Address: ")

    if email:
        return username, password, email_address
    else:
        return username, password



def _copy_file(source, destination):
    print "Copying %s to %s" % (source, destination)
    shutil.copy(source, destination)

def bundle(args):
    manifest_filepath = args.bundle
    manifest_filename = os.path.basename(manifest_filepath)
    manifest_file = open(manifest_filepath)
    manifest_text = manifest_file.read()
    manifest_json = json.loads(manifest_text)
    bundle_name = manifest_json['name']
    bundle_file_map = manifest_json['files']
    bundle_zip_filepath = '%s.zip' % bundle_name
    bundle_working_path = os.path.join('./', bundle_name)

    # create a directory for the bundle. folder should be 
    if os.path.exists(bundle_working_path):
        print "Previous bundle failed. Please delete %s" % bundle_working_path
        return False
    else:
        print "Creating bundle working directory."
        os.makedirs(bundle_working_path)

    # copy the manifest into the working directory
    manifest_copy_path = os.path.join(bundle_working_path, manifest_filename)
    _copy_file(manifest_filepath, manifest_copy_path)

    # copy files listed in manifest
    for file_name, file_path in bundle_file_map.iteritems():
        source = os.path.expanduser(file_path)
        destination = os.path.join(bundle_working_path, file_name)
        _copy_file(source, destination)


    # create a .zip of the directory
    zipdir(bundle_working_path, bundle_zip_filepath)

    # cleanup working directory
    print "Deleting bundle working directory."
    shutil.rmtree(bundle_working_path)

    print args


def install(args):
    package_name = args.install

    # send a request to the server
    # execute some code


def register(args):
    username, password, email = _collect_credentials(args, email=True)
    data = {'username': username, 'password': password, 'email': email}

    url = "http://127.0.0.1:8000/register/"
    resp = requests.post(url, data=data)

    print resp.text
    # make a request to the server
    # confirm


def upload(args):
    username, password = _collect_credentials(args)
    data = {'username': username, 'password': password}

    files = {'package': open(args.upload, 'rb')}
    # url = 'http://httpbin.org/post'
    url = "http://127.0.0.1:8000/upload/"
    resp = requests.post(url, data=data, files=files)

    print resp.text
    # send the files to a server
    # confirm upload


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", "--bundle", help="creates a bundle from a manifest file")
    parser.add_argument("-i", "--install", help="install a bundle from the package server")
    parser.add_argument("-r", "--register", action="store_true", help="register a user with the package server")
    parser.add_argument("-u", "--upload", help="upload a bundle to the package server")
    parser.add_argument("-U", "--username", help="specify a username on the package server")
    parser.add_argument("-P", "--password", help="specify a password on the package server")
    parser.add_argument("-E", "--email", help="specify a password on the package server")
    args = parser.parse_args()

    if args.bundle:
        print "Preparing to bundle"
        bundle(args)


    if args.install:
        print "Preparing to install"
        install(args)


    if args.register:
        print "Preparing to register"
        register(args)


    if args.upload:
        print "Preparing to upload"
        upload(args)


