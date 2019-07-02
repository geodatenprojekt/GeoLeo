from gui.input.model import Model as IModel
from gui.input.view import View as IView

from gui.main_window.model import Model as MModel
from gui.main_window.view import View as MView

from gui.output.model import Model as OModel
from gui.output.view import View as OView

class Controller:
    def __init__(self, tkroot):
        self.root = tkroot
        self.imodel = IModel()
        self.iview = IView(self.root, self.imodel, self)

    def run(self):
        self.root.title("Pointcloud view")
        self.root.resizable(True, True) 
        self.root.deiconify()
        self.raise_in()
        self.root.withdraw()
        self.root.mainloop()

    def raise_in(self):
        self.iview.frame.tkraise()

    def raise_main(self):
        self.mmodel = MModel(self.imodel.lasPath, self.imodel.gmlPath)
        self.mview = MView(self.root, self.mmodel, self)
        self.mview.frame.tkraise()

    def raise_out(self):
        self.omodel = OModel(self.imodel.lasPath, self.imodel.gmlPath, self.mmodel.moveX, self.mmodel.moveY)
        self.oview = OView(self.root, self.omodel, self)
        self.oview.frame.tkraise()