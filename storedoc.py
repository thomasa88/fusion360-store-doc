#!/usr/bin/python3

import shutil
import os
import re
import subprocess

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

TMP_FILE = 'tmp.md'
README = 'README.md'
OUT_FILE = 'store.html'

LINK_NAME = re.compile(r'\[(.*?)\]\(.*?\)')
H2 = re.compile(r'^## (.+)')
H3 = re.compile(r'^### (.+)')
IMAGE = re.compile(r'(!\[.*?\]\((.+?)\))')
INTERNAL_LINK = re.compile(r'\[(.*?)\]\(#.*?\)')
LOCAL_LINK = re.compile(r'(?<!!)\[(.*?)\]\([^:]+?\)')
CODE = re.compile(r'`(.*?)`')
INTRO_POST = """This add-in is free, but if you like it, you can [buy me a coffee (Ko-fi link)](https://ko-fi.com/thomasa88).

&nbsp;

The add-in is licensed under the MIT license.

"""

def code_format(string):
    return '<span class=code>' + code_escape(string) + '</span>'

def code_escape(string):
    return string.replace('_', r'\_').replace('*', '\*')

INTRO = 1
CONTENT = 2
CHANGELOG = 3
part = INTRO
with open(README, 'r') as readme:
    with open(TMP_FILE, 'w') as tmp:
        tmp.write('Chrome is better at retaining table formatting than Firefox!\n\n')
        
        for line in readme:
            if part == INTRO and line.startswith('##'):
                part = CONTENT
                line = INTRO_POST + line
            if line.startswith('## Changelog'):
                part = CHANGELOG
                tmp.write('<pre>')

            # Short description needs double newlines to create paragraphs
            if part == INTRO:
                line = IMAGE.sub(r'', line)
                if line.strip() == '':
                    line += '\r\n&nbsp;\r\n\r\n'
            elif part == CHANGELOG:
                line = LINK_NAME.sub(r'\1', line)
                line = line.replace('`', '"')
                first_asterisk = line.find('*')
                line = (line[0:first_asterisk+1] +
                        line[first_asterisk+1:].replace('*', '"'))
                
            line = H2.sub(r'**\1**', line)
            line = H3.sub(r'<br><u>\1</u>', line)
            # TODO: Turn images into embeeded resources.
            line = IMAGE.sub(r'<span style="background: red;">\1 \2</span>', line)
            line = INTERNAL_LINK.sub(r'*\1*', line)
            line = LOCAL_LINK.sub(r'<span style="background: red;">\1<span>', line)

            # Code tags look super big in the store

            line = CODE.sub(lambda m: code_format(m.group(1)), line)

            tmp.write(line)
        tmp.write('</pre>')

        tmp.write(
"""
**Additional Information**

This add-in is free, but if you like it, you can [buy me a coffee (Ko-fi link)](https://ko-fi.com/thomasa88).

The add-in is licensed under the MIT license.

<u>Disclaimer</u>

The software is provided "as is", without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose and non-infringement. In no event shall the authors or copyright holders be liable for any claim, damages, or other liability, whether in an action of contract, tort or otherwise, arising from, out of or in connection with the software or the use or other dealings in the software.

**Support Information**

Feel free to send an e-mail if there are problems with the add-in, or even better, report them <span style="background: red;">FIX URL:</span> [here](https://github.com/thomasa88/PROJECT/issues). Please describe exactly what to do to trigger the problem. Also, include any error messages.
"""
)
        
subprocess.check_call(['pandoc',
                       '--css', 'store.css',
                       '-s',
                       '--metadata', 'pagetitle="README"',
                       '-fmarkdown-implicit_figures',
                       '-o', OUT_FILE,
                       TMP_FILE])
shutil.copy(f'{SCRIPT_DIR}/store.css', 'store.css')
