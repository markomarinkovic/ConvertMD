#!/usr/bin/env python

# readme.io markdown to GitHub-flavoured markdown conversion script, v3
# Author: Marko Marinkovic (marko.marinkovic@sbgenomics.com)
# TO DO:
# - Code conversion needs to be adapted to match two tabs within a single code block

# Imports
import sys
import json
import re
import os.path
import urllib

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
    blockTable = False
    blockContent = []
    convertedCallouts = 0
    convertedImages = 0
    convertedCode = 0
    convertedTables = 0
    downloadedImages = 0
    for line in content:

        if line.startswith("[block:callout]"):
            blockCallout = True
        elif line.startswith("[block:image]"):
            blockImg = True
        elif line.startswith("[block:code]"):
            blockCode = True
        elif line.startswith("[block:parameters]"):
            blockTable = True
        if blockCallout or blockImg or blockCode or blockTable:
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
                imagefile = data['images'][0]['image'][0].replace("https", "http")
                print "Downloading " + data['images'][0]['image'][1]
                if not os.path.exists("images"):
                    os.makedirs("images")
                urllib.urlretrieve(imagefile, "images/" + data['images'][0]['image'][1])
                outputFile.write("\n" + "![" + data['images'][0]['image'][1] + "](" + data['images'][0]['image'][0] + " \"\")" "\n")
                blockContent = []
                convertedImages += 1
                downloadedImages += 1

        elif blockCode and line.startswith("[/block]"):
            blockCode = False
            lastitem = len(blockContent)-1
            jsonString = " ".join(blockContent[1:lastitem])
            if jsonString != "":
                data = json.loads(jsonString)
                outputFile.write("\n" + "```" + data['codes'][0]['language'] + "\n" + data['codes'][0]['code'] + "\n" + "```")
                blockContent = []
                convertedCode += 1

        elif blockTable and line.startswith("[/block]"):
            blockTable = False
            lastitem = len(blockContent)-1
            jsonString = " ".join(blockContent[1:lastitem])
            if jsonString != "":
                data = json.loads(jsonString)
                cols = data['cols']
                rows = data['rows']
                outputFile.write("\n")
                for i in range(0, cols):
                    headercell = "h-" + str(i)
                    outputFile.write("|" + data['data'][headercell])
                    if i == cols -1:
                        outputFile.write("|" + "\n")
                outputFile.write("|------|------|------|" + "\n")
                for x in range(0, rows):
                    for y in range(0, cols):
                        cell = str(x) + "-" + str(y)
                        linecont = data['data'][cell].replace('\n', '<br />')
                        outputFile.write("|" + linecont)
                        if y == cols - 1:
                            outputFile.write("|" + "\n")
                blockContent = []
                convertedTables += 1

print "--------------"
print "Conversion log"
print "--------------"
print "Converted callouts: " + str(convertedCallouts)
print "Converted images: " + str(convertedImages)
print "Converted code blocks: " + str(convertedCode)
print "Converted tables: " + str(convertedTables)
print "Downloaded images: " + str(downloadedImages)
print "Output file: " + fName
