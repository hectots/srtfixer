# File: srt.py
# Summary: Models for SRT subtitles format.

import re


class Subtitle(object):
    """Represents a single subtitle line in SRT format."""

    TIME_FORMAT = "%02d:%02d:%02d,%d"
    SRT_FORMAT = "%s\r\n%s --> %s\r\n%s\r\n\r\n"

    def __init__(self, frame, start, end, message):
        self.frame = frame
        self.start = start
        self.end = end
        self.message = message

    def getFrame(self):
        """Returns the frame number of the subtitle."""
        return self.frame

    def setFrame(self, frame):
        """Sets the frame number for the subtitle."""
        self.frame = frame

    def getStartTime(self):
        """Returns the start time of the subtitle."""
        return self.start

    def setStartTime(self, hours, minutes, seconds, milliseconds):
        """Set the start time for the subtitle."""
        self.start = self.TIME_FORMAT % (hours, minutes, seconds, milliseconds)

    def getEndTime(self):
        """Returns the end time of the subtitle."""
        return self.end

    def setEndTime(self, hours, minutes, seconds, milliseconds):
        """Set the end time for the subtitle."""
        self.end = self.TIME_FORMAT % (hours, minutes, seconds, milliseconds)

    def changeTime(self, hours, minutes, seconds, milliseconds, operation):
        start_h, start_m, start_s = self.start.split(":")
        start_s, start_ms = start_s.split(',')

        end_h, end_m, end_s = self.end.split(":")
        end_s, end_ms = end_s.split(',')

        delta_time = hours * 3600000 + minutes * 60000 + seconds * 1000 + milliseconds

        start_time = int(start_h) * 3600000 + int(start_m) * 60000 + int(start_s) * 1000 + int(start_ms)
        new_start_time = operation(start_time, delta_time)

        self.setStartTime(
            new_start_time / 3600000,
            new_start_time % 3600000 / 60000,
            new_start_time % 3660000 % 60000 / 1000,
            new_start_time % 3600000 % 60000 % 1000)

        end_time = int(end_h) * 3600000 + int(end_m) * 60000 + int(end_s) * 1000 + int(end_ms)
        new_end_time = operation(end_time, delta_time)

        self.setEndTime(
            new_end_time / 3600000,
            new_end_time % 3600000 / 60000,
            new_end_time % 3600000 % 60000 / 1000,
            new_end_time % 3600000 % 60000 % 1000)

    def addTime(self, hours, minutes, seconds, milliseconds):
        """Add time to the subtitle start and end times."""
        self.changeTime(
            hours, minutes, seconds, milliseconds, lambda x, y: x + y)

    def substractTime(self, hours, minutes, seconds, milliseconds):
        """Substract time to the subtitle start and end times."""
        self.changeTime(
            hours, minutes, seconds, milliseconds, lambda x, y: x - y)

    def __str__(self):
        return self.SRT_FORMAT % (
            self.frame, self.start, self.end, self.message)


class Subtitles(object):
    """Parser for SRT formatted subtitles."""

    def __init__(self):
        self.subtitles = []

    def parse(self, string):
        """Parse a string containing a subtitle."""
        regex = r'(\d+)\s*?\n(\d+\:\d+\:\d+\,\d+)\s\-\-\>\s(\d+\:\d+\:\d+\,\d+)\s+(.*?\r?\n.*\r?\n)'
        matcher = re.compile(regex, re.I | re.M)
        matches = matcher.findall(string)

        for match in matches:
            self.subtitles.append(Subtitle(match[0], match[1], match[2], match[3]))

    def load(self, filename):
        """Load subtitles from a file."""
        file_handle = open(filename)
        self.parse(file_handle.read())
        file_handle.close()

    def save(self, filename):
        """Save subtitles in a file."""
        file_handle = open(filename, 'w')
        for subtitle in self.subtitles:
            file_handle.write(str(subtitle))
        file_handle.close()

    def addTime(self, hours, minutes, seconds, milliseconds):
        """Add time to the subtitle start and end times."""

        for subtitle in self.subtitles:
            subtitle.addTime(hours, minutes, seconds, milliseconds)

    def substractTime(self, hours, minutes, seconds, milliseconds):
        """Substract time to the subtitle start and end times."""

        for subtitle in self.subtitles:
            subtitle.substractTime(hours, minutes, seconds, milliseconds)
