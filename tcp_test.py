import socket
import threading

HOST = '0.0.0.0'
PORT = 5000

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(1)

print(f"TCP Server 啟動，監聽 {HOST}:{PORT}")
print("等待 EZDTU 連線...")

client = None
addr = None

def recv_thread():
    global client
    while True:
        try:
            data = client.recv(1024)
            if not data:
                print("\n[系統] 對方斷線")
                break

            print("\n[收到] ", data.decode('utf-8', errors='ignore'))
        except:
            break

def send_thread():
    global client
    while True:
        try:
            msg = input()
            if msg.lower() == "exit":
                print("[系統] 關閉連線")
                client.close()
                break
            client.send((msg + "\r\n").encode('utf-8'))
        except:
            break

while True:
    client, addr = s.accept()
    print(f"\n=== EZDTU 連上來了：{addr} ===")

    # 建立接收執行緒
    t1 = threading.Thread(target=recv_thread)
    t1.daemon = True
    t1.start()

    # 建立發送執行緒
    t2 = threading.Thread(target=send_thread)
    t2.daemon = True
    t2.start()

    t1.join()
    t2.join()

    print("等待下一個連線...")
