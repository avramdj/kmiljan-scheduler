from datetime import date
import datetime as dt
import config
import time
import random as rd
import threading

from kmiljan_parser import download_courses, download_modules

class DataServer:
    def __init__(self):
        self.all_courses = []
        self.all_modules = {}
        self.last_update = None
        self.update_thread = threading.Thread(target = self.update_loop, args = {})
        self.update_thread.start()

    def get_courses(self):
        return self.all_courses

    def get_modules(self):
        return self.all_modules

    def update_loop(self):
        while True:
            self.update()
            next_update_time_at = 2*config.HOUR + config.DB_UPDATE_INTERVAL * rd.random()
            print("Sleeping. Next update at: " + str(dt.datetime.now() + dt.timedelta(seconds = next_update_time_at)))
            time.sleep(next_update_time_at)

    def update(self):
        print("Updating database...")
        self.all_courses = (
            download_courses()
        )  # pickle.load(open('pickles/courses.p', 'rb'))
        self.all_modules = download_modules(
            self.all_courses
        )  # pickle.load(open('pickles/modules.p', 'rb'))

        # MINI IZMENE
        if len(self.all_courses) == 0:
            return

        # pickle.dump(self.all_courses, open('pickles/courses.p', 'wb'))
        # pickle.dump(self.all_modules, open('pickles/modules.p', 'wb'))

        today = date.today().strftime("%b_%d_%Y")
        self.last_update = today
