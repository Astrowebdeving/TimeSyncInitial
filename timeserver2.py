import socket
import subprocess
import time

# Get server self name
def get_server_self_name():
    return subprocess.check_output(
        "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep $ip | awk '{print $2}'",
        shell=True, text=True
    ).strip()

server_self_name = get_server_self_name()

# Create UDP socket for receiving
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 13897))

# Create UDP socket for responding
response_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    try:
        # Receive message with a buffer size of 1024
        data, address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')

        # Check for EOT marker
        if message.endswith('\x04'):
            message = message[:-1]  # Remove the EOT character

            if message.startswith("T1"):
                # Handle T1 message
                time_on_reception = time.time()
                parts = message.split(';')
                client_self_name = parts[2]
                current_time_received = float(parts[4])

                # Write received data to files
                with open(f"Time1_{client_self_name}.txt", 'w') as f:
                    f.write(str(current_time_received))
                current_server_time = time.time()
                with open(f"time_curr1_{server_self_name}.txt", 'w') as f:
                    f.write(str(current_server_time))
                
                # Send T2 message
                response_message = f"T2;x;{server_self_name};g*;{time_on_reception};y;{current_server_time}".encode('utf-8')
                response_socket.sendto(response_message, (address[0], 13898))
    except Exception as e:
        print(f"Error: {e}")
