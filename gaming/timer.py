#!/usr/bin/env python

import threading




class Timer:
    """
    A simple timer that runs in a separated thread for avoid blocking.

    Timeout: Seconds before 'ring'

    Repeat: How many times the timer will be restarted.
            For a one-shot timer, set 0. -1 for an endless looping.

    OnElapsed: Function to call when timer 'rings'
    """
    def __init__(self, timeout: float, repeat: int, on_elapsed) -> None:
        self._timeout = timeout
        self._func = on_elapsed
        self._running = False
        self._thread = None
        self._repeat = repeat
        self._loops = 0


    def reset (self) -> None:
        """
        Resets the current loops
        """
        self._loops = 0


    def running (self) -> bool:
        """
        Returns if the timer is running
        """
        return self._running


    def start (self) -> None:
        """
        Starts the timer thread
        """
        if not self._running:
            self._running = True
            t = threading.Thread (target=self.__timer_thread)
            t.start ()


    def stop (self) -> None:
        """
        Stops a running timer
        """
        if self._running:
            self._running = False


    def __timer_thread (self) -> None:
        while self._running:
            self._thread = threading.Timer (self._timeout, self._func)
            self._thread.start ()
            self._thread.join ()

            if (self._repeat >= 1):
                if (self._loops < self._repeat):
                    self._loops += 1
                else:
                    self.stop ()
                    break
