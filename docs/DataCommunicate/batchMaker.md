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
| connectStatus | connectBtn |

* connectStatus value
    * CONNECT_Y_MSG
    * CONNECT_N_MSG
* connectBtn value
    * CONNECT_BTN_MSG
    * CONNECT_BTN_RESET_MSG

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