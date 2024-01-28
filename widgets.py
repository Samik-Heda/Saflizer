from tkinter import Label

import customtkinter as ctk
from tkinter.ttk import Separator
import cv2
from PIL import Image, ImageTk

from settings import *


class Menu(ctk.CTkFrame):
    def __init__(self, parent, show_account_options, add_trip, username, add_driver):
        super().__init__(master=parent)

        img = Image.open("data/add_driver_icon.png")
        ctk_img = ctk.CTkImage(img)

        self.add_button = ctk.CTkButton(master=self, text='Add Driver', image=ctk_img, command=add_driver)
        self.add_button.pack(side='left', padx=10, pady=10)

        img = Image.open("data/clock_icon.png")
        ctk_img = ctk.CTkImage(img)

        self.schedule_button = ctk.CTkButton(master=self, text='Schedule Trips', image=ctk_img, command=add_trip)
        self.schedule_button.pack(side='left', padx=10, pady=10)

        img = Image.open("data/account_icon.png")
        ctk_img = ctk.CTkImage(img)

        self.account_button = ctk.CTkButton(master=self, text=username, image=ctk_img, compound='right',
                                            command=show_account_options)
        self.account_button.pack(side='right', padx=10, pady=10)

        self.pack(fill='x', padx=20, pady=20)


class DriverList(ctk.CTkScrollableFrame):
    def __init__(self, parent, driver_info, delete_user, edit_user, display_driver_info):
        super().__init__(master=parent)

        self.search_var = ctk.StringVar()
        self.search_bar = ctk.CTkEntry(self, placeholder_text='Search', textvariable=self.search_var)
        self.search_bar.pack(fill='x', padx=5, pady=5)

        self.driver_info = driver_info
        self.delete_driver = delete_user
        self.edit_driver = edit_user
        self.display_driver = display_driver_info
        self.driver_displays = []

        self.display_drivers()

        self.search_var.trace("w", self.display_drivers)

        self.pack(fill='both', expand=True, padx=20, pady=20, ipadx=20, ipady=20)

    def display_drivers(self, *args):
        for driver_display in self.driver_displays:
            driver_display.pack_forget()

        self.driver_displays = []

        for id, info in self.driver_info.items():
            if self.search_bar.get() in info['name']:
                self.driver_displays.append(
                    DriverDisplay(self, info['name'], id, self.delete_driver, self.edit_driver, self.display_driver))


class DriverDisplay(ctk.CTkFrame):
    def __init__(self, parent, name, id, delete, edit, display_driver_info):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=3)

        self.name_label = ctk.CTkLabel(self, text=name)
        self.name_label.pack(side='left', padx=10, pady=10)

        img = Image.open("data/trash_icon.png")
        ctk_img = ctk.CTkImage(img)

        self.delete_button = ctk.CTkButton(self,
                                           text='',
                                           image=ctk_img,
                                           command=lambda: delete(id),
                                           text_color=WHITE,
                                           fg_color='transparent',
                                           width=40,
                                           height=40,
                                           corner_radius=0,
                                           hover_color=CLOSE_RED)

        self.delete_button.pack(side='right')

        edit_icon = Image.open("data/edit_icon.png")
        ctk_edit_icon = ctk.CTkImage(edit_icon)

        self.edit_button = ctk.CTkButton(self,
                                         text='',
                                         image=ctk_edit_icon,
                                         command=lambda: edit(id),
                                         text_color=WHITE,
                                         fg_color='transparent',
                                         width=40,
                                         height=40,
                                         corner_radius=0,
                                         hover_color=EDIT_GREEN)

        self.bind('<Enter>', self.hovered)
        self.bind('<Leave>', self.unhovered)
        self.bind('<Button-1>', lambda _: display_driver_info(id))

        self.edit_button.pack(side='right')

        self.pack(fill='x', padx=5, pady=5)

    def hovered(self, *args):
        self.configure(fg_color=DARK_BLUE)

    def unhovered(self, *args):
        self.configure(fg_color=DARK_GREY)


