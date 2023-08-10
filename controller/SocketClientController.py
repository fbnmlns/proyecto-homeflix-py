import socket
import os
import io

from Controller.DataInputStream import DataInputStream


class SocketClientController:

    def connect(self):
        s = socket.socket()
        port = 3400
        s.connect(('localhost', port))

        data = s.recv(1024)
        stream = io.BytesIO(data)
        dataInputStream = DataInputStream(stream)
        fileNameLength = dataInputStream.read_int()
        print(fileNameLength)
        result = ''
        if fileNameLength > 0:
            fileNameBytes = s.recv(fileNameLength)
            fileName = fileNameBytes.decode()
            print(fileName)

            data = s.recv(1024)
            stream = io.BytesIO(data)
            dataInputStream = DataInputStream(stream)

            fileContentLength = dataInputStream.read_int()
            print(fileContentLength)

            if fileContentLength > 0:
                fileContentBytes = s.recv(1024)
                file = open(fileName, "wb")


                while fileContentBytes:
                    file.write(fileContentBytes)
                    fileContentBytes = s.recv(1024)

                working_directory = os.getcwd()
                result = os.path.join(working_directory, file.name)
                print(result)
                file.close()

        s.close()
        return result
