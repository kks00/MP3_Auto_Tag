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

def GetWebContent(url=""):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    reqWeb = requests.get(url, headers=headers)
    if (reqWeb.status_code == 200):
        return reqWeb.content
    else:
        return ""

ProcessCount = [0, 0]

for curFileName in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/mp3"):
    print("Processing File : {0}...".format(curFileName))
    
    curAudioFile = eyed3.load(os.path.dirname(os.path.realpath(__file__)) + "/mp3/" + curFileName)
    
    curFileName = curFileName[:curFileName.find(".mp3")]
    curTitle = curFileName.split(" - ")[0]
    if len(curTitle.split(" ")) > 1:
        curTitle = "{0} {1}".format(curTitle.split(" ")[0], curTitle.split(" ")[1])
    else:
        curTitle = curTitle.split(" ")[0]
    curArtist = curFileName.split(" - ")[1]
    if len(curArtist.split(" ")) > 0:
        curArtist = curArtist.split(" ")[0]
    curKeyword = "{0} {1}".format(curTitle, curArtist)

    curAudioFile.initTag()

    resSearch = GetDataList(GetWebData("https://www.genie.co.kr/search/searchSong?query=" + parse.quote(curKeyword) + "&page=1&pagesize=100"), '<tr class="list" songid="', '">')
    if len(resSearch) > 0:
        curSongTitle = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0]), '<meta property="og:title" content="', ' - genie"/>')
        curSongTitle = curSongTitle[:curSongTitle.find("/")]
        print("Title = {0}".format(curSongTitle))
        curAudioFile.tag.title = curSongTitle
        
        curSongArtist = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0]), "fnGoMore('artistInfo'", '</span>')
        curSongArtist = parseStr(curSongArtist, '">', '</a>')
        print("Artist = {0}".format(curSongArtist))
        curAudioFile.tag.artist = curSongArtist

        curSongAlbum = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0]), "fnGoMore('albumInfo'", '</span>')
        curSongAlbum = parseStr(curSongAlbum, '">', '</a>')
        print("Album = {0}".format(curSongAlbum))
        curAudioFile.tag.album = curSongAlbum

        curSongAlbumArt = parseStr(GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + resSearch[0]), '<div class="photo-zone">', '</div>')
        curSongAlbumArt = "https:" + parseStr(curSongAlbumArt, '<a href="', '"')
        print("AlbumArt = {0}".format(curSongAlbumArt))

        if not os.path.exists('AlbumArt'):
            os.makedirs('AlbumArt')
        fAlbumArt = open('AlbumArt/' + curFileName + '.jfif', "wb")
        fAlbumArt.write(GetWebContent(curSongAlbumArt))
        fAlbumArt.close()
        curAudioFile.tag.images.remove(u'')
        fAlbumArt = open('AlbumArt/' + curFileName + '.jfif', "rb")
        curAudioFile.tag.images.set(3, fAlbumArt.read(), "image/jpeg")
        fAlbumArt.close()
        
        curAudioFile.tag.save(encoding='utf-8', version=eyed3.id3.ID3_V2_4)
        
        print("Success!")
        ProcessCount[0] += 1
    else:
        print("Failed!")
        ProcessCount[1] += 1

print("Completed! Success : {0}, Failed: {1}".format(str(ProcessCount[0]), str(ProcessCount[1])))
