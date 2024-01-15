import ttkbootstrap as tb
from ttkbootstrap.toast import ToastNotification

import requests as req
from json import dumps
from K import *
from views.helper import View


class TaskButtons(tb.Frame):

    def __init__(self, master, app):
        super().__init__(master)
        self.pack(expand=TRUE, anchor=SE)


        create_button = tb.Button(self, text="Create Task", command=app.show_create_task_view, bootstyle=SUCCESS)
        create_button.pack(anchor=E,
                           pady=(20, 0),
                           padx=(0, 25),
                           side=RIGHT
                           )

        # delete_button = tb.Button(self, text="Delete Task", command=app.show_create_task_view, bootstyle=DANGER)
        # delete_button.pack(anchor=NE,
        #                    pady=(20, 0),
        #                    padx=(25, 0),
        #                    side=LEFT
        #                    )

        # detail_button = tb.Button(self, text="To task detail", command=self.master.show_task_view, bootstyle=PRIMARY)
        # detail_button.pack(anchor=NE
        #                    )


class AllTasks(tb.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=X, anchor=NW)

        all_tasks_label = tb.Label(self, text="Your Tasks:", font=H6)
        all_tasks_label.pack(anchor=W)

class TaskForList(tb.Frame):

    def __init__(self, master, app, task, task_index):
        super().__init__(master)
        self.pack(fill=BOTH, padx=100, pady=25, side=TOP, anchor=N)

        self.app = app
        self.task = task

        self.status_bool = tb.BooleanVar
        self.status_bool = self.task.get("complete")

        self.index_label = tb.Label(self, text=f"#{task_index+1}", bootstyle=PRIMARY, font=PS, anchor=N, width=5)

        self.name_button = tb.Button(self, text=self.task.get("title"), command=self.get_current_task, bootstyle=(PRIMARY, LINK), width=20)

        self.status = "✅" if self.task.get("complete") else "❎"
        self.label_color = SUCCESS if self.status_bool else DANGER

        self.status_label = tb.Label(self, text=self.status, bootstyle=self.label_color, font=PS, width=5)

        # detail_button = tb.Button(self, text="To task detail", command=app.show_task_view, bootstyle=PRIMARY)
        self.detail_button = tb.Button(self, text="Toggle Completion", command=self.toggle_completion, bootstyle=PRIMARY)

        self.delete_button = tb.Button(self, text="Delete", command=self.delete_task, bootstyle=DANGER)



        self.index_label.pack(side=LEFT, padx=(0, 25), pady=5, anchor=NW)
        self.name_button.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        self.status_label.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        self.detail_button.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        self.delete_button.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        # _text = f"#{index + 1} Task Name: {task.get('name')} Priority: ✅ {task.get('priority')} Status: {status}"
        # task = tb.Label(self, text=label_text, padding=(50, 0), font=PS, bootstyle=(PRIMARY, INVERSE),
        #                     borderwidth=10)
        # task.pack(pady=5)

    def get_current_task(self):
        print(self.task["id"])
        response = req.get(url=f"{self.app.url}/tasks/{self.task['id']}",
                           headers={"Authorization": f"Bearer {self.app.token['access_token']}",
                                    "Content-Type": "application/json"})
        if response.status_code == 200:
            self.app.current_task = response.json()

            print(self.app.current_task)

            self.app.views.get("view_task").task_name.set(self.app.current_task.get("title"))
            self.app.views.get("view_task").task_description.set(self.app.current_task.get("description"))
            self.app.views.get("view_task").task_priority.set(self.app.current_task.get("priority"))

            print(self.app.current_task.get("complete"))
            if self.app.current_task.get("complete"):
                self.app.views.get("view_task").task_status_text.set("Complete")
            else:
                self.app.views.get("view_task").task_status_text.set("Not Complete")


            self.app.show_task_view()
        else:
            self.create_toast(f"{response} Error", "Could Not Get Task Details")


        # self.app.current_task = self.task.get("id")
        # print(self.app.current_task)
        # self.app.views("view_task").task = self.app.get_task()
        # print("jnxwkj")
        # print(self.app.views("view_task").task)
        # self.app.show_task_view()

    def return_task_id(self):
        task_id = self.task["id"]
        print(task_id)
        return int(task_id)

    @staticmethod
    def create_toast(title, detail):
        toast = ToastNotification(
            title=title,
            message=detail,
            duration=3000,
        )
        toast.show_toast()


    def delete_task(self):
        try:
            response = self.app.delete_task(task_id=int(self.task.get("id")))

            if response == 204:
                self.app.views.get("view_tasks").all_tasks.remove(self.task)

                self.index_label.destroy()
                self.name_button.destroy()
                self.status_label.destroy()
                self.detail_button.destroy()
                self.delete_button.destroy()

            else:
                self.create_toast(f"{response} Error", "Could Not Delete Task")

        except:
            self.create_toast(f"Connection Error", "Could Not Connect To Server")

    def toggle_completion(self):
        try:
            response = self.app.toggle_database_complete(task_id=int(self.task.get("id")),
                                                         task_complete=not bool(self.task.get("complete")),
                                                         task_description=str(self.task.get("description")),
                                                         task_title=str(self.task.get("title")),
                                                         task_priority=int(self.task.get("priority"))
                                                         )
            print(response)

            if response == 204:
                self.status_bool = not self.status_bool
                self.status = "✅" if self.status_bool else "❎"
                self.label_color = SUCCESS if self.status_bool else DANGER

                self.status_label.configure(text=self.status, bootstyle=self.label_color)

            else:
                self.create_toast(f"{response} Error", "Could Not Update Status")
        except:
            self.create_toast("Connection Error", "Could Not Connect To Server")


