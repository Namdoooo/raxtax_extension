def main():
    message = "Hello World"
    print(message)

    filename = "hello.txt"
    with open(filename, "w") as f:
        f.write(message)

if __name__ == "__main__":
    main()