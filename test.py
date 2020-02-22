import time
import locale


def textBox(text, width, align="right", fix=True):
    ####
    # this function do :
    # 1: add extra spaces in original string for left/center/right alignment
    # 2: add extra newlines ("\n") to write text on a box instead of a single line, width represents the width of the box
    ####

    #if no align is needed, return @_@
    if align=="none":
        return text
    # delete arabic decorations on the first call only
    if fix:
        text = text.translate({i: None for i in range(1611, 1649)})
    # base case
    if len(text) <= width:
        if align == "right":
            return \
                text[0:len(text)] \
                + " "*(width-len(text)-1) + "\n" 
        elif align == "center":
            return \
            " "*int((width-len(text)-1)/2) \
             + text[0:len(text)] \
            + " "*int((width-len(text)-1)/2) + "\n" 
        elif align == "left":
            return \
            " "*(width-len(text)-1) + \
            text[0:len(text)] + "\n"
    ###
    i = 0
    last_space = 0
    while i <= width:
        # find the index of last space in the width slice
        if text[i] == " ":
            last_space = i
        i += 1

    # retutn the string depending on alingment
    if align == "right":
        return \
            text[0:last_space] \
            + " "*(width-last_space-1) + "\n" \
            + textBox(text[last_space+1:], width, align, False)
    elif align == "center":
        return \
            " "*int((width-last_space-1)/2) \
            + text[0:last_space] \
            + " "*int((width-last_space-1)/2) + "\n" \
            + textBox(text[last_space+1:], width, align, False)
    elif align == "left":
        return \
            " "*(width-last_space-1) + \
            text[0:last_space] + "\n"\
            + textBox(text[last_space+1:], width, align, False)


s = "سيكونُ الطقسُ فانتاستكِ جداً جداً و جميلا كثيرا"

x = textBox(s,11)
print(list(x))
