from tkinter import *
import tkinter
# from chat import get_response, bot_name
import pyaudio
import threading
import time
from PIL import Image
import emoji
from emoji import emojize

BG_GRAY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COLOR = "#EAECEE"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

def reset_tabstop(event):
    event.widget.configure(tabs=(event.width-30, "right"))

class ChatApplication(threading.Thread):
    
    def __init__(self):
        # threading.Thread.__init__(self)
        # self.start()
        self.window = Tk()
        self.logfile = ""
        self.currentline = 0

        self._setup_main_window()
        
    def run(self):

        self.window.mainloop()
        
    def _setup_main_window(self, chunk=3024, frmat=pyaudio.paInt16, channels=1, rate=44100, py=pyaudio.PyAudio()):
        self.window.title("Demo For Voice Email")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=600, height=1100, bg=BG_COLOR)


        # self.backimg = tkinter.PhotoImage(file="img.png")
        # self.backlabel = Label(self.window, image=self.backimg)
        # self.backlabel.image=self.backimg
        # self.backlabel.pack()

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.p = py
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Welcome to VoiEmail!", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        

        # self.canvas = Canvas(self.window, width=400, height=550)
        # self.canvas.pack()


        # tiny divider
        line = Label(self.window, width=450, bg=BG_GRAY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR, padx=5, pady=5, font=("Helvetica", 24, "bold"))

            
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        self.text_widget.bind("<Configure>", reset_tabstop)
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        

        self.backlabel = Label(self.window, bg=BG_GRAY, height=80)
        self.backlabel.place(relwidth=1, rely=0.825)
        
        # message entry box

        
        # # send button
        send_button = Button(self.backlabel, text="Record", font=FONT_BOLD, width=20, bg=BG_GRAY)
        
        # send_button.place(relx=0.38, rely=0.8, relheight=0.06, relwidth=0.22)
        send_button.place(relx=0.38, rely=0.008, relheight=0.06, relwidth=0.22)


     

        
    def _insert_message(self, msg, sender):
        if not msg:
            return
        self.msg_entry.delete(0, END)
        
        msg1 = f"          \t {sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        # self.text_widget.tag_config("justified", justify=CENTER)
        self.text_widget.insert(END, msg1, "justified")
        self.text_widget.configure(state=DISABLED)
        
        # msg2 = f"{bot_name}: {get_response(msg)}\n\n"
        msg2 = "Got command reply!\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg2)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
    

    def insertMsg(self):
        with open('../log.txt') as fp:
            lines = fp.readlines()
            length = len(lines)
            
            if length > 0 and self.currentline < length:
                print('self current line', self.currentline)
                

                line = lines[self.currentline]
                msg = "🤖️" +":" + line + "\n\n"

                if len(line)> 5 and line[0:5] == "User:":
                    str_ = emojize(":boy:")
                    msg = "\t" +  line[5:len(line)-1] +":"+ str_ +"\n\n"  
                    self.text_widget.configure(state=NORMAL)
                    self.text_widget.insert(END, msg)
                    self.text_widget.configure(state=DISABLED)
                    self.currentline += 1
                elif len(line) > 4 and line[0:4] == "SHOW":
                    print(line)
                    msg = line[4:]
                    self.text_widget.configure(state=NORMAL)
                    self.text_widget.insert(END, msg)
                    self.text_widget.configure(state=DISABLED)
                    self.currentline += 1
                    for i in range(self.currentline, length):
                        msg = lines[i]
                        if (self.currentline== length -1):
                            msg = "🤖️" +":" + msg + "\n\n"
                        self.text_widget.configure(state=NORMAL)
                        self.text_widget.insert(END, msg)
                        self.text_widget.configure(state=DISABLED)
                        self.currentline+= 1
                    
                else:
                    self.text_widget.configure(state=NORMAL)
                    self.text_widget.insert(END, msg)
                    self.text_widget.configure(state=DISABLED)
                    self.currentline += 1
        
        self.window.after(1000,self.insertMsg)
        
if __name__ == "__main__":
    open('../log.txt','w')
    app = ChatApplication()
    app.insertMsg()
    app.run()

    # print()
    # print(type(emojize(":thumbs_up:")))