import ttkbootstrap as tb
import requests as req
from K import *
from views import login, tasks


class TaskApp(tb.Window):
    def __init__(self):
        super().__init__(themename="sandstone")
        self.title("Task Manager")
        self.geometry("854x640")

        # User variables
        self.authenticated = False
        self.email = tb.StringVar()
        self.token: dict = {}

        self.url = "http://192.168.50.220:8000"

        self.tasks = []

        # Views variables
        self.current_view = None
        self.header_frame = None
        self.views = {
            "login": login.LoginView(self),
            "view_tasks": tasks.TasksView(self),
            "view_task": tasks.TaskView(self),
            "create_task": tasks.CreateTaskView(self)
        }


        # Init Welcome Screen
        self.create_header()
        self.show_login_view()
        # self.show_tasks_view()
        # self.show_task_view()

    # def get_tasks(self):
    #     self.tasks = req.get(f"{self.url}/tasks?auth={self.token['access_token']}",
    #                         headers={"Authorization": f"Bearer {self.token['access_token']}",
    #                         "Content-Type": "application/json"}).json()
    #
    #     return self.tasks
    def create_header(self):
        self.header_frame = tb.Frame(self, bootstyle=PRIMARY)

        logout_button = tb.Button(self.header_frame, text="Logout", command=self.logout, bootstyle=SECONDARY)
        logout_button.pack(side=RIGHT, padx=PS, pady=PXS)

    def show_header(self):
        self.header_frame.pack(fill=X)

    def hide_header(self):
        self.header_frame.pack_forget()

    def logout(self):
        self.authenticated = False
        self.show_login_view()

    def show_login_view(self):
        self.set_current_view("login")


    def show_task_view(self):
        self.set_current_view("view_task")

    def show_tasks_view(self):
        self.set_current_view("view_tasks")


    def show_create_task_view(self):
        self.set_current_view("create_task")


    def set_current_view(self, key):
        self.destroy_current_view()
        self.current_view = key
        if self.authenticated:
            self.show_header()
        else:
            self.hide_header()
        self.views.get(key).pack_view()

    def destroy_current_view(self):
        if self.current_view:
            self.views.get(self.current_view).unpack_view()


if __name__ == "__main__":
    app = TaskApp()
    app.place_window_center()
    app.mainloop()
