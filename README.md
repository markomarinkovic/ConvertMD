# Convert MD

The purpose of this script is to convert `[block][/block]` elements found in readme.io markdown to regular markdown.

## Update Dec 11, 2016:
* Included handling of improperly formatted headings (adds a space between the las hash symbol and the heading text, if necessary).
* The script now converts `[block:parameters]` (tables) to standard markdown tables.
* Images included in the file that is being converted are automatically downloaded and stored in the `images` subdirectory of the output directory.

## Initial commit
[block] elements handled in the initial version are:
* [block:callout]
* [block:image]
* [block:code]