class DriverDetailsWindow(ctk.CTkToplevel):
    def __init__(self, parent, info, id, update_duty):
        super().__init__(master=parent)
        self.minsize(width=300, height=350)
        self.title('Driver Details')

        font = ctk.CTkFont(size=36, weight='bold')

        ctk.CTkLabel(self, text=info['name'], font=font).pack(padx=20, pady=20)

        Separator(self, orient='horizontal').pack(fill='x', padx=20, pady=10)

        self.duty_var = ctk.BooleanVar(self, info['duty'])
        self.duty_switch = ctk.CTkSwitch(self, text='On-Duty', switch_width=48, switch_height=24, variable=self.duty_var)
        self.duty_switch.pack(padx=10, pady=10, anchor='nw')

        self.duty_var.trace('w', lambda _: update_duty(self.duty_var.get(), id))

        self.indiscretions_frame = ctk.CTkFrame(self, fg_color='transparent')

        sub_heading_font = ctk.CTkFont(size=24, weight='bold')
        ctk.CTkLabel(self.indiscretions_frame, text='Past Indiscretions', font=sub_heading_font).pack(side='top')

        self.indiscretions_log = ctk.CTkFrame(self.indiscretions_frame, fg_color=DARK_GREY)
        for indiscretion in info['test']:
            ctk.CTkLabel(self.indiscretions_log, text=indiscretion).pack()

        self.indiscretions_log.pack(fill='both', expand=True, side='bottom')

        self.indiscretions_frame.pack(fill='both', expand=True, padx=20, pady=10, side='bottom')


class AddDriverWindow(ctk.CTkToplevel):
    def __init__(self, parent, take_scan, add_driver):
        super().__init__(master=parent)
        self.title('Add Driver')

        self.add_driver = add_driver
        self.take_scan = take_scan
        self.image_added = False

        self.name_frame = ctk.CTkFrame(self, fg_color='transparent')
        ctk.CTkLabel(self.name_frame, text='Name: ').pack(side='left')
        self.name_entry = ctk.CTkEntry(self.name_frame, placeholder_text='')
        self.name_entry.pack(side='right')
        self.name_frame.pack(padx=20, pady=20)

        self.add_picture = ctk.CTkButton(self, text='Add Picture', command=take_scan)
        self.add_picture.pack(padx=20, pady=10)

        self.exit_options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.okay_button = ctk.CTkButton(self.exit_options_frame, text='Okay',
                                         command=lambda: add_driver(self.name_entry.get()))
        self.okay_button.pack(side='left', padx=5)
        self.cancel_button = ctk.CTkButton(self.exit_options_frame, text='Cancel', command=lambda: self.destroy())
        self.cancel_button.pack(side='right', padx=5)
        self.exit_options_frame.pack(padx=20, pady=20)

    def popoutwebcam(self):
        self.image_added = True
        self.take_scan()

    def confirm_details(self):
        if self.image_added:
            self.add_driver(self.name_entry.get())
            self.destroy()


class EditDriverWindow(ctk.CTkToplevel):
    def __init__(self, parent, info, take_scan, edit_details, id):
        super().__init__(master=parent)
        self.title('Edit Driver')

        self.edit_details = edit_details
        self.id = id

        self.name_frame = ctk.CTkFrame(self, fg_color='transparent')
        ctk.CTkLabel(self.name_frame, text='Name: ').pack(side='left')
        self.name_entry = ctk.CTkEntry(self.name_frame, placeholder_text=info['name'])
        self.name_entry.pack(side='right')
        self.name_frame.pack(padx=20, pady=20)

        self.image_edited = False
        self.take_scan = take_scan

        self.change_picture_button = ctk.CTkButton(self, text='Change Picture', command=self.popoutwebcam)
        self.change_picture_button.pack(padx=20, pady=10)

        self.exit_options_frame = ctk.CTkFrame(self, fg_color='transparent')
        self.okay_button = ctk.CTkButton(self.exit_options_frame, text='Okay', command=self.confirm_details)
        self.okay_button.pack(side='left', padx=5)
        self.cancel_button = ctk.CTkButton(self.exit_options_frame, text='Cancel', command=lambda: self.destroy())
        self.cancel_button.pack(side='right', padx=5)
        self.exit_options_frame.pack(padx=20, pady=20)

    def popoutwebcam(self):
        self.image_edited = True
        self.take_scan()

    def confirm_details(self):
        self.edit_details(self.name_entry.get(), self.id, self.image_edited)
        self.destroy()


class WebCamPopout(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.title('Webcam')

        self.vid = cv2.VideoCapture(0)

        # Declare the width and height in variables
        width, height = 600, 400

        # Set the width and height
        self.vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        self.label_widget = Label(self)
        self.label_widget.pack()
        self.open_camera()

        self.scan_button = ctk.CTkButton(self, text='Scan', command=self.scan)
        self.scan_button.place(rely=0.9, relx=0.4)

    def open_camera(self):
        # Capture the video frame by frame
        _, self.frame = self.vid.read()

        # Convert image from one color space to other
        opencv_image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGBA)

        # Capture the latest frame and transform to image
        captured_image = Image.fromarray(opencv_image)

        # Convert captured image to photoimage
        photo_image = ImageTk.PhotoImage(image=captured_image)

        # Displaying photoimage in the label
        self.label_widget.photo_image = photo_image

        # Configure image in the label
        self.label_widget.configure(image=photo_image)

        # Repeat the same process after every 10 seconds
        self.label_widget.after(10, self.open_camera)

    def scan(self):
        cv2.imwrite('data/image.png', self.frame)
        self.destroy()


