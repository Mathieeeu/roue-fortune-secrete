import time

DISPLAY = True

def write_log(message, type="info"):
    if type == "space":
        log_message = "\n"
    else:
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        log_message = f"[{timestamp}] [{type.upper()}] {message}"
    
    if DISPLAY:
        print(log_message)
    
    with open("script.log", "a", encoding="utf-8") as log_file:
        log_file.write(log_message + "\n")
