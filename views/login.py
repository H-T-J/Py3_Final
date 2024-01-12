import ttkbootstrap as tb
import requests as req
from K import *
from views.helper import View



class LoginView(View):
    def __init__(self, app):
        super().__init__(app)
        self.email_var = tb.StringVar()
        self.password_var = tb.StringVar()
        self.create_widgets()

        self.url = self.app.url

    def create_widgets(self):
        email_label = tb.Label(self.frame, text="Email:")
        email_label.pack(anchor="w")

        email_entry = tb.Entry(self.frame, textvariable=self.email_var)
        email_entry.pack(pady=(0, 20), fill=X)

        pass_label = tb.Label(self.frame, text="Password:")
        pass_label.pack(anchor="w")

        pass_entry = tb.Entry(self.frame, textvariable=self.password_var, show="*")
        pass_entry.pack(pady=(0, 20), fill=X)

        login_button = tb.Button(self.frame, text="Login", command=self.login, bootstyle=SUCCESS)
        login_button.pack(expand=True, fill=X, anchor=S, pady=100)


    def login(self):
        # Your authentication would need to be implemented here
        email = self.email_var.get()
        password = self.password_var.get()

        response = req.post(f"{self.url}/token",
                            data={"username": email,
                            "password": password}
                            ).json()

        if response.get("access_token"):
            self.app.authenticated = TRUE
            self.app.token = {"access_token": response.get("access_token"), "token_type": "bearer"}
            print(self.app.token)
            self.app.email = email
            self.password_var.set("")
            self.app.show_tasks_view()

            self.app.views.get("view_tasks").all_tasks = req.get(f"{self.app.url}/tasks?auth={self.app.token['access_token']}",
                                                                 headers={"Authorization": f"Bearer {self.app.token['access_token']}",
                                                                 "Content-Type": "application/json"}).json()
            print(self.app.views.get("view_tasks").all_tasks)
        else:
            self.create_toast("401 Error", "Bad Credentials")




