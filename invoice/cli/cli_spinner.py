import itertools
import sys
import threading
import time


class Spinner:
    """
    A class that represents a spinner animation in the console.

    Attributes:
        spinner (itertools.cycle): An iterator that cycles through a list of spinner animation characters.
        delay (float): The delay between each spinner character.
        spinner_active (bool): A flag indicating whether the spinner animation is active.
        thread (threading.Thread): A thread that runs the spinner animation.

    Methods:
        __init__(self, delay=0.1): Initializes the Spinner object with the specified delay.
        spin(self): Prints the spinner animation characters in the same position using '\r'.
        start(self): Starts the spinner animation.
        stop(self): Stops the spinner animation.
        __enter__(self): Starts the spinner animation when used as a context manager.
        __exit__(self, exc_type, exc_val, exc_tb): Stops the spinner animation when used as a context manager.

    Example usage:
        >>> with Spinner():
                # Perform some long-running task
                time.sleep(5)"""

    def __init__(self, delay=0.1):
        # Spinner animation characters
        self.spinner = itertools.cycle(["-", "/", "|", "\\"])
        self.delay = delay
        self.spinner_active = False
        self.thread = threading.Thread(target=self.spin)

    def spin(self):
        # Print spinner characters in the same position using '\r'
        while self.spinner_active:
            sys.stdout.write(next(self.spinner))  # write the next character
            sys.stdout.flush()  # flush output buffer
            sys.stdout.write("\r")  # return to start of line
            time.sleep(self.delay)

    def start(self):
        self.spinner_active = True
        self.thread.start()

    def stop(self):
        self.spinner_active = False
        self.thread.join()  # wait for spinner thread to finish
        sys.stdout.write("\r")  # clear spinner

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
