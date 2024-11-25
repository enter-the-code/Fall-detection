# 11/25 회의
11/25(월) 오후 6시 비대면 회의 - zoom 통해 진행

## AI
* https://colab.research.google.com/drive/1IFHuTxp7eSWACrXd4VDpAYe-9F3kJTuj?usp=sharing
### 1인 처리 모델
* 레이블은 원-핫 인코딩
* 시퀸스 처리는 5개 sequence, stride는 2
* 기존 GRU 모델 사용시 76% 정확도
* pycaret 라이브러리 사용해서 다양한 모델 비교하는 것 시도
    * extra tree classifier 에서 90% 정확도
        * F1 : 0.90
        * Recall : 0.90
        * Precision : 0.91
* feature수 5x5를 flatten하여 처리 : pycaret 처리 위함
    * 5명에 대해 각 5개
### Clustering
* 여러 인원 처리 -> 군집화 및 추적 필요
* Doppler나 SNR값은 현재 제외하고 테스트한 상태
    * 평균값 취해서 사용하는 방법 검토중
* DBSCAN으로 클러스터링 수행
* 클러스터링 모델 완성하면 1인처리 모델과 결합하여 완성

## UI
* 기존 선 상태 구현
    * 누운 상태, 앉은 상태 추가 구현
    * 적용 및 테스트 필요
* AI에서 상태 전달 가능한지 확인 -> 가능

## 종합
* AI 모델 결합하여 완성하면, UI파트에 임베딩하여 완성
* Input은 Data Communication에서, Output은 UI 팀에서 처리

# 멘토님 언급
* 모델 변경 긍정적
* 시각화까지 모델까지의 결합 확인이 필요
* 다음주 대면 미팅때 프로그램 연결 확인

## 차기 일정
* 12/2(월) 대면회의 진행
* 회의실 예약 필요