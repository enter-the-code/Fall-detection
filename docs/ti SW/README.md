# TI 제공 각종 SW
센서만 사용하는 방법으로 진행 시(UART serial)
* Radar Tool Box
* UniFlash

EVM 보드로 진행 시(UDP datagram)
* mmWave Studio
* MATLAB
* Lattice Diamond Programmer (optional)

필요하며, 공통적으로 [드라이버](#drivers) 설치 필요

## [Radar Tool Box](https://dev.ti.com/tirex/explore/node?node=A__AEIJm0rwIeU.2P1OBWwlaA__radar_toolbox__1AslXXD__LATEST)
위 링크 들어간 후, 왼쪽 붉은색으로 표시된 Radar Tool Box에 커서 갖다대고 : 눌러서 Download 가능\
다양한 Demo와 그와 관련된 Flash Binary , cfg 파일, Visualizer 및 소스코드 제공

## [UniFlash](./UniFlash.md)
Firmware 업로드 기능 제공

## mmWave Studio
Raw Data를 EVM 보드 통해 UDP 패킷으로 직접 받아 처리하기 위해 필요

## CCS Studio
C/C++ 기반 펌웨어 개발 기능 제공\
최신 Theia 버전 사용할 것

## [3D People Track](https://dev.ti.com/tirex/content/radar_toolbox_2_20_00_05/source/ti/examples/People_Tracking/3D_People_Tracking/docs/3d_people_tracking_user_guide.html)
해당 프로젝트의 Flash 기반으로 작업 예정\
작업 이전에 [Out-of-Box Demo](https://dev.ti.com/tirex/explore/content/radar_toolbox_2_20_00_05/source/ti/examples/Out_Of_Box_Demo/docs/Out_Of_Box_Demo_User_Guide.html) 시도 권장

## [mmWave Visualizer](./mmWave%20Visualizer.md)
많은 ti demo 프로젝트에서 사용하는 visualizer\
PyQt2 기반, 소스코드 제공됨

## Drivers
* CP210x Universal Windows Driver
* FTDI CDM Driver