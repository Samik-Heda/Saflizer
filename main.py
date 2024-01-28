import json
import os
from threading import Thread

import customtkinter as ctk
import requests
from CTkMessagebox import CTkMessagebox
from PIL import Image

from account_manager import AccountManager
from widgets import (Menu, DriverList, EditDriverWindow, WebCamPopout, AddDriverWindow, DriverDetailsWindow, TimePicker,
                     TripSchedulerWindow)


class App(ctk.CTk):
    def __init__(self):
        # setup
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('800x600')
        self.title('Saflizer Software V1')
        self.minsize(800, 500)

        self.key = os.environ.get('KEY')

        with open('data/current_user.txt', 'r') as f:
            self.username = f.read()

        self.error_codes = {'401': 'Invalid Authentication',
                            '403': 'Username already exists',
                            '404': 'Username does not exist',
                            '409': 'Wrong password',
                            '200': 'Success'}

        self.driver_list = None

        self.account_manager = AccountManager(self, self.login, self.register_account)
        if not self.username:
            self.account_manager.open_start_page()
        else:
            self.open_home()
            self.check_alerts()

        self.mainloop()

    def check_alerts(self):
        alerts = json.loads(requests.post('https://saflizer.onrender.com/alerts',
                                          {'apikey': self.key, 'username': self.username}).text)['alerts']

        if alerts:
            for alert in alerts:
                name = json.loads(requests.post('https://saflizer.onrender.com/getdriverinfo',
                                                {'apikey': self.key, 'username': self.username,
                                                 'id': alert.split(':')[0]}).text)['name']
                if alert.split(':')[1] == 'Test not completed':
                    CTkMessagebox(self, title='Test not completed!',
                                  message=f'{name} has NOT completed his test before DEPARTURE!'
                                          f' ({alert.split(':')[1]})', icon='warning')

                CTkMessagebox(self, title='ALERT!', message=f'{name}\'s alcohol level is above the LEGAL LIMIT!'
                                                            f' ({alert.split(':')[1]})', icon='warning')

        alerts_thread = Thread(target=self.check_alerts)
        self.after(3000, alerts_thread.start)

    def refresh(self):
        if self.driver_list:
            self.driver_list.pack_forget()

        driver_ids = json.loads(requests.post('https://saflizer.onrender.com/getdrivers',
                                              {'apikey': self.key, 'username': self.username}).text)['ids']

        driver_info_dict = {}

        for driver_id in driver_ids:
            driver_info_dict[driver_id] = json.loads(requests.post('https://saflizer.onrender.com/getdriverinfo',
                                                                   {'apikey': self.key, 'username': self.username,
                                                                    'id': driver_id}).text)

        self.driver_list = DriverList(self, driver_info_dict, self.delete_driver, self.edit_driver,
                                      self.display_driver_info)

    def open_home(self):
        self.menu = Menu(self, self.show_account_options, self.open_trip_scheduler, self.username,
                         self.open_add_driver_window)
        self.refresh()

    def open_trip_scheduler(self):
        times = json.loads(requests.post('https://saflizer.onrender.com/gettimes',
                                         {'apikey': self.key, 'username': self.username}).text)['times']

        self.trip_scheduler = TripSchedulerWindow(self, self.open_time_picker, times, self.delete_trip)

    def open_time_picker(self):
        TimePicker(self, self.add_trip)

    def open_webcam(self):
        WebCamPopout(self)

    def open_add_driver_window(self):
        AddDriverWindow(self, self.open_webcam, self.add_driver)

    def show_account_options(self):
        self.account_options_window = ctk.CTkToplevel(self)
        self.account_options_window.resizable(width=False, height=False)
        logout_icon = ctk.CTkImage(Image.open("data/logout_icon.png"))
        ctk.CTkButton(master=self.account_options_window, text='Logout', image=logout_icon, compound='right',
                      command=self.logout).pack(padx=10, pady=10)
        edit_icon = ctk.CTkImage(Image.open("data/edit_icon.png"))
        ctk.CTkButton(master=self.account_options_window, text='Edit Options', image=edit_icon, compound='right').pack(
            padx=10, pady=10)

    def update_duty(self, duty, driver_id):
        requests.post('https://saflizer.onrender.com/duty',
                      {'apikey': self.key, 'username': self.username, 'duty': duty, 'id': driver_id})

    def add_trip(self, time):
        requests.post('https://saflizer.onrender.com/addtime',
                      {'apikey': self.key, 'username': self.username, 'time': time})

        times = json.loads(requests.post('https://saflizer.onrender.com/gettimes',
                                         {'apikey': self.key, 'username': self.username}).text)['times']

        self.trip_scheduler.refresh(times)

    def delete_trip(self, time):
        requests.post('https://saflizer.onrender.com/removetime',
                      {'apikey': self.key, 'username': self.username, 'time': time})

        times = json.loads(requests.post('https://saflizer.onrender.com/gettimes',
                                         {'apikey': self.key, 'username': self.username}).text)['times']

        self.trip_scheduler.refresh(times)

    def login(self, username, password, remember_me):
        result = requests.post('https://saflizer.onrender.com/login',
                               {'apikey': self.key, 'username': username, 'password': password}).text

        if result == '200':
            self.username = username
            self.account_manager.close()
            self.open_home()
            self.check_alerts()
            if remember_me:
                with open('data/current_user.txt', 'w') as f:
                    f.write(self.username)
        else:
            CTkMessagebox(title=f"Error {result}", message=self.error_codes[result], icon="cancel")

    def logout(self):
        self.account_options_window.destroy()
        self.menu.pack_forget()
        self.driver_list.pack_forget()
        self.account_manager.open_start_page()
        self.username = ''
        with open('data/current_user.txt', 'w') as f:
            f.write(self.username)

    def register_account(self, username, password, remember_me):
        result = requests.post('https://saflizer.onrender.com/signup',
                               {'apikey': self.key, 'username': username, 'password': password}).text

        if result == '200':
            self.username = username
            self.account_manager.close()
            self.open_home()
            self.check_alerts()
            CTkMessagebox(title=f"Congratulations", message='You have successfully created a supervisor account',
                          icon="check", option_1='Thanks')
            if remember_me:
                with open('data/current_user.txt', 'w') as f:
                    f.write(self.username)
        else:
            CTkMessagebox(title=f"Error {result}", message=self.error_codes[result], icon="cancel")

    def add_driver(self, name):
        files = {'image': open('data/image.png', 'rb')}
        result = requests.post('https://saflizer.onrender.com/adddriver',
                               {'apikey': self.key, 'username': self.username, 'name': name}, files=files).text

        if result == '200':
            CTkMessagebox(title=f"Success!", message=f'You have successfully added {name}.',
                          icon="check")
        else:
            CTkMessagebox(title=f"Error {result}", message=self.error_codes[result], icon="cancel")

        self.refresh()

    def delete_driver(self, driver_id):
        requests.post('https://saflizer.onrender.com/deletedriver',
                      {'apikey': self.key, 'username': self.username,
                       'id': driver_id})
        self.refresh()

    def save_details(self, name, driver_id, image_edited):
        if image_edited:
            files = {'image': open('data/image.png', 'rb')}
            requests.post('https://saflizer.onrender.com/editdriver',
                          {'apikey': self.key, 'username': self.username, 'name': name}, files=files)
        else:
            files = {'image': 'None'}
            requests.post('https://saflizer.onrender.com/editdriver',
                          {'apikey': self.key, 'username': self.username,
                           'id': driver_id, 'name': name}, files=files)

        self.refresh()

    def edit_driver(self, driver_id):
        driver_info = json.loads(requests.post('https://saflizer.onrender.com/getdriverinfo',
                                               {'apikey': self.key, 'username': self.username,
                                                'id': driver_id}).text)

        EditDriverWindow(self, driver_info, self.open_webcam, self.save_details, driver_id)

    def display_driver_info(self, driver_id):
        driver_info = json.loads(requests.post('https://saflizer.onrender.com/getdriverinfo',
                                               {'apikey': self.key, 'username': self.username,
                                                'id': driver_id}).text)

        DriverDetailsWindow(self, driver_info, driver_id, self.update_duty)


if __name__ == '__main__':
    App()
