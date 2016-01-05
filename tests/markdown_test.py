from captions import FigcaptionExtension

from md_svg_animation_plugin import PvExtension
from jinja2 import Template
from md_svg_parser import ParseError

__author__ = 'sander'

from markdown import markdown

TEMPLATE=u'''
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <title>PowerView demo</title>
    <style>
        .anim {
            margin-top: 20px;
            margin-left: auto;
            width: 80%;
        }
    </style>
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, minimal-ui">
    <script src="js/snap.svg-min.js"></script>
</head>

<body>
{{guides}}
</body>

</html>
'''

if __name__=="__main__":
    import jinja2

    with open("text.md") as fl:
        input = fl.read()
    try:
        txt = markdown(input,extensions=[PvExtension(),FigcaptionExtension()])
    except ParseError as e:
        print(e)
    template=Template(TEMPLATE)
    html = template.render(guides=txt)

    with open("out.html",'w')as fl:
        for ln in html:
            fl.write(ln)


