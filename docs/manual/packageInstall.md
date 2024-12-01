# Package Installation
## Visualizer
Visualizer 구동을 위해서는 아래와 같은 패키지 설치가 필요하다
### Pyside2
Pyside2(Qt5 기반)는 python 3.5 ~ 3.10에서 구동된다\
아래는 Conda 환경에서 Pyside2를 설치하는 명령어입니다
```cmd
conda create -n env_name python=3.x
conda activate env_name
conda install -c conda-forge pyside2
```
pip로 설치 시
```cmd
pip install Pyside2
```
로 설치 가능하다

### 이외
```cmd
pip install pyqtgraph pyserial numpy tensorflow pyopengl json-fix
conda install scikit-learn pandas
```