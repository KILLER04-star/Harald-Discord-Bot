import datetime
import sys


def log_error( exception, message):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    message = str("Error_Code: " + str(exception) + "\nError_Type: " + str(exc_type) + "\nLine: " + str(
        exc_tb.tb_lineno) + "\nMessage: " + str(message))
    file = open("../log/errorlog.txt", "a+", encoding="utf-8")
    file.write('\n' + "-------------------------------" + '\n')
    file.write(str(datetime.datetime.today()) + " " + message)
    file.close()
    print(str(datetime.datetime.today()) + " " + message)