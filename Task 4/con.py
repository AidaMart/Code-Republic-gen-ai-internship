# concurrency 
# parallelism 
# execution unit 

# pipe, socket, mapping file 

import socket
import multiprocessing

def server():
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind(("127.0.0.1", 12345))
	server_socket.listen(1)

	connection, address = server_socket.accept()
	message = connection.recv(1024).decode()

	print("Server received: ", message)

	connection.close()


def client():
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client_socket.connect(("127.0.0.1", 12345))

	client_socket.send("Client connected".encode())

	client_socket.close()


if __name__ == "__main__":
	server_process = multiprocessing.Process(target=server)
	client_process = multiprocessing.Process(target=client)

	server_process.start()
	client_process.start()


