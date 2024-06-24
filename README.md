# DT팀의 SSD 프로젝트
- 프로젝트 기간 : 2024-06-18 ~ 2024-06-25
- 프로젝트 개요 : SSD 를 구현하고, SSD 를 테스트 할 수 있는 환경을 제공하고 추가적으로 Logger, Runner, Buffer 기능까지 개발한다.
- 프로젝트 목표 : SSD, Shell 기능 구현시 TDD 를 적용하여 점진적으로 빠르고 쉽게 구현하고, Code Coverage 80% 이상을 달성하고, 리팩토링을 통해 클린코드를 작성할 수 있도록 합니다.  팀 단위 프로젝트를 통한 <b>팀 협업, 커뮤니케이션 능력을 향상시키고, 최종적으로는 실무에서도 클린코드 전파교육을 통해 품질 높은 코드를 작성하는 문화가 정착될 수 있도록 하는 것이 목표입니다.</b> 💪💪💪


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
|문석기님|👑팀장👑<br><b>코드의 수호자</b> 이자 <b>스피드 스타터</b> 이며 <b>리더십의 판도라</b>.. 즉 <b>`코딩 고수`</b>|skm04614@gmail.com|
|김도경님|리뷰어 - 🧙‍♂️<b>품질의 수호자</b> <br>뛰어난 품질을 유지하도록 코드를 보호하는 수호자|dolgyuk@gmail.com|
|이상혁님|개발자 - 🎵<b>코드 마에스트로</b><br>뛰어난 지휘력으로 코드를 작성하고 관리하는 뛰어난 지도자|hyugi012@gmail.com|
|박진희님|테스터 - 🕵️‍♂️<b>버그 탐험가</b><br>발생 가능한 오류를 발견하는 탐험가|genie121110@gmail.com|
|이성화님|개발자 - 🥷<b>코딩 닌자</b><br>훌륭한 코딩 기술과 빠른 개발 속도를 자랑하는 팀의 닌자|sunghwaa.lee@gmail.com|
|김영민님|리뷰어 - 🦅<b>매의 눈</b><br>명세서를 샅샅히 뒤져 누락된 부분을 보완해주는 철저한 검토자|arcetral@gmail.com|

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

### 1. 가상 SSD 제작
가상 SSD는 소프트웨어 기반으로 SSD를 시뮬레이션하며, 실제 하드웨어를 대체할 수 있도록 설계되었습니다.

#### 기능:
- **기본 명령어**: Read와 Write 명령어를 지원합니다.
- **LBA 크기**: 각 논리 블록 주소(Logical Block Address, LBA)는 4 바이트입니다.
- **저장 용량**: 100개의 LBA를 지원하며, 총 400 바이트를 저장할 수 있습니다.

#### 명령어 예시:
- **Write 명령어**: `ssd W 3 0x1298CDEF` (값 `0x1298CDEF`를 LBA 3에 저장합니다)
- **Read 명령어**: `ssd R 2` (LBA 2에 저장된 값을 읽습니다)

#### 저장 방식:
- **Write 작업**: 데이터는 `nand.txt` 파일에 저장됩니다.
- **Read 작업**: 데이터는 `nand.txt` 파일에서 읽어오고, 결과는 `result.txt` 파일에 저장됩니다.

### 2. Test Shell 애플리케이션 개발
Test Shell 애플리케이션은 가상 SSD와 상호 작용할 수 있는 인터페이스를 제공하여 사용자로부터 명령어를 입력받고 결과를 출력합니다.

#### 사용 가능한 명령어:
- `write [LBA] [value]`: 특정 LBA에 값을 씁니다.
- `read [LBA]`: 특정 LBA에서 값을 읽습니다.
- `exit`: 쉘을 종료합니다.
- `help`: 각 명령어에 대한 도움말을 출력합니다.
- `fullwrite [value]`: 모든 LBA에 특정 값을 씁니다.
- `fullread`: 모든 LBA의 값을 읽어 화면에 출력합니다.

#### 사용 예시:
- **Write 명령어**: `write 3 0xAAAABBBB` (값 `0xAAAABBBB`를 LBA 3에 씁니다)
- **Read 명령어**: `read 3` (LBA 3에 저장된 값을 읽어 결과를 출력합니다)

### 3. Test Script 개발
Test Script는 가상 SSD의 기능을 자동으로 테스트하여 정상 작동 여부를 확인합니다.

#### 예시 Test Script:
1. **TestApp1**: 
   - `fullwrite`를 수행하여 모든 LBA에 특정 값을 씁니다.
   - `fullread`를 수행하여 모든 값이 올바르게 기록되었는지 확인합니다.

2. **TestApp2**:
   - LBA 0-5에 값을 여러 번 씁니다.
   - 동일한 LBA에 새로운 값을 덮어씁니다.
   - LBA 0-5의 값을 읽어 최종 값을 확인합니다.



## UML

## 사용방법

### 1. Python 환경 설정
```bash
$ $ pip install virtualenv
$ python -m virtualenv <venv dir>
$ source <venv dir>/bin/activate
$ pip install -r requirements.txt 
```

### 2. 터미널에서 실행
```bash
$ python -m custom_shell.cshell
```

### 3. Test 시나리오 실행
```python
====================================================================
# 도움말
>> help
write [lba] [val]         -   writes a val on lba (ex. write 10 0x1234ABCD)
read [lba]                -   reads the val written on lba (ex. read 10)
exit                      -   exits program
help                      -   prints manual to stdout
fullwrite [val]           -   writes val to all lbas ranging from 0 to 99
fullread                  -   reads all vals written on each lba ranging from 0 to 99 and prints to stdout
erase [lba] [size]        -   wipes ssd 'size' amount of lbas starting from lba
erase_range [slba] [elba] -   wipes ssd lba in range [slba, elba)
list_tc                   -   lists all testable scenarios (tcs)
run [tc #1] [tc #2] ...   -   runs test scenarios if such scenario is defined in the testing_suite
====================================================================
# Test 시나리오 리스트 조회
>> list_tc
tc_app_1
tc_app_2
tc_fail
tc_fullread_10_times_compare
tc_single_random_lba_val_write_compare
tc_write_10_times_and_compare
====================================================================
# Test 수행
>> run tc_app_1 tc_fail tc_write_10_times_and_compare
* tc_app_1 ------------------------------------------ Run...Pass
* tc_fail ------------------------------------------- Run...FAIL!
* tc_write_10_times_and_compare --------------------- Run...Pass
====================================================================
```


