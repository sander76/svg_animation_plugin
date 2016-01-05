# Markdown svg parser. Creation of SnapSVG animations.

## usage.

```
_PVMAN_                        # Opens the block.
SVG: ../imgs/remote_white.svg  # Refer to the relative location of the SVG file.
TIMING                         # Start the Timing definitions.
[#stop]{"text":["Press and hold stop","until the remote starts blinking"]}
[#stop]{"fill":"orange"}
[#text_up, #text_down, #text_open,#text_close,#text_arrow_down,#text_arrow_up,#text_stop]{"blinkstart":{"fill":"lightblue"},"after":3500}
[#text_1]{"fill":"lightblue","after":0}
[#blind_button]{"text":["Press and hold the blind button...","...keep pressing"],"after":3000}
[#bottom_bar]{"text":["...And see the blind jog","as confirmation"],"after":1000}
[#bottom_bar]{"transform":"t0,-20","speed":800,"after":1000}
[#bottom_bar]{"transform":"t0,0","speed":800,"after":1000}
#</blind>
[#blind_button]{"text":["Release the blind button"],"after":2000}
[#blind_button]{"fill":"white","after":2000}
[#text_start]{"text":["Finished !"],"after":2000}
[#text_up, #text_down, #text_open,#text_close,#text_arrow_down,#text_arrow_up,#text_stop]{"blinkstop":{"fill":"#333333"}}
END                           # Ends the timing definitions.
_PVMAN_                       # Closes the block
```

## Installation:
```python
python setup.py install
```

In the mkdocs project:

- create a new theme folder in the root of the project.
- In the ```docs``` folder create a ```js``` folder and put ```snap.svg-min.js``` in it.

Copy your desired ```base.html``` theme to the new theme folder. Move 
```
{%- for path in extra_javascript %}
    <script src="{{ path }}"></script>
{%- endfor %}
```
inside the ```<head>``` tag.

In the ```config.yaml``` file enter:
```yaml
markdown_extensions:
  - md_svg_animation_plugin
  
extra_javascript:
  - "js/snap.svg-min.js"
  
theme_dir: 'new_theme' # Your created theme folder.
```




