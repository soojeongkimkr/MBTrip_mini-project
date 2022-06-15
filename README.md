## MBTrip 🛬
각자의 성향, 성격을 파악할 수 있는 MBTI별로 추천하는 서울 여행지

![KakaoTalk_20220512_175629082](https://user-images.githubusercontent.com/99132215/168429045-7d9af0a6-922b-4884-b796-65e99d92e6f6.png)


## 1. 제작 기간 & 팀원 소개 👨‍👩‍👧‍👧  ##
- **2022년 5월 9일 ~ 2022년 5월 12일 4인 1조 프로젝트**
- 김수정 : 상세 페이지, 사이드바
- 김하얀 : 로그인, 회원가입 
- 이다희 : 메인 페이지
- 홍수민 : 리뷰 쓰기 

## 2. 사용 기술 🛠
- **언어**
<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=Python&logoColor=white">
<img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=JavaScript&logoColor=white">
<img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=HTML5&logoColor=white">
<img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=CSS3&logoColor=white">

- **프레임워크**
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=Flask&logoColor=white">

- **데이터베이스**
<img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=MongoDB&logoColor=white">

- **호스팅**
<img src="https://img.shields.io/badge/Amazon AWS-232F3E?style=for-the-badge&logo=Amazon AWS&logoColor=white">

- **협업**
<img src="https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=GitHub&logoColor=white">

## 3. 실행화면  💻

- **로그인 페이지**

<img width="1269" alt="로그인 페이지" src="https://user-images.githubusercontent.com/99132215/168429024-e744c201-edf1-4e6b-9bad-a5cc505c10a9.PNG">


- **메인 페이지**
<img width="683" alt="메인 페이지" src="https://user-images.githubusercontent.com/99132215/168429032-eacdb355-0967-47d6-88a7-cdaf0a677a7d.PNG">


- **상세 페이지**
<img width="777" alt="상세페이지" src="https://user-images.githubusercontent.com/99132215/168429037-dbf7331d-f546-4bd9-8730-a414e9428e4f.PNG">

🔍 [MBTrip 사이트](http://mbtrip.shop/)

🎥 [MBTrip 시연영상](https://www.youtube.com/watch?v=-QKiKGg499s)


## 4. 핵심 기능 💡
**로그인**
 - JWT 방식으로 구현
 - 회원가입 버튼 클릭 시 회원가입 페이지로 변경

**회원가입**
  - 아이디 중복확인시 아이디 입력 여부, 형식, 중복 아이디 체크
  - 비밀번호 2번 입력으로 비밀번호 형식, 일치 여부 체크

**메인 화면**
  - MBTI 카드 클릭 시 MBTI 별 서울 여행지 추천 상세 및 리뷰 페이지로 이동

**상세 화면**
 - MBTI별 서울 추천 여행지 정보 구현
 - 다른 MBTI 페이지로 넘어갈 수 있는 사이드바 구현

**리뷰 화면**
- 작성 하기 버튼 클릭 시, DB에 해당 리뷰 저장
- jina2언어를 사용하여 리뷰에 로그인한 사용자의 이름을 보이는 기능 구현
- 휴지통 아이콘 클릭 시, 리뷰 삭제 기능 : 작성한 아이디 데이터를 이용하여 포스트 삭제 기능
- 하트 아이콘 클릭 시,리뷰 좋아요 기능 : db에 저장된 좋아요 수 증가, 어떤 포스터에 좋아요가 눌러졌는지 확인하는 기능
