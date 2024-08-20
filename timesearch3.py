import asyncio
import subprocess
import time
import socket

# Get client self name
client_self_name = subprocess.check_output(
    "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep $ip | awk '{print $2}'",
    shell=True, text=True
).strip()

async def handle_response(data):
    try:
        # Decode message
        message = data.decode('utf-8')
        print(f"Received response: {message}")

        # Split header and message using the delimiter
        parts = message.split(';f*;', 1)
        if len(parts) == 2:
            header, msg = parts
        else:
            header = parts[0]
            msg = ""  # No message part found

        header_parts = header.split(';')
        server_self_name = header_parts[2] if len(header_parts) > 2 else "unknown"

        # Parse the message for starting_server_time and ending_server_time
        time_parts = msg.split(';y;', 1)
        if len(time_parts) == 2:
            starting_server_time, ending_server_time = time_parts
        else:
            starting_server_time = time_parts[0]
            ending_server_time = ""  # No ending time part found

        # Convert times to float
        starting_server_time = float(starting_server_time) if starting_server_time else 0.0
        ending_server_time = float(ending_server_time) if ending_server_time else 0.0

        # Write ending server time to file
        with open(f"time_end_{server_self_name}.txt", 'w') as f:
            f.write(str(ending_server_time))

        # Write starting server time to file
        with open(f"time_start_{server_self_name}.txt", 'w') as f:
            f.write(str(starting_server_time))

        # Write final client time to file
        final_client_time = time.time()
        with open(f"time_end_{client_self_name}.txt", 'w') as f:
            f.write(str(final_client_time))

        # Calculate and write transmission time
        with open(f"time_init_{client_self_name}.txt", 'r') as f:
            time_client_init = float(f.read().strip())
        transmission_time = ((final_client_time - time_client_init) - (ending_server_time - starting_server_time)) / 2
        with open(f"time_transmission_{server_self_name}.txt", 'w') as f:
            f.write(str(transmission_time))

        # Print results
        print("#################")
        print(f"transmission_time_{server_self_name}: {transmission_time}")
        print(f"time_client_init: {time_client_init}")
        print(f"final_client_time: {final_client_time}")
        print(f"ending_server_time - starting_server_time: {ending_server_time - starting_server_time}")
        print(f"starting_server_time: {starting_server_time}")
        print(f"ending_server_time: {ending_server_time}")
        print("#################")
    except Exception as e:
        print(f"Error in handling response: {e}")

async def main():
    # Initialize UDP socket for receiving responses
    loop = asyncio.get_running_loop()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(('0.0.0.0', 18837))
    client_socket.setblocking(False)

    print("Client server is running...")

    while True:
        try:
            # Use sock_recvfrom to get both data and address (non-blocking)
            data, address = await loop.sock_recvfrom(client_socket, 1024)
            print(f"Data received from {address}")

            # Handle the response asynchronously
            asyncio.create_task(handle_response(data))
        
        except Exception as e:
            print(f"Error in main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
