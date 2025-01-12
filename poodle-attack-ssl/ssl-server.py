import ssl
import socket

def run_ssl_server():
    # サーバーのホストとポート
    host = "127.0.0.1"
    port = 8443

    # SSLコンテキストの作成
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  # SSL 3.0
    context.load_cert_chain(certfile="server.crt", keyfile="server.key")  # 証明書と秘密鍵を設定

    # ソケットの作成
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print(f"SSL 3.0 Server is running on {host}:{port}...")
    with context.wrap_socket(server_socket, server_side=True) as ssl_server_socket:
        while True:
            client_socket, client_addr = ssl_server_socket.accept()
            print(f"Connection established with {client_addr}")
            try:
                # クライアントからのメッセージを受信
                data = client_socket.recv(1024)
                print(f"Received: {data.decode('utf-8')}")
                # レスポンスを送信
                response = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!"
                client_socket.sendall(response.encode("utf-8"))
            except Exception as e:
                print(f"Error: {e}")
            finally:
                client_socket.close()

if __name__ == "__main__":
    run_ssl_server()
