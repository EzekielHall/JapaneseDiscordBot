from datetime import datetime

def log(text: str, console: bool = True) -> None:
    """
    param text: Takes in a string to log to a file and console
    """
    logMsg = str(datetime.now().replace(microsecond=0)) + "  ::  " + text + "\n"
    try:
        with open("log.txt", "a", encoding="utf-8") as logFile:
            logFile.write(logMsg)
    except Exception as e:
        print(f"Failed to save to file log. Bypassing file logging. ERROR: {e}")
    if console:
        print(logMsg,end="")