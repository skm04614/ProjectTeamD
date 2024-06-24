# DT팀의 SSD 프로젝트
- 프로젝트 기간 : 2024-06-18 ~ 2024-06-25
- 프로젝트 개요 : SSD 를 구현하고, SSD 를 테스트 할 수 있는 환경을 제공하고 추가적으로 Logger, Runner, Buffer 기능까지 개발한다.
- 프로젝트 목표 : SSD, Shell 기능 구현시 TDD 를 적용하여 점진적으로 빠르고 쉽게 구현하고, Code Coverage 80% 이상을 달성하고, 리팩토링을 통해 클린코드를 작성할 수 있도록 한다.  팀 단위 프로젝트를 통해 팀 협업, 커뮤니케이션 능력을 향상시키고 <b>최종적으로는 실무에서도 클린코드 전파교육을 통해 품질 높은 코드를 작성하는 문화가 정착될 수 있도록 하는 것이 목표이다.</b> 💪💪💪


## 목차
[팀 소개](#팀소개)

[주요 기능](#주요기능)

[UML](#UML)

[사용 방법](#사용방법)



## 팀소개
### DT(Dream Team) 이란?
실력이 뛰어난 멤버들로 구성되어 있는 팀

### 팀원 소개
역할 할당


|팀원|역할|mail|
|------|---|---|
|문석기님|⭐️팀장##|skm04614@gmail.com|
|김도경님|##|dolgyuk@gmail.com|
|이상혁님|##|hyugi012@gmail.com|
|박진희님|##|genie121110@gmail.com|
|이성화님|##|sunghwaa.lee@gmail.com|
|김영민님|##|arcetral@gmail.com|

### Groud Rule
1. 매일 인사하기
2. 퇴근 5시
3. 당일 올라온 PR은 4시반 이전에 마무리
4. PR 최소 리뷰어 수 = 2
5. PR에 변경 필요하다고 생각되면 requests change와 함께 comment 달기
6. 하나의 PR에는 하나의 commit 내용만 (SRP)
7. PR의 source branch는 개인 branch이니 PR comment로 인한 변경점을 하나의 commit으로 묶어서 제출하기 (force push & amend 하여)
8. 빌드 테스트하여 동작 확인하고 올리기
9. 커밋 태그 통일 (fix / feat / hotfix / 등)
   ```
   예) fix: Driver의 x 기능 수정
   예) feat: Driver의 y 기능 추가
   예) hotfix: Driver의 core module z에 심각한 결함이 있어 이를 수정함
   ```
10. 브랜치명은 dev/사용자명 (예: dev/heehoha)
11. 1시간 내 리뷰를 고려하여 200라인 이하의 짧은 코드로 커밋을 구성한다
12. 최대한 PR 올라온 순으로 처리하기
13. 개발자는 변경 코드의 커밋을 구성하여 리뷰어 선정 및 리뷰요청을 해야하며 리뷰어의 코드리뷰를 마친 코드만이 마스터 브랜치에 머지할 수 있다.


## 주요기능

## UML

## 사용방법

### 1. Python 환경 설정
```
$ $ pip install virtualenv
$ python -m virtualenv <venv dir>
$ source <venv dir>/bin/activate
$ pip install -r requirements.txt 
```

### 2. 터미널에서 실행
```
$ python -m custom_shell.cshell
```


