import cv2
import time

RTSP_URL = input("📡 RTSP 주소를 입력하세요 (웹캠 사용 시 0 입력): ")

if RTSP_URL.isdigit():
    RTSP_URL = int(RTSP_URL)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
fps = 20.0
out = None
recording = False
flip_mode = 1  # 기본값: 좌우 반전


def adjust_brightness_contrast(img, brightness=0, contrast=0):
    beta = brightness - 50
    alpha = contrast / 50
    return cv2.convertScaleAbs(img, alpha=alpha, beta=beta)


def connect_camera():
    cap = cv2.VideoCapture(RTSP_URL)  # 기본 OpenCV 사용

    cap.set(cv2.CAP_PROP_BUFFERSIZE, 3)
    cap.set(cv2.CAP_PROP_OPEN_TIMEOUT_MSEC, 60000)  # 60초 타임아웃
    cap.set(cv2.CAP_PROP_READ_TIMEOUT_MSEC, 60000)  # 프레임 읽기 타임아웃

    if cap.isOpened():
        print("✅ RTSP 스트림 연결 성공!")
    else:
        print("❌ RTSP 스트림 연결 실패! 5초 후 재시도...")

    return cap


cv2.namedWindow("IP Camera Stream")
cv2.createTrackbar('Brightness', 'IP Camera Stream', 50, 100, lambda x: None)
cv2.createTrackbar('Contrast', 'IP Camera Stream', 50, 100, lambda x: None)

cap = connect_camera()

while True:
    if not cap.isOpened():
        print("RTSP 재연결 중...")
        time.sleep(5)
        cap = connect_camera()

    ret, frame = cap.read()
    if not ret:
        print("프레임 수신 실패. 다시 시도 중...")
        cap.release()
        time.sleep(3)
        cap = connect_camera()
        continue

    # 🔹 녹화 프레임과 화면 표시 프레임을 분리
    record_frame = frame.copy()

    brightness = cv2.getTrackbarPos('Brightness', 'IP Camera Stream')
    contrast = cv2.getTrackbarPos('Contrast', 'IP Camera Stream')

    frame = adjust_brightness_contrast(frame, brightness, contrast)
    record_frame = adjust_brightness_contrast(record_frame, brightness, contrast)

    if flip_mode == 1:
        frame = cv2.flip(frame, 1)
        record_frame = cv2.flip(record_frame, 1)
    elif flip_mode == 0:
        frame = cv2.flip(frame, 0)
        record_frame = cv2.flip(record_frame, 0)
    elif flip_mode == -1:
        frame = cv2.flip(frame, -1)
        record_frame = cv2.flip(record_frame, -1)

    # 🔴 화면에만 빨간 원 표시 (녹화 영상에는 저장되지 않음)
    if recording:
        cv2.circle(frame, (50, 50), 10, (0, 0, 255), -1)
        out.write(record_frame)  # 녹화는 빨간 원 없는 프레임 사용

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
        if flip_mode == 1:
            flip_mode = 0
        elif flip_mode == 0:
            flip_mode = -1
        else:
            flip_mode = 1

cap.release()
if out:
    out.release()
cv2.destroyAllWindows()
