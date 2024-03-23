import eyed3
import os
import requests
from urllib import parse

def parseStr(strTarget="", strStart="", strEnd=""):
    inxStart = strTarget.find(strStart)
    if (inxStart == -1): return ""
    strTarget = strTarget[inxStart+len(strStart):]
    inxEnd = strTarget.find(strEnd)
    if (inxEnd == -1): return ""
    return strTarget[0:inxEnd]

def GetDataList(strTarget="", strStart="", strEnd=""):
    ResultList = []
    Index = 0
    while True:
        inxStart = strTarget.find(strStart)
        if (inxStart == -1): break;
        strTarget = strTarget[inxStart+len(strStart):]
        inxEnd = strTarget.find(strEnd)
        if (inxEnd == -1): break;
        ResultList.insert(Index, strTarget[0:inxEnd])
        strTarget = strTarget[inxEnd+len(strEnd):]
        Index += 1
    return ResultList

def GetWebData(url=""):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    reqWeb = requests.get(url, headers=headers)
    if (reqWeb.status_code == 200):
        return reqWeb.text
    else:
        return ""

ProcessCount = [0, 0]

for curFileName in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/mp3"):
    print("Processing File : {0}... ".format(curFileName), end="");
    
    curAudioFile = eyed3.load(os.path.dirname(os.path.realpath(__file__)) + "/mp3/" + curFileName)

    curArtist = curAudioFile.tag.artist
    if (type(curArtist) == str):
        if (curArtist.find(" ") != -1):
            curArtist = curArtist[:curArtist.find(" ")]
    curKeyword = "{0} {1}".format(curArtist, curAudioFile.tag.title)

    resSearch = GetDataList(GetWebData("https://www.genie.co.kr/search/searchSong?query=" + parse.quote(curKeyword) + "&page=1&pagesize=100"), '<tr class="list" songid="', '">')
    if len(resSearch) > 0:
        curSongLyrics = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0]), '<pre id="pLyrics">', '</pre>')
        curSongLyrics = parseStr(curSongLyrics, '<p>', '</p>')
        curAudioFile.tag.lyrics.set(curSongLyrics)
        curAudioFile.tag.save()
        print("Success!")
        ProcessCount[0] += 1
    else:
        print("Failed!")
        ProcessCount[1] += 1

print("Completed! Success : {0}, Failed: {1}".format(str(ProcessCount[0]), str(ProcessCount[1])))
