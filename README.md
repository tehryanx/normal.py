# normal.py
Find unicode codepoints to use in normalisation and transformation attacks. 

Search for unicode codepoints that you can use to replace characters in a given string
```
$ ./normal.py -s bountyplz.xyz
...
𝓾 -> u | (U+120062) -> [117] | (MATHEMATICAL BOLD SCRIPT SMALL U) : NFKC                                                                              
𝔁 -> x | (U+120065) -> [120] | (MATHEMATICAL BOLD SCRIPT SMALL X) : NFKD                                                                              
𝔁 -> x | (U+120065) -> [120] | (MATHEMATICAL BOLD SCRIPT SMALL X) : NFKC                                                                              
𝔂 -> y | (U+120066) -> [121] | (MATHEMATICAL BOLD SCRIPT SMALL Y) : NFKD                                                                              
𝔂 -> y | (U+120066) -> [121] | (MATHEMATICAL BOLD SCRIPT SMALL Y) : NFKC                                                                              
𝔃 -> z | (U+120067) -> [122] | (MATHEMATICAL BOLD SCRIPT SMALL Z) : NFKD
...
```
Check every normalized codepoint against a regex pattern to find useful characters:
```
$ ./normal.py -r "\.\."
‥ -> .. | (U+8229) -> [46, 46] | (TWO DOT LEADER) : NFKD
‥ -> .. | (U+8229) -> [46, 46] | (TWO DOT LEADER) : NFKC
… -> ... | (U+8230) -> [46, 46, 46] | (HORIZONTAL ELLIPSIS) : NFKD
… -> ... | (U+8230) -> [46, 46, 46] | (HORIZONTAL ELLIPSIS) : NFKC
︙ -> ... | (U+65049) -> [46, 46, 46] | (PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS) : NFKD
︙ -> ... | (U+65049) -> [46, 46, 46] | (PRESENTATION FORM FOR VERTICAL HORIZONTAL ELLIPSIS) : NFKC
︰ -> .. | (U+65072) -> [46, 46] | (PRESENTATION FORM FOR VERTICAL TWO DOT LEADER) : NFKD
︰ -> .. | (U+65072) -> [46, 46] | (PRESENTATION FORM FOR VERTICAL TWO DOT LEADER) : NFKC

$ ./normal.py -r "[a-z]/[a-z]"
℀ -> a/c | (U+8448) -> [97, 47, 99] | (ACCOUNT OF) : NFKD
℀ -> a/c | (U+8448) -> [97, 47, 99] | (ACCOUNT OF) : NFKC
℁ -> a/s | (U+8449) -> [97, 47, 115] | (ADDRESSED TO THE SUBJECT) : NFKD
℁ -> a/s | (U+8449) -> [97, 47, 115] | (ADDRESSED TO THE SUBJECT) : NFKC
℅ -> c/o | (U+8453) -> [99, 47, 111] | (CARE OF) : NFKD
℅ -> c/o | (U+8453) -> [99, 47, 111] | (CARE OF) : NFKC
℆ -> c/u | (U+8454) -> [99, 47, 117] | (CADA UNA) : NFKD
℆ -> c/u | (U+8454) -> [99, 47, 117] | (CADA UNA) : NFKC

```
Look up specific unicode characters/codepoints for a list of details and transformations. 
```
$ ./normal.py -c 127277
CIRCLED CD : 🄭
Unicode codepoint: U+127277
URL Encoded: %F0%9F%84%AD
NFD : 🄭 [127277]
NFC : 🄭 [127277]
NFKD : CD [67, 68]
NFKC : CD [67, 68]
HTML Entity decimal: &#127277
HTML Entity hex: &#x1f12d
To upper-case 🄭
To lower-case 🄭

$ ./normal.py -c ß
LATIN SMALL LETTER SHARP S : ß
Unicode codepoint: U+223
URL Encoded: %C3%9F
NFD : ß [223]
NFC : ß [223]
NFKD : ß [223]
NFKC : ß [223]
HTML Entity name: &szlig;
HTML Entity decimal: &#223
HTML Entity hex: &#xdf
To upper-case SS
To lower-case ß
```
