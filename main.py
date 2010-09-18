"""
                      +---------+                       
+---------------------|  About  |----------------------+
|                     +---------+                      |
|   A script to generate nicely boxed paragraphs, it   |
|   might be usefull for readme files ect              |
|                                                      |
|   Written By Hugoagogo, 2010                         |
|   http://www.importsoul.net/                         |
+------------------------------------------------------+
"""
import textwrap

## GENERAL SETTINGS
WIDTH = 50
JUSTIFY = True
PADDING_X = 3
PADDING_Y = 1

## Heading Settings
HEADING = "About Readme files"
HEADING_POS = "c"
HEADING_PADDING_X = 2
HEADING_PADDING_Y = 0

## SETTING FOR JUSTIFICATION
MIN_FILL = 0.5

f = open("demo.txt")
text = f.read()
f.close()

def justify(string,width):
    """
    A nice little functuion to create even spacing between words to fill a line
    It Still needs some work to look more natural
    """
    bits = string.split(" ")
    raw_width = len("".join(bits))
    if raw_width/float(width) > MIN_FILL and len(bits)-1:
        joiner_size = (width-raw_width)/(len(bits)-1)
        spares = (width-raw_width)%(len(bits)-1)
        out = ""
        for bit in bits:
            out+=bit+" "*joiner_size
            if spares:
                out+=" "
                spares -= 1
        return out.strip().ljust(width)
    else:
        return string.ljust(width)
    
def boxit(strings,padding_X,padding_Y):
    """
    puts lists of stings in boxes
    """
    ms = len(max(strings,key=len))
    out = ["+"+"-"*(ms+padding_X*2)+"+"]
    out.extend( ["|"+" "*(ms+padding_X*2)+"|"]*padding_Y )
    pad = " "*padding_X
    for string in strings:
        out.append("|"+pad+justify(string,ms)+pad+"|")
    out.extend( ["|"+" "*(ms+padding_X*2)+"|"]*padding_Y )
    out.append( "+"+"-"*(ms+padding_X*2)+"+")
    return out

def heading_pos(box,width,padding,pos):
    """
    Takes a nice formatted box and adds some bits to make a heading
    """
    if pos == "r":    base = [(" "*padding+l+" "*padding).rjust(width) for l in box]
    elif pos == "l":  base = [(" "*padding+l+" "*padding).ljust(width) for l in box]
    else:             base = [(" "*padding+l+" "*padding).center(width) for l in box]
    mid = len(base)/2
    a,b,c = base[mid].split("|")
    base[mid] = a.replace(" ","-")+"|"+b+"|"+c.replace(" ","-")
    for x in range(mid,len(base)):
        base[x]="|"+base[x][1:-1]+"|"
    base[mid]="+"+base[mid][1:-1]+"+"
    return base
##    if pos == "c":
        
    

bits = [textwrap.wrap(part,WIDTH) for part in text.split("\n")] ##do some paragraph layout
chunks = [item for sublist in bits for item in sublist or [""]] ## join the paragraphs

box = boxit(chunks,PADDING_X,PADDING_Y)
menu = heading_pos(boxit([HEADING],HEADING_PADDING_X,HEADING_PADDING_Y),len(box[0]),HEADING_PADDING_X,HEADING_POS)
box.pop(0)
menu.extend(box)
print "\n".join( menu )
