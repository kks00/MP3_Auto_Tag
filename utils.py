import requests

def GetWebData(url="", cookies=None):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    reqWeb = requests.get(url, headers=headers, cookies=cookies)
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


def parseStr(strTarget, strStart, strEnd):
    inxStart = strTarget.find(strStart)
    if inxStart == -1:
        return ""
    strTarget = strTarget[inxStart+len(strStart):]
    inxEnd = strTarget.find(strEnd)
    if inxEnd == -1:
        return ""
    return strTarget[0:inxEnd]

def GetDataList(strTarget, strStart, strEnd):
    ResultList = []
    while True:
        inxStart = strTarget.find(strStart)
        if inxStart == -1:
            break
        strTarget = strTarget[inxStart+len(strStart):]
        inxEnd = strTarget.find(strEnd)
        if inxEnd == -1:
            break
        ResultList.append(strTarget[0:inxEnd])
        strTarget = strTarget[inxEnd+len(strEnd):]
    return ResultList
