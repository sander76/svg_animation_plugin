__author__ = 'sander'
from md_svg_parser import PvParser

testinput=["SEQUENCE","[#test],{fill:'black'},11100010101","END"]

def test_timing():
    timing="     1     1"
    timings = PvParser.parse_timing(timing)
    assert len(timings)==2
    assert timings[0]==5
    assert timings[1]==11

def test_parse_line():
    line="[#css1,#css2],{fill:'red'},000000111"
    ln = PvParser.parse_line(line)
    assert len(ln.groups())==3

def test_create_animation():
    line=[]