import eyed3
import os
import requests
from urllib import parse

GenieID = 'your genie id'
GeniePW = 'your genie pw'

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

def GetWebData(url, reqCookie):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    reqWeb = requests.get(url, headers=headers, cookies=reqCookie)
    if (reqWeb.status_code == 200):
        return reqWeb.text
    else:
        return ""

reqHeaders = {'Content-Type': 'application/x-www-form-urlencoded',
              'Referer': 'https://www.genie.co.kr/member/popLogin?page_rfr=https%3A//genie.co.kr/',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
reqData = 'login_suxd=&login_suxn=&login_suxt=&chk=&login_http=https&uxd={0}&uxx={1}&ucc=&uxglk=0&f_JoinType=&mh=&lk_rfr='.format(GenieID, GeniePW)
reqLogin = requests.post('https://www.genie.co.kr/auth/signIn', data=reqData, headers=reqHeaders)
if (reqLogin.status_code == 200):
    ProcessCount = [0, 0]

    for curFileName in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/mp3"):
        print("Processing File : {0}... ".format(curFileName), end="");
        
        curAudioFile = eyed3.load(os.path.dirname(os.path.realpath(__file__)) + "/mp3/" + curFileName)

        curArtist = curAudioFile.tag.artist
        if (type(curArtist) == str):
            if (curArtist.find(" ") != -1):
                curArtist = curArtist[:curArtist.find(" ")]
        curKeyword = "{0} {1}".format(curArtist, curAudioFile.tag.title)

        resSearch = GetDataList(GetWebData("https://www.genie.co.kr/search/searchSong?query=" + parse.quote(curKeyword) + "&page=1&pagesize=100", reqLogin.cookies), '<tr class="list" songid="', '">')
        if len(resSearch) > 0:
            curSongLyrics = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0], reqLogin.cookies), '<pre id="pLyrics">', '</pre>')
            curSongLyrics = parseStr(curSongLyrics, '<p>', '</p>')
            curAudioFile.tag.lyrics.set(curSongLyrics)
            curAudioFile.tag.save()
            print("Success!")
            ProcessCount[0] += 1
        else:
            print("Failed!")
            ProcessCount[1] += 1

    print("Completed! Success : {0}, Failed: {1}".format(str(ProcessCount[0]), str(ProcessCount[1])))
