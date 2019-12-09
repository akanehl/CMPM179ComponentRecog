import tkinter as tk

class Application(tk.Frame):
    def update(self, q):
        obj = q.get()
        self.counter = obj['counter']
        self.roll = obj['roll']
        self.label['text'] = 'Next capture in '+str(self.counter)+' seconds.'
        self.diceRolled['text'] = 'You rolled: '+str(self.roll)

    def __init__(self, master=None):
        super().__init__(master)
        self.roll = '-'
        self.counter = '2'
        self.master = master
        self.pack()
        self.create_widgets()
        #self.master.mainloop()


    def create_widgets(self):
        self.label = tk.Label(self, text='Next capture in '+str(self.counter)+' seconds.')
        self.label.pack()
        self.diceRolled = tk.Label(self, text='You rolled: '+str(self.roll))
        self.diceRolled.pack()

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()
