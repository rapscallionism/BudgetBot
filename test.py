

def main():
    test_var = ['Grocery Item,Amount\r\n', 'sausage,2\r\n']
    print(test_var[0].replace("\r", "").replace("\n", "").split(","))

if __name__ == "__main__":
    main()