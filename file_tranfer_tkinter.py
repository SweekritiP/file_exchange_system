import tkinter as tk
from tkinter import filedialog, messagebox, Label, Entry, Button, Toplevel
import socket
import threading
import os

# Dictionary to store usernames and passwords
user_credentials = {}
connections = {}  # to store connected users and their status

class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        border = tk.LabelFrame(
            self, text='Login', bg='ivory', bd=10, font=("Arial", 20))
        border.pack(fill="both", expand="yes", padx=150, pady=150)

        Label1 = tk.Label(border, text="Username",
                          font=("Arial Bold", 15), bg='ivory')
        Label1.place(x=50, y=20)
        self.Txt1 = tk.Entry(border, width=30, bd=5)
        self.Txt1.place(x=180, y=20)

        Label2 = tk.Label(border, text="Password",
                          font=("Arial Bold", 15), bg='ivory')
        Label2.place(x=50, y=80)
        self.TXT2 = tk.Entry(border, width=30, show='*', bd=5)
        self.TXT2.place(x=180, y=80)

        def verify():
            try:
                with open("credential.txt", "r") as f:
                    info = f.readlines()
                    i = 0
                    for e in info:
                        u, p = e.split(",")
                        if u.strip() == self.Txt1.get() and p.strip() == self.TXT2.get():
                            user_credentials['username'] = self.Txt1.get().strip()
                            connections[user_credentials['username']] = 'available'
                            controller.show_frame(SecondPage)
                            i = 1
                            break
                    if i == 0:
                        messagebox.showinfo(
                            "Error", "Please provide correct username and password!!")
            except:
                messagebox.showinfo(
                    "Error", "Please provide correct username and password!!")

        BTN1 = tk.Button(border, text="Submit",
                         font=("Arial", 15), command=verify)
        BTN1.place(x=320, y=115)

        def register():
            window = tk.Toplevel(controller)
            window.resizable(0, 0)
            window.configure(bg="deep sky blue")
            window.title("Register")
            Label1 = tk.Label(window, text="Username:", font=(
                "Arial", 15), bg="deep sky blue")
            Label1.place(x=10, y=10)
            txt1 = tk.Entry(window, width=30, bd=5)
            txt1.place(x=200, y=10)

            lbl2 = tk.Label(window, text="Password:", font=(
                "Arial", 15), bg="deep sky blue")
            lbl2.place(x=10, y=60)
            txt2 = tk.Entry(window, width=30, show="*", bd=5)
            txt2.place(x=200, y=60)

            lbl3 = tk.Label(window, text="Confirm Password:",
                            font=("Arial", 15), bg="deep sky blue")
            lbl3.place(x=10, y=110)
            txt3 = tk.Entry(window, width=30, show="*", bd=5)
            txt3.place(x=200, y=110)

            def check():
                if txt1.get() != "" or txt2.get() != "" or txt3.get() != "":
                    if txt2.get() == txt3.get():
                        with open("credential.txt", "a") as f:
                            f.write(txt1.get()+","+txt2.get()+"\n")
                            messagebox.showinfo(
                                "Welcome", "You are registered successfully!!")
                        window.destroy()
                    else:
                        messagebox.showinfo(
                            "Error", "Your password didn't get match!!")
                else:
                    messagebox.showinfo(
                        "Error", "Please fill the complete field!!")

            btn1 = tk.Button(window, text="Sign in", font=(
                "Arial", 15), bg="#ffc22a", command=check)
            btn1.place(x=170, y=150)

            window.geometry("470x220")

        BTN2 = tk.Button(self, text="Register", bg="dark orange",
                         font=("Arial", 15), command=register)
        BTN2.place(x=650, y=20)


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.user_status = tk.StringVar()
        self.user_status.set("Status: Disconnected")

        self.user_size_limit = tk.StringVar()
        self.user_size_limit.set("Size limit: Not set")

        Button1 = tk.Button(self, text="Send Files", font=(
            "Arial", 15), command=self.send_files)
        Button1.place(x=300, y=100)

        Button2 = tk.Button(self, text="Receive Files", font=(
            "Arial", 15), command=self.receive_files)
        Button2.place(x=300, y=200)

        Button3 = tk.Button(self, text="Back", font=(
            "Arial", 15), command=self.disconnect)
        Button3.place(x=300, y=300)

        status_label = tk.Label(self, textvariable=self.user_status,
                                font=("Arial", 15), bg='ivory')
        status_label.place(x=300, y=400)

        size_label = tk.Label(self, textvariable=self.user_size_limit,
                              font=("Arial", 15), bg='ivory')
        size_label.place(x=300, y=450)

    def send_files(self):
        Send(self.controller, self.user_status)

    def receive_files(self):
        Receive(self.controller)

    def disconnect(self):
        connections[user_credentials['username']] = 'unavailable'
        self.user_status.set("Status: Disconnected")
        self.user_size_limit.set("Size limit: Not set")
        self.controller.show_frame(FirstPage)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # creating a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=500)
        window.grid_columnconfigure(0, minsize=800)

        self.frames = {}
        for F in (FirstPage, SecondPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("Application")


def Send(controller, user_status):
    window = tk.Toplevel(controller)
    window.title("Send")
    window.geometry("450x560+500+200")
    window.configure(bg="white")
    window.resizable(False, False)

    receiver_info_label = Label(window, text="No receiver connected", bg='white', fg='red')
    receiver_info_label.place(x=20, y=250)

    disconnected_label = Label(window, text="", bg='white', fg='red')
    disconnected_label.place(x=20, y=320)

    filename = None
    s = None  # Initialize socket variable

    def select_file():
        nonlocal filename
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select File',
            filetypes=(('Text Files', '*.txt'),
                       ('Image Files', '*.png;*.jpg;*.jpeg'),
                       ('Word Files', '*.docx;*.doc'),
                       ('PDF Files', '*.pdf'),
                       ('All Files', '*.*'))
        )
        if filename:
            print(f"File selected: {filename}")
        else:
            print("No file selected")

    def start_server():
        nonlocal s
        nonlocal filename
        def handle_client(conn, addr):
            receiver_info_label.config(text=f"Connected to {addr}")
            try:
                 while True:
                      if filename:
                            with open(filename, 'rb') as file:
                              file_data = file.read(1024)
                              while file_data:
                                conn.send(file_data)
                                file_data = file.read(1024)
                            print("Data has been transmitted successfully")
                            conn.close()
                            break
                      else:
                           pass
            except Exception as e:
                print(f"An error occurred in handle_client: {e}")
            finally:
                conn.close()
        
        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        try:
            s.bind((host, port))
            s.listen(1)
            print(f"Listening on {host}:{port}...")

            conn, addr = s.accept()
            receiver_info_label.config(text=f"Connected to {addr}")
            select_file_button.config(state='normal')
            threading.Thread(target=handle_client, args=(conn, addr)).start()
        except Exception as e:
             print(f"An error occurred in start_server: {e}")
        finally:
             s.close()

    def disconnect_from_receiver():
        nonlocal s
        try:
            s.close()
            disconnected_label.config(text="User has been disconnected successfully")
            user_status.set("Status: Disconnected")
        except:
            disconnected_label.config(text="No connection to disconnect")

    threading.Thread(target=start_server, daemon=True).start()

    sender_id = socket.gethostname()
    Label(window, text=f'Sender ID (Hostname): {sender_id}', bg='white', fg='black').place(x=20, y=290)
    select_file_button = Button(window, text="+ Select File", width=12, height=1, font='Arial 14 bold', bg="#fff", fg="#000", state='disabled', command=select_file)
    select_file_button.place(x=120, y=150)
    send_button = Button(window, text="Send", width=8, height=1, font='Arial 14 bold', bg="#fff", fg="#000", command=lambda: threading.Thread(target=start_server, daemon=True).start())
    send_button.place(x=300, y=150)
    disconnect_button = Button(window, text="Disconnect", font=('arial', 14, 'bold'), bg='white', fg='black', command=disconnect_from_receiver)
    disconnect_button.place(x=300, y=200)


