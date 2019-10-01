import Scanner as scanner
import Type as type


if __name__ == "__main__":
    scaninho = scanner.Scanner('exemplo1.txt')
    scaninho.open_file()
    char = scaninho.getToken().type
    while(char != type.Type().FIMARQ):
        print(char)
        char = scaninho.getToken().type
