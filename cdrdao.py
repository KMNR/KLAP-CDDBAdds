import subprocess
import os
import shlex
import winshell
import sys

SCRIPT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))
CDRDAO_EXEC = os.path.join(SCRIPT_DIR,"cdrdao.exe")
TOC_FILE = os.path.join(winshell.application_data(),"KLAP-TOC.dat")

def scan_devices():
    cmd = [ CDRDAO_EXEC, "scanbus", "-v", "0" ]
    print cmd
    result = subprocess.check_output(cmd,stderr=subprocess.STDOUT)
    result = result.split("\n")
    lst = []
    for line in result:
        if len(line) == 0:
            continue
        chunks = line.split(":")
        deviceid = chunks[0].strip()
        devicename = chunks[1].strip()
        lst.append( (deviceid,devicename) )
    return lst
    
def read_toc(device):
    try:
        os.remove(TOC_FILE)
    except WindowsError:
        pass
    cmd = [ CDRDAO_EXEC, "read-toc", "--fast-toc", "--device", device, TOC_FILE ]
    print cmd
    subprocess.call(cmd)
    r = parse_toc_data(TOC_FILE)
    os.remove(TOC_FILE)
    return r
    
def get_discid(device):
    cmd = [ CDRDAO_EXEC, "discid", "--query-string", "--device", device ]
    print cmd
    result = subprocess.check_output(cmd)
    print "\n--------------------------\n"
    return result.strip().split()
    
def parse_toc_data(file):
    fp = open(file)
    stack = [{'TRACKS':[]}]
    in_track = False
    for line in fp:
        tokens = shlex.split(line)
        plist = []
        for item in tokens:
            if item == "//":
                #This is annoying because it is effectively a nested thing, but backwards
                if in_track == True:
                    stack.pop()
                in_track = True
                number = int(line.replace("// Track","").strip())
                subd = {'NUMBER': number}
                stack[0]['TRACKS'].append(subd)
                stack.append(subd)
                break
            elif item == "{":
                subd = {}
                key = ' '.join(plist)
                stack[-1][key] = subd
                stack.append(subd)
                plist = []
            elif item == "}":
                stack.pop()
            else:
                plist.append(item)
        if len(plist) == 1:
            try:
                d = stack[-1]
                d['PROPERTIES'].append(plist[0])
            except KeyError:
                d['PROPERTIES'] = [ plist[0] ]
        elif len(plist) > 1:
            key = plist.pop(0)
            value = ' '.join(plist)
            d = stack[-1]
            try:
                d[key].append(value)
            except AttributeError:
                d[key] = [ d[key] ]
                d[key].append(value)
            except KeyError:
                d[key] = value
                
    return stack[0]
    
def toc_to_KLAP(toc_data):
    # First, establish what language to use
    language_choices = toc_data['CD_TEXT']['LANGUAGE_MAP']
    language = None
    for (lang,code) in language_choices.iteritems():
        if int(code) == 9:
            language = lang.replace(":","")
            break
    else:
        language = "0"
    language = "LANGUAGE {}".format(language)
    
    # Next, identify artist and album
    artist = toc_data['CD_TEXT'][language]['PERFORMER']
    album = toc_data['CD_TEXT'][language]['TITLE']
    
    #Then for each track, extract the title and number
    tracks = []
    for track in toc_data['TRACKS']:
        subd = {'number': track['NUMBER']}
        subd['title'] = track['CD_TEXT'][language]['TITLE']
        performer = track['CD_TEXT'][language]['PERFORMER']
        #if performer != artist:
        #    subd['performer'] = performer
        tracks.append(subd)
    
    return {'artist': artist, 'album':album, 'tracks':tracks}