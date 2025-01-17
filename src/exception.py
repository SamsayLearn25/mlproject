import sys, os

def error_message_details(error, error_detail:sys):
    
    #exc_tb : on which file, lineno error occured
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_no = exc_tb.tb_lineno

    error_message = f"error occured in:\n python script name: {file_name}\n lineno: {line_no}\n error_message: {error}"

    return error_message

class CustomException(Exception):

    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.error_message = error_message_details(error_message, error_detail)

    def __str__(self):
        return self.error_message
    

