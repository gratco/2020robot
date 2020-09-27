#!/usr/bin/env python3
"""

"""

from __future__ import print_function

import odrive
from fibre.utils import Event, Logger


class Odriver:

    def __init__(self):

        self.interactive_variables = {}
        self.discovered_devices = []

        self.drive_count = 0
        self.odrives = self.find_all_odrives()

        if self.odrives != None:
            print('found {} ODrives'.format(len(self.odrives)))
            for odrv in self.odrives:
                print(odrv.serial_number)

    def get_board(self, board_num):
        array_length = len(self.odrives)
        if board_num < array_length:
            return self.odrives[board_num]
        return None

    def get_board_count(self):
        return len(self.odrives)

    def find_all_odrives(self, path="usb", serial_number=None,
                         search_cancellation_token=None, channel_termination_token=None,
                         timeout=30, logger=Logger(verbose=True)):
        """
        Blocks until timeout
        """
        result = []
        done_signal = Event(search_cancellation_token)
        self.drive_count = 0

        def did_discover_object(obj):
            result.append(obj)
            self.drive_count += 1

        odrive.find_all(path, serial_number, did_discover_object, done_signal, channel_termination_token, logger)
        try:
            done_signal.wait(timeout=timeout)

        except TimeoutError:
            print("Timeouted")
        finally:
            done_signal.set()  # terminate find_all
        return result