# tryna make the button also update the task through the database

class TasksView(View):
    def __init__(self, app):
        super().__init__(app)

        self.all_tasks = []
        self.all_tasks_widgets = []

        # self.create_widgets()



    def create_widgets(self):
        # Add code to display a list of tasks here
        # self.get_tasks()
        print(self.all_tasks)

        self.make_tasks()

    def make_tasks(self):
        if self.all_tasks:
            self.show_all_tasks = AllTasks(self.frame)

            if self.all_tasks_widgets:
                self.show_all_tasks.destroy()
                self.task_buttons.destroy()
                for frame in self.all_tasks_widgets:
                    frame.destroy()
                print("test")

            for index, task in enumerate(self.all_tasks):
                task_widgets = TaskForList(self.frame, app=self.app, task=task, task_index=index)
                self.all_tasks_widgets.append(task_widgets)
                print(self.all_tasks_widgets)

            self.task_buttons = TaskButtons(self.frame, app=self.app)

        return self.all_tasks_widgets



class TaskView(View):
    def __init__(self, app, current_task):
        super().__init__(app)

    def create_widgets(self):
        # self.task = self.app.views("view_tasks").task

        # print(f"-------------\n"
        #       f"{self.task}")
        self.task = {
                "id": 1,
                "name": "Calculus HW",
                "description": "eifnlkjwqndbnwlqjbdlj",
                "priority": 3,
                "done": True
            }



        self.task_name = tb.StringVar(value=self.task.get("name"))
        self.task_description = tb.StringVar(value=self.task.get("description"))
        self.task_priority = tb.StringVar(value=self.task.get("priority"))

        self.task_status_text = tb.StringVar(value="")


        manager_label = tb.Label(self.frame, text="Task Manager", font=H6, )
        return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.app.show_tasks_view)
        # return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.submit_changes)

        name_label = tb.Label(self.frame, text="Task Name:")
        name_value = tb.Label(self.frame, textvariable=self.task_name, font=H6, bootstyle=PRIMARY)

        description_label = tb.Label(self.frame, text="Task Description:")
        description_value = tb.Label(self.frame, textvariable=self.task_description, font=H6, bootstyle=PRIMARY)

        priority_label = tb.Label(self.frame, text="Task Priority:")
        priority_value = tb.Label(self.frame, textvariable=self.task_priority, font=H6, bootstyle=PRIMARY)

        status_label = tb.Label(self.frame, text="Task Status:")
        status_value = tb.Label(self.frame, textvariable=self.task_status_text, font=H6, bootstyle=PRIMARY)



        submit_button = tb.Button(self.frame, text="Submit", bootstyle=SUCCESS)

        return_button.pack(anchor=NW)
        manager_label.pack(padx=10)

        name_label.pack(anchor="w")
        name_value.pack(pady=(0, 30), fill=X)

        description_label.pack(anchor="w")
        description_value.pack(pady=(0, 30), fill=X)

        priority_label.pack(anchor="w")
        priority_value.pack(pady=(0, 30), fill=X)

        status_label.pack(anchor="w")
        status_value.pack(pady=(0, 30), fill=X)

        submit_button.pack(anchor="se", expand=True)




