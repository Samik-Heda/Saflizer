import customtkinter as ctk

from settings import *


class AccountManager:
    def __init__(self, parent, login, register):
        self.parent = parent

        self.login = login
        self.register = register
        self.current_page = StartPage(self.parent, self.open_login_page, self.open_register_page)

    def open_login_page(self):
        self.current_page.pack_forget()
        self.current_page = LoginPage(self.parent, self.open_start_page, self.login)

    def open_register_page(self):
        self.current_page.pack_forget()
        self.current_page = RegisterPage(self.parent, self.open_start_page, self.register)

    def open_start_page(self):
        self.current_page.pack_forget()
        self.current_page = StartPage(self.parent, self.open_login_page, self.open_register_page)

    def close(self):
        self.current_page.pack_forget()


class StartPage(ctk.CTkFrame):
    def __init__(self, parent, open_login_page, open_register_page):
        super().__init__(master=parent)

        ctk.CTkButton(self, text='Login', command=open_login_page).pack(padx=10, pady=10)
        ctk.CTkButton(self, text='Register', command=open_register_page).pack(padx=10, pady=10)

        self.pack(expand=True)


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, close, login):
        super().__init__(master=parent)

        ctk.CTkButton(self, text='x', command=close, text_color=WHITE, fg_color='transparent', width=30, height=30,
                      corner_radius=0, hover_color=CLOSE_RED).pack(anchor='ne')

        username_entry = ctk.CTkEntry(self, placeholder_text='Username')
        username_entry.pack(padx=10, pady=10)

        password_entry = ctk.CTkEntry(self, placeholder_text='Password', show='*')
        password_entry.pack(padx=10, pady=10)

        remember_me_checkbox = ctk.CTkCheckBox(self, text='Remember Me?')
        remember_me_checkbox.pack(padx=10, pady=10)

        ctk.CTkButton(self, text='Login', command=lambda: login(username_entry.get(), password_entry.get(),
                                                                  remember_me_checkbox.get())).pack(padx=10, pady=10)

        self.pack(expand=True)


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, close, register):
        super().__init__(master=parent)

        ctk.CTkButton(self, text='x', command=close, text_color=WHITE, fg_color='transparent', width=30, height=30,
                      corner_radius=0, hover_color=CLOSE_RED).pack(anchor='ne')

        username_entry = ctk.CTkEntry(self, placeholder_text='Username')
        username_entry.pack(padx=10, pady=10)

        password_entry = ctk.CTkEntry(self, placeholder_text='Password', show='*')
        password_entry.pack(padx=10, pady=10)

        remember_me_checkbox = ctk.CTkCheckBox(self, text='Remember Me?')
        remember_me_checkbox.pack(padx=10, pady=10)

        ctk.CTkButton(self, text='Register', command=lambda: register(username_entry.get(), password_entry.get(),
                                                                   remember_me_checkbox.get())).pack(padx=10, pady=10)

        self.pack(expand=True)
