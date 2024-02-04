from pyHoneygain import HoneyGain
from typing import Any
from time import gmtime, strftime
from threading import Lock

class Updater:
    def __init__(self, honeygain_user: HoneyGain):
        self._lock = Lock()
        self.honeygain_user = honeygain_user
        self.me = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.devices = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.stats = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.stats_today = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.stats_today_jt = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.notifications = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.payouts = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}
        self.balances = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def update_me(self) -> None:
        try:
            with self._lock:
                self.me = self.honeygain_user.me()
                self.me["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting me")
            with self._lock:
                self.me = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}


    def get_me(self) -> Any:
        with self._lock:
            return self.me


    def update_devices(self) -> None:
        try:
            with self._lock:
                self.devices = self.honeygain_user.devices()

                for id in range(len(self.devices)):
                    self.devices[id]["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting devices")
            with self._lock:
                self.devices = [{"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}]

    def get_devices(self) -> Any:
        with self._lock:
            return self.devices


    def update_stats(self) -> None:
        try:
            with self._lock:
                self.stats = self.honeygain_user.stats()
                self.stats["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting stats")
            with self._lock:
                self.stats = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def get_stats(self) -> Any:
        with self._lock:
            return self.stats


    def update_stats_today(self) -> None:
        try:
            with self._lock:
                self.stats_today = self.honeygain_user.stats_today()
                self.stats_today["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting stats today")
            with self._lock:
                self.stats_today = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def get_stats_today(self) -> Any:
        with self._lock:
            return self.stats_today


    def update_stats_today_jt(self) -> None:
        try:
            with self._lock:
                self.stats_today_jt = self.honeygain_user.stats_today_jt()
                self.stats_today_jt["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting stats today jt")
            with self._lock:
                self.stats_today_jt = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def get_stats_today_jt(self) -> Any:
        with self._lock:
            return self.stats_today_jt


    def update_notifications(self) -> None:
        try:
            with self._lock:
                self.notifications = self.honeygain_user.notifications()

                for id in range(len(self.notifications)):
                    self.notifications[id]["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting notifications")
            with self._lock:
                self.notifications = [{"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}]

    def get_notifications(self) -> Any:
        with self._lock:
            return self.notifications


    def update_payouts(self) -> None:
        try:
            with self._lock:
                self.payouts = self.honeygain_user.payouts()

                for id in range(len(self.payouts)):
                    self.payouts[id]["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting payouts")
            with self._lock:
                self.payouts = [{"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}]

    def get_payouts(self) -> Any:
        with self._lock:
            return self.payouts


    def update_balances(self) -> None:
        try:
            with self._lock:
                self.balances = self.honeygain_user.balances()
                self.balances["last_updated"] = strftime("%Y-%m-%d %H:%M:%S", gmtime())

        except:
            print("There was error while getting balances")
            with self._lock:
                self.balances = {"last_updated": strftime("%Y-%m-%d %H:%M:%S", gmtime())}

    def get_balances(self) -> Any:
        with self._lock:
            return self.balances


