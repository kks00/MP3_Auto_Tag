# MP3 Auto Tag

- ### 유튜브 다운로더 등으로 구한 MP3음원의 태그, 앨범아트, 가사를 자동으로 재설정 해주는 스크립트

- ### python의 eyed3 라이브러리를 이용하여 MP3파일의 메타정보 변경

    #### 사진을 클릭해주세요
    ![Honeycam 2024-03-23 22-28-52](https://github.com/kks00/MP3_Auto_Tag/assets/68108664/ab1ce416-d81d-4679-baec-6b9878ca17fb)

---
<br><br>

# 구성 요소

- ### lyrics.py
    - ### MP3파일의 가사 데이터를 지니뮤직에서 크롤링하여 자동으로 설정해주는 스크립트

<br>

- ### lyrics19.py
    - ### 19금 음원의 가사 데이터를 자동으로 설정해주는 스크립트
    - ### 지니뮤직 정책 상 성인인증이 된 계정으로만 19금 음원의 가사를 열람할 수 있으므로 스크립트 내에서 성인 인증이 이루어진 계정으로의 로그인이 필요

        ```python
        import eyed3
        import os
        import requests
        from urllib import parse

        GenieID = 'your genie id' <
        GeniePW = 'your genie pw' <
        ```

<br>

- ### tag.py
    - ### MP3파일의 태그정보, 앨범아트를 지니뮤직에서 크롤링하여 자동으로 설정해주는 스크립트
