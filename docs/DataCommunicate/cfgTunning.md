# CFG Tunning
## 공통사항
* %로 시작하는 항목은 주석
```
sensorStop
flushCfg

[Sensor Front-end param]
[Detection layer param]
[Board related param]
[Tracking layer param]

sensorStart
```
* 위 형식 유지, 중간에 설정값 전송
* wall mount와 ceil mount 모두 cfg 편집에 따라 사용 가능
* 세부 사항은 3D_people_tracking_detection_layer_tuning_guide.pdf 등을 참조
## [Online Quick Setting](https://dev.ti.com/gallery/view/mmwave/mmWaveSensingEstimator/ver/2.4.0/)

## Static values in 3D People Tracking Demo
```
dfeDataOutputMode 1
channelCfg 15 7 0
adcCfg 2 1
adcbufCfg -1 0 1 1 1
lowPower 0 0
```

## Sensor Front-End Parameters
* Wall Mount의 경우 3DWM 값을 사용을 추천한다
### profileCfg
```
profileCfg 0 60.75 30.00 25.00 59.10 657930 0 54.71 1 96 2950.00 2 1 36 
```

### Frame Configuration
* 각 TX 안테나의 TDM-MIMO와 BPM-MIMO 스키마 지정
* 3D People Tracking Demo의 경우 2개의 BPM 지원하기에 세번째 안테나는 TDM 모드로 진행한다
    * BPM 사용 시, 두 개의 안테나가 같은 방위각(azimuth axis) 가져야 한다

#### TDM 사용하는 경우
```
chirpCfg 0 0 0 0 0 0 0 1
chirpCfg 1 1 0 0 0 0 0 2
chirpCfg 2 2 0 0 0 0 0 4
frameCfg 0 2 96 0 55.00 1 0
```
#### BPM(TX0, TX1) + TDM(TX2) 사용 시
```
chirpCfg 0 0 0 0 0 0 0 5
chirpCfg 1 1 0 0 0 0 0 2
chirpCfg 2 2 0 0 0 0 0 5
frameCfg 0 2 96 0 55.00 1 0
```
* 밑의 bpmCfg 설정 필수


## Detection Layer Parameters
* Wall Mount의 경우 3DWM 값을 사용을 추천한다

### dynamicRangeAngleCfg
```
dynamicRangeAngleCfg -1 0.75 0.0010 1 0
```

### dynamicRACfarCfg
* CFAR 알고리즘 적용방식에 따라 값 변화
```
dynamicRACfarCfg -1 4 4 2 2 8 12 4 8 5.00 8.00 0.40 1 3
```

### dynamic2DAngleCfg
* 2번째 값 최소값 1.0
    * fovCfg 값 따라 값 변경
```
dynamic2DAngleCfg -1 1.5 0.0300 1 0 1 0.30 0.85 8.00
```

### staticRangeAngleCfg
* Bartlett Beamforming 알고리즘을 통한 range-angle heatmap 예상 알고리즘 사용 여부 및 설정
* 2번째 값이 0이면 disabled : 알고리즘 미수행으로 인한 리소스 사용 감소
```
staticRangeAngleCfg -1 0 8 2
```

### staticRACfarCfg
* static 환경에서의 CFAR 알고리즘 관련 설정
```
staticRACfarCfg -1 6 2 2 2 8 8 6 4 8.00 15.00 0.30 0 0
```

### fineMotionCfg
* static people의 fine motion(standing, sitting still, sleeping ...)을 추적
    * 3D People Tracking에 필수적인 사항은 아님
* 2번째 값 0 일시 비활성화
* 10으로 설정된 frame에 대해서 알고리즘 수행
* 마지막값은 Doppler threshold
```
fineMotionCfg -1 1 1.0 10 2
```

### bpmCfg
* 이전 chirpCfg에서 BPM 사용시 설정해야 함
* SNR을 3dB 개선하며 demo의 성능도 개선된다
```
bpmCfg -1 1 0 2
```

## Board Related Parameters
* IWR6843ISK 기준
```
antGeometry0 0 -1 -2 -3 -2 -3 -4 -5 -4 -5 -6 -7
antGeometry1 -1 -1 -1 -1 0 0 0 0 -1 -1 -1 -1
antPhaseRot 1 1 1 1 1 1 1 1 1 1 1 1
compRangeBiasAndRxChanPhase 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0 1 0
fovCfg -1 70.0 20.0
```

## Detection Layer Parameters
* 사용 환경에 맞는 설정이 필요
