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
import textwrap, sys
from copy import copy
from getopt import gnu_getopt as getopt
from getopt import GetoptError

raws = {
    ## GENERAL SETTINGS
    'WIDTH':        (int,   'w',    50),
    'FILE':         (bool,  'f',    False),
    'FILE_MODE':    (str,   'm',    'w'),
##    'JUSTIFY':      (bool, True),
    'PADDING_X':    (int,   'x',    3),
    'PADDING_Y':    (int,   'y',    1),
    
    ## Heading Settings
    'HEADING':      (str,   'h',    'README'),
    'HEADING_POS':  (str,   'p',    'c'),
    'HEADING_PADDING_X':(int,'X',   2),
    'HEADING_PADDING_Y':(int,'Y',   0),

    ## SETTING FOR JUSTIFICATION
    'JUST_MIN_FILL':(int,   'j',    0.5),
    }
short_raws = dict((val[1], opt) for opt, val in raws.items())

defaults = dict((opt, val[2]) for opt, val in raws.items())

f = open("demo.txt")
text = f.read()
f.close()

def justify(string,width,min_fill=defaults['JUST_MIN_FILL']):
    """
    A nice little functuion to create even spacing between words to fill a line
    It Still needs some work to look more natural
    """
    bits = string.split(" ")
    raw_width = len("".join(bits))
    if raw_width/float(width) > min_fill and len(bits)-1:
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

def heading_pos(box,menu_box,padding,pos):
    """
    Takes a nice formatted box and adds some bits to make a heading
    """
    ## Create Copys
    box = copy(box)
    menu_box = copy(menu_box)

    ## Load the width
    width = len(box[0])

    ## Justify
    if pos == "r":    base = [(" "*padding+l+" "*padding).rjust(width) for l in menu_box]
    elif pos == "l":  base = [(" "*padding+l+" "*padding).ljust(width) for l in menu_box]
    else:             base = [(" "*padding+l+" "*padding).center(width) for l in menu_box]

    ## Do some fidling to put the menu box on a line    
    mid = len(base)/2
    a,b,c = base[mid].split("|")
    base[mid] = a.replace(" ","-")+"|"+b+"|"+c.replace(" ","-")
    for x in range(mid,len(base)):
        base[x]="|"+base[x][1:-1]+"|"
    base[mid]="+"+base[mid][1:-1]+"+"

    ## Join the menu into the main box
    box.pop(0)
    base.extend(box)
    return base

def usage():
    keys = [key.lower() for key in sorted(defaults.keys())]
    print "Possible arguments"
    for key in keys:
        print "--"+key

def clean_opts(opt_list):
    opts = {}
    for opt, arg in opt_list:
        opt = opt.strip('-')
        if opt in short_raws:
            opt = short_raws[opt]
        else:
            opt = opt.upper()
        if opt in raws:
            opts[opt] = raws[opt][0](arg)
    print opts
    return opts
    
def main(**new_args):

    ## Loads all default values and then overides some
    ## All settings are in upper case
    global defaults
    args = copy(defaults)
    for arg in new_args:
        args[arg] = new_args[arg]

    ## Reduce the width so that the padding and boarders are included
    args['WIDTH'] -= args['PADDING_X']*2+2
        
    bits = [textwrap.wrap(part,args['WIDTH']) for part in text.split("\n")] ##do some paragraph layout
    chunks = [item for sublist in bits for item in sublist or [""]] ## join the paragraphs

    box = boxit(chunks,
                args['PADDING_X'],
                args['PADDING_Y'])
    
    menu = boxit([args['HEADING']],
                 args['HEADING_PADDING_X'],
                 args['HEADING_PADDING_Y'])
    
    menu = heading_pos(box,
                       menu,
                       args['HEADING_PADDING_X'],
                       args['HEADING_POS'])

    if args['FILE']:
        f.open(args['FILE'],args['FILE_MODE'])
        f.write("\n".join( menu ))
        f.close()
    else:
        print "\n".join( menu )

if __name__ == "__main__":
    try:
        opt_list, args = getopt(sys.argv,"".join(key+":" for key in short_raws.keys()),(key.lower()+"=" for key in raws.keys()))
        opt_list = clean_opts(opt_list)
        main(**opt_list)

    except GetoptError:          
        usage()                         
        sys.exit(2)        
           
