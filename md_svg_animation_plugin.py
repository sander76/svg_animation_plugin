from jinja2 import Template
from markdown.blockprocessors import BlockProcessor
from markdown.extensions import Extension
from markdown.util import etree
from mkdocs.relative_path_ext import path_to_url

from md_svg_parser import PvParser, ParseError


def makeExtension(*args, **kwargs):
    return PvExtension(*args, **kwargs)


PVMAN_RE = r'_PVMAN([^;]+);PVMAN'

TEMPLATE1 = u'''
    <svg id="{{id}}" preserveAspectRatio="xMidYMid meet"></svg>
    <script>
        // IE doesn't seem to scale the svg propery. Using below to set it at a hacky 500px height.
        var ua = window.navigator.userAgent;
        var ms_ie = ~ua.indexOf('MSIE ') || ~ua.indexOf('Trident/');
        var {{id}} = Snap("#{{id}}");
        if (ms_ie){
            {{id}}.attr("height","500px");
        }

        Snap.load("{{svg}}", function (f) {
            var objs={"guide_text0":f.select('#guide_text1'),
                      "guide_text1":f.select('#guide_text2')};
            var fullzoom_bbox = f.select("#full_zoom").getBBox();
            var tooltip = f.select('#tooltip'); //tooltip containing all text elements
            var text_container = f.select('#text_container'); //the textspan element which contains all text
            var tooltip_frame = f.select('#text_background'); //the background of the text.
            var text_delay=300; //an extra delay added for text to fade in and out.
            var animations=[];
            var playing=false; //true if the animation is playing. This will determine behaviour of stop/play and pause buttons.
            var firstplay=true;
            var pointer = f.select('#pointer');
            var text_start=f.select("#text_start");
            {{id}}.attr({
                viewBox: fullzoom_bbox.vb
            });
            var delete_timeouts=function(){
                for (var i=0;i<animations.length;i+=1){
                    clearTimeout(animations[i]);
                    }
            };
            var reset=function(){
                for (var i=0;i<items.length;i+=1){
                    if (items[i].hasOwnProperty('items')){
                        for (var k=0;k<items[i].items.length;k+=1){
                            _reset(items[i].items[k]);
                        }
                    }
                    else{
                        _reset(items[i]);
                    }
                }
            };
            var _reset=function(item){
                item.stop();
                var keys = item.data('keys');
                    for (var k=0;k<keys.length;k+=1){
                        var key = keys[k];
                        if (key === 'transform'){
                            console.log("translate");
                            var trans = item.data(key)
                            trans=trans.toString();
                            item.attr(key,trans);
                        }
                        else{
                            var val = item.data(keys[k]);
                            item.attr(key,val);}
                    }
            };
            var reset_text=function(){
                _setText(['Press play to start the animation'],undefined,text_start);
            };
            var init=function(item,keys){
                if (item.hasOwnProperty('items')){
                    for (var i=0;i<item.items.length;i+=1){
                        _init(item[i],keys);
                    }
                }
                else{
                    _init(item,keys);
                }
            };
            var _init=function(item,keys){
                item.data("keys",keys);
                for (var i=0;i<keys.length;i+=1){
                    console.log(keys[i]);
                    console.log(item.attr(keys[i]));
                    item.data(keys[i],item.attr(keys[i]));
                }
            };
            var _anim = function (svg, props, delay, speed) {
                if (speed === undefined){speed=200;}
                if (delay) {
                    animations.push(setTimeout(function () {
                        svg.animate(props, speed)
                    }, delay));
                } else {
                    svg.animate(props, speed);
                }
            };
            var animation_stop=function(){
                playing = false;
                disable_stop();
                enable_play();
                //reset();
                console.log("animation stopped");
            };
            var disable_play=function(){
                play.attr({"pointer-events":"none","visibility":"hidden"});
            };
            var enable_play=function(){
                play.attr({"pointer-events":"visible","visibility":"visible"});
            };
            var enable_stop=function(){
                stop.attr({"pointer-events":"visible","visibility":"visible"});
            };
            var disable_stop=function(){
                stop.attr({"pointer-events":"none","visibility":"hidden"});
            };
            var _setText = function ( text, delay, target) {
                    if (delay === undefined){delay=0;}
                    var func = function () {
                        //_anim(tooltip,{"opacity":0},undefined,text_delay);
                        _anim(text_container,{"opacity":0},undefined,text_delay);
                        setTimeout(function(){
                            //clean the second line to be sure.
                            objs['guide_text1'].node.innerHTML='';
                            for (var i =0;i<text.length;i+=1){
                                objs["guide_text"+i].node.innerHTML=text[i];
                            }
                            // get the bounding box with the newly added text.
                            var _bbox_container = text_container.getBBox();
                            move_and_transform_text(target,_bbox_container);
                            // Resize the background according to the new text container.
                            //_anim(tooltip_frame,{"width":background_width,"height":background_height},200,text_delay);
                            //_moveText(target);
                            _anim(text_container,{"opacity":0.95},500,text_delay);
                            },text_delay);
                    };
                    if (delay) {
                        animations.push(setTimeout(function () {
                            func()
                        }, delay));
                    } else {
                        func();
                    }
            };
            var move_and_transform_text = function (target,text_bbox) {
                    var ttip_padding=10;
                    var _tooltip_bbox = tooltip.getBBox();
                    var _transform = tooltip.transform();
                    var _target_bbox = target.getBBox();
                    var _pointer_x=0;
                    var _pointer_y=0;
                    var _x = text_bbox.width+ttip_padding + _target_bbox.x2;
                    if (_x > fullzoom_bbox.x2){
                        var _dx = _target_bbox.x - (_tooltip_bbox.x + text_bbox.width + ttip_padding);
                        _pointer_x=text_bbox.width + ttip_padding;
                    }else{
                        var _dx = _target_bbox.x2 - _tooltip_bbox.x;
                        _pointer_x=0;
                    }
                    var _y = _target_bbox.y - (text_bbox.height + ttip_padding);
                    if (_y \> fullzoom_bbox.y){
                        var _dy = _target_bbox.y - (_tooltip_bbox.y + text_bbox.height + ttip_padding);
                        _pointer_y=text_bbox.height + ttip_padding;
                    }else{
                        var _dy = _target_bbox.y2 - _tooltip_bbox.y;
                        _pointer_y=0
                    }
                    _transform.globalMatrix.translate(_dx,_dy);
                    var translate =_transform.globalMatrix.toTransformString();
                    _anim(tooltip,{transform: translate},200,text_delay);
                    _anim(tooltip_frame,{"width":text_bbox.width + ttip_padding,"height":text_bbox.height + ttip_padding},200,text_delay);
                    _anim(pointer,{"transform":'t'+_pointer_x+',' + _pointer_y},200,text_delay);
                };
            var stop = f.select("#stop_button")
            disable_stop();
            var play = f.select("#play_button");

            {{elements}}
            {{items}}
            play.click(function () {
                if (firstplay === false){
                    reset();
                }
                firstplay=false;
                enable_stop();
                disable_play();
            {{animations}}
            });
            stop.click(function(){
                playing=false;
                enable_play();
                disable_stop();
                delete_timeouts();
                reset_text();
                reset();
            });
            {{id}}.append(f);
            {% for init in inits %}{{init}}{% endfor %}
        });
</script>
'''


