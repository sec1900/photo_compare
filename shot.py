import cv2
import time
from datetime import datetime
import os

def capture_images(interval=60, camera_index=0):
    # 打开摄像头，camera_index=0表示内部摄像头，1表示外接摄像头
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print("无法打开摄像头")
        return

    try:
        while True:
            # 读取摄像头的帧
            ret, frame = cap.read()

            if not ret:
                print("无法读取摄像头帧")
                break

            # 获取当前时间并格式化为"月日时分"
            timestamp = datetime.now().strftime("%m%d%H%M")
            output_path = f"{timestamp}.jpg"

            # 保存捕获的帧到指定路径
            cv2.imwrite(output_path, frame)
            print(f"图片已保存到 {output_path}")

            # 检查文件是否成功保存
            if not os.path.isfile(output_path):
                print(f"文件保存失败：{output_path}")
                continue

            # 等待指定的间隔时间（秒）
            time.sleep(interval)
    except KeyboardInterrupt:
        print("捕获中断")

    # 释放摄像头
    cap.release()
    cv2.destroyAllWindows()

# 调用函数，每隔一分钟拍照并保存图片
capture_images(interval=60)
