import cv2
import time

RTSP_URL = input("📡 RTSP 주소를 입력하세요 (웹캠 사용 시 0 입력): ")

if RTSP_URL.isdigit():
    RTSP_URL = int(RTSP_URL)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0
out = None
recording = False
flip_mode = 1

def adjust_brightness_contrast(img, brightness=0, contrast=0):
    beta = brightness - 50
    alpha = contrast / 50
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)

def connect_camera():
    cap = cv2.VideoCapture(RTSP_URL)
    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 60000)
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 60000)

    if cap.isOpened():
        print("✅ RTSP 스트림 연결 성공!")
    else:
        print("❌ RTSP 스트림 연결 실패! 5초 후 재시도...")

    return cap

# 🔹 OpenCV 창 생성 후 트랙바 추가
cv2.namedWindow("IP Camera Stream")

cv2.createTrackbar('Brightness', 'IP Camera Stream', 50, 100, lambda x: None)
cv2.createTrackbar('Contrast', 'IP Camera Stream', 50, 100, lambda x: None)

cap = connect_camera()

while True:
    if not cap.isOpened():
        print("🔄 RTSP 재연결 중...")
        time.sleep(5)
        cap = connect_camera()

    ret, frame = cap.read()
    if not ret:
        print("📢 프레임 수신 실패. 다시 시도 중...")
        cap.release()
        time.sleep(3)
        cap = connect_camera()
        continue

    brightness = cv2.getTrackbarPos('Brightness', 'IP Camera Stream')
    contrast = cv2.getTrackbarPos('Contrast', 'IP Camera Stream')
    frame = adjust_brightness_contrast(frame, brightness, contrast)

    frame = cv2.flip(frame, flip_mode)

    if recording:
        cv2.circle(frame, (50, 50), 10, (0, 0, 255), -1)
        out.write(frame)

    cv2.imshow("IP Camera Stream", frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:
        break
    elif key == 32:
        recording = not recording
        if recording:
            print("🔴 녹화 시작...")
            out = cv2.VideoWriter('output.avi', fourcc, fps, (frame.shape[1], frame.shape[0]))
        else:
            print("⏹ 녹화 중지")
            out.release()
            out = None
    elif key == ord('f'):
        flip_mode = (flip_mode + 1) % 3 - 1

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
