import socket
import time

HOST = '127.0.0.1'
PORT = 65432

precision = 0.1


def calculate_time(bit):
    if bit == '0':
        return 0.1 * precision
    return 0.2 * precision


def convert_message_to_bits(message):
    bits_list = [format(ord(char), '08b') for char in message]
    bits = ''.join(bits_list)
    return bits


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
    client_socket.connect((HOST, PORT))
    hidden_message = input('Enter hidden message to send: ')
    hidden_bits = convert_message_to_bits(hidden_message)
    counter_hidden = 0
    message = input("Enter message to send: ")
    while len(hidden_bits) > len(message):
        message += '|' + message
    message += ';'
    for char in message:
        client_socket.sendall(char.encode())
        # send hidden data
        if counter_hidden < len(hidden_bits):
            send_bit = hidden_bits[counter_hidden]

            time.sleep(calculate_time(send_bit))
            counter_hidden += 1
