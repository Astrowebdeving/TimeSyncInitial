import asyncio
import subprocess
import time
import socket

# Get server self name
server_self_name = subprocess.check_output(
    "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep $ip | awk '{print $2}'",
    shell=True, text=True
).strip()

# Asynchronous function to handle received messages
async def handle_message(data, address, response_socket):
    try:
        # Immediately capture starting time
        starting_server_time = time.time()

        # Decode message
        message = data.decode('utf-8')
        print(f"Received message: {message} from {address}")

        # Parse the message using the correct delimiter
        parts = message.split(';f*;', 1)
        if len(parts) == 2:
            header, msg = parts
        else:
            header = parts[0]
            msg = ""  # No message part found

        header_parts = header.split(';')
        client_self_name = header_parts[2] if len(header_parts) > 2 else "unknown"
        first_time_client = float(msg) if msg else 0.0

        # Write received time to file
        with open(f"first_time_{client_self_name}.txt", 'w') as f:
            f.write(str(first_time_client))
        
        # Initialize response header and capture ending time
        response_header = f"Tm3;y;{server_self_name};f*;"
        ending_server_time = time.time()

        # Prepare response message
        response_message = f"{starting_server_time};y;{ending_server_time}"
        response_packet = f"{response_header}{response_message}".encode('utf-8')

        # Send response back to client on the correct port (18837)
        response_socket.sendto(response_packet, (address[0], 18837))
        print(f"Sent response to {address}")

        # Write ending server time to file
        with open(f"time_end_{server_self_name}.txt", 'w') as f:
            f.write(str(ending_server_time))

    except Exception as e:
        print(f"Error in handling message: {e}")

async def main():
    # Initialize UDP socket for receiving
    loop = asyncio.get_running_loop()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 18736))
    server_socket.setblocking(False)

    print("Server is running...")

    while True:
        try:
            # Use sock_recvfrom to get both data and address (non-blocking)
            data, address = await loop.sock_recvfrom(server_socket, 1024)
            print(f"Data received from {address}")

            # Handle the received message asynchronously
            asyncio.create_task(handle_message(data, address, server_socket))
        
        except Exception as e:
            print(f"Error in main loop: {e}")

if __name__ == "__main__":
    asyncio.run(main())
