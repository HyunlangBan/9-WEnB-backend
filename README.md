# introduction

*  세계 최대의 숙박 공유 서비스이며 2초당 한 건 씩 예약이 이뤄지고 있는 Airbnb의 웹사이트 클론 프로젝트 
* 개발기간 : 2020.07.06 ~ 2020.07.17(약 2주)
* 개발인원 : 6명
   - Front-end: 정수빈, 이한별, 김정현
   - Back-end: 권오성, 반현랑, 이민서
* [Front-end Github](https://github.com/wecode-bootcamp-korea/9-WEnB-frontend)
* [Back-end Github](https://github.com/wecode-bootcamp-korea/9-WEnB-backend)

# Demo
[![](https://images.velog.io/images/langssi/post/57edc6fb-0533-406b-ad5b-a53a50673560/image.png)](https://www.youtube.com/watch?v=28Q003gHF4Q)

# Model

![](https://images.velog.io/images/langssi/post/b0f377ec-6c16-44e0-91c8-49c75fb1a666/image.png)

# Technologies

* Python
* Django
* Beautifulsoup, Selenium
* Bcrypt
* JWT
* Unittest
* MySQL
* CORS headers
* Git, Github
* AWS EC2, RDS
* Docker

# Features

* user
   - 카카오 소셜 로그인
     - 카카오 API로 로그인 후 받아온 사용자 정보로 로그인/회원가입
     - 로그인시 JWT Access 토큰 발행
   - 로그인 데코레이터로 로그인 상태 확인
   - 위시리스트
   
* stay
   - 숙소 리스트 구현
   - 숙소 디테일 구현
   - 메인 페이지에서 검색시 키워드에 따른 숙소 필터링 구현
   - 숙소 리스트 페이지에서 숙소 타입에 따른 필터링 구현
   
* reservation
   - 숙소 예약 기능 구현
   - 예정된 예약, 이전 예약 분류기능
