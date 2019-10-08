import mod_funcs
import mod_materials
import wx

class MyFrame(wx.Frame):

    def __init__(self):
        # initiate GUI
        super().__init__(parent=None, title='Depletion region demos')
        panel = wx.Panel(self)
        my_sizer = wx.BoxSizer(wx.VERTICAL)
        self.color = (0,0,0)

        self.listbox_name = wx.StaticText(panel, id = wx.ALIGN_LEFT, label="Junction material")
        my_sizer.Add(self.listbox_name,0,wx.ALL,5)
        mat_choices = ["AlGaAs","4H-SiC"]
        self.listbox_ctrl = wx.ListBox(panel, id = wx.LB_SINGLE, choices=mat_choices)
        self.listbox_ctrl.Bind(wx.EVT_LISTBOX,self.on_select)
        my_sizer.Add(self.listbox_ctrl,0,wx.ALL,5)

        panel.SetSizer(my_sizer)
        self.Show()

    def on_select(self,event):
        value = self.listbox_ctrl.GetSelection()
        string = self.listbox_ctrl.GetString(value)
        mod_funcs.run_main(string)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()

