import tkinter as tk
from tkinter import messagebox
import requests
import threading

API_URL = "http://127.0.0.1:5000/api/v1"
TOKEN = None


class APIClient:
    def __init__(self):
        self.token = None

    def set_token(self, token):
        self.token = token

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def login(self, username, password):
        r = requests.post(
            f"{API_URL}/auth/login",
            json={"username": username, "password": password}
        )
        return r

    def register(self, username, password):
        return requests.post(
            f"{API_URL}/auth/register",
            json={"username": username, "password": password}
        )

    def get_products(self):
        return requests.get(
            f"{API_URL}/products",
            headers=self.headers()
        )


api = APIClient()


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("API Client | Tkinter")
        self.geometry("500x450")
        self.resizable(False, False)
        self.show_login()

    def clear(self):
        for w in self.winfo_children():
            w.destroy()

    # ================= LOGIN =================
    def show_login(self):
        self.clear()

        tk.Label(self, text="🔐 LOGIN", font=("Arial", 18, "bold")).pack(pady=15)

        self.username = tk.Entry(self)
        self.username.pack(pady=5)
        self.username.insert(0, "username")

        self.password = tk.Entry(self, show="*")
        self.password.pack(pady=5)
        self.password.insert(0, "password")

        tk.Button(self, text="Login", width=20, command=self.login).pack(pady=10)
        tk.Button(self, text="Register", width=20, command=self.show_register).pack()

    def login(self):
        def task():
            r = api.login(self.username.get(), self.password.get())
            if r.status_code == 200:
                token = r.json()['access_token']
                api.set_token(token)
                self.show_products()
            else:
                messagebox.showerror("Xato", "Login yoki parol noto‘g‘ri")

        threading.Thread(target=task).start()

    # ================= REGISTER =================
    def show_register(self):
        self.clear()

        tk.Label(self, text="📝 REGISTER", font=("Arial", 18, "bold")).pack(pady=15)

        self.r_user = tk.Entry(self)
        self.r_user.pack(pady=5)
        self.r_user.insert(0, "username")

        self.r_pass = tk.Entry(self, show="*")
        self.r_pass.pack(pady=5)
        self.r_pass.insert(0, "Password123")

        tk.Button(self, text="Register", width=20, command=self.register).pack(pady=10)
        tk.Button(self, text="Back", width=20, command=self.show_login).pack()

    def register(self):
        def task():
            r = api.register(self.r_user.get(), self.r_pass.get())
            if r.status_code == 201:
                messagebox.showinfo("OK", "Ro‘yxatdan o‘tildi")
                self.show_login()
            else:
                messagebox.showerror("Xato", r.json().get("message", "Xatolik"))

        threading.Thread(target=task).start()

    # ================= PRODUCTS =================
    def show_products(self):
        self.clear()

        tk.Label(self, text="📦 MAHSULOTLAR", font=("Arial", 16, "bold")).pack(pady=10)

        self.listbox = tk.Listbox(self, width=50, height=15)
        self.listbox.pack(pady=10)

        tk.Button(self, text="🔄 Yangilash", command=self.load_products).pack()
        tk.Button(self, text="🚪 Logout", command=self.show_login).pack(pady=5)

        self.load_products()

    def load_products(self):
        def task():
            self.listbox.delete(0, tk.END)
            r = api.get_products()
            if r.status_code == 200:
                for p in r.json()['items']:
                    self.listbox.insert(
                        tk.END, f"{p['name']} — ${p['price']}"
                    )
            else:
                messagebox.showerror("Xato", "Token eskirgan")

        threading.Thread(target=task).start()


if __name__ == "__main__":
    App().mainloop()
