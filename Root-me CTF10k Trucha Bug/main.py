import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("ctf10k.root-me.org", 7000))

input = s.recv(2048)
print("[+] Received : {}".format(input.decode().strip('\n')))

s.sendall(b"flagz1\n")
print("[+] Sent flagz1\n")

input = s.recv(2048)
print("[+] Received : {}".format(input[:-1].decode().strip('\n')))

msg = b"0\n"
s.sendall(msg)
print("[+] Sent 0\n")

input = s.recv(2048)
print("[+] Received : {}".format(input.decode().strip('\n')))