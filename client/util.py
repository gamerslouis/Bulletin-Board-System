def SendServer(sock, input):
    sock.sendall((input+'\n').encode())

    while True:
        try:
            message = sock.recv(2048)
        except OSError:
            return ''
        if len(message) == 0:
            return ''
        message_buffer = b''
        message_buffer += message
        message_buffer = message_buffer.replace(b'\r\n', b'\n')
        try:
            idx = message_buffer.index(b'\n')
            if idx != -1:
                command = message_buffer[:idx]
                message_buffer = message_buffer[idx + 1:]
                return command.decode()
        except ValueError:
            # command line still not end
            pass
