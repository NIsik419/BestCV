# BestCV


##  기능 설명
이 프로그램은 OpenCV를 사용하여 **실시간 RTSP 스트리밍**을 표시하고 **녹화**할 수 있습니다.  
추가적으로 **밝기/대비 조절** 및 **화면 반전** 기능이 포함되어 있습니다.

### 📌 주요 기능
1. **RTSP 및 로컬 웹캠 지원**  
   - RTSP 주소를 입력하면 IP 카메라 스트리밍  
   - `0` 입력 시 로컬 웹캠 사용  

2. **자동 재연결 기능**  
   - RTSP 연결이 끊어지면 5초 후 자동으로 다시 연결  

3. **녹화 기능**  
   - `Space 키`를 누르면 **녹화 시작 / 중지**  
   - `output.avi` 파일로 저장  

4. **밝기 및 대비 조절 기능**  
   - `Brightness` 및 `Contrast` 슬라이더를 조절 가능  
   - OpenCV `convertScaleAbs()` 적용  

5. **화면 반전 (Flip) 기능**  
   - `'f'` 키를 누르면 **좌우 → 상하 → 상하좌우** 순환 변경  

## 🎮 조작법
| 키 입력 | 동작 |
|---------|---------------------------|
| `Space` | 녹화 시작 / 중지 |
| `'f'` | 화면 반전 모드 변경 (좌우/상하/상하좌우) |
| `ESC` | 프로그램 종료 |

## 결과물

[녹화된 영상 보기](https://github.com/NIsik419/BestCV/blob/main/output.avi)

![녹화 중](https://github.com/NIsik419/BestCV/blob/main/%ED%99%94%EB%A9%B4%20%EC%BA%A1%EC%B2%98%202025-03-18%20213836.png)



## 📂 실행 방법
1. **Python 및 OpenCV 설치**
   ```sh
   pip install opencv-python

