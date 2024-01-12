import ttkbootstrap as tb
from ttkbootstrap.toast import ToastNotification
from K import *


class View:
    def __init__(self, app):
        self.app = app
        self.frame = tb.Frame(app)

    def pack_view(self):
        self.frame.pack(expand=TRUE, fill=BOTH, padx=50, pady=50)

    def unpack_view(self):
        self.frame.pack_forget()

    @staticmethod
    def create_toast(title, detail):
        toast = ToastNotification(
            title=title,
            message=detail,
            duration=3000,
        )
        toast.show_toast()
