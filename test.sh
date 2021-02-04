#!/bin/bash

./vimwiki_markdown.py \
    0 \
    markdown \
    .md \
    $(pwd) \
    /home/stefantb/Dropbox/Documents/Notes/workwiki/M1200.md \
    style.css \
    $(pwd) \
    efault \
    .tpl \
    - \
    "{\
\"css_files\":\"\
/home/stefantb/Dropbox/Documents/Notes/workwiki/html/style.css:css/style.css\
,/home/stefantb/Dropbox/Documents/Notes/workwiki/html/style.css\
\"\
}"