class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.task_title_var = tb.StringVar()
        self.task_description_var = tb.StringVar()
        self.task_priority_var = tb.StringVar
        self.create_widgets()


    def create_widgets(self):
        manager_label = tb.Label(self.frame, text="Task Creator", font=H6, )
        return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.app.show_tasks_view)
        # return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.submit_changes)

        name_label = tb.Label(self.frame, text="Task Name: (22 characters or less)")
        self.name_value = tb.Entry(self.frame, textvariable=self.task_title_var, font=H6, bootstyle=PRIMARY)
        description_label = tb.Label(self.frame, text="Task Description:")
        self.description_value = tb.Entry(self.frame, textvariable=self.task_description_var, font=H6, bootstyle=PRIMARY)
        # priority_label = tb.Label(self.frame, text="Task Priority:")
        # self.priority_value = tb.Entry(self.frame, font=H6, bootstyle=PRIMARY)
        self.priority_meter = tb.Meter(self.frame, metersize=180, padding=5, amounttotal=5, metertype="semi", subtext="Task Priority", interactive=True, stripethickness=55)
        # self.priority_meter = tb.Meter(self.frame)


        submit_button = tb.Button(self.frame, text="Submit",command=self.create_task, bootstyle=SUCCESS)

        return_button.pack(anchor=NW)
        manager_label.pack(padx=10)

        name_label.pack(anchor="w")
        self.name_value.pack(pady=(0, 30), fill=X)

        description_label.pack(anchor="w")
        self.description_value.pack(pady=(0, 30), fill=X)

        # priority_label.pack(anchor="w")
        self.priority_meter.pack(pady=(0, 30), fill=X)

        submit_button.pack(side=RIGHT, anchor=S, expand=True)

    def create_task(self):
        # Add your code to create a task here
        task_title = self.task_title_var.get()
        task_description = self.task_description_var.get()
        task_priority = self.priority_meter.amountusedvar.get()

        try:
            response = self.app.create_task(task_title=task_title,
                                            task_description=task_description,
                                            task_priority=task_priority
                                            )
            print(response)
            print(self.priority_meter.amountusedvar.get())

            if response == 201:
                self.app.views.get("view_tasks").all_tasks = req.get(f"{self.app.url}/tasks",
                                                                     headers={
                                                                         "Authorization": f"Bearer {self.app.token['access_token']}",
                                                                         "Content-Type": "application/json"}).json()
                # new_task_view = TasksView(app=self.app)
                self.app.show_tasks_view()
                # print(new_task_view.tasks)

                #Honestly dont know how to get this to work, want it to add task to view_tasks in the same instance of the app it was made in... :(
                # self.app.views("view_tasks").make_tasks(self.frame)

                self.create_toast("Task Created", f"Task '{task_title}' created successfully")
                # After creating the task, show the task page

            else:
                self.create_toast(f"{response} Error", "Could Not Create Task")
                print(task_title)
                print(task_description)
                print(task_priority)
        except:
            self.create_toast("Connection Error", "Could Not Connect To Server")
