from __future__ import absolute_import
from __future__ import unicode_literals

__author__ = "knarfeh@outlook.com"

def get_template_content(file_path):
    with open(file_path) as f:
        content = f.read()
        f.close()
        return content
