# HW Insight
```
IWR6843ISK : 60-64GHz(4GHz bandwidth) mmWave Rader transceiver & antennas on PCB (temp range : -20~60 celcious)
-----------------------------------------------------
configure |  | ADC(Analog to Digital Converter) data
-----------------------------------------------------
DCA1000EVM(Evaluation Model) : stream ADC data over Ethernet
```
1. Raw mode : streams captured LVDS data
2. Data separated mode : FPGA 레벨에서 datatype에 따른 header 구분하도록 직접 세팅(port 구분하여 UDP 전송)

## Data Communication
* IWR6843ISK : UART Serial communication
* DCA1000EVM : captures raw ADC, high speed debug, post process
* MMWAVEICBOOST : x



# IWR6843ISK

## 60 Pin
60pin HD connector enables interfacing of LVDS(Low Voltage Differential Signaling) signals to the DCA1000EVM for data capturing\
Block diagram에 따르면 LVDS전용 하나, JTAG/SPI/LVDS/GPIO 범용 하나씩 60pin 존재
(범용이 3.3V 전압을 EVM 통해 공급)\
> 보드 가장 끝부분에 위치한 60pin이 direct DCA1000EVM interface

## Mode & Muxing Scheme
1. Modular Mode
single USB로 연결(UART + power supply - CP2015 USB to UART emulator)\
정상 연결 시 장치 관리자에 2개의 virtual COM port 표시됨

### S1 switch Settings
* Flashing mode\
on/off/on/on/off/-
* Functional mode\
off/off/on/on/off/-

2. DCA1000EVM Mode 
(direct connection without cable between boards)\
power supplied from 60pin\
연결 시 mmWave Sensor guid 44p 참조\
off/on/on/off/off/-

# Led list
mmWave Sensor guid 35p 참조\
(Power / USB enumeration / Reset / 5V indicator / GPIO2)\
Mux Pin 밑의 LED가 USB enumeration LED



# DCA1000EVM Board

# Prerequisites
* Host : static IP 192.168.33.30 / Win 10 / mmWave Studio required
* DCA1000EVM(default val) : System IP 192.168.33.30 / FPGA IP 192.168.33.180 / MAC 12:34:56:78:90:12


## DCA1000EVM interface
* SPI - SPI flash
* GPIOs - Led & Switches
* FTDI(+JTAG) - Micro USB
* SDIO - Micro SD
* Ethernet - RJ-45
* Ethernet 근처 USB(J1, RADAR_FTDI) : Raw mode / 반대편(J4, FPGA_JTAG)은 FPGA 처리 후 JTAG 통해 전달 : Data mode

## Switches
* FPGA config : 혼자 떨어진 거
* User mode selection : small one
* Config : big one

### configuration - DCA1000EVM user guid 13p 참조
* LVDS stream 1 / 16 playback
* capture saved on SD 2 / 15 streamed over network
* 4-lane(1243) 3 / 14 2-lane(AR1642)
* Raw mode 4 / 13 Data mode
* EEPROM config 6 / 11 FPGA config

## UDP data format(Byte unit size)

### Command Format from configuation port(usually FPGA)
* command request\
Header(2) / Cmd(2) / Data size(2) / Data(0-504) / Footer(2)
* command response\
Header(2) / Cmd(2) / Status(2) / Footer(2)

Data는 TLV(Tag/Length/Value) sequence로 예상됨

### Data Format from data port
* Raw mode\
Seq #(4) / Byte count(6) / Data(48-1462)
* Data separated mode\
Seq #(4) / Byte count(6) / identifier(8) / length field(8) / Data(48-1446)

파일로 저장될 때는 2번째 필드로 Data length filed(4) 추가되어 저장된다


## FPGA programming
* Lattice Diamond Programmer standalone tool
* FPGA JTAG USB port(J4) 통해 연결
* onboard SPI Flash에 FPGA image 기록

## MISC
SD 카드는 playback 기록용



# People Track (UART without EVM)
## Tracking Algorithm (Spherical to Cartesian)
* input
range(R), azimuth(pi), elevation(theta), Doppler, SNR
* tracks objects in cartesian space(output)
* EKF(Extended Kalman Filter) process



# mmWaveStudio(DCA1000EVM)
communicate device over SPI(Serial Peripheral Interface)
* Board control
* Config TI rader device(Radar API cmd)
* Raw ADC data capture
* Post processing of ADC data & visualization(Matlab : exact version of "32bit Matlab Runtime Engine 8.5.1" required)
