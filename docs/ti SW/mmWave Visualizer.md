# mmWave Visualizer
[User Guid](https://dev.ti.com/tirex/explore/content/radar_toolbox_2_20_00_05/tools/visualizers/Applications_Visualizer/docs/mmWave_Applications_Visualizer_User_Guide.html)

## How to use
1. Industrial Visualizer 실행\
 <toolbox_install_dir>\tools\visualizers\Applications_Visualizer\Industrial_Visualizer

2. 센서의 물리 리셋 버튼 1회 누르기

3. COM 포트 지정 후 Connect
* CLI COM : Enhanced Port
* DATA COM : Standard Port

4. Select Configuration에서 .cfg 파일 선택\
<RADAR_TOOLBOX_INSTALL_DIR>\src\ti\examples\<ExampleName>\chirp_configs

5. Start and Send Configuration

6. Plot Controls 및 3D Plot / Range Plot 전환 기능 제공

7. 실행 데이터는 ./binData 에 저장, Playback 기능 제공

## Source 구성
#### gui_main.py
starts the application.
#### gui_core.py
handles the GUI and backend processing for the GUI
#### gui_parser.py
defines an object used for parsing the UART stream. If you want to parse the UART data, you can use this file to do so.
#### gui_threads.py
defines the different threads that are run by the demo. These threads handle updating the plot and calling the UART parser.
#### graph_utilities.py
contains functions used to draw objects.
gui_common.py aggregates several variables and configurables which are used across several files.
#### parseFrame.py
responsible for parsing the frame format of incoming data.
#### parseTLVs.py
responsible for parsing all TLV’s which are defined in the demos.
#### tlv_defines.py
defines tlv’s used in the examples.
#### demo_defines.py
defines which examples work with which devices.
#### Demo_Classes/
directory that contains example-specific source files.
#### Common_Tabs/
directory that contains common plotting tabs like 1D or 3D plots.

