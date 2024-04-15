import socket
import time

HOST = '127.0.0.1'
PORT = 65432

precision = 0.1

def calculate_bit(time_diff):
    if 0.2 * precision > time_diff:
        return '0'
    return '1'


def convert_bits_to_message(hidden_message):
    bytes_list = [hidden_message[i:i + 8] for i in range(0, len(hidden_message), 8)]
    message = ''.join([chr(int(byte, 2)) for byte in bytes_list])
    return message


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))

    server_socket.listen()
    print('Server is listening...')

    conn, addr = server_socket.accept()

    with conn:
        received_message = ''
        hidden_message = ''
        prev_time = None
        dont_count_any_more = False
        while True:
            # Receive data from client
            data = conn.recv(1)
            if not data:
                break

            # Check if the semicolon is received -> for end of message
            if data == b';':
                print('Received Message:', received_message)
                print('Hidden Message:', convert_bits_to_message(hidden_message))
                received_message = ''

            else:
                if dont_count_any_more is False and data == b'|':
                    dont_count_any_more = True

                if dont_count_any_more is False:
                    received_message += data.decode()

                # Check if this is not the first character -> received hidden message
                if prev_time is not None:
                    current_time = time.time()
                    time_difference = current_time - prev_time
                    prev_time = current_time
                    hidden_message += calculate_bit(time_difference)
                else:
                    prev_time = time.time()
