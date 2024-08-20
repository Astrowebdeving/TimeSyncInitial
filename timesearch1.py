import asyncio
import subprocess
import time
import socket

# Get client self name
client_self_name = subprocess.check_output(
    "ip=$(hostname -I | awk '{print $1}')\n cat /etc/hosts | grep $ip | awk '{print $2}'",
    shell=True, text=True
).strip()

def get_ip_from_hosts(name):
    """Retrieve IP address from /etc/hosts based on hostname."""
    with open('/etc/hosts', 'r') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[1] == name:
                return parts[0]
    raise ValueError(f"No IP address found for hostname {name}")

async def send_message(ip, port, message):
    """Send a UDP message asynchronously."""
    loop = asyncio.get_running_loop()
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.setblocking(False)
    addr = ip, port  # Address tuple
    try:
        # Use sendto to specify the address and port
        await loop.sock_sendto(client_socket, message.encode('utf-8'), addr)
        print(f"Message sent to {ip}:{port}")
    except Exception as e:
        print(f"Error sending message to {ip}:{port}: {e}")
    finally:
        client_socket.close()

async def main():
    hostlist = ["manager", "worker1", "worker2"]
    port = 18736
    first_time_client = time.time()

    # Write initial time to file
    with open(f"time_init_{client_self_name}.txt", 'w') as f:
        f.write(str(first_time_client))

    tasks = []
    for host in hostlist:
        if host != client_self_name:
            try:
                # Resolve host address from /etc/hosts
                ip = get_ip_from_hosts(host)
                message = f"Tm1;x;{client_self_name};f*;{first_time_client}"

                # Create and schedule sending tasks
                tasks.append(send_message(ip, port, message))
            except ValueError as ve:
                print(f"Error resolving address for {host}: {ve}")
            except Exception as e:
                print(f"Unexpected error: {e}")
    
    # Await all tasks to ensure all messages are sent before exiting
    await asyncio.gather(*tasks)
    print("All messages sent.")

if __name__ == "__main__":
    asyncio.run(main())
