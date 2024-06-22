import eyed3
import os

from get_song_info import get_song_list, get_song_albumart

for curFileName in os.listdir(os.path.dirname(os.path.realpath(__file__)) + "/mp3"):
    print("현재 파일: {0}".format(curFileName))
    
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

    song_list = get_song_list(curKeyword, 10)
    if len(song_list) > 0:
        for index, curr_song in enumerate(song_list):
            curr_title = curr_song["Title"]
            curr_artist = curr_song["Artist"]
            curr_album = curr_song["Album"]
            print("{0}: 제목: {1}, 아티스트: {2}, 앨범: {3}".format(index, curr_title, curr_artist, curr_album))
        selected_index = int(input(""))

        curAudioFile.initTag()
        selected_song = song_list[selected_index]
        curAudioFile.tag.title = selected_song["Title"]
        curAudioFile.tag.artist = selected_song["Artist"]
        curAudioFile.tag.album = selected_song["Album"]

        if not os.path.exists('AlbumArt'):
            os.makedirs('AlbumArt')
        fAlbumArt = open('AlbumArt/' + curFileName + '.jfif', "wb")
        fAlbumArt.write(get_song_albumart(selected_song["AlbumArtURL"]))
        fAlbumArt.close()
        curAudioFile.tag.images.remove(u'')
        fAlbumArt = open('AlbumArt/' + curFileName + '.jfif', "rb")
        curAudioFile.tag.images.set(3, fAlbumArt.read(), "image/jpeg")
        fAlbumArt.close()
        
        curAudioFile.tag.save(encoding='utf-8', version=eyed3.id3.ID3_V2_4)
        
        print("태그 설정에 성공하였습니다.")
    else:
        print("검색 결과가 존재하지 않아 실패하였습니다.")