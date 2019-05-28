from tkinter import filedialog
from tkinter import *

class SampleApp(Tk):

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.geometry("300x300")

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(Frame):

    def __init__(self,parent,controller):
        Frame.__init__(self,parent)
        self.controller = controller
        self.file_select_frame()

    def file_select_frame(self):
        self.las_path = StringVar()
        self.cgml_path = StringVar()

        self.las_path.set("No Path")
        self.cgml_path.set("No Path")

        button_cgml_path = Button(self, text="Choose cityGML File", command=lambda: self.callback_choose_file(self.cgml_path)).grid(row=2)
        button_las_path = Button(self, text="Choose Las/Laz File", command=lambda: self.callback_choose_file(self.las_path)).grid(row=1)
        
        label_las_path = Label(self, textvariable = self.las_path).grid(row = 1, column = 1)
        label_cgml_path = Label(self, textvariable = self.cgml_path).grid(row = 2, column = 1)

    def callback_choose_file(self, path_var):
        path = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Las/Laz Pointcloud","*.las"),("all files","*.*")))
        if path:
            path_var.set(path)

        self.update()

class PageOne(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        label = Label(self, text="This is page 1")
        label.pack(side="top", fill="x", pady=10)
        button = Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()