class PvExtension(Extension):
    """Extensions: text between _pv_ will be modified"""

    def extendMarkdown(self, md, md_globals):
        md.parser.blockprocessors.add('pvman',
                                      PvBlockParser(md.parser, md_globals),
                                      '<hashheader')


class PvBlockParser(BlockProcessor):
    def __init__(self, parser, md_globals):
        BlockProcessor.__init__(self, parser)
        self.md_globals = md_globals
        if "pvman" not in md_globals:
            md_globals['pvman'] = {'svg_id': 0,
                                   'template': self.loadTemplate()}

    def loadTemplate(self):
        return Template(TEMPLATE1)

    def _get_svg_id(self):
        self.md_globals['pvman']['svg_id'] += 1
        return 'pvman_svg_{}'.format(self.md_globals['pvman']['svg_id'])

    def test(self, parent, block):
        st = block.startswith('_PVMAN_')
        stop = block.endswith('_PVMAN_')
        return st and stop

    def run(self, parent, blocks):
        block = blocks.pop(0)
        div = etree.SubElement(parent, 'div')
        # template=Template(TEMPLATE1)
        # txt=''
        try:
            pv = PvParser(block.split('\n'))
        except ParseError as e:
            txt = e.value
        else:
            svg_loc = pv.svg_location
            try:
                blockp = self.parser.markdown.treeprocessors['relpath']
                svg_loc = path_to_url(pv.svg_location, blockp.site_navigation, blockp.strict)
            except Exception as e:
                pass
            txt = self.md_globals['pvman']['template'].render(id=self._get_svg_id(),
                                                              elements='\n'.join(pv.item_selectors),
                                                              animations='\n'.join(pv.animations + pv.texts),
                                                              svg=svg_loc,
                                                              items='var items= [{}];'.format(','.join(pv.items)),
                                                              inits=pv.inits)
        div.set('class', 'anim')

        div.text = txt
