import Scanner as scanner


if __name__ == "__main__":
    scaninho = scanner.Scanner('exemplo1.txt')
    scaninho.open_file()
    for i in range(0 , 10):
        print(scaninho.getToken().type)
