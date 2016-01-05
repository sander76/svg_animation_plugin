This is a test
--------------

![test](../imgs/testing.png)

this is a test.

## Duplicate a remote
_PVMAN
SVG: remote_pairing.svg
TIMING
#<reset a remote>
[#reset]{"text":["Press and hold the reset button","with a pencilpoint."]}
[#reset]{"fill":"orange","after":3000}
[#group3]{"text":["You will imediately see the remote blink","its groups."]}
[#text_one, #text_two, #text_three,#text_four,#text_five,#text_six]{"blinkstart":{"fill":"lightblue"},"after":3500}
[#text_one, #text_two, #text_three,#text_four,#text_five,#text_six]{"blinkstop":{"fill":"#333333"},"after":1500}
[#reset]{"text":["keep pressing...","until you see a second flasing of the buttons"]}
[#text_one, #text_two, #text_three,#text_four,#text_five,#text_six]{"blinkstart":{"fill":"lightblue"},"after":3500}
[#text_one, #text_two, #text_three,#text_four,#text_five,#text_six]{"blinkstop":{"fill":"#333333"},"after":1500}
[#reset]{"text":["release the reset button"],"after":1000}
[#reset]{"fill":"white","after":2000}
#</reset>
END
_PVMAN
