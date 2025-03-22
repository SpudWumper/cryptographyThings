from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk

algorithmNames = ["Caesar", "Substitution", "Vigenere", "Hill", "El Gammal", "RSA"]

#create a class thats just a wrapper for all my algorithms?

#class for the main window for gui?
class cryptographyUI:
    def __init__(self, w: int, h:int):
        self.window = tk.Tk()
        self.window.title("Cryptography Algorithms")
        
        sizeFrame = tk.Frame(width = w, height = h)
        sizeFrame.pack()
        top = tk.Frame(master=sizeFrame, height=h/2)
        top.pack(fill=tk.X)


        inTextFrame = tk.Frame(master=top, width=w/2, height=h/2)
        outTextFrame = tk.Frame(master=top, width=w/2, height=h/2)
        inTextFrame.pack(side=tk.LEFT)
        outTextFrame.pack(side=tk.RIGHT)

        inTextBox = tk.Text(master=inTextFrame)
        inTextBox.insert("1.0", "Enter the string you want to encrypt...")
        outTextBox = tk.Text(master=outTextFrame)
        outTextBox.insert("1.0", "...Encrypted string shows up here")
        inTextBox.place(relwidth=1,relheight=1)
        outTextBox.place(relwidth=1,relheight=1)

        algFrame = tk.Frame(master=sizeFrame,width=w, height=h/2)
        #algFrame.pack_propagate(False)
        algFrame.pack(side=tk.BOTTOM)

        for buttonNames in algorithmNames:
            button = tk.Button(
                master=algFrame,
                text=buttonNames,
                width=10,
                height=5,
                relief="raised"
            )
            button.pack(side=tk.LEFT)
        
        

    def enterMain(self):
        self.window.mainloop()

if __name__ == "__main__":
    gui = cryptographyUI(800,600)
    gui.enterMain()