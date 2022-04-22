from selenium import webdriver
from time import sleep
import hashlib
import shutil
import glob
import os

# data_path = '/data/python-screenshots'
data_path = '.'

def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

html_body = "\
<style>\n\
* {\n\
  box-sizing: border-box;\n\
}\n\
\n\
.img-container {\n\
  float: left;\n\
  width: 20%;\n\
  padding: 5px;\n\
}\n\
\n\
.clearfix::after {\n\
  content: '';\n\
  clear: both;\n\
  display: table;\n\
}\n\
</style>\n\
<div class='clearfix'>\n\
\n"

sitelist = [ \
    'https://www.nu.nl', \
    'https://tweakers.net', \
    'https://nos.nl', \
    'https://scientias.nl/', \
    'https://rtlnieuws.nl/', \
    'https://python.org/', \
    'https://google.nl/', \
    'https://pypi.org/', \
    'https://www.redhat.com/en', \
    'https://www.ansible.com/', \
    'https://pypi.org/', \
]

driver = webdriver.Firefox()
while True:
    html = html_body
    for site in sitelist:
        driver.get(site)
        sleep(1)

        filename = "{}.png".format(site.split('/')[2].replace('.','-'))

        # first hash will fails always
        first_hash = '0'
        try:
            first_hash = md5('{}/{}'.format(data_path, filename))
        except:
            pass

        driver.get_screenshot_as_file('{}/{}'.format(data_path, filename))
        second_hash = md5('{}/{}'.format(data_path, filename))
        print(first_hash, '{}/{}'.format(data_path, filename))
        print(second_hash, '{}/{}'.format(data_path, filename))
        if first_hash != second_hash:
            print('file {}/{}) is different or did not exist'.format(data_path, filename))
            shutil.copyfile('{}/{}'.format(data_path, filename), '{}/images/{}'.format(data_path, filename))
    
    for file in glob.glob("*.png"):
        html += f"\n\
    <div class='img-container'>\n\
        <img src='{file}' style='width:100%'>\n\
        </div>\n\
    \n  "        
    html += f"</div>\n"

    outputfile = open("{}/images/index.html".format(data_path), "w")
    outputfile.write(html)
    outputfile.close()
        
    sleep(10)
driver.quit()
