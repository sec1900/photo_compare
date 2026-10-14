import cv2
import time
from datetime import datetime
import os
from skimage.metrics import structural_similarity as ssim
from playsound import playsound
import threading

def play_sound_for_duration(file_path, duration):
    end_time = time.time() + duration
    while time.time() < end_time:
        playsound(file_path)
        # 播放完成后添加延迟，确保在一分钟内不会超过播放频率
        time.sleep(1) 

def capture_images(interval=60, camera_index=1):
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    previous_frame = None
    start_time = time.time()

    try:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("无法读取摄像头帧")
                break

            timestamp = datetime.now().strftime("%m%d%H%M")
            output_path = f"{timestamp}.jpg"

            cv2.imwrite(output_path, frame)
            print(f"图片已保存到 {output_path}")

            if not os.path.isfile(output_path):
                print(f"文件保存失败：{output_path}")
                continue

            if previous_frame is not None:
                current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                previous_frame_gray = cv2.cvtColor(previous_frame, cv2.COLOR_BGR2GRAY)

                similarity, _ = ssim(previous_frame_gray, current_frame_gray, full=True)
                print(f"相似度: {similarity:.2f}")

                if similarity > 0.9:
                    print("没事")
                else:
                    print("有事")
                    # 启动线程循环播放音频
                    threading.Thread(target=play_sound_for_duration, args=('1.mp3', 60)).start()

            previous_frame = frame

            # 拍摄下一张照片前每两秒输出一个 *
            elapsed_time = 0
            while elapsed_time < interval:
                if time.time() - start_time >= 2:
                    print("*", end='', flush=True)
                    start_time = time.time()
                time.sleep(1)
                elapsed_time += 1
    except KeyboardInterrupt:
        print("捕获中断")

    cap.release()
    cv2.destroyAllWindows()

capture_images(interval=60)
