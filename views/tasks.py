import ttkbootstrap as tb
import requests as req
from json import dumps
from K import *
from views.helper import View


class TaskButtons(tb.Frame):

    def __init__(self, master, app):
        super().__init__(master)
        self.pack(expand=TRUE, anchor=SE)


        create_button = tb.Button(self, text="Create Task", command=app.show_create_task_view, bootstyle=SUCCESS)
        create_button.pack(anchor=NE,
                           pady=(20, 0),
                           padx=(0, 25),
                           side=LEFT
                           )

        delete_button = tb.Button(self, text="Delete Task", command=app.show_create_task_view, bootstyle=DANGER)
        delete_button.pack(anchor=NE,
                           pady=(20, 0),
                           padx=(25, 0),
                           side=LEFT
                           )

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

        self.status_bool = tb.BooleanVar
        self.status_bool = task.get("complete")

        index_label = tb.Label(self, text=f"#{task_index+1}", bootstyle=PRIMARY, font=PS, anchor=N)
        name_label = tb.Label(self, text=task.get("title"), border=5, bootstyle=PRIMARY, font=PS)

        self.status = "✅" if task.get("complete") else "❎"
        self.label_color = SUCCESS if self.status == "✅" else DANGER

        self.status_label = tb.Label(self, text=self.status, bootstyle=self.label_color, font=PS)

        # detail_button = tb.Button(self, text="To task detail", command=app.show_task_view, bootstyle=PRIMARY)
        detail_button = tb.Button(self, text="Toggle Completion", command=self.toggle_completion, bootstyle=PRIMARY)



        index_label.pack(side=LEFT, padx=(0, 25), pady=5, anchor=NW)
        name_label.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        self.status_label.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        detail_button.pack(side=LEFT, padx=(25, 0), pady=5, anchor=NW)
        # _text = f"#{index + 1} Task Name: {task.get('name')} Priority: ✅ {task.get('priority')} Status: {status}"
        # task = tb.Label(self, text=label_text, padding=(50, 0), font=PS, bootstyle=(PRIMARY, INVERSE),
        #                     borderwidth=10)
        # task.pack(pady=5)

    def toggle_completion(self):
        self.status_bool = not self.status_bool
        print(self.status_bool)
        self.status = "✅" if self.status_bool else "❎"
        self.label_color = SUCCESS if self.status == "✅" else DANGER


        self.status_label.configure(text=self.status, bootstyle=self.label_color)



class TasksView(View):
    def __init__(self, app):
        super().__init__(app)

        self.all_tasks = []

        # self.create_widgets()



    def create_widgets(self):
        # Add code to display a list of tasks here
        # self.get_tasks()
        print(self.all_tasks)


        show_all_tasks = AllTasks(self.frame)

        for index, task in enumerate(self.all_tasks):
            TaskForList(self.frame, app=self.app, task=task, task_index=index)

        task_buttons = TaskButtons(self.frame, app=self.app)



        #
        # create_button = tb.Button(self.frame, text="Create Task", command=self.app.show_create_task_view, bootstyle=SUCCESS)
        # create_button.pack(anchor=NE,
        #                    pady=(20,0)
        #                    )
        #
        # edit_button = tb.Button(self.frame, text="Edit Task", command=self.app.show_create_task_view, bootstyle=(SUCCESS, OUTLINE))
        # edit_button.pack(anchor=NE,
        #                  pady=(20, 0)
        #                  )
        #
        # delete_button = tb.Button(self.frame, text="Delete Task", command=self.app.show_create_task_view, bootstyle=DANGER)
        # delete_button.pack(anchor=NE,
        #                    pady=(20, 0)
        #                    )


class TaskView(View):
    def __init__(self, app):
        super().__init__(app)

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
        self.task_status = tb.BooleanVar(value=self.task.get("complete"))

        self.create_widgets()

    def create_widgets(self):
        manager_label = tb.Label(self.frame, text="Task Manager", font=H6, )
        return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.app.show_tasks_view)
        # return_button = tb.Button(self.frame, text="Back to View Tasks", command=self.submit_changes)

        name_label = tb.Label(self.frame, text="Task Name:")
        name_value = tb.Label(self.frame, textvariable=self.task_name, font=H6, bootstyle=PRIMARY)
        description_label = tb.Label(self.frame, text="Task Description:")
        description_value = tb.Label(self.frame, textvariable=self.task_description, font=H6, bootstyle=PRIMARY)
        priority_label = tb.Label(self.frame, text="Task Priority:")
        priority_value = tb.Label(self.frame, textvariable=self.task_priority, font=H6, bootstyle=PRIMARY)

        done_toggle = tb.Checkbutton(self.frame, style="Roundtoggle.Toolbutton", text="Completion Status", variable=self.task_status, onvalue=self.task_status, offvalue=self.task_status)


        # submit_button = tb.Button(self.frame, text="Submit", bootstyle=SUCCESS)

        return_button.pack(anchor=NW)
        manager_label.pack(padx=10, pady=50)

        name_label.pack(anchor="w")
        name_value.pack(pady=(0, 30), fill=X)

        description_label.pack(anchor="w")
        description_value.pack(pady=(0, 30), fill=X)

        priority_label.pack(anchor="w")
        priority_value.pack(pady=(0, 30), fill=X)

        done_toggle.pack()

        # submit_button.pack(anchor="se", expand=True)


    def submit_changes(self, ):
        print(self.task.get("complete"))

    def toggle_checkbutton(self):
        # Toggle the state of the Checkbutton
        self.task["complete"] = self.task_status.get()
        self.task_status.set(not self.task_status.get())
        print("yo")

class CreateTaskView(View):
    def __init__(self, app):
        super().__init__(app)
        self.task_name_var = tb.StringVar()
        self.task_description_var = tb.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tb.Label(self.frame, text="Task Name:").pack()
        tb.Entry(self.frame, textvariable=self.task_name_var).pack()
        tb.Label(self.frame, text="Description:").pack()
        tb.Entry(self.frame, textvariable=self.task_description_var).pack()

        tb.Button(self.frame, text="Create Task", command=self.create_task).pack()
        tb.Button(self.frame, text="Back", command=self.app.show_task_view).pack()

    def create_task(self):
        # Add your code to create a task here
        task_name = self.task_name_var.get()
        task_description = self.task_description_var.get()

        self.create_toast("Task Created", f"Task '{task_name}' created successfully")

        # After creating the task, show the task page
        self.app.show_task_view()
