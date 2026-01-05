import cv2
import socket
import struct
import numpy as np

# 設定伺服器監聽的 IP 和端口
HOST = '0.0.0.0'  # 監聽所有網路介面
PORT = 5000       # 你可以改成其他端口，例如 12345

print(f"伺服器啟動，監聽 {HOST}:{PORT}")
print("等待 client 連線...（按 Ctrl+C 停止伺服器）")

# 建立 socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

conn, addr = server_socket.accept()
print(f"client 連線進來：{addr}")

data = b""
payload_size = struct.calcsize(">L")

try:
    while True:
        # 接收長度資訊
        while len(data) < payload_size:
            packet = conn.recv(4096)
            if not packet:
                print("client 斷開連線")
                raise Exception("斷線")
            data += packet

        packed_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_size)[0]

        # 接收 JPEG 資料
        while len(data) < msg_size:
            packet = conn.recv(4096)
            if not packet:
                print("client 斷開連線")
                raise Exception("斷線")
            data += packet

        jpeg_data = data[:msg_size]
        data = data[msg_size:]

        # 解碼並顯示
        frame = cv2.imdecode(np.frombuffer(jpeg_data, dtype=np.uint8), cv2.IMREAD_COLOR)
        if frame is not None:
            cv2.imshow(f'遠端鏡頭 - {addr} (按 q 離開)', frame)
            if cv2.waitKey(1) == ord('q'):
                break

except Exception as e:
    print(f"連線結束：{e}")

finally:
    conn.close()
    server_socket.close()
    cv2.destroyAllWindows()
    print("伺服器已關閉")