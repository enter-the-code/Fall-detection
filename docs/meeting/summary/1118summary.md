# 11/18 회의
11/18(월) 오후 6시 비대면 회의 - zoom 통해 진행

## Front
* height 사용한 모델 조정

## Ai
* 모델 학습은 한명에 대해서만 학습
* 장면에 여러 사람을 clustering : dbscan 사용
    * data frame 구분이 가능
    * cluster에 대한 레이블 부여 확인
* 학습방법
    * frame이 불연속적인 한계
    * 한 프레임의 point 수가 제각각
    * 즉, input layer 구성의 어려움
    * 프레임 사이의 값 변화를 사용하는 방법 검토중
* 가변적인 point input에 대한 처리
    * 추가 논의 필요

### TODO
* 시계열 길이 결정
* 길이에 맞게 데이터 생성 및 라벨링
* pycaret, gru 모델 사용하여 성능 비교
* 시각화 자료 만들기
* 모델의 visualizer에 적용방법
* 발표 준비

### Ai와 Visualizer 연결
* 전처리 포함한 모델을 python code로 첨부
* fall_detection.py의 step 메서드의 input을 outputDict 그대로 사용하게 변경
* 시계열 데이터 처리를 위한 변환이 필요

## DataCommunicate
* 개발한 코드 pyinstaller로 빌드 후 깃허브에 배포

### 데이터 전처리를 Converter에서 수행가능한가?
* 통신 오류에 대한 예외처리 문제로 불가능
    * threading 방식 변경 필요하여 전체 코드 고쳐야 하기에 시간적으로 불가능