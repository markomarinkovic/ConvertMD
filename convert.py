#!/usr/bin/env python

# readme.io markdown to GitHub-flavoured markdown conversion script, v3
# Author: Marko Marinkovic (marko.marinkovic@sbgenomics.com)
# TO DO:
# - Hash symbols in headers need to be spaced from the text that follows
# - Code conversion needs to be adapted to match two tabs within a single code block

# Imports
import sys
import json
import re
import os.path

# Define output file name based on input file name
inputFile = sys.argv[1]
fName = str(inputFile).split(".")[0] + ".converted" + ".md"

# Clear the content of the output file if the file already exists
if os.path.isfile(fName):
    open(fName, 'w').close()
outputFile = open(fName, 'a')

with open(inputFile, 'r') as content:
    blockCallout = False
    blockImg = False
    blockCode = False
    blockContent = []
    convertedCallouts = 0
    convertedImages = 0
    convertedCode = 0
    for line in content:

        if line.startswith("[block:callout]"):
            blockCallout = True
        elif line.startswith("[block:image]"):
            blockImg = True
        elif line.startswith("[block:code]"):
            blockCode = True
        if blockCallout or blockImg or blockCode:
            blockContent.append(line)
        else:
            heading = re.match(r'#+[a-zA-Z]', line)
            if heading:
                insertpos = heading.end() - 1
                outputFile.write(line[:insertpos] + " " + line[insertpos:])
            else:
                outputFile.write(line)

        if blockCallout and line.startswith("[/block]"):
            blockCallout = False
            lastitem = len(blockContent)-1
            jsonString = " ".join(blockContent[1:lastitem])
            if jsonString != "":
                data = json.loads(jsonString)
                if 'title' not in data:
                    outputFile.write("\n" + "[" + data['type'] + " : " + data['body'] + "]" + "\n")
                else:
                    outputFile.write("\n" + "[" + data['type'] + " : " + data['title'] + " : " + data['body'] + "]" + "\n")
                blockContent = []
                convertedCallouts += 1

        elif blockImg and line.startswith("[/block]"):
            blockImg = False
            lastitem = len(blockContent)-1
            jsonString = " ".join(blockContent[1:lastitem])
            if jsonString != "":
                data = json.loads(jsonString)
                outputFile.write("\n" + "![" + data['images'][0]['image'][1] + "](" + data['images'][0]['image'][0] + " \"\")" "\n")
                blockContent = []
                convertedImages += 1

        elif blockCode and line.startswith("[/block]"):
            blockCode = False
            lastitem = len(blockContent)-1
            jsonString = " ".join(blockContent[1:lastitem])
            if jsonString != "":
                data = json.loads(jsonString)
                outputFile.write("\n" + "```" + data['codes'][0]['language'] + "\n" + data['codes'][0]['code'] + "\n" + "```")
                blockContent = []
                convertedCode += 1


print "--------------"
print "Conversion log"
print "--------------"
print "Converted callouts: " + str(convertedCallouts)
print "Converted images: " + str(convertedImages)
print "Converted code blocks: " + str(convertedCode)
print "Output file: " + fName
