import wx
import libs.utilities as util


class MainFrame(wx.Frame):

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(MainFrame, self).__init__(*args, **kw)
        self.contentNotSaved = False

        self.makeMenuBar()

        panel = wx.Panel(self)
        # self.panel.SetBackgroundColour('#ff0000')
        main_window_sizer = wx.BoxSizer(wx.VERTICAL)

        attribute_fields_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.text1 = wx.StaticText(panel, label="Title1")
        self.t1 = wx.TextCtrl(panel)
        self.text2 = wx.StaticText(panel, label="Title2")
        self.text3 = wx.StaticText(panel, label="Title3")
        attribute_fields_sizer.Add(self.text1, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        attribute_fields_sizer.Add(self.t1, 1, wx.EXPAND | wx.ALIGN_LEFT | wx.ALL, 5)
        attribute_fields_sizer.Add(self.text2, 0, wx.ALIGN_LEFT | wx.ALL, 10)
        attribute_fields_sizer.Add(self.text3, 0, wx.ALIGN_LEFT | wx.ALL, 10)

        main_window_sizer.Add(attribute_fields_sizer, 1, wx.EXPAND)

        content_sizer = wx.BoxSizer(wx.HORIZONTAL)
        grid_1 = wx.GridSizer(12, 2, 0, 0)
        grid_1.AddMany(wx.StaticText(panel, label=str(i)) for i in range(24))
        content_sizer.Add(grid_1, 1, wx.EXPAND | wx.ALL, 3)
        grid_2 = wx.GridSizer(10, 3, 0, 0)
        grid_2.AddMany(wx.StaticText(panel, label=str(i)) for i in range(30))
        content_sizer.Add(grid_2, 1, wx.EXPAND | wx.ALL, 3)

        main_window_sizer.Add(content_sizer, 1, wx.EXPAND)


        panel.SetSizer(main_window_sizer)

        # and a status bar
        self.CreateStatusBar()
        self.SetStatusText("Select log file")
#

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        fileMenu = wx.Menu()
        loadLogFileItem = fileMenu.Append(-1, "Load from &file\tCtrl-F", "Loads event log from a file")
        loadLogUrlItem = fileMenu.Append(-1, "Load from &URL\tCtrl-U", "Loads event log requesting given URL")
        fileMenu.AppendSeparator()
        saveFilteredResultsItem = fileMenu.Append(-1, "&Save filtered results as...\tCtrl-S", "Saves filtered events to file")
        fileMenu.AppendSeparator()
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # When using a stock ID we don't need to specify the menu item's
        # label

        # Now a help menu for the about item

        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnLoadLogFile, loadLogFileItem)
        self.Bind(wx.EVT_MENU, self.OnLoadLogUrl, loadLogUrlItem)
        self.Bind(wx.EVT_MENU, self.OnExit,  exitItem)
        self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def OnExit(self, event):
        """Close the frame, terminating the application."""
        self.Close(True)

    def OnLoadLogFile(self, event):

        if self.contentNotSaved:
            if wx.MessageBox("Current content has not been saved! Proceed?", "Please confirm",
                             wx.ICON_QUESTION | wx.YES_NO, self) == wx.NO:
                return

        # otherwise ask the user what new file to open
        with wx.FileDialog(self, "Open TXT file", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:

            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            try:
                util.extract_log_events(pathname, True)
                self.SetStatusText(f"{pathname} successfully parsed")

                #with open(pathname, 'r') as file:
                #    self.doLoadDataOrWhatever(file)
            except IOError:
                wx.LogError(f"Cannot open {pathname}")

    def OnLoadLogUrl(self, event):
        wx.MessageBox("This utility will be implemented later", "Under construction")

    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("SLF4J Log parser",
                      "About",
                      wx.OK|wx.ICON_INFORMATION)


def run():
    app = wx.App()
    frm = MainFrame(None, title='Log Beautifier alpha', size=wx.Size(1000, 600))
    frm.Show()
    app.MainLoop()