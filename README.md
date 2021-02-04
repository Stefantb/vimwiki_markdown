# vimwiki-markdown

[vimwiki](https://github.com/vimwiki/vimwiki) markdown file to html with syntax highlighting and image handling.

Note: [This project](https://github.com/Stefantb/vimwiki_markdown) is a fork of [https://github.com/WnP/vimwiki_markdown](https://github.com/WnP/vimwiki_markdown). It is not the same as you can download from PyPi.

## Install

```sh
git clone git@github.com:Stefantb/vimwiki_markdown.git
cd vimwik_markdown
python3 -m pip install --user .
```
## Features

* Converts markdown to html using [python-markdown](https://python-markdown.github.io).
* Copies images referenced in the markdown to the html directory. (can be turned off.)
* Can fix links that end with '/' by appending `index.html` to them. (must be turned on.)
* Allows the user to specify css files to be copied to the html directory.
  This allows for no fuss regeneration of the html directory.
* Allows the user to specify extra markdown [extensions](https://python-markdown.github.io/extensions/).


## Usage

Try adding the following to your `~/.vimrc`:

```vim
let g:vimwiki_list = [{
    \ 'path': '~/vimwiki',
    \ 'syntax': 'markdown', 'ext': '.md',
    \ 'path_html': '~/vimwiki/site_html/',
    \ 'custom_wiki2html': 'vimwiki_markdown',
    \ 'template_path': '~/vimwiki/templates/',
    \ 'template_default': 'default',
    \ 'template_ext': '.tpl',
    \ 'css_name': 'css/vw_style.css',
    \ 'custom_wiki2html_args':
    \ '\{\"css_files\":\"
    \~/vimwiki/css/style.css:css/my_style.css
    \\"}'
    \ }]
```

1. If `~/vimwiki/templates/default.tpl` exists it will be used to generate the html.
    * In that case the style in the template must have its css correctly specified in the settings.
2. If `~/vimwiki/css/style.css` exists, it will be copied out to `<path_html>/css/my_style.css`

If the default template does not exist, a [default](#default-template-and-theme) template and matching css will be used.

## Detailed Usage
Try running `vimwiki_markdown -h`:
```sh
$vimwiki_markdown -h
usage: vimwiki_markdown [-h] force syntax extension output_dir input_file css_file template_path template_default template_ext root_path options

Convert wiki markdown to html.

positional arguments:
  force             force conversion. (ignored, always forced)
  syntax            syntax to convert. (only markdown supported)
  extension         input file extension.
  output_dir        full path to the output directory.
  input_file        full path to the input file.
  css_file          full path to css style file. (ignored)
  template_path     full path to directory with html templates.
  template_default  default html template file name. (without extension).
  template_ext      html template file extension.
  root_path         relative path from the output directory to the output root. (e.g. ../../)  ("-" means in root)
  options           json dictionary with options for this program.
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

optional arguments:
  -h, --help        show this help message and exit

```

## Markdown extensions

The following [markdown extensions](https://python-markdown.github.io/extensions/)
are activated by default:

- [fenced_code](https://python-markdown.github.io/extensions/fenced_code_blocks/)
- [tables](https://python-markdown.github.io/extensions/tables/)
- [CodeHilite](https://python-markdown.github.io/extensions/code_hilite/)

But you can add more extensions using the `options` argument.
## Syntax highlighting

Syntax highlighting is provided by [Pygments](http://pygments.org/), which will
try to guess language by default.

You can use regular markdown indented code blocks:

```
	:::python
	for value range(42):
		print(value)
```

Or Fenced Code Blocks

	```python
	for value range(42):
		print(value)
	```

You can also highlight line using `hl_lines` argument:

	```python hl_lines="1 3"
	for value range(42):
		print(value)
	```

Pygments can generate CSS rules for you. Just run the following command from
the command line:

```
pygmentize -S default -f html -a .codehilite > styles.css
```

If you would like to use a different theme, swap out `default` for the desired
theme. For a list of themes installed on your system, run the following
command:

```
pygmentize -L style
```

## Default Template and Theme

The default theme provided is a dark theme and applies code highlighting with the `monokai` theme.

The default theme and template can be triggered by specifying an invalid html template in your `vimrc`.

For simplicity the [default template and css is defined in the source code](https://github.com/Stefantb/vimwiki_markdown/blob/master/vimwiki_markdown.py#L16-L213).

## Developing

Editable install:
```
python3 -m pip install --user --no-use-pep517 -e .
```
