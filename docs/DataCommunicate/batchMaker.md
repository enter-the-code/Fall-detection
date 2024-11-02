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

### macro const
* connectStatus value
    * CONNECT_Y_MSG
    * CONNECT_N_MSG
    * CONNECT_NA_MSG
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

### macro const
* sendCfgBtn value
    * SEND_CFG_BTN_START_MSG
    * SEND_CFG_BTN_RUN_MSG
    * SEND_CFG_BTN_RST_MSG

### Signal
* selectCfgBtn -> selectCfg(filenameCfg)
* sendCfgBtn -> StartSensor

# class Core()
내부 기능 정의
* ini 파일로 기존값 저장
* 파일 선택, 파싱

# tlv_defines.py
## 3D People Tracking
### TLV Header type
* 1020 : point cloud
* 1010 : target object list
* 1011 : target index
* 1012 : target height
* 1021 : presence indication - unused TLV