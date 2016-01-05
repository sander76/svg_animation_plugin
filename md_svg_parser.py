import json
import re
from json.decoder import JSONDecodeError

__author__ = 'sander'


class ParseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class Line():
    def __init__(self):
        self.var = None
        self.attributes = {}
        self.text = None
        self.speed = 200
        self.after = 1000
        self.timing = None
        self.item = None
        self.blinkstart = None
        self.blinkstop = None
        self.blinkend = None
        self.blinks = []
        self.animations = []

    def set_timing(self, timing):
        self.timing = timing
        self.create_animation()
        self.create_tooltip()

    def create_animation(self):
        if len(self.attributes.keys()) > 0:
            # self.animation = "_anim({},{},{},{});".format(self.item, self.attributes, self.timing , self.speed)
            self.animations.append("_anim({},{},{},{});".format(self.item, self.attributes, self.timing, self.speed))

    def create_tooltip(self):
        if self.text is not None:
            self.animations.append("_setText({},{},{});".format(self.text, self.timing, self.item))
            # self.tooltip_text = "_setText({},{},{});".format(self.text,self.timing,self.item)

    def process_blink(self):
        if self.blinkstart is not None:
            for i in range(self.timing, self.blinkend + 1, 1000):
                self.blinks.append("_anim({},{},{},{});".format(self.item, self.blinkstart, i, 200))
                self.blinks.append("_anim({},{},{},{});".format(self.item, self.blinkstop, i + 500, 200))


class PvParser():
    def __init__(self, str):
        self.str = str
        self.title = ''
        self.svg_location = None
        self.animations = []
        self.texts = []
        # a unique number assigned to each var in javascript to identify individual components.
        self._item_nr = 0
        self._item_selectors = []
        self.item_selectors = []
        self.items = []
        # inits are used for getting the svg attributes at startup to return to the initial state when stop is pressed.
        self.inits = []
        # generator to iterate through all lines in the text.
        self.line = self._line()
        # self.animation_length=0
        # the time the animation is currently in.
        self.current_time = 0
        # each line representing data for an animation.
        self._lines = []
        self.parse()

    timing = re.compile('^\[([^\[\]]+)\]({.*)')

    def parse_line(self, line):
        if line.startswith("#"):
            return None
        else:
            ln = PvParser.timing.match(line)
            if ln:
                if len(ln.groups()) == 2:
                    return ln
                else:
                    raise ParseError(
                            "parsing of regex not correct. Error in line {} of your markdown file".format(self.idx))
            else:
                raise ParseError(
                        "parsing of regex not correct. Error in line {} of your markdown file".format(self.idx))

    def parse_attributes(attributes):
        ln = Line()
        obj = json.loads(attributes)
        keys = []

        def add_key(key):
            if key not in keys:
                keys.append(key)

        for key, value in obj.items():
            if key == "text":
                ln.text = value
            elif key == "speed":
                ln.speed = value
            elif key == "after":
                ln.after = value
            elif key == "blinkstart":
                ln.blinkstart = value
                # get the keys which are going to be changed to reset them later.
                for ky in value.keys():
                    add_key(ky)
            elif key == "blinkstop":
                ln.blinkstop = value
            else:
                ln.attributes[key] = value
                add_key(key)
        return ln, keys

    def parse_css_selectors(selectors):
        _selectors = sorted([sel.strip() for sel in selectors.strip().split(',')])
        return ','.join(_selectors)

    def _line(self):
        for idx, ln in enumerate(self.str):
            self.idx = idx
            yield ln

    def _get_item(self, css_selector, keys):
        # var items and their corresponding css selectors and their property keys.
        for x in self._item_selectors:
            if css_selector == 'text_start':
                return "text_start"
            elif x[1] == css_selector:
                # update the property keys for the existing item.
                for key in keys:
                    if key not in x[2]:
                        x[2].append(key)
                return x[0]
        else:
            # create a new item and add it to the list of selectors.
            itm = "item_{}".format(self._item_nr)
            self._item_nr += 1
            self._item_selectors.append((itm, css_selector, keys))
            return itm

    def _parse_line(self):
        for idx, ln in enumerate(self.line):
            if ln == "END":
                return
            else:
                match = self.parse_line(ln)
                if match is not None:
                    try:
                        attributes, keys = PvParser.parse_attributes(match.group(2))
                    except JSONDecodeError as e:
                        raise ParseError("Error parsing animation code at line: {}".format(idx))
                    css_selectors = PvParser.parse_css_selectors(match.group(1))
                    itm = self._get_item(css_selectors, keys)
                    attributes.item = itm
                    self._lines.append(attributes)

    def _parse_svg_location(self, ln):
        self.svg_location = ln.split(':')[1].strip()

    def _process_lines(self):
        for ln in self._lines:
            self.current_time += ln.after
            ln.set_timing(self.current_time)
            if ln.blinkstop is not None:
                start = next(x for x in self._lines if
                             x.item == ln.item and x.blinkstart is not None and x.blinkstop == None)
                start.blinkstop = ln.blinkstop
                start.blinkend = ln.timing
                start.process_blink()

    def _post_process(self):
        self._process_lines()
        for itm, css_selectors, keys in self._item_selectors:
            if ',' in css_selectors:
                self.item_selectors.append("var {} = f.selectAll('{}');".format(itm, css_selectors))
            else:
                self.item_selectors.append("var {} = f.select('{}');".format(itm, css_selectors))
            if len(keys) > 0:
                self.inits.append("init({},{});".format(itm, keys))
                self.items.append(itm)
        for ln in self._lines:
            self.animations.extend(ln.animations)
            self.animations.extend(ln.blinks)

        self.animations.append(
                "animations.push(setTimeout(function () {{animation_stop();}},{}));".format(self.current_time))

    def parse(self):
        for ln in self.line:
            if ln == "TIMING":
                self._parse_line()
            # elif ln.startswith("TITLE"):
            #     self._parse_title(ln)
            elif ln.startswith("SVG"):
                self._parse_svg_location(ln)
        self._post_process()


if __name__ == "__main__":
    lines = '''
TITLE: Assigning a group to a shade
SVG: /imgs/test.svg
TIMING
01,                 [#stop],{fill:'orange'}
00000001,           [#stop],{fill:'white'}
00000010101010101,  [#text_up, #text_down, #text_open,#text_close,#text_arrow_down,#text_arrow_up,#text_stop],{fill:'lightblue'}
00000001010101010,  [#text_up, #text_down, #text_open,#text_close,#text_arrow_down,#text_arrow_up,#text_stop],{fill:'#333333'}
0000001000001, ["#text"],{text:open up mother fucker}
END
    '''
    pv = PvParser(lines.split('\n'))

    import pprint

    pprint.pprint(pv.__dict__)
