import time


class Stopwatch:
    def __init__(self, auto_start=False, interval_print=False, reset_timer_on_interval_print=False):
        self.start_at = 0
        self.stop_at = 0
        self.interval_print = interval_print
        self.prefix = 'DONE at '
        self.reset_timer_on_interval_print = reset_timer_on_interval_print

        if auto_start:
            self.start()

    def start(self):
        self.start_at = time.time()
        self.stop_at = 0

    def stop(self):
        self.stop_at = time.time()

    def sec(self):
        return round((self.stop_at - self.start_at), 2)

    def __interval_sec(self):
        return round((time.time() - self.start_at), 2)

    @staticmethod
    def print_seconds_nice(seconds, prefix=''):
        if seconds < 60:
            return '{}{}s'.format(prefix, seconds)

        minutes = seconds // 60
        seconds -= minutes * 60

        if minutes < 60:
            seconds = round(seconds, 2)
            return '{}{}m {}s'.format(prefix, minutes, seconds)

        hours = minutes // 60
        minutes -= hours * 60

        if hours < 24:
            minutes = int(minutes)
            seconds = round(seconds, 2)
            return '{}{}h {}m {}s'.format(prefix, hours, minutes, seconds)

        days = hours // 24
        hours -= days * 24

        seconds = round(seconds, 2)
        return '{}{}d {}h {}m {}s'.format(prefix, days, hours, minutes, seconds)

    def __str__(self):
        if self.interval_print:
            seconds = round(self.__interval_sec(), 2)
            if self.reset_timer_on_interval_print:
                self.start()
        else:
            seconds = round(self.sec(), 2)

        return Stopwatch.print_seconds_nice(seconds)
