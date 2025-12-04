from tkinter import *
from socket import *
import _thread

def initialize_server():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 1234

    s.bind((host, port))
    s.listen(1)

    print("Servidor aguardando conexão...")
    conn, addr = s.accept()
    print("Cliente conectado:", addr)

    return conn

def update_chat(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)

    if state == 0:  
        chatlog.insert(END, f"\nVocê: {msg}", "Você")
    else:           
        chatlog.insert(END, f"\nCliente: {msg}", "Outro")

    chatlog.config(state=DISABLED)
    chatlog.yview(END)

def send():
    global textbox
    msg = textbox.get("1.0", END).strip()
    textbox.delete("1.0", END)

    if msg:
        update_chat(msg, 0)
        conn.send(msg.encode("ascii"))

def receive():
    while True:
        try:
            data = conn.recv(1024)
            msg = data.decode("ascii")
            if msg:
                update_chat(msg, 1)
        except:
            pass

def press(event):
    send()

def GUI():
    global chatlog
    global textbox

    gui = Tk()
    gui.title("Servidor (Cinza)")
    gui.geometry("400x460")
    gui.configure(bg="#E8E8E8") 

    chatlog = Text(gui, bg="white", font=("Segoe UI", 10), wrap=WORD)
    chatlog.config(state=DISABLED)

    textbox = Text(gui, bg="white", height=2, font=("Segoe UI", 10))

    sendbutton = Button(gui, text="Enviar", bg="#5A5A5A", fg="white",
                        font=("Segoe UI", 10, "bold"), command=send)

    chatlog.place(x=10, y=10, width=380, height=380)
    textbox.place(x=10, y=400, width=290, height=40)
    sendbutton.place(x=310, y=400, width=80, height=40)

    textbox.bind("<Return>", press)

    _thread.start_new_thread(receive, ())

    gui.mainloop()


if __name__ == "__main__":
    chatlog = textbox = None
    conn = initialize_server()
    GUI()
