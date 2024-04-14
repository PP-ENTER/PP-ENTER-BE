공용 UI 작업
(피그마)[https://www.figma.com/file/78bA1taofPgdNSXMKUzZ9c/Untitled?type=design&mode=design&t=ePYJJeT7TlkQEvAa-0]

![header]([https://capsule-render.vercel.app/api?type=venom&height=300&color=auto&text=PPnENTER&fontColor=white])

# PP-ENTER
## 영상통화 기능이 가능한 소셜 미디어 웹 서비스

## 1. 목표와 기능

### 1.1 목표
- 영상통화를 중심으로 한 실시간 소통과 일상 공유 플랫폼 구축
- 영상통화 중 감정 인식 기술을 활용해 참여자의 경험 향상
- 영상통화 중 생성된 콘텐츠(스크린샷)를 바탕으로 한 커뮤니티 활성화

### 1.2 기능
- 실시간 영상통화 기능 (1:1 및 최대 4인 그룹 통화)
- 영상통화 중 참여자의 감정을 인식하고 분석하여 배경 필터 자동 적용
- 필터가 적용된 영상통화 화면 스크린샷 캡처 및 저장
- 저장된 스크린샷을 피드에 포스팅하여 공유 및 소통
- 포스팅에 댓글, 좋아요 등 소셜 네트워크 기본 기능 지원
- 친구 추가, 팔로우 등 사용자 간 연결 기능


### 1.3 팀 구성
- 실제 사진을 업로드 하시길 권합니다.
<table>
	<tr>
		<th>박상현</th>
		<th>엄영철</th>
		<th>이은희</th>
		<th>진성현</th>
	</tr>
 	<tr>
		<td><img src="my.jpg" width="100%"></td>
		<td><img src="my.jpg" width="100%"></td>
		<td><img src="my.jpg" width="100%"></td>
		<td><img src="my.jpg" width="100%"></td>
	</tr>
</table>

## 2. 개발 환경 및 배포 URL
### 2.1 개발 환경
- Web Framework
  - Django 3.x (Python 3.8)
- FE
  - tailwind, JS
- 기능라이브러리??
  - Deepface, OpenCV
- 서비스 배포 환경
  - Amazon Lightsail
 
### 2.2 배포 URL
- https://www.
- 테스트용 계정
  ```
  id : test@test.test
  pw : test11!!
  ```

### 2.3 URL 구조(마이크로식)


| URL 패턴 | 뷰 클래스 | 설명 |
|----------|-----------|------|
| **계정 (accounts)** |
| `register/` | `RegisterView` | 회원가입 기능 |
| `login/` | `LoginView` | 로그인 기능 |
| `logout/` | `LogoutView` (mixins: `LogoutMixin`) | 로그아웃 기능 |
| `profile/` | `UserProfileView` | 사용자 프로필 정보 조회 및 수정 |
| `password/change/` | `PasswordChangeView` (mixins: `PasswordChangeFormMixin`) | 비밀번호 변경 기능 |
| **게시물 (posts)** |
| `posts/` | `PostListView` | 게시물 목록 조회 |
| `posts/create/` | `PostCreateView` | 새로운 게시물 작성 |
| `posts/<int:pk>/` | `PostDetailView` | 개별 게시물 상세 정보 조회 |
| `posts/<int:pk>/update/` | `PostUpdateView` | 게시물 수정 |
| `posts/<int:pk>/delete/` | `PostDeleteView` | 게시물 삭제 |
| `posts/<int:pk>/like/` | `PostLikeView` (mixins: `LikeMixin`) | 게시물 좋아요 기능 |
| `posts/<int:pk>/favorite/` | `PostFavoriteView` (mixins: `FavoriteMixin`) | 게시물 즐겨찾기 기능 |
| `posts/<int:pk>/tags/` | `PostTagListView` | 게시물 태그 목록 조회 |
| `posts/<int:pk>/tags/create/` | `PostTagCreateView` | 게시물 태그 추가 |
| `posts/<int:pk>/tags/<int:tag_pk>/delete/` | `PostTagDeleteView` | 게시물 태그 삭제 |
| `posts/<int:pk>/comments/` | `CommentListView` | 게시물 댓글 목록 조회 |
| `posts/<int:pk>/comments/create/` | `CommentCreateView` | 새로운 댓글 작성 |
| `posts/<int:pk>/comments/<int:comment_pk>/update/` | `CommentUpdateView` | 댓글 수정 |
| `posts/<int:pk>/comments/<int:comment_pk>/delete/` | `CommentDeleteView` | 댓글 삭제 |
| **친구 (friends)** |
| `friends/` | `FriendListView` | 친구 목록 조회 |
| `friends/requests/` | `FriendRequestListView` | 친구 요청 목록 조회 |
| `friends/requests/<int:pk>/accept/` | `FriendRequestAcceptView` (mixins: `FriendRequestMixin`) | 친구 요청 수락 |
| `friends/requests/<int:pk>/reject/` | `FriendRequestRejectView` (mixins: `FriendRequestMixin`) | 친구 요청 거절 |
| `friends/<int:pk>/remove/` | `FriendRemoveView` (mixins: `FriendRemoveMixin`) | 친구 삭제 |
| **실시간 채팅 (facechats)** |
| `facechats/` | `FaceChatListView` | 실시간 채팅방 목록 조회 |
| `facechats/create/` | `FaceChatCreateView` | 새로운 실시간 채팅방 생성 |
| `facechats/<int:pk>/` | `FaceChatDetailView` | 개별 실시간 채팅방 정보 조회 |
| `facechats/<int:pk>/join/` | `FaceChatJoinView` (mixins: `FaceChatMixin`) | 실시간 채팅방 참가 |
| `facechats/<int:pk>/leave/` | `FaceChatLeaveView` (mixins: `FaceChatMixin`) | 실시간 채팅방 나가기 |
| `facechats/<int:pk>/messages/` | `FaceChatMessageListView` | 실시간 채팅 메시지 목록 조회 |
| `facechats/<int:pk>/messages/create/` | `FaceChatMessageCreateView` | 새로운 실시간 채팅 메시지 생성 |


## 3. 요구사항 명세와 기능 명세
- https://www.mindmeister.com/ 등을 사용하여 모델링 및 요구사항 명세를 시각화하면 좋습니다.
- 이미지는 셈플 이미지입니다.
<img src="map.png" width="100%">
- 머메이드를 이용해 시각화 할 수 있습니다.
  
```mermaid
    sequenceDiagram
    actor A as client
    participant B as Web
    participant C as server
    A->>+B: 로그인 요청
    B->>+A: 로그인 정보 요구
    A->>+C: id, pw 전달
    alt 로그인 정보가 있고 로그인 정보가 맞을 시
    C->>+B: access token, refresh token 전달
    B->>+A: 로그인 성공
    else 로그인 정보가 없거나 정보가 맞지 않을시
    C->>+B: False
    B->>+A: 로그인 실패
    end
```

## 4. 프로젝트 구조와 개발 일정
### 4.1 프로젝트 구조
- 해당 프로젝트에서 폴더 트리 잘 다듬어 사용하세요. 필요하다면 주석을 달아주세요.
📦tutorial  
 ┣ 📂accounts  
 ┃ ┣ 📂migrations  
 ┃ ┣ 📂__pycache__  
 ┃ ┣ 📜admin.py  
 ┃ ┣ 📜apps.py  
 ┃ ┣ 📜forms.py  
 ┃ ┣ 📜models.py  
 ┃ ┣ 📜tests.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜views.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂blog  
 ┃ ┣ 📂migrations  
 ┃ ┣ 📂__pycache__  
 ┃ ┣ 📜admin.py  
 ┃ ┣ 📜apps.py  
 ┃ ┣ 📜forms.py  
 ┃ ┣ 📜models.py  
 ┃ ┣ 📜tests.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜views.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂board  
 ┃ ┣ 📂migrations  
 ┃ ┣ 📂__pycache__  
 ┃ ┣ 📜admin.py  
 ┃ ┣ 📜apps.py  
 ┃ ┣ 📜forms.py  
 ┃ ┣ 📜models.py  
 ┃ ┣ 📜tests.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜views.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂main  
 ┃ ┣ 📂migrations  
 ┃ ┣ 📂__pycache__  
 ┃ ┣ 📜admin.py  
 ┃ ┣ 📜apps.py  
 ┃ ┣ 📜models.py  
 ┃ ┣ 📜tests.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜views.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂media  
 ┃ ┣ 📂accounts  
 ┃ ┣ 📂blog  
 ┃ ┗ 📂board  
 ┣ 📂static  
 ┃ ┣ 📂assets  
 ┃ ┃ ┣ 📂css  
 ┃ ┃ ┃ ┣ 📂apps  
 ┃ ┃ ┃ ┣ 📂authentication  
 ┃ ┃ ┃ ┣ 📂components  
 ┃ ┃ ┃ ┣ 📂dashboard  
 ┃ ┃ ┃ ┣ 📂elements  
 ┃ ┃ ┃ ┣ 📂forms  
 ┃ ┃ ┃ ┣ 📂pages  
 ┃ ┃ ┃ ┣ 📂tables  
 ┃ ┃ ┃ ┣ 📂users  
 ┃ ┃ ┣ 📂images  
 ┃ ┃ ┃ ┣ 📂mockup_image  
 ┃ ┃ ┣ 📂img  
 ┃ ┃ ┗ 📂js  
 ┃ ┣ 📂bootstrap  
 ┃ ┃ ┣ 📂css  
 ┃ ┃ ┗ 📂js  
 ┃ ┗ 📂plugins  
 ┣ 📂tech_blog  
 ┃ ┣ 📂__pycache__  
 ┃ ┣ 📜.env  
 ┃ ┣ 📜asgi.py  
 ┃ ┣ 📜settings.py  
 ┃ ┣ 📜urls.py  
 ┃ ┣ 📜wsgi.py  
 ┃ ┗ 📜__init__.py  
 ┣ 📂templates  
 ┃ ┣ 📂accounts  
 ┃ ┃ ┣ 📜login.html  
 ┃ ┃ ┣ 📜password_change.html  
 ┃ ┃ ┣ 📜profile.html  
 ┃ ┃ ┣ 📜profile_edit.html  
 ┃ ┃ ┣ 📜signup.html  
 ┃ ┃ ┗ 📜user_list.html  
 ┃ ┣ 📂blog  
 ┃ ┃ ┣ 📜blog_base.html  
 ┃ ┃ ┣ 📜post_detail.html  
 ┃ ┃ ┣ 📜post_form.html  
 ┃ ┃ ┣ 📜post_list.html  
 ┃ ┃ ┗ 📜post_not_found.html  
 ┃ ┣ 📂board  
 ┃ ┃ ┣ 📜board_base.html  
 ┃ ┃ ┣ 📜board_post_detail.html  
 ┃ ┃ ┣ 📜board_post_form.html  
 ┃ ┃ ┗ 📜board_post_list.html  
 ┃ ┣ 📂main  
 ┃ ┃ ┗ 📜index.html  
 ┃ ┣ 📜404.html  
 ┃ ┗ 📜base.html  
 ┣ 📜CONVENTION.md  
 ┣ 📜db.sqlite3  
 ┣ 📜manage.py  
 ┣ 📜README.md  
 ┗ 📜requirements.txt  

### 4.1 개발 일정(WBS)
* 아래 일정표는 머메이드로 작성했습니다.
```mermaid

gantt
    title 피피앤엔터 개발 일정
    dateFormat YY-MM-DD
    section 계획
        조사 및 분석 : 2024-03-29, 3일
        기능 명세서 : 2024-04-01, 1일
        앱 구성 계획 : 2024-04-02, 1일
        기능 상세 설계 : 2024-04-03, 1일
        감정 표현 모델 개발 : 2024-04-01, 3일
    section 계정
        회원가입 뷰 : 2024-04-04, 3일
        로그인 뷰 : 2024-04-07, 3일
        로그아웃 뷰 : 2024-04-10, 3일
        프로필 뷰 : 2024-04-13, 3일
        비밀번호 변경 뷰 : 2024-04-16, 3일
    section 게시물
        게시물 목록 뷰 : 2024-04-04, 3일
        게시물 생성 뷰 : 2024-04-07, 3일
        게시물 상세 뷰 : 2024-04-10, 3일
        게시물 수정 뷰 : 2024-04-13, 3일
        게시물 삭제 뷰 : 2024-04-16, 3일
        게시물 좋아요 뷰 : 2024-04-19, 3일
        게시물 즐겨찾기 뷰 : 2024-04-22, 3일
        게시물 태그 목록 뷰 : 2024-04-25, 3일
        게시물 태그 생성 뷰 : 2024-04-28, 3일
        게시물 태그 삭제 뷰 : 2024-05-01, 3일
        댓글 목록 뷰 : 2024-05-04, 3일
        댓글 생성 뷰 : 2024-05-07, 3일
        댓글 수정 뷰 : 2024-05-10, 3일
        댓글 삭제 뷰 : 2024-05-13, 3일
    section 친구
        친구 목록 뷰 : 2024-04-18, 3일
        친구 요청 목록 뷰 : 2024-04-21, 3일
        친구 요청 수락/거절 뷰 : 2024-04-24, 3일
        친구 삭제 뷰 : 2024-04-27, 3일
    section 라이브 채팅
        라이브 채팅 목록 뷰 : 2024-05-01, 3일
        라이브 채팅 생성 뷰 : 2024-05-04, 3일
        라이브 채팅 상세 뷰 : 2024-05-07, 3일
        라이브 채팅 참여/나가기 뷰 : 2024-05-10, 3일
        라이브 채팅 메시지 목록 뷰 : 2024-05-13, 3일
        라이브 채팅 메시지 생성 뷰 : 2024-05-16, 3일
    section 감정 인식 및 비디오 콜 (미래)
        감정 인식 모델 개발 : 2024-04-01, 3일
        비디오 콜 기능 개발 : 2024-05-01, 10일
        감정 모델 통합 : 2024-05-15, 5일
    section 완료
        통합 테스트 : 2024-05-20, 1일
        마지막 완료 : 2024-05-21, 1일

```

* 아래 WBS는 엑셀을 이용했습니다. 양식은 [다운로드](./WBS_sample.xlsx) 받아 사용하세요. (출처 : https://techcommunity.microsoft.com/gxcuf89792/attachments/gxcuf89792/ExcelGeneral/204594/1/WBS_sample.xlsx)
<img src="wbs_xlsx.png" width="80%">

* 좀 더 가벼운 프로젝트는 아래 일정표를 사용하세요.
* 아래 일정표는 [habitmaker.co.kr](https://habitmaker.co.kr) 에서 작성되었습니다.
* 관련된 스택 표시는 [dev.habitmaker.co.kr](https://dev.habitmaker.co.kr) 에서 작성되었습니다.
<img src="habit.jpg" width="50%">
<img src="blob.png" width="50%">

## 5. 역할 분담

- 팀장 : 진성현
- FE : 박상현
- FE : 엄영철
- BE : 이은희
- BE : 진성현
- 디자인 : 팀원공통 기획

## 6. 와이어프레임 / UI / BM

### 6.1 와이어프레임
- 아래 페이지별 상세 설명, 더 큰 이미지로 하나하나씩 설명 필요
<img src="ui.png" width="60%">

- 와이어 프레임은 디자인을 할 수 있다면 '피그마'를, 디자인을 할 수 없다면 '카카오 오븐'으로 쉽게 만들 수 있습니다.

### 6.2 화면 설계
- 화면은 gif파일로 업로드해주세요.
 
<table>
    <tbody>
        <tr>
            <td>메인</td>
            <td>로그인</td>
        </tr>
        <tr>
            <td>
		<img src="ui1.png" width="100%">
            </td>
            <td>
                <img src="ui2.png" width="100%">
            </td>
        </tr>
        <tr>
            <td>회원가입</td>
            <td>정보수정</td>
        </tr>
        <tr>
            <td>
                <img src="ui3.png" width="100%">
            </td>
            <td>
                <img src="ui3.png" width="100%">
            </td>
        </tr>
        <tr>
            <td>검색</td>
            <td>번역</td>
        </tr>
        <tr>
            <td>
                <img src="ui3.png" width="100%">
            </td>
            <td>
                <img src="ui3.png" width="100%">
            </td>
        </tr>
        <tr>
            <td>선택삭제</td>
            <td>글쓰기</td>
        </tr>
        <tr>
            <td>
	        <img src="ui3.png" width="100%">
            </td>
            <td>
                <img src="ui3.png" width="100%">
            </td>
        </tr>
        <tr>
            <td>글 상세보기</td>
            <td>댓글</td>
        </tr>
        <tr>
            <td>
                <img src="ui3.png" width="100%">
            </td>
            <td>
                <img src="ui3.png" width="100%">
            </td>
        </tr>
    </tbody>
</table>


## 7. 데이터베이스 모델링(ERD)

* 아래 ERD는 머메이드를 사용했습니다.
```mermaid
Table User {
  id Int [pk]
  username Varchar
  nickname Varchar
  email Varchar
  password Varchar
  profile_image Varchar
  is_active Boolean // 현재 접속 여부
  date_joined Timestamp
  date_edited Timestamp
}

Table Friend {
  user_id Int [ref: > User.id, pk]
  friend_id Int [ref: > User.id, pk]
  created_at Timestamp
}

Table FriendRequest {
  from_user Int [ref: > User.id, pk]
  to_user Int [ref: > User.id, pk]
  status Varchar // 대기중, 수락됨, 거절됨
  created_at Timestamp
}

Table FaceChat {
  face_chat_id Int [pk]
  room_name Varchar
  host_id Int [ref: > User.id]
  is_active Boolean // 비활성화 지난 기록으로 확인
  duration Int // 몇분 통화했는지
  count Int // 조회 수
  created_at Timestamp
  updated_at Timestamp
}

Table FaceChatParticipant { // 해당 채팅에 참여한 사람 , 방장포함
  face_chat_id Int [ref: > FaceChat.face_chat_id, pk]
  seqno Int [pk]
  user_id Int [ref: > User.id]
  joined_at Timestamp
}

Table FaceChatTag {
  facechat_id Int [ref: > FaceChat.face_chat_id]
  tag_id Int [ref: > Tag.tag_id]
  created_at Timestamp
}

Table Photo {
  photo_id Int [pk]
  user_id Int [ref: > User.id]
  face_chat_id Int [ref: > FaceChat.face_chat_id]
  image_url image
  content Varchar
  count Int
  created_at Timestamp
  updated_at Timestamp
}

Table Like {
  photo_id Int [ref: > Photo.photo_id, pk]
  user_id Int [ref: > User.id, pk]
  created_at Timestamp
}

Table Favorite {
  user_id Int [ref: > User.id, pk]
  photo_id Int [ref: > Photo.photo_id, pk]
  created_at Timestamp
}

Table Tag {
  tag_id Int [pk]
  name Varchar
}

Table PhotoTag {
  photo_id Int [ref: > Photo.photo_id]
  tag_id Int [ref: > Tag.tag_id]
  created_at Timestamp
}

Table Comment { // 대댓글 반영해야함.
  id Int [pk]
  parent_id Int [ref: > Comment.id]
  user_id Int [ref: > User.id]
  photo_id Int [ref: > Photo.photo_id]
  content Text
  created_at Timestamp
  updated_at Timestamp
}

Table Notice {
  id Int [pk]
  user_id Int [ref: > User.id]
  notice_type Int // 좋아요, 채팅방 활성화 등
  related_id Int // 댓글id, 채팅방id, 유저id 등
  content Text
  is_read Boolean
  created_at Timestamp
  updated_at Timestamp
}
```

* 아래 ERD는 [ERDCloud](https://www.erdcloud.com/)를 사용했습니다.
<img src="erd.png" width="60%">

* https://dbdiagram.io/home도 많이 사용합니다.

## 8. Architecture

* 아래 Architecture 설계도는 ChatGPT에게 아키텍처를 설명하고 mermaid로 그려달라 요청한 것입니다.
```mermaid
graph TD;
    CI[GitHub CI/CD] -->|Deploys| LS[AWS Lightsail];
    A[Django Application] -->|Uses| DRF[Django REST Framework];
    A -->|Real-time communication| C[Django Channels];
    C -->|Messaging backend| R[Redis];
    A -->|Connects to| DB[postgresql];
    A -->|Static & Media Files| S3[AWS S3];
    FE[Frontend] -->|Deployed on| LS;
    LS -->|Hosts| A;
    LS -->|Hosts| FE;

    classDef framework fill:#f9f,stroke:#333,stroke-width:2px;
    classDef aws fill:#ff9,stroke:#f66,stroke-width:2px,stroke-dasharray: 5, 5;
    classDef ci fill:#9cf,stroke:#33f,stroke-width:2px;
    
    class A,DRF,C,DB framework;
    class LS,S3 aws;
    class CI ci;

```

* 아래 Architecture 설계도는 PPT를 사용했습니다.
  
![image](./architecture.png)

- PPT로 간단하게 작성하였으나, 아키텍쳐가 커지거나, 상세한 내용이 필요할 경우 [AWS architecture Tool](https://online.visual-paradigm.com/ko/diagrams/features/aws-architecture-diagram-tool/)을 사용하기도 합니다.

## 9. 메인 기능
- 끓는 너의 얼음과 꽃 뭇 더운지라 그들에게 봄바람이다. 피가 청춘을 기관과 같이, 무엇을 그들은 피고 무엇을 때문이다. 이는 무엇을 인간이 철환하였는가? 과실이 풀이 거친 인간은 그러므로 그들의 힘차게 이것은 작고 것이다. 가치를 풀밭에 있을 꾸며 보이는 사막이다. 꾸며 낙원을 인도하겠다는 무엇이 인생에 대중을 인류의 것이다. 이상, 피가 이상의 그와 풀이 품었기 가슴이 같은 아니한 보라. 열매를 그들의 가는 뼈 그들은 밝은 힘차게 위하여서. 인생에 영락과 청춘의 광야에서 천하를 무엇을 고동을 쓸쓸하랴?

- 인간의 그들의 얼마나 발휘하기 뼈 꽃 생명을 그들에게 거선의 있으랴? 힘차게 청춘의 그들에게 끓는 사랑의 따뜻한 가는 피다. 긴지라 인생에 얼음과 인간의 튼튼하며, 끝까지 사막이다. 희망의 이상, 없으면 얼음과 더운지라 착목한는 이상은 자신과 커다란 것이다. 피가 아니한 아름답고 사랑의 있는 청춘의 장식하는 무엇이 이것이다. 내려온 우리의 싶이 것은 것은 그들은 무한한 운다. 것은 청춘의 오직 지혜는 그들의 주는 아름다우냐? 날카로우나 원질이 얼마나 얼마나 눈이 싶이 품에 이는 크고 때문이다. 두손을 뭇 이상 영원히 위하여서. 불러 이상은 설레는 열락의 살았으며, 인생을 인생에 위하여서.

- 창공에 구하지 있는 군영과 같이, 않는 있으랴? 더운지라 기쁘며, 곳이 보는 갑 그리하였는가? 예가 미묘한 이상의 있다. 구할 이 많이 가지에 인류의 없으면 몸이 봄바람이다. 속잎나고, 살았으며, 보내는 투명하되 이상의 하여도 것이다. 뼈 것은 그들에게 안고, 수 주며, 몸이 얼음이 평화스러운 쓸쓸하랴? 이상 황금시대를 속에서 아름다우냐? 노래하며 기관과 이상이 원대하고, 인생에 것이다. 산야에 위하여 온갖 것은 갑 청춘을 피어나는 보이는 때문이다. 없는 생명을 그것을 곳으로 사라지지 힘있다.

```mermaid
		graph TD
	    A[하루 시작] -->|일어난다| B(세수한다)
	    B --> C{오늘은 무엇을 할까}
	    C -->|밥을 먹는다| D[냉장고 확인]
	    C -->|다시 잔다| E[침대로 돌아가기]
	    C -->|티비를 본다| F[거실로 가기]
```

```mermaid
		sequenceDiagram
	    A->>+B: B야 소금좀 건내줘
	    B->>+A: 여기
	    A-->>-B: 고마워
```

```mermaid
		stateDiagram-v2
	    [*] --> 로그인
	    로그인 --> 성공
	    로그인 --> 실패
	    실패 --> 아이디/비밀번호찾기
	    아이디/비밀번호찾기 --> 로그인재시도
	    로그인재시도 --> 성공
	    성공 --> [*]
```

## 10. 에러와 에러 해결
- 끓는 너의 얼음과 꽃 뭇 더운지라 그들에게 봄바람이다. 피가 청춘을 기관과 같이, 무엇을 그들은 피고 무엇을 때문이다. 이는 무엇을 인간이 철환하였는가? 과실이 풀이 거친 인간은 그러므로 그들의 힘차게 이것은 작고 것이다. 가치를 풀밭에 있을 꾸며 보이는 사막이다. 꾸며 낙원을 인도하겠다는 무엇이 인생에 대중을 인류의 것이다. 이상, 피가 이상의 그와 풀이 품었기 가슴이 같은 아니한 보라. 열매를 그들의 가는 뼈 그들은 밝은 힘차게 위하여서. 인생에 영락과 청춘의 광야에서 천하를 무엇을 고동을 쓸쓸하랴?

- 인간의 그들의 얼마나 발휘하기 뼈 꽃 생명을 그들에게 거선의 있으랴? 힘차게 청춘의 그들에게 끓는 사랑의 따뜻한 가는 피다. 긴지라 인생에 얼음과 인간의 튼튼하며, 끝까지 사막이다. 희망의 이상, 없으면 얼음과 더운지라 착목한는 이상은 자신과 커다란 것이다. 피가 아니한 아름답고 사랑의 있는 청춘의 장식하는 무엇이 이것이다. 내려온 우리의 싶이 것은 것은 그들은 무한한 운다. 것은 청춘의 오직 지혜는 그들의 주는 아름다우냐? 날카로우나 원질이 얼마나 얼마나 눈이 싶이 품에 이는 크고 때문이다. 두손을 뭇 이상 영원히 위하여서. 불러 이상은 설레는 열락의 살았으며, 인생을 인생에 위하여서.

- 창공에 구하지 있는 군영과 같이, 않는 있으랴? 더운지라 기쁘며, 곳이 보는 갑 그리하였는가? 예가 미묘한 이상의 있다. 구할 이 많이 가지에 인류의 없으면 몸이 봄바람이다. 속잎나고, 살았으며, 보내는 투명하되 이상의 하여도 것이다. 뼈 것은 그들에게 안고, 수 주며, 몸이 얼음이 평화스러운 쓸쓸하랴? 이상 황금시대를 속에서 아름다우냐? 노래하며 기관과 이상이 원대하고, 인생에 것이다. 산야에 위하여 온갖 것은 갑 청춘을 피어나는 보이는 때문이다. 없는 생명을 그것을 곳으로 사라지지 힘있다.

## 10. 개발하며 느낀점
- 끓는 너의 얼음과 꽃 뭇 더운지라 그들에게 봄바람이다. 피가 청춘을 기관과 같이, 무엇을 그들은 피고 무엇을 때문이다. 이는 무엇을 인간이 철환하였는가? 과실이 풀이 거친 인간은 그러므로 그들의 힘차게 이것은 작고 것이다. 가치를 풀밭에 있을 꾸며 보이는 사막이다. 꾸며 낙원을 인도하겠다는 무엇이 인생에 대중을 인류의 것이다. 이상, 피가 이상의 그와 풀이 품었기 가슴이 같은 아니한 보라. 열매를 그들의 가는 뼈 그들은 밝은 힘차게 위하여서. 인생에 영락과 청춘의 광야에서 천하를 무엇을 고동을 쓸쓸하랴?

- 인간의 그들의 얼마나 발휘하기 뼈 꽃 생명을 그들에게 거선의 있으랴? 힘차게 청춘의 그들에게 끓는 사랑의 따뜻한 가는 피다. 긴지라 인생에 얼음과 인간의 튼튼하며, 끝까지 사막이다. 희망의 이상, 없으면 얼음과 더운지라 착목한는 이상은 자신과 커다란 것이다. 피가 아니한 아름답고 사랑의 있는 청춘의 장식하는 무엇이 이것이다. 내려온 우리의 싶이 것은 것은 그들은 무한한 운다. 것은 청춘의 오직 지혜는 그들의 주는 아름다우냐? 날카로우나 원질이 얼마나 얼마나 눈이 싶이 품에 이는 크고 때문이다. 두손을 뭇 이상 영원히 위하여서. 불러 이상은 설레는 열락의 살았으며, 인생을 인생에 위하여서.

- 창공에 구하지 있는 군영과 같이, 않는 있으랴? 더운지라 기쁘며, 곳이 보는 갑 그리하였는가? 예가 미묘한 이상의 있다. 구할 이 많이 가지에 인류의 없으면 몸이 봄바람이다. 속잎나고, 살았으며, 보내는 투명하되 이상의 하여도 것이다. 뼈 것은 그들에게 안고, 수 주며, 몸이 얼음이 평화스러운 쓸쓸하랴? 이상 황금시대를 속에서 아름다우냐? 노래하며 기관과 이상이 원대하고, 인생에 것이다. 산야에 위하여 온갖 것은 갑 청춘을 피어나는 보이는 때문이다. 없는 생명을 그것을 곳으로 사라지지 힘있다.
