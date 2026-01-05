import cv2
import socket
import struct
import numpy as np
import sys

if len(sys.argv) != 2:
    print("用法: python camera_client.py <cpolar公開地址:端口>")
    print("範例: python camera_client.py 10.tcp.cpolar.top:12731")
    sys.exit(1)

host, port_str = sys.argv[1].split(':')
port = int(port_str)

print(f"正在連接 {host}:{port} 並傳送本地鏡頭影像...")

# 開啟本地相機（0 通常是內建鏡頭，1、2...是外接鏡頭）
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("錯誤：無法開啟相機，請檢查攝影機是否被佔用")
    sys.exit(1)

# 設定畫質（可選，傳輸更順暢）
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    print("已連線成功，開始傳送影像... 按 Ctrl+C 結束")

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("無法讀取相機畫面")
                break

            # 壓縮成 JPEG（品質 80 剛好，傳輸快又清楚）
            _, jpeg_data = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            jpeg_bytes = jpeg_data.tobytes()

            # 先傳 4 bytes 長度（大端序）
            s.sendall(struct.pack(">L", len(jpeg_bytes)))
            # 再傳 JPEG 資料
            s.sendall(jpeg_bytes)

    except KeyboardInterrupt:
        print("\n你按了 Ctrl+C，結束傳送")

    except Exception as e:
        print(f"傳送中斷：{e}")

    finally:
        cap.release()
        print("相機已釋放")
        print("程式結束")