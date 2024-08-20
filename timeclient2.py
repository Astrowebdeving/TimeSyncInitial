import socket
import subprocess
import time

# Get client self name
def get_client_self_name():
    return subprocess.check_output(
        "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep $ip | awk '{print $2}'",
        shell=True, text=True
    ).strip()

client_self_name = get_client_self_name()

# Create UDP socket for receiving response
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(('', 13898))

while True:
    try:
        # Receive response with a buffer size of 1024
        data, address = server_socket.recvfrom(1024)
        message = data.decode('utf-8')

        if message.startswith("T2"):
            parts = message.split(';')
            time_on_reception = float(parts[4])
            curr_time = float(parts[6])
            
            # Write times to files
            curr_client_time = time.time()
            with open(f"time3_{client_self_name}.txt", 'w') as f:
                f.write(str(curr_client_time))
            server_self_name = address[0]  # Assuming server_self_name can be derived from the response address
            with open(f"time3_{server_self_name}_i.txt", 'w') as f:
                f.write(str(time_on_reception))
            with open(f"time3_{server_self_name}_f.txt", 'w') as f:
                f.write(str(curr_time))

            # Read initial client time
            with open(f"time_curr1_{client_self_name}.txt", 'r') as f:
                initial_client_time = float(f.read().strip())

            # Calculate times
            time_diff = curr_time - time_on_reception
            full_diff = curr_client_time - initial_client_time
            Cristian_time = (curr_time + time_on_reception) / 2 + (full_diff) / 2
            Trans_time = (full_diff - time_diff) / 2
            time_delta = curr_client_time - Cristian_time 
            # Print results
            print("#######################")
            print(f"Using server with name: {server_self_name}")
            print(f"time_diff: {time_diff}")
            print(f"full_diff: {full_diff}")
            print(f"Cristian_time: {Cristian_time}")
            print(f"Trans_time: {Trans_time}")
            print(f"curr_client_time: {curr_client_time}")
            print(f"time_delta: {time_delta}")
            print("#######################")
    except Exception as e:
        print(f"Error: {e}")

#server_socket.close()
