from datetime import datetime

def log(text: str) -> None:
    logMsg = str(datetime.now().replace(microsecond=0)) + "  ::  " + text + "\n"
    try:
        with open("log.txt", "a", encoding="utf-8") as logFile:
            logFile.write(logMsg)
    except Exception as e:
        print(f"Failed to save to file log. Bypassing file logging. ERROR: {e}")
    print(logMsg,end="")