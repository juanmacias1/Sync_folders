import os
import time

def logger(log_file_path, message):
    if not os.path.exists(os.path.dirname(log_file_path)):
        os.makedirs(os.path.dirname(log_file_path))
    
    with open(log_file_path, "a") as file:
        file.write("\n")
        file.write(f"{time.ctime()}: {message}")
        print(message)

def exit_handler(log_file_path):
    with open(log_file_path, "a") as file:
        file.write("\n")
        file.write("Script terminated\n")
        file.write("\n")

