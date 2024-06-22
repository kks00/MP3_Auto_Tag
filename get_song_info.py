import requests
from urllib import parse

from utils import GetWebData, GetWebContent, parseStr, GetDataList

def get_song_list(keyword, top_n, cookies=None):
    song_id_list = GetDataList(GetWebData("https://www.genie.co.kr/search/searchSong?query=" + parse.quote(keyword) + "&page=1&pagesize=100"), '<tr class="list" songid="', '">')
    if len(song_id_list) < 1:
        return {}

    result = []
    for i in range(min(len(song_id_list), top_n)):
        curr_song_id = song_id_list[i]

        curr_song_info = GetWebData("https://www.genie.co.kr/detail/songInfo?xgnm=" + curr_song_id, cookies=cookies)
        curr_song_title = parseStr(curr_song_info, '<meta property="og:title" content="', ' - genie"/>')

        curr_song_artist = parseStr(curr_song_info, "fnGoMore('artistInfo'", '</span>')
        curr_song_artist = parseStr(curr_song_artist, '">', '</a>')

        curr_song_album = parseStr(curr_song_info, "fnGoMore('albumInfo'", '</span>')
        curr_song_album = parseStr(curr_song_album, '">', '</a>')

        curr_song_album_art = parseStr(curr_song_info, '<div class="photo-zone">', '</div>')
        curr_song_album_art = "https:" + parseStr(curr_song_album_art, '<a href="', '"')

        curr_song_lyrics = parseStr(curr_song_info, '<pre id="pLyrics">', '</pre>')
        curr_song_lyrics = parseStr(curr_song_lyrics, '<p>', '</p>')

        curr_result = {}
        curr_result["Title"] = curr_song_title
        curr_result["Artist"] = curr_song_artist
        curr_result["Album"] = curr_song_album
        curr_result["AlbumArtURL"] = curr_song_album_art
        curr_result["lyrics"] = curr_song_lyrics
        result.append(curr_result)
    return result

def get_song_albumart(url):
    return GetWebContent(url)

def get_genie_login_cookie(id, pw):
    reqHeaders = {'Content-Type': 'application/x-www-form-urlencoded',
                  'Referer': 'https://www.genie.co.kr/member/popLogin?page_rfr=https%3A//genie.co.kr/',
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
    reqData = 'login_suxd=&login_suxn=&login_suxt=&chk=&login_http=https&uxd={0}&uxx={1}&ucc=&uxglk=0&f_JoinType=&mh=&lk_rfr='.format(id, pw)
    reqLogin = requests.post('https://www.genie.co.kr/auth/signIn', data=reqData, headers=reqHeaders)
    if (reqLogin.status_code == 200):
        return reqLogin.cookies
    return None