class TimePicker(ctk.CTkToplevel):
    def __init__(self, parent, add_trip):
        super().__init__(master=parent)
        self.geometry('150x115')
        self.resizable(width=False, height=False)

        self.add_trip = add_trip

        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=2, uniform='a')
        self.columnconfigure(2, weight=1, uniform='a')

        font = ctk.CTkFont(size=28, weight='bold')
        self.time_var = ctk.StringVar(self, '00:00')
        self.time_label = ctk.CTkLabel(self, textvariable=self.time_var, font=font)
        self.time_label.grid(row=0, rowspan=2, column=1)

        hour_up_button = ctk.CTkButton(self, text='+', command=lambda: self.adjust_time('+', 'hr'), width=30, height=30)
        hour_up_button.grid(row=0, column=0)
        hour_down_button = ctk.CTkButton(self, text='-', command=lambda: self.adjust_time('-', 'hr'), width=30,
                                         height=30)
        hour_down_button.grid(row=1, column=0)
        min_up_button = ctk.CTkButton(self, text='+', command=lambda: self.adjust_time('+', 'min'), width=30, height=30)
        min_up_button.grid(row=0, column=2)
        min_down_button = ctk.CTkButton(self, text='-', command=lambda: self.adjust_time('-', 'min'), width=30,
                                        height=30)
        min_down_button.grid(row=1, column=2)

        confirm_button = ctk.CTkButton(self, text='Confirm', command=self.confirm_time)
        confirm_button.grid(column=0, columnspan=3, row=3)

    def adjust_time(self, value, unit):
        if unit == 'hr':
            if value == '+':
                updated_value = int(self.time_var.get().split(':')[0]) + 1
            else:
                updated_value = int(self.time_var.get().split(':')[0]) - 1

            if updated_value > 24:
                updated_value = 00
            elif updated_value < 0:
                updated_value = 24

            if updated_value < 10:
                updated_value = '0' + str(updated_value)

            self.time_var.set(f'{updated_value}:{self.time_var.get().split(':')[1]}')
        else:
            if value == '+':
                updated_value = int(self.time_var.get().split(':')[1]) + 1
            else:
                updated_value = int(self.time_var.get().split(':')[1]) - 1

            if updated_value > 60:
                updated_value = 00
            elif updated_value < 0:
                updated_value = 60

            if updated_value < 10:
                updated_value = '0' + str(updated_value)

            self.time_var.set(f'{self.time_var.get().split(':')[0]}:{updated_value}')

    def confirm_time(self):
        self.add_trip(self.time_var.get())
        self.destroy()


class ScheduledTrip(ctk.CTkFrame):
    def __init__(self, parent, time, delete_trip):
        super().__init__(master=parent, fg_color=DARK_GREY, corner_radius=3)

        self.time_label = ctk.CTkLabel(self, text=time)
        self.time_label.pack(side='left', padx=10, pady=10)

        img = Image.open("data/trash_icon.png")
        ctk_img = ctk.CTkImage(img)

        self.delete_button = ctk.CTkButton(self,
                                           text='',
                                           image=ctk_img,
                                           command=lambda: delete_trip(time),
                                           text_color=WHITE,
                                           fg_color='transparent',
                                           width=30,
                                           height=30,
                                           corner_radius=0,
                                           hover_color=CLOSE_RED)

        self.delete_button.pack(side='right', padx=10, pady=10)

        self.pack(fill='x', padx=5, pady=5)

        self.bind('<Enter>', lambda _: self.configure(fg_color=DARK_BLUE))
        self.bind('<Leave>', lambda _: self.configure(fg_color=DARK_GREY))


class TripSchedulerWindow(ctk.CTkToplevel):
    def __init__(self, parent, open_time_picker, times, delete_time):
        super().__init__(master=parent)
        self.title('Trip Scheduler')
        self.geometry('300x250')

        self.scheduled_trips = []
        self.add_trip_button = None

        self.delete_time = delete_time
        self.open_time_picker = open_time_picker

        self.refresh(times)

    def refresh(self, times):
        for scheduled_trip in self.scheduled_trips:
            scheduled_trip.pack_forget()

        self.scheduled_trips = []

        for time in times:
            self.scheduled_trips.append(ScheduledTrip(self, time, self.delete_time))

        if self.add_trip_button:
            self.add_trip_button.pack_forget()

        self.add_trip_button = ctk.CTkButton(self, text='Add Trip', command=self.open_time_picker)
        self.add_trip_button.pack(padx=10, pady=10)

