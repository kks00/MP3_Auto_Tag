import eyed3
import os

from get_song_info import get_song_list, get_genie_login_cookie, GenieID, GeniePW, is_first_auto

genie_cookie = get_genie_login_cookie(GenieID, GeniePW)
if genie_cookie is None:
    print("지니 로그인에 실패하였습니다. 19금 음원의 가사를 가져오지 못할 수 있습니다.")

for curFileName in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/mp3"):
    print("현재 파일: {0}".format(curFileName))

    curAudioFile = eyed3.load(os.path.dirname(os.path.realpath(__file__)) + "/mp3/" + curFileName)

    curFileName = curFileName[:curFileName.find(".mp3")]
    curTitle = curFileName.split(" - ")[0]
    curArtist = curFileName.split(" - ")[1]
    curKeyword = "{0} {1}".format(curTitle, curArtist)

    song_list = get_song_list(curKeyword, 10, genie_cookie)
    if len(song_list) > 0:
        selected_index = 0
        if (len(song_list) > 1) and (not is_first_auto):
            for index, curr_song in enumerate(song_list):
                curr_title = curr_song["Title"]
                curr_artist = curr_song["Artist"]
                curr_album = curr_song["Album"]
                print("{0}: 제목: {1}, 아티스트: {2}, 앨범: {3}".format(index, curr_title, curr_artist, curr_album))
            selected_index = int(input(""))

        selected_song = song_list[selected_index]
        curAudioFile.tag.lyrics.set(selected_song["lyrics"])
        curAudioFile.tag.save()
        print("가사 설정에 성공하였습니다.")
    else:
        print("검색 결과가 존재하지 않아 실패하였습니다.")
