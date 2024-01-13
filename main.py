import ttkbootstrap as tb
import requests as req
from json import dumps


import views.tasks
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
    def create_task(self, task_title, task_description, task_priority):
        data = {
            "complete": False,
            "description": str(task_description),
            "priority": int(task_priority),
            "title": str(task_title)
        }

        response = req.post(url=f"{self.url}/tasks",
                            headers={"Authorization": f"Bearer {self.token['access_token']}", "Content-Type": "application/json"},
                            data=dumps(data))
        return response.status_code

    def delete_task(self, task_id):

        response = req.delete(url=f"{self.url}/tasks/{task_id}",
                              headers={"Authorization": f"Bearer {self.token['access_token']}", "Content-Type": "application/json"}
                              )

        return response.status_code


    def toggle_database_complete(self, task_id, task_complete, task_description, task_title, task_priority):
        response = req.put(url=f"{self.url}/tasks/{task_id}",
                           headers={"Authorization": f"Bearer {self.token['access_token']}", "Content-Type": "application/json"},
                           data=dumps({
                               "complete": task_complete,
                               "description": task_description,
                               "title": task_title,
                               "priority": task_priority
                           })
                           )
        print(response)
        return response.status_code


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
