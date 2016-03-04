# EBAY ITEM № 151990485080

This repo contains the source code used to generate the produce for [EBAY ITEM № 151990485080][original_post]: the sale of one printed copy of the auction page's html. 

A slightly modified digital version of the actual item is also in this repo. It is 274 pages long:

- [View as PDF][pdf].
- [View as webpage][page] (takes a few seconds to load).

## How it was Made
I tried a number of different tools before coming up with a workflow that kind of worked for generating this item. Tools like LaTeX, Jekyll's syntax highlighting, and [PrinceXML](http://www.princexml.com), couldn't handle how awesome this project was, either and hung or refused to work at all.

1. In a clean Chrome browser session, I collected the complete page load of the auction page using Fiddler. This was exported as a fiddler archive.
2. The archive was processed with `process.py` (some terrible, terrible code BTW) to extract all request data and transform it into HTML content.
3. A webpage version of the archive was generated using Jekyll. Highlight.js was used for syntax highlighting.
4. I printed from Chrome to a pdf. 


[original_post]: http://blog.mattbierner.com/listing-151990485080/

[pdf]: https://github.com/mattbierner/Ebay-Item-151990485080/raw/gh-pages/result.pdf
[page]: http://mattbierner.github.io/Ebay-Item-151990485080