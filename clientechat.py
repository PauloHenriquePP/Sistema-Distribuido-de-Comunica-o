from tkinter import *
from socket import *
import _thread

def initialize_client():
    s = socket(AF_INET, SOCK_STREAM)
    host = 'localhost'
    port = 1234
    s.connect((host, port))
    print("Cliente conectado ao servidor!")
    return s

# update chat window
def update_chat(msg, state):
    global chatlog

    chatlog.config(state=NORMAL)

    if state == 0:  # YOU
        chatlog.insert(END, f"\nVocê: {msg}", "Você")
    else:           # OTHER
        chatlog.insert(END, f"\nServidor: {msg}", "Outro")

    chatlog.config(state=DISABLED)
    chatlog.yview(END)

# send message
def send():
    global textbox
    msg = textbox.get("1.0", END).strip()
    textbox.delete("1.0", END)

    if msg:
        update_chat(msg, 0)
        s.send(msg.encode("ascii"))

def receive():
    while True:
        try:
            data = s.recv(1024)
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
    gui.title("Cliente (Azul)")
    gui.geometry("400x460")
    gui.configure(bg="#DCEBFF")  

    # CHAT LOG 
    chatlog = Text(gui, bg="white", font=("Segoe UI", 10), wrap=WORD)
    chatlog.config(state=DISABLED)

    # estilo para mensagens
    chatlog.tag_config("you", background="#B8D4FF", foreground="black")
    chatlog.tag_config("other", background="#E3E3E3", foreground="black")

    # TEXTO PARA DIGITAR
    textbox = Text(gui, bg="white", height=2, font=("Segoe UI", 10))

    # BOTÃO DE ENVIO
    sendbutton = Button(gui, text="Enviar", bg="#4A90E2", fg="white",
                        font=("Segoe UI", 10, "bold"), command=send)

    # POSICIONAMENTO
    chatlog.place(x=10, y=10, width=380, height=380)
    textbox.place(x=10, y=400, width=290, height=40)
    sendbutton.place(x=310, y=400, width=80, height=40)

    textbox.bind("<Return>", press)

    _thread.start_new_thread(receive, ())

    gui.mainloop()


if __name__ == "__main__":
    chatlog = textbox = None
    s = initialize_client()
    GUI()
