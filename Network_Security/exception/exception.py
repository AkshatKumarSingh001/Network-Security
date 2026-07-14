import sys
from Network_Security.logging import logger

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details:sys):
        self.error_message = error_message
        _,_,exc_tb = error_details.exc_info()

        # Prefer the traceback attached to the exception object itself —
        # this works even if you're raising from a different function/frame.
        exc_tb = getattr(error_message, "__traceback__", None)
        if exc_tb is None:
            # fallback for cases where error_message isn't an exception object
            _, _, exc_tb = error_details.exc_info()

        if exc_tb is not None:
            self.lineno = exc_tb.tb_lineno
            self.file_name = exc_tb.tb_frame.f_code.co_filename
        else:
            self.lineno = None
            self.file_name = None

    def __str__(self):
        return (f"Error occured in script: [{self.file_name}] "
                f"at line number: [{self.lineno}] "
                f"error message: [{self.error_message}]")
    
if __name__=='__main__':
    try:
        logger.logging.info("Entered the try block")
        a = 1/0
        print("This will not be printed",a)
    except Exception as e:
        logger.logging.error("An error occurred")
        raise NetworkSecurityException(e, sys)