def Receive(controller):
    window = Toplevel(controller)
    window.title("Receive")
    window.geometry("450x560+500+200")
    window.configure(bg="white")
    window.resizable(False, False)

    connected = False

    def connect_to_sender():
        nonlocal connected
        try:
            ID = SenderID.get()
            size_limit = int(size_limit_entry.get()) * 1024  # convert to bytes
            s = socket.socket()
            port = 8080
            s.connect((ID, port))
            connected = True
            messagebox.showinfo("Connected", f"Connected to sender: {ID}")

            receiver_ip = socket.gethostbyname(socket.gethostname())
            with open("receiver_ip.txt", "w") as file:
                file.write(receiver_ip)
            SenderID.config(state='disabled')
            connect_button.config(state='disabled')
            receive_button.config(state='normal')

        except Exception as e:
            print(f"An error occurred: {e}")

    def disconnect_from_sender():
        nonlocal connected
        connected = False
        SenderID.config(state='normal')
        connect_button.config(state='normal')
        receive_button.config(state='disabled')
        messagebox.showinfo("Disconnected", "User has been disconnected successfully")

    def receiver():
        nonlocal connected
        if connected:
            try:
                ID = SenderID.get()
                filename1 = filedialog.asksaveasfilename(
                    initialdir=os.getcwd(),
                    title='Save File As',
                    filetypes=(('All Files', '*.*'),)
                )
                if not filename1:
                    messagebox.showerror("Error", "No file path specified!")
                    return

                size_limit = int(size_limit_entry.get()) * 1024  # convert to bytes

                s = socket.socket()
                port = 8080
                s.connect((ID, port))

                file_size = 0
                with open(filename1, 'wb') as file:
                    file_data = s.recv(1024)
                    while file_data:
                        file_size += len(file_data)
                        if file_size > size_limit:
                            messagebox.showerror("Error", "File is too large to receive!")
                            file.close()
                            os.remove(filename1)
                            break
                        file.write(file_data)
                        file_data = s.recv(1024)

                if file_size <= size_limit:
                    print("File has been received successfully")

            except Exception as e:
                print(f"An error occurred: {e}")
            finally:
                s.close()

    Label(window, text="Receive", font=('arial', 20), bg='white').place(x=160, y=10)
    Label(window, text="Input sender ID (Hostname or IP):", font=('arial', 10, 'bold'), bg='white').place(x=20, y=60)
    SenderID = Entry(window, width=25, fg="black", border=2, bg='white', font=("arial", 15))
    SenderID.place(x=20, y=90)
    SenderID.focus()
    Label(window, text="Max file size (KB):", font=('arial', 10, 'bold'), bg='white').place(x=20, y=130)
    size_limit_entry = Entry(window, width=25, fg="black", border=2, bg='white', font=("arial", 15))
    size_limit_entry.place(x=20, y=160)
    connect_button = Button(window, text="Connect", font=('arial', 14, 'bold'), bg='white', fg='black', command=connect_to_sender)
    connect_button.place(x=20, y=200)
    receive_button = Button(window, text="Receive", font=('arial', 14, 'bold'), bg='white', fg='black', command=receiver, state='disabled')
    receive_button.place(x=20, y=240)
    disconnect_button = Button(window, text="Disconnect", font=('arial', 14, 'bold'), bg='white', fg='black', command=disconnect_from_sender)
    disconnect_button.place(x=20, y=280)


if __name__ == "__main__":
    app = Application()
    app.mainloop()
