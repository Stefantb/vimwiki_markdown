#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import datetime
import os
import shutil
import subprocess
import sys
import json
import textwrap
import markdown
from typing import Dict, Tuple, Optional
from pathlib import Path


#******************************************************************************
#
#******************************************************************************
default_template = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8" />
        <meta name="date" content="%date%" scheme="YYYY-MM-DD">
        <meta name="viewport" content="width=device-width" />
        <title>%title%</title>
        <link rel="Stylesheet" href="%root_path%css/default_style.css" type="text/css"
         media="screen" title="no title" charset="utf-8">
    </head>
    <body>
    <a href="%root_path%index.html">Index</a> |
    <a href="%root_path%diary/diary.html">Diary</a>
    <hr>
    <div class="content">
%content%
    </div>
    </body>
</html>
"""


#******************************************************************************
#
#******************************************************************************
default_css = """
body {font-family: Tahoma, Geneva, sans-serif; margin: 1em 2em 1em 2em; font-size: 100%; line-height: 130%;max-width:50rem;margin:auto;background:#252525;color:darkgray;padding-bottom:10rem;}
h1, h2, h3, h4, h5, h6 {font-family: Trebuchet MS, Helvetica, sans-serif; font-weight: bold; line-height:100%; margin-top: 1.5em; margin-bottom: 0.5em;}
h1 {font-size: 2.6em; color: #909090;}
h2 {font-size: 2.2em; color: #909090;}
h3 {font-size: 1.8em; color: #909090;}
h4 {font-size: 1.4em; color: #909090;}
h5 {font-size: 1.3em; color: #989898;}
h6 {font-size: 1.2em; color: #9c9c9c;}
p, pre, blockquote, table, ul, ol, dl {margin-top: 1em; margin-bottom: 1em;}
strong {color: orangered;}
ul ul, ul ol, ol ol, ol ul {margin-top: 0.5em; margin-bottom: 0.5em;}
li {margin: 0.3em auto;}
ul {margin-left: 2em; padding-left: 0.5em;}
dt {font-weight: bold;}
a {color: #3296c8;text-decoration: none;}
img {border: none;}
pre {padding: 0.5em 1rem;box-shadow: 0px 0px 1px 0px rgba(0,0,0,0.75);}
.codehilite, pre {border-radius:1%};
blockquote {padding: 0.4em; background-color: #f6f5eb;}
th, td {border: 1px solid #ccc; padding: 0.3em;}
th {background-color: #f0f0f0;}
hr {border: none; border-top: 1px solid #ccc; width: 100%;}
del {text-decoration: line-through; color: #777777;}
.toc li {list-style-type: none;}
.todo {font-weight: bold; background-color: #f0ece8; color: #a03020;}
.justleft {text-align: left;}
.justright {text-align: right;}
.justcenter {text-align: center;}
.center {margin-left: auto; margin-right: auto;}
.tag {background-color: #eeeeee; font-family: monospace; padding: 2px;}

/* classes for items of todo lists */
.rejected {
    /* list-style: none; */
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAMAAAAMCGV4AAAACXBIWXMAAADFAAAAxQEdzbqoAAAAB3RJTUUH4QgEFhAtuWgv9wAAAPZQTFRFmpqam5iYnJaWnJeXnpSUn5OTopCQpoqKpouLp4iIqIiIrYCAt3V1vW1tv2xsmZmZmpeXnpKS/x4e/x8f/yAg/yIi/yQk/yUl/yYm/ygo/ykp/yws/zAw/zIy/zMz/zQ0/zU1/zY2/zw8/0BA/0ZG/0pK/1FR/1JS/1NT/1RU/1VV/1ZW/1dX/1pa/15e/19f/2Zm/2lp/21t/25u/3R0/3p6/4CA/4GB/4SE/4iI/46O/4+P/52d/6am/6ur/66u/7Oz/7S0/7e3/87O/9fX/9zc/93d/+Dg/+vr/+3t/+/v//Dw//Ly//X1//f3//n5//z8////gzaKowAAAA90Uk5T/Pz8/Pz8/Pz8/Pz8/f39ppQKWQAAAAFiS0dEEnu8bAAAAACuSURBVAhbPY9ZF4FQFEZPSKbIMmWep4gMGTKLkIv6/3/GPbfF97b3w17rA0kQOPgvAeHW6uJ6+5h7HqLdwowgOzejXRXBdx6UdSru216xuOMBHHNU0clTzeSUA6EhF8V8kqroluMiU6HKcuf4phGPr1o2q9kYZWwNq1qfRRmTaXpqsyjj17KkWCxKBUBgXWueHIyiAIg18gsse4KHkLF5IKIY10WQgv7fOy4ST34BRiopZ8WLNrgAAAAASUVORK5CYII=);
    background-repeat: no-repeat;
    background-position: 0 .2em;
    padding-left: 1.5em;
}
.done0 {
    /* list-style: none; */
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAxQAAAMUBHc26qAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAA7SURBVCiR7dMxEgAgCANBI3yVRzF5KxNbW6wsuH7LQ2YKQK1mkswBVERYF5Os3UV3gwd/jF2SkXy66gAZkxS6BniubAAAAABJRU5ErkJggg==);
    background-repeat: no-repeat;
    background-position: 0 .2em;
    padding-left: 1.5em;
}
.done1 {
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAxQAAAMUBHc26qAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABtSURBVCiR1ZO7DYAwDER9BDmTeZQMFXmUbGYpOjrEryA0wOvO8itOslFrJYAug5BMM4BeSkmjsrv3aVTa8p48Xw1JSkSsWVUFwD05IqS1tmYzk5zzae9jnVVVzGyXb8sALjse+euRkEzu/uirFomVIdDGOLjuAAAAAElFTkSuQmCC);
    background-repeat: no-repeat;
    background-position: 0 .15em;
    padding-left: 1.5em;
}
.done2 {
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAxQAAAMUBHc26qAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAB1SURBVCiRzdO5DcAgDAVQGxjAYgTvxlDIu1FTIRYAp8qlFISkSH7l5kk+ZIwxKiI2mIyqWoeILYRgZ7GINDOLjnmF3VqklKCUMgTee2DmM661Qs55iI3Zm/1u5h9sm4ig9z4ERHTFzLyd4G4+nFlVrYg8+qoF/c0kdpeMsmcAAAAASUVORK5CYII=);
    background-repeat: no-repeat;
    background-position: 0 .15em;
    padding-left: 1.5em;
}
.done3 {
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA8AAAAPCAYAAAA71pVKAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAxQAAAMUBHc26qAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAABoSURBVCiR7dOxDcAgDATA/0DtUdiKoZC3YhLkHjkVKF3idJHiztKfvrHZWnOSE8Fx95RJzlprimJVnXktvXeY2S0SEZRSAAAbmxnGGKH2I5T+8VfxPhIReQSuuY3XyYWa3T2p6quvOgGrvSFGlewuUAAAAABJRU5ErkJggg==);
    background-repeat: no-repeat;
    background-position: 0 .15em;
    padding-left: 1.5em;
}
.done4 {
    background-image: url(data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABIAAAAQCAYAAAAbBi9cAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAAzgAAAM4BlP6ToAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAIISURBVDiNnZQ9SFtRFMd/773kpTaGJoQk1im4VDpWQcTNODhkFBcVTCNCF0NWyeDiIIiCm82QoIMIUkHUxcFBg1SEQoZszSat6cdTn1qNue92CMbEr9Sey+XC/Z/zu+f8h6ukUil3sVg0+M+4cFxk42/jH2wAqqqKSCSiPQdwcHHAnDHH9s/tN1h8V28ETdP+eU8fT9Nt62ancYdIPvJNtsu87bmjrJlrTDVM4RROJs1JrHPrD4Bar7A6cpc54iKOaTdJXCUI2UMVrQZ0Js7YPN18ECKkYNQcJe/OE/4dZsw7VqNXQMvHy3QZXQypQ6ycrtwDjf8aJ+PNEDSCzLpn7+m2pD8ZKHlKarYhy6XjEoCYGcN95qansQeA3fNdki+SaJZGTMQIOoL3W/Z89rxv+tokubNajlvk/vm+LFpF2XnUKZHI0I+QrI7Dw0OZTqdzUkpsM7mZTyfy5OPGyw1tK7AFSvmB/Ks8w8YwbUYbe6/3QEKv0vugfxWPnMLJun+d/kI/WLdizpNjMbAIKrhMF4OuwadBALqqs+RfInwUvuNi+fBd+wjogfogAFVRmffO02q01mZZ0HHdgXIzdz0QQLPezIQygX6llxNKKgOFARYCC49CqhoHIUTlss/Vx2phlYwjw8j1CAlfAiwQiJpiy7o1VHnsG5FISkoJu7Q/2YmmaV+i0ei7v38L2CBguSi5AAAAAElFTkSuQmCC);
    background-repeat: no-repeat;
    background-position: 0 .15em;
    padding-left: 1.5em;
}

code {
    font-family: Monaco,"Courier New","DejaVu Sans Mono","Bitstream Vera Sans Mono",monospace;
    -webkit-border-radius: 1px;
    -moz-border-radius: 1px;
    border-radius: 6px;
    -moz-background-clip: padding;
    -webkit-background-clip: padding-box;
    background-clip: padding-box;
    padding: 0px 3px;
    display: inline-block;
    color: #e8e8e8;
    border: 1px solid rgba(255, 255, 255, .1) !important;
}

code {
    border-radius: 6px;
    background-color: #3c2e2e;
}
.codehilite code {
    border-radius: 1px;
    background-color: #272822;
}

img {
    max-width: 80%;
}

.codehilite .hll { background-color: #49483e }
.codehilite  { background: #272822; color: #f8f8f2 }
.codehilite .c { color: #75715e } /* Comment */
.codehilite .err { color: #960050; background-color: #1e0010 } /* Error */
.codehilite .k { color: #66d9ef } /* Keyword */
.codehilite .l { color: #ae81ff } /* Literal */
.codehilite .n { color: #f8f8f2 } /* Name */
.codehilite .o { color: #f92672 } /* Operator */
.codehilite .p { color: #f8f8f2 } /* Punctuation */
.codehilite .ch { color: #75715e } /* Comment.Hashbang */
.codehilite .cm { color: #75715e } /* Comment.Multiline */
.codehilite .cp { color: #75715e } /* Comment.Preproc */
.codehilite .cpf { color: #75715e } /* Comment.PreprocFile */
.codehilite .c1 { color: #75715e } /* Comment.Single */
.codehilite .cs { color: #75715e } /* Comment.Special */
.codehilite .gd { color: #f92672 } /* Generic.Deleted */
.codehilite .ge { font-style: italic } /* Generic.Emph */
.codehilite .gi { color: #a6e22e } /* Generic.Inserted */
.codehilite .gs { font-weight: bold } /* Generic.Strong */
.codehilite .gu { color: #75715e } /* Generic.Subheading */
.codehilite .kc { color: #66d9ef } /* Keyword.Constant */
.codehilite .kd { color: #66d9ef } /* Keyword.Declaration */
.codehilite .kn { color: #f92672 } /* Keyword.Namespace */
.codehilite .kp { color: #66d9ef } /* Keyword.Pseudo */
.codehilite .kr { color: #66d9ef } /* Keyword.Reserved */
.codehilite .kt { color: #66d9ef } /* Keyword.Type */
.codehilite .ld { color: #e6db74 } /* Literal.Date */
.codehilite .m { color: #ae81ff } /* Literal.Number */
.codehilite .s { color: #e6db74 } /* Literal.String */
.codehilite .na { color: #a6e22e } /* Name.Attribute */
.codehilite .nb { color: #f8f8f2 } /* Name.Builtin */
.codehilite .nc { color: #a6e22e } /* Name.Class */
.codehilite .no { color: #66d9ef } /* Name.Constant */
.codehilite .nd { color: #a6e22e } /* Name.Decorator */
.codehilite .ni { color: #f8f8f2 } /* Name.Entity */
.codehilite .ne { color: #a6e22e } /* Name.Exception */
.codehilite .nf { color: #a6e22e } /* Name.Function */
.codehilite .nl { color: #f8f8f2 } /* Name.Label */
.codehilite .nn { color: #f8f8f2 } /* Name.Namespace */
.codehilite .nx { color: #a6e22e } /* Name.Other */
.codehilite .py { color: #f8f8f2 } /* Name.Property */
.codehilite .nt { color: #f92672 } /* Name.Tag */
.codehilite .nv { color: #f8f8f2 } /* Name.Variable */
.codehilite .ow { color: #f92672 } /* Operator.Word */
.codehilite .w { color: #f8f8f2 } /* Text.Whitespace */
.codehilite .mb { color: #ae81ff } /* Literal.Number.Bin */
.codehilite .mf { color: #ae81ff } /* Literal.Number.Float */
.codehilite .mh { color: #ae81ff } /* Literal.Number.Hex */
.codehilite .mi { color: #ae81ff } /* Literal.Number.Integer */
.codehilite .mo { color: #ae81ff } /* Literal.Number.Oct */
.codehilite .sa { color: #e6db74 } /* Literal.String.Affix */
.codehilite .sb { color: #e6db74 } /* Literal.String.Backtick */
.codehilite .sc { color: #e6db74 } /* Literal.String.Char */
.codehilite .dl { color: #e6db74 } /* Literal.String.Delimiter */
.codehilite .sd { color: #e6db74 } /* Literal.String.Doc */
.codehilite .s2 { color: #e6db74 } /* Literal.String.Double */
.codehilite .se { color: #ae81ff } /* Literal.String.Escape */
.codehilite .sh { color: #e6db74 } /* Literal.String.Heredoc */
.codehilite .si { color: #e6db74 } /* Literal.String.Interpol */
.codehilite .sx { color: #e6db74 } /* Literal.String.Other */
.codehilite .sr { color: #e6db74 } /* Literal.String.Regex */
.codehilite .s1 { color: #e6db74 } /* Literal.String.Single */
.codehilite .ss { color: #e6db74 } /* Literal.String.Symbol */
.codehilite .bp { color: #f8f8f2 } /* Name.Builtin.Pseudo */
.codehilite .fm { color: #a6e22e } /* Name.Function.Magic */
.codehilite .vc { color: #f8f8f2 } /* Name.Variable.Class */
.codehilite .vg { color: #f8f8f2 } /* Name.Variable.Global */
.codehilite .vi { color: #f8f8f2 } /* Name.Variable.Instance */
.codehilite .vm { color: #f8f8f2 } /* Name.Variable.Magic */
.codehilite .il { color: #ae81ff } /* Literal.Number.Integer.Long */
"""


#******************************************************************************
#
#******************************************************************************
def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


#******************************************************************************
#
#******************************************************************************
def copy_if_newer(src, dst):
    # print(f'would be copying {src} -> {dst}')
    # return
    if not dst.exists() or (src.stat().st_mtime - dst.stat().st_mtime > 0):
        shutil.copy2(src, dst)


#******************************************************************************
#
#******************************************************************************
def write_to_file(output_file: Path, content: str):
    with open(output_file, 'w') as o:
        o.write(content)


#******************************************************************************
#
#******************************************************************************
class LinkInlineProc(markdown.inlinepatterns.LinkInlineProcessor):
    """Fix wiki links"""

    def __init__(self, *args, auto_index, **kwargs):
        super(LinkInlineProc, self).__init__(*args, **kwargs)
        self.auto_index = auto_index

    def getLink(self, *args, **kwargs):
        href, title, index, handled = super().getLink(*args, **kwargs)
        if not href.startswith('http') and not href.endswith('.html'):
            if self.auto_index and href.endswith('/'):
                href += 'index.html'
            elif not href.endswith('/'):
                href += '.html'
        return href, title, index, handled


#******************************************************************************
#
#******************************************************************************
class ImageInlineProc(markdown.inlinepatterns.ImageInlineProcessor):
    """Fix wiki image links"""

    def __init__(self, *args, src_file_dir: Path, output_dir: Path, **kwargs):
        super(ImageInlineProc, self).__init__(*args, **kwargs)
        self.src_file_dir = src_file_dir
        self.output_dir = output_dir

    def getLink(self, *args, **kwargs):
        href, title, index, handled = super().getLink(*args, **kwargs)

        src = self.src_file_dir / href
        dst = self.output_dir / href

        Path(dst.parent).mkdir(parents=True, exist_ok=True)
        copy_if_newer(src, dst)

        return href, title, index, handled


#******************************************************************************
#
#******************************************************************************
def setup_markdown_converter(options, src_file_dir: Path, dst_dir: Path) -> markdown.Markdown:
    extensions = ['fenced_code', 'tables','codehilite']
    if 'markdown_extensions' in options:
        extensions += options['markdown_extensions'].split(',')
    extensions = set([e for e in extensions if e])

    md = markdown.Markdown(extensions=extensions)
    md.inlinePatterns.register(
        LinkInlineProc(
            markdown.inlinepatterns.LINK_RE,
            md,
            auto_index=options.get('auto_index', False)
        ), 'link', 160
    )
    if options.get('copy_images', True):
        md.inlinePatterns.register(
            ImageInlineProc(
                markdown.inlinepatterns.IMAGE_LINK_RE,
                md,
                src_file_dir=src_file_dir,
                output_dir=dst_dir
            ), 'image', 160
        )
    return md


#******************************************************************************
#
#******************************************************************************
def try_read_html_template(tpl_dir: Path, tpl_name: str, tpl_ext: str) -> Optional[str]:
    template = None
    template_file = tpl_dir / Path(tpl_name + tpl_ext)

    if template_file.is_file():
        with open(template_file, 'r') as f:
            template = f.read()
    else:
        eprint(f'{template_file} is not a file!')

    return template


#******************************************************************************
#
#******************************************************************************
def apply_defaults(root_path: Path) -> str:
    # lets write out the default stylesheet as well
    dst = root_path / 'css/default_style.css'
    Path(dst.parent).mkdir(parents=True, exist_ok=True)
    write_to_file(dst, default_css)

    return default_template


#******************************************************************************
#
#******************************************************************************
def process_input_file(md: markdown.Markdown, input_file: Path, rel_root_path: str) -> Tuple[Dict[str, str], str]:
    placeholders = {
        '%root_path%': rel_root_path,
        '%title%':     input_file.stem,
        '%date%':      datetime.datetime.today().strftime( '%Y-%m-%d')
    }

    template = None
    with open(input_file, 'r') as f:
        content = ''
        # Retrieve vimwiki placeholders
        for line in f:
            if line.startswith('%nohtml'):
                sys.exit(0)
            elif line.startswith('%title'):
                placeholders['%title%'] = line[7:-1]
            elif line.startswith('%date'):
                placeholders['%date%'] = line[6:-1]
            elif line.startswith('%template'):
                template = line[10:-1]
            else:
                content += line

        placeholders['%content%'] =  md.convert(content)

    return (placeholders, template)


#******************************************************************************
#
#******************************************************************************
def copy_css(root_path: Path, options: Dict):
    css_files = options.get('css_files').split(',')
    for css_file in css_files:
        src_dst = css_file.split(':')
        src = Path(src_dst[0])
        dst = root_path
        if len(src_dst) > 1:
            dst = root_path / src_dst[1]

        Path(dst.parent).mkdir(parents=True, exist_ok=True)
        copy_if_newer(src, dst)


#******************************************************************************
#
#******************************************************************************
def render_template(template: str, placeholders: Dict) -> str:
    for placeholder, value in placeholders.items():
        template = template.replace(placeholder, value)
    return template


#******************************************************************************
#
#******************************************************************************
def main():
    # print(sys.argv)
    # exit(0)
    options = textwrap.dedent(r'''
    the options are a json string with the following optional keys:
        markdown_extensions: string with comma separated python-markdown extensions to use.
                             see https://python-markdown.github.io/extensions/.
            default: "fenced_code,tables,codehilite".
            note! you only add to that list.
        auto_index: boolean, if true automatically append index.html to links that end with /.
            default: false.
        css_files: string with a comma separated list of css files to copy to output_root dir.
            output root dir = dir(input_file) + root_path
            optionally use a colon and specify a relative directory and name for the copied file.
            example: "/full-path-to/some_style.css:css/style.css"
            default: None.
        copy_images: boolean (default true). if true will copy images in image links to the output directory.
            default: true.
    example:
    {
        "markdown_extensions": "admonition",
        "auto_index": false,
        "css_files": "/home/stefantb/css/style.css:css_files/somestyle.css"
    }
    ''')

    parser = argparse.ArgumentParser(description='Convert wiki markdown to html.', formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('force',               type=bool, help='force conversion. (ignored, always forced)')
    parser.add_argument('syntax',              type=str,  help='syntax to convert. (only markdown supported)')
    parser.add_argument('extension',           type=str,  help='input file extension.')
    parser.add_argument('output_dir',          type=Path, help='full path to the output directory.')
    parser.add_argument('input_file',          type=Path, help='full path to the input file.')
    parser.add_argument('css_file',            type=Path, help='full path to css style file. (ignored)')
    parser.add_argument('template_path',       type=Path, help='full path to directory with html templates.')
    parser.add_argument('template_default',    type=str,  help='default html template file name. (without extension).')
    parser.add_argument('template_ext',        type=str,  help='html template file extension.')
    parser.add_argument('root_path',           type=str,  help=r'relative path from the output directory to the output root. (e.g. ../../)  ("-" means in root)')
    parser.add_argument('options',             type=str,  help=f'json dictionary with options for this program. {options}')

    args = parser.parse_args()

    rel_root_path = args.root_path if args.root_path != '-' else ""
    root_path = args.output_dir / rel_root_path
    output_file = args.output_dir / Path(args.input_file.stem + '.html')

    options = {}
    if args.options:
        options = json.loads(args.options)

    # Only markdown is supported
    if args.syntax != 'markdown':
        eprint('Unsupported syntax: ' + args.syntax)
        sys.exit(1)

    md = setup_markdown_converter(options, args.input_file.parent, args.output_dir)

    placeholders, template = process_input_file(md, args.input_file, rel_root_path)

    template = try_read_html_template(
            args.template_path,
            args.template_default,
            args.template_ext
    ) or apply_defaults(root_path)

    html = render_template(template, placeholders)

    write_to_file(output_file, html)

    copy_css(root_path, options)


#******************************************************************************
#
#******************************************************************************
if __name__ == '__main__':
    main()

