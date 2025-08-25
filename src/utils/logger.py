"""
This files logs messages to the screen or to a log file.

"""
import numpy as np

class Logger:
    """
    Utility class for logging messages.
    """
    def __init__(self, log_file = "log.txt", len_info = 50, frame_string = None, frame_margin = 0):
        """
        len_info is used to set the maximum length of information """
        self.log_file = log_file
        self.len_info = len_info
        if frame_string is not None:
            assert isinstance(frame_string, str)
            assert len(frame_string) == 1, "Frame string must be a single character."
            assert isinstance(frame_margin, int)
            assert frame_margin >= 0, "Frame margin must be positive."
            self.frame_string = frame_string
            self.frame_margin = frame_margin
            self.frame_top = self.frame_string * self.frame_margin
            self.frame_bottom = self.frame_string * self.frame_margin
            self.frame_left = self.frame_string + " " * (self.frame_margin - 1)
            self.frame_right = " " * (self.frame_margin - 1) + self.frame_string
            self.frame_separation = self.frame_left + " " * self.len_info + self.frame_right
        else:
            self.frame_string = None
            self.frame_margin = 0
            self.frame_top = ''
            self.frame_bottom = ''
            self.frame_left = ''
            self.frame_right = ''


    @staticmethod
    def string_to_array(string, nlen):
        """
        Given a sentence, this function converts it to an array of lines, with each line having
        at most nlen characters.

        It does so by first check if the string contains only one word. If so, check if the length
        of the word is greater than nlen, if so, split the word into an array of strings with nlen-1
        characters each, and for each but the last string, add a hyphen.

        In case where the string contains multiple words, split the string into words and join them
        into lines with at most nlen characters.
        """
        if len(string) == 0:
            return [""]
        words = string.split(" ")
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + 1 > nlen:
                lines.append(current_line)
                current_line = word
            else:
                if current_line:
                    current_line += " "
                current_line += word
        lines.append(current_line)
        return lines
    
    @staticmethod
    def append_string_with_character(string, character, nlen):
        assert isinstance(string, str), "String must be a string."
        assert isinstance(character, str), "Character must be a string."
        assert isinstance(nlen, int), "nlen must be an integer."
        assert nlen >= 0, "nlen must be greater than 0."
        assert len(character) == 1, "Character must be a single character."
        ndiff = nlen - len(string)
        if ndiff <= 0:
            return string
        else:
            return string + ndiff * character

    def log_highlight(self, message, level=None):
        """
        level: The level of the log message.
            type: int or str
            values: 0 or R. regular message
                    1 or W. warning message
                    2 or E. error message
        Logs a message to the console and to the log file.

        If level is None, then ilevel = 0.
        If the type of level is string, then obtain the first character
        in the string and upper it. Based on whether it is R, W, E, set ilevel
        to 0, 1, 2, respectively. Otherwise set ilevel to 0.
        If the type of level is integer, set ilevel to level accordingly. If
        level is not 0, 1, or 2, set ilevel to 0.

        1.  Print self.frame_top to the console and to self.log_file
        2.  If ilevel is 1, print append_string_with_character("WARNING", ' ', self.len_info)
        to the console and to the log file.
            If ilevel is 2, print append_string_with_character("ERROR", ' ', self.len_info)
        to the console and to the log file.
        3.  Get the current date time as date_time. print self.frame_left,
        append_string_with_character(date_time, ' ', self.len_info), and self.frame_right
        in the same line to the console and to self.log_file
        4.  Convert the message into an array using string_to_array. For each element
        in the array, print self.frame_left, append_string_with_character(element, ' ', self.len_info),
        and self.frame_right to the console and to the log file
        5.  Print self.frame_bottom to the console and to the log file
        """

        if level is None:
            ilevel = 0
        elif isinstance(level, str):
            ilevel = {"R": 0, "W": 1, "E": 2}.get(level[0].upper(), 0)
        elif isinstance(level, int):
            ilevel = level
            if ilevel not in [0, 1, 2]:
                ilevel = 0
        else:
            ilevel = 0

        with open(self.log_file, 'a') as f:
            print(self.frame_top)
            f.write(self.frame_top + "\n")    
            print(self.frame_separation)
            f.write(self.frame_separation + "\n")
            if ilevel == 1:
                string_to_print = self.frame_left + self.append_string_with_character("WARNING", ' ', self.len_info) + self.frame_right
                f.write(string_to_print + "\n")
            if ilevel == 2:
                string_to_print = self.frame_left + self.append_string_with_character("ERROR", ' ', self.len_info) + self.frame_right
                f.write(string_to_print + "\n")
            date_time = np.datetime64('now', 's')
            string_to_print = self.frame_left + self.append_string_with_character(date_time, ' ', self.len_info) + self.frame_right
            print(string_to_print)
            f.write(string_to_print + "\n")
            for element in self.string_to_array(message, self.len_info):
                string_to_print = self.frame_left + self.append_string_with_character(element, ' ', self.len_info) + self.frame_right
                print(string_to_print)
                f.write(string_to_print + "\n")
            print(self.frame_separation)
            f.write(self.frame_separation + "\n")
            print(self.frame_bottom)
            f.write(self.frame_bottom + "\n")

    def log_info(self, message):
        with open(self.log_file, 'a') as f:
            for element in self.string_to_array(message, self.len_info):
                string_to_print = self.append_string_with_character(element, ' ', self.len_info)
                print(string_to_print)
                f.write(string_to_print + "\n")
