from server import *

def __log(status="INFO", message=""):
    print("[{status}] {message}".format(status=status, message=message))

def main():
    __log("Starting web server")
    app.run(HOST, PORT)

    time.sleep(5)
    __log("Server should be running")

if __name__ == "__main__":
    main()