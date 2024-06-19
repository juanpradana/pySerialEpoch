# import serial
# import serial.tools.list_ports
# import time

# def list_serial_ports():
#     ports = serial.tools.list_ports.comports()
#     return [(port.device, port.description) for port in ports]

# def get_epoch_time_10_digits():
#     epoch_time = int(time.time())
#     return str(epoch_time)

# def send_epoch_time_via_serial(port):
#     ser = serial.Serial(port, 9600, timeout=1)
#     time.sleep(2)
#     epoch_time = get_epoch_time_10_digits()
#     ser.write(epoch_time.encode())
#     print(f"Sent: {epoch_time} to {port}")
#     time.sleep(1)
#     ser.close()

# if __name__ == "__main__":
#     available_ports = list_serial_ports()
#     if not available_ports:
#         print("No serial ports found")
#     else:
#         print("Available serial ports:")
#         for i, (port, description) in enumerate(available_ports):
#             print(f"{i}: {port} - {description}")

#         port_index = int(input("Select port index: "))
#         selected_port = available_ports[port_index][0]
#         send_epoch_time_via_serial(selected_port)

import serial
import serial.tools.list_ports
import time
import threading

def list_serial_ports():
    ports = serial.tools.list_ports.comports()
    return [(port.device, port.description) for port in ports]

def get_epoch_time_10_digits():
    epoch_time = int(time.time())
    return str(epoch_time)

def send_epoch_time_via_serial(ser):
    # ser = serial.Serial(port, 9600, timeout=1)
    # time.sleep(2)
    epoch_time = get_epoch_time_10_digits()
    ser.write(epoch_time.encode())
    print(f"Sent: {epoch_time}")
    time.sleep(1)
    # ser.close()

def read_from_serial(ser):
    while True:
        if ser.in_waiting > 0:
            received_data = ser.readline().decode().strip()
            print(f"Received: {received_data}")

if __name__ == "__main__":
    available_ports = list_serial_ports()
    if not available_ports:
        print("No serial ports found")
    else:
        print("Available serial ports:")
        for i, (port, description) in enumerate(available_ports):
            print(f"{i}: {port} - {description}")

        port_index = int(input("Select port index: "))
        selected_port = available_ports[port_index][0]

        ser = serial.Serial(selected_port, 9600, timeout=1)
        time.sleep(2)

        send_thread = threading.Thread(target=send_epoch_time_via_serial, args=(ser,))
        read_thread = threading.Thread(target=read_from_serial, args=(ser,))
        send_thread.start()
        read_thread.start()

        send_thread.join()
        read_thread.join()