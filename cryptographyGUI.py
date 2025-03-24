from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)

import tkinter as tk

import encryptionAlgorithms as enc

algorithmNames = ["Caesar", "Substitution", "Hill", "Railfence" , "Autokey", "El Gammal", "RSA"]

#create a class thats just a wrapper for all my algorithms?
class encryptAlgs:
    def __init__(self):
        self.currentlySelected = ""

    def caesar(self, plaintext: str, n: int, doFormat: bool):
        return enc.caesenc(plaintext, n, doFormat)
    
    def subkey(self, plaintext: str, key: str):
        return enc.subenckey(plaintext, key)
    
    def hill(self, plaintext: str, key: str):
        return enc.hillEnc(plaintext, key)
    
    def autokey(self, plaintext: str, key: str):
        return enc.autokey(plaintext, key)
    
    def rail(self, plaintext: str, keyL: int):
        return enc.railfence(plaintext, keyL)
    
    # def elG(self, plaintext: str, n: int, doFormat: bool):
    #     return enc.caesenc(plaintext, n, doFormat)
    
    # def rsa(self, plaintext: str, n: int, doFormat: bool):
    #     return enc.caesenc(plaintext, n, doFormat)

#class for the main window for gui?
class cryptographyUI:
    def __init__(self, w: int, h:int):
        self.encryptionAlgorithms = encryptAlgs()

        self.window = tk.Tk()
        self.window.title("Cryptography Algorithms")
        self.window.resizable(False,False)

        self.buttons = []
        
        sizeFrame = tk.Frame(width = w, height = h)
        sizeFrame.pack()
        top = tk.Frame(master=sizeFrame, height=h/2)
        top.pack(fill=tk.X)


        inTextFrame = tk.Frame(master=top, width=w/2, height=h/2)
        outTextFrame = tk.Frame(master=top, width=w/2, height=h/2)
        inTextFrame.pack(side=tk.LEFT)
        outTextFrame.pack(side=tk.RIGHT)

        self.inTextBox = tk.Text(master=inTextFrame)
        self.inTextBox.insert("1.0", "Enter the string you want to encrypt...")
        self.outTextBox = tk.Text(master=outTextFrame)
        self.outTextBox.insert("1.0", "...Encrypted string shows up here")
        self.inTextBox.place(relwidth=1,relheight=1)
        self.outTextBox.place(relwidth=1,relheight=1)

        self.algOptFrame = tk.Frame(master=sizeFrame, width=w)
        self.algOptFrame.pack(side=tk.BOTTOM)
        self.errCheck = False

        algFrame = tk.Frame(master=sizeFrame,width=w, height=h/6)
        #algFrame.pack_propagate(False)
        algFrame.pack(side=tk.BOTTOM)

        for buttonNames in algorithmNames:
            button = tk.Button(
                master=algFrame,
                text=buttonNames,
                width=10,
                height=2,
                relief="raised"
            )
            button.grid(row=0, column=algorithmNames.index(buttonNames), padx=10, pady=10)
            self.buttons.append(button)

    def encrypt(self, event):
        parentName = event.widget.winfo_parent()
        parent = event.widget._nametowidget(parentName)

        plain = self.inTextBox.get(1.0, tk.END)

        match self.encryptionAlgorithms.currentlySelected:
            case "Caesar":
                n = 0
                for widget in parent.winfo_children():
                    if widget.winfo_class() == "Entry":
                        t = widget.get()
                        try:
                            n = int(t)
                        except ValueError:
                            if not self.errCheck:
                                errorL = tk.Label(master=self.algOptFrame,text="Enter valid number", fg="red")
                                errorL.pack(fill="x",side=tk.BOTTOM)
                                self.errCheck = True

                if n:
                    ciph = self.encryptionAlgorithms.caesar(plain, n, True)
                    self.outTextBox.delete(1.0, tk.END)
                    self.outTextBox.insert(1.0, ciph)

                    if self.errCheck:
                        self.algOptFrame.winfo_children()[-1].destroy()
                        self.errCheck = False

            case "Substitution":
                ciph = self.encryptionAlgorithms.subkey(plain, "test")
                self.outTextBox.insert(1.0, ciph)
            case "Hill":
                ciph = self.encryptionAlgorithms.hill(plain, "whiterabb")
                self.outTextBox.insert(1.0, ciph)
            case "Railfence":
                ciph = self.encryptionAlgorithms.rail(plain, 5)
                self.outTextBox.insert(1.0, ciph)
            case "Autokey":
                ciph = self.encryptionAlgorithms.autokey(plain, "test")
                self.outTextBox.insert(1.0, ciph)

    def select(self, event):
        alg = event.widget["text"]

        match alg:
            case "Caesar":
                self.encryptionAlgorithms.currentlySelected = alg

                for widget in self.algOptFrame.winfo_children():
                    widget.destroy()
                
                shiftL = tk.Label(master=self.algOptFrame,text="Choose the shift (nonzero int) to use for encryption:")
                shiftL.pack(fill="x",side=tk.TOP)

                shiftT = tk.Entry(master=self.algOptFrame,width=10)
                shiftT.pack(side=tk.TOP)

                encButton = tk.Button(master=self.algOptFrame,width=10,height=2,text="Encrypt")
                encButton.bind("<Button-1>", self.encrypt)
                encButton.pack(side=tk.TOP)

                #ciph = self.encryptionAlgorithms.caesar(plain, 5, True)
                #self.outTextBox.insert(1.0, ciph)
            # case "Substitution":
            #     ciph = self.encryptionAlgorithms.subkey(plain, "test")
            #     self.outTextBox.insert(1.0, ciph)
            # case "Hill":
            #     ciph = self.encryptionAlgorithms.hill(plain, "whiterabb")
            #     self.outTextBox.insert(1.0, ciph)
            # case "Railfence":
            #     ciph = self.encryptionAlgorithms.rail(plain, 5)
            #     self.outTextBox.insert(1.0, ciph)
            # case "Autokey":
            #     ciph = self.encryptionAlgorithms.autokey(plain, "test")
            #     self.outTextBox.insert(1.0, ciph)


    def enterMain(self):
        for b in self.buttons:
            b.bind("<Button-1>", self.select)

        self.window.mainloop()

if __name__ == "__main__":
    gui = cryptographyUI(800,600)
    gui.enterMain()