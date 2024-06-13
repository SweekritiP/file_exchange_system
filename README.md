# file_exchange_system
![image](https://github.com/SweekritiP/file_exchange_system/assets/168674913/9a103797-bdb3-4c91-8420-e215e97ec10d)
![image](https://github.com/SweekritiP/file_exchange_system/assets/168674913/038998c1-bd5d-4ea2-a800-a77a37b5b366)
![image](https://github.com/SweekritiP/file_exchange_system/assets/168674913/82b6e7a2-5b97-4e27-824e-7abcae896eb1)
![image](https://github.com/SweekritiP/file_exchange_system/assets/168674913/634db236-82ef-4f9a-b6a5-7dec0fc6128f)




tkinter: Used for creating GUI applications.
socket: Used for network connections.
threading: Used to run tasks in parallel.
os: Used for file system operations.

FirstPage Class
Handles the login and registration functionality.
parent: The parent widget.
controller: The main application controller.



GUI Components
LabelFrame: A bordered frame with a title, used to group widgets.
Label: Displays text.
Entry: Allows user input.
verify: Reads credentials from a file and checks if the provided username and password match.

Register Function
register: Opens a new window for user registration.
check: Validates the registration form and writes new credentials to a file.


SecondPage Class
Handles file transfer operations.

Constructor (init)
SecondPage: Creates buttons for sending and receiving files, and labels to display status.
send_files: Opens the send file window.
receive_files: Opens the receive file window.
disconnect: Changes the user status to 'unavailable' and returns to the login screen.

Application Class
Main application controller.

Constructor (init)
Application: Initializes the main window and handles frame switching.

Send Function
Handles sending files to a receiver.

GUI Components
Toplevel: Creates a new window for sending files.
Labels: Display connection status.
Select File Function
select_file: Opens a file dialog to select a file to send.

Start Server Function
start_server: Starts a server to listen for incoming connections and handles file transfer.


Receive Function
Handles receiving files from a sender.

GUI Components
Receive Function
Handles receiving files from a sender.

GUI Components
start_client: Connects to the server and receives the file.
Main Function
main: Starts the application.
This annotated guide provides a detailed understanding of how each part of the code works, allowing you to understand the logic and functionality implemented for login, registration, and file transfer.
