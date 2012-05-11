
# Copyright George Notaras

REL_FILES = [
	'cc-configurator.php',
	'LICENSE',
	'NOTICE',
	'README',
    'screenshot-1.png',
    'uninstall.php',
]

PLUGIN_METADATA_FILE = 'cc-configurator.php'

POT_HEADER = """#  POT (Portable Object Template)
#
#  This file is part of the Creative-Commons-Configurator plugin for WordPress.
#
#  http://www.g-loaded.eu/2006/01/14/creative-commons-configurator-wordpress-plugin/
#
#  Copyright (C) 2006-2012 George Notaras <gnot@g-loaded.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
"""

# ==============================================================================

import sys
import os
import zipfile
import shutil
import subprocess

def get_name_release():
	def get_data(cur_line):
		return cur_line.split(':')[1].strip()
	f = open(PLUGIN_METADATA_FILE)
	name = ''
	release = ''
	for line in f:
		if line.lower().startswith('plugin name:'):
			name = get_data(line)
		elif line.lower().startswith('version:'):
			release = get_data(line)
		if name and release:
			break
	f.close()
	
	if not name:
		raise Exception('Cannot determine plugin name')
	elif not release:
		raise Exception('Cannot determine plugin version')
	else:
		# Replace spaces in name and convert it to lowercase
		name = name.replace(' ', '-')
		name = name.lower()
		return name, release

name, release = get_name_release()



# Translation
pot_domain = os.path.splitext(PLUGIN_METADATA_FILE)[0]

# Generate POT file
args = ['xgettext', '--default-domain=%s' % pot_domain, '--output=%s.pot' % pot_domain, '--language=PHP', '--from-code=UTF-8', '--keyword=__', '--keyword=_e', '--no-wrap', '--package-name=%s' % pot_domain, '--package-version=%s' % release, '--copyright-holder', 'George Notaras <gnot@g-loaded.eu>', '%s.php' % pot_domain]
p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()

# Replace POT Header

f = open('%s.pot' % pot_domain, 'r')
pot_lines = f.readlines()
f.close()
f = open('%s.pot' % pot_domain, 'w')
f.write(POT_HEADER)
for n, line in enumerate(pot_lines):
    if n < 4:
        continue
    f.write(line)
f.close()

# Because of the stupidity of the WordPress plugin registration system
# the plugin directory ends with ``-1``
name_release_dir = name + '-1'

# Create release dir and move release files inside it
os.mkdir(name_release_dir)
for p_file in REL_FILES:
	shutil.copy(p_file, os.path.join(name_release_dir, p_file))


# Create distribution package

d_package_path = '%s-%s.zip' % (name, release)
d_package = zipfile.ZipFile(d_package_path, 'w', zipfile.ZIP_DEFLATED)

for p_file in REL_FILES:
	d_package.write(os.path.join(name_release_dir, p_file))

d_package.testzip()

d_package.comment = 'Official packaging by CodeTRAX'

d_package.printdir()

d_package.close()


# Remove the release dir

shutil.rmtree(name_release_dir)

