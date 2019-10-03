import Scanner as scanner
import Type as type


if __name__ == "__main__":
    scaninho = scanner.Scanner('exemplo1.txt')
    scaninho.open_file()
    token = scaninho.getToken()
    while(token.type != type.Type().FIMARQ):
        print(str(token.type) , " -> " , str(token.line))
        token = scaninho.getToken()
