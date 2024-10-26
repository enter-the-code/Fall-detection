# BatchMaker
코드 구조 참고용

# class Window()
ui 정의
## Connection
| | |
| --- | --- |
| Demo | demoList |
| CLI COM | cli_num_line |
| Data COM | data_num_line |
| CONNECT_N/Y_MSG | connectBtn |

### Signal
* demoList -> demoChanged
* connectBtn -> startConnect

## Config
| | |
| --- | --- |
| filenameCfg | selectCfgBtn |
| sendCfgBtn | |

### Signal
* selectCfgBtn -> selectCfg(filenameCfg)
* sendCfgBtn -> StartSensor

# class Core()
내부 기능 정의
* ini 파일로 기존값 저장
* 파일 선택, 파싱