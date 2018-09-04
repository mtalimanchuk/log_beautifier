import wx
import wx.adv
import wx.xrc
import wx.richtext
import datetime
import libs.gui_util as gu
import libs.utilities as util

###########################################################################
## Class ResultsFrame
###########################################################################


class ResultsFrame(wx.Frame):

    def __init__(self, parent, results_to_show):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Filtered results", pos=wx.DefaultPosition,
                          size=wx.Size(1024, 768), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)
        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)
        self.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        self.results_toolBar = self.CreateToolBar(wx.TB_DEFAULT_STYLE, wx.ID_ANY)
        self.results_toolBar.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        self.save_results_tool = self.results_toolBar.AddTool(wx.ID_ANY, u"Save results",
                                                                   wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE,
                                                                                            wx.ART_TOOLBAR),
                                                                   wx.NullBitmap, wx.ITEM_NORMAL,
                                                                   u"Save filtered results in a file", wx.EmptyString,
                                                                   None)

        self.results_toolBar.AddSeparator()

        self.results_searchCtrl = wx.SearchCtrl(self.results_toolBar, wx.ID_ANY, wx.EmptyString, wx.Point(-1, -1),
                                                wx.DefaultSize, 0)
        self.results_searchCtrl.ShowSearchButton(True)
        self.results_searchCtrl.ShowCancelButton(False)
        self.results_toolBar.AddControl(self.results_searchCtrl)
        self.results_toolBar.Realize()

        results_sizer = wx.BoxSizer(wx.VERTICAL)

        self.results_richText = wx.richtext.RichTextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition,
                                                         wx.DefaultSize,
                                                         wx.TE_READONLY | wx.BORDER_SUNKEN | wx.HSCROLL | wx.VSCROLL | wx.WANTS_CHARS)

        for line in results_to_show:
            self.results_richText.AppendText((str(line.timestamp) + line.log_level + line.instance + line.message + '\n'))
        results_sizer.Add(self.results_richText, 1, wx.EXPAND, 5)

        self.instance_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                       wx.BORDER_STATIC | wx.TAB_TRAVERSAL)
        self.instance_panel.SetForegroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))
        self.instance_panel.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        instance_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        instance_listBoxChoices = [u"12", u"5ihgcjhcj", u"yfylfili", u"ilhifiydhd", u"gfdgsfgsfh", u"sfghsfghsghsfs",
                                   u"fsf2222", u"gfdgdfgdf", u"dfgdfgdfgs", u"tg4g45g45g", u"54g45g45g45",
                                   u"brtgbrtbrtbrtb", u"trbwrgbgngfngfn", u"fgrfbrgbrtthetr", u"fgerth25hhw45h6",
                                   u"iygpiygpiyvf", u"iugpugp9uu", u"lvuyckugucljh", u"fggsgsss"]
        self.instance_listBox = wx.ListBox(self.instance_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           instance_listBoxChoices, wx.LB_MULTIPLE)
        instance_panel_sizer.Add(self.instance_listBox, 0, wx.ALL | wx.EXPAND, 5)

        self.instance_panel.SetSizer(instance_panel_sizer)
        self.instance_panel.Layout()
        instance_panel_sizer.Fit(self.instance_panel)
        results_sizer.Add(self.instance_panel, 0, wx.EXPAND, 5)

        self.SetSizer(results_sizer)
        self.Layout()
        self.results_statusBar = self.CreateStatusBar(1, wx.STB_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)
        self.Show()

        # Connect Events
        self.Bind(wx.EVT_TOOL, self.OnSaveResultsTool, id=self.save_results_tool.GetId())
        self.results_searchCtrl.Bind(wx.EVT_TEXT_ENTER, self.OnSearchResults)

    def __del__(self):
        pass

    # Virtual event handlers, overide them in your derived class
    def OnSaveResultsTool(self, event):
        event.Skip()

    def OnSearchResults(self, event):
        event.Skip()


class MainFrame(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Log Beautifier alpha", pos=wx.DefaultPosition,
                          size=wx.Size(600, 600), style=wx.CAPTION | wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.TAB_TRAVERSAL)
        self.log = None  # TODO store parsed log in .csv

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        self.main_statusBar = self.CreateStatusBar(1, wx.STB_DEFAULT_STYLE, wx.ID_ANY)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)

        self._init_main_menu_panel()

    def __del__(self):
        pass

    def _init_main_menu_panel(self):
        self.menu_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL)
        menu_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        new_connection_sizer = wx.StaticBoxSizer(wx.StaticBox(self.menu_panel, wx.ID_ANY, u"New connection"),
                                                 wx.VERTICAL)

        self.new_connection_url_staticText = wx.StaticText(new_connection_sizer.GetStaticBox(), wx.ID_ANY, u"URL",
                                                           wx.DefaultPosition, wx.DefaultSize, 0)
        self.new_connection_url_staticText.Wrap(-1)

        new_connection_sizer.Add(self.new_connection_url_staticText, 0, wx.ALL, 5)

        self.new_connection_url_textCtrl = wx.TextCtrl(new_connection_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                       wx.DefaultPosition, wx.DefaultSize, 0)
        new_connection_sizer.Add(self.new_connection_url_textCtrl, 0, wx.ALL | wx.EXPAND, 5)

        self.new_connection_alias_staticText = wx.StaticText(new_connection_sizer.GetStaticBox(), wx.ID_ANY,
                                                             u"Alias (short name)", wx.DefaultPosition, wx.DefaultSize,
                                                             0)
        self.new_connection_alias_staticText.Wrap(-1)

        new_connection_sizer.Add(self.new_connection_alias_staticText, 0, wx.ALL, 5)

        self.new_connection_alias_textCtrl = wx.TextCtrl(new_connection_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                                         wx.DefaultPosition, wx.DefaultSize, 0)
        new_connection_sizer.Add(self.new_connection_alias_textCtrl, 0, wx.ALL | wx.EXPAND, 5)

        self.save_new_connection_button = wx.Button(new_connection_sizer.GetStaticBox(), wx.ID_ANY, u"Save",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        new_connection_sizer.Add(self.save_new_connection_button, 0, wx.ALL, 5)

        menu_panel_sizer.Add(new_connection_sizer, 1, wx.ALL | wx.EXPAND, 5)

        saved_connections_sizer = wx.StaticBoxSizer(wx.StaticBox(self.menu_panel, wx.ID_ANY, u"Saved connections"),
                                                    wx.HORIZONTAL)

        saved_connections_listBoxChoices = [u"localhost:8000/src/log", u"github.com/mtalimanchuk",
                                            u"localhost:8000/log/daniil", u"localhost:8000/src/log/"]
        self.saved_connections_listBox = wx.ListBox(saved_connections_sizer.GetStaticBox(), wx.ID_ANY,
                                                    wx.DefaultPosition, wx.DefaultSize,
                                                    saved_connections_listBoxChoices, 0)
        saved_connections_sizer.Add(self.saved_connections_listBox, 0, wx.ALL | wx.EXPAND, 5)

        saved_connections_utility_sizer = wx.BoxSizer(wx.VERTICAL)

        self.fetch_button = wx.Button(saved_connections_sizer.GetStaticBox(), wx.ID_ANY, u"Fetch", wx.DefaultPosition,
                                      wx.DefaultSize, 0)
        saved_connections_utility_sizer.Add(self.fetch_button, 0, wx.ALL, 5)

        self.fetch_all_button = wx.Button(saved_connections_sizer.GetStaticBox(), wx.ID_ANY, u"Fetch all",
                                          wx.DefaultPosition, wx.DefaultSize, 0)
        saved_connections_utility_sizer.Add(self.fetch_all_button, 0, wx.ALL, 5)

        self.connection_info_staticText = wx.StaticText(saved_connections_sizer.GetStaticBox(), wx.ID_ANY,
                                                        u"Last fetched: 02-05-1995 01:12.034", wx.DefaultPosition,
                                                        wx.DefaultSize, 0)
        self.connection_info_staticText.Wrap(-1)

        self.connection_info_staticText.SetMinSize(wx.Size(-1, 80))

        saved_connections_utility_sizer.Add(self.connection_info_staticText, 0, wx.ALL | wx.SHAPED, 5)

        self.open_log_button = wx.Button(saved_connections_sizer.GetStaticBox(), wx.ID_ANY, u"Open log",
                                         wx.DefaultPosition, wx.DefaultSize, 0)
        saved_connections_utility_sizer.Add(self.open_log_button, 0, wx.ALL | wx.EXPAND, 5)

        saved_connections_sizer.Add(saved_connections_utility_sizer, 1, wx.EXPAND, 5)

        menu_panel_sizer.Add(saved_connections_sizer, 1, wx.ALL | wx.EXPAND, 5)

        open_local_log_file_sizer = wx.StaticBoxSizer(wx.StaticBox(self.menu_panel, wx.ID_ANY, u"Or choose log file"),
                                                      wx.VERTICAL)

        self.open_local_log_file_button = wx.Button(open_local_log_file_sizer.GetStaticBox(), wx.ID_ANY,
                                                    u"Open log from a local file", wx.DefaultPosition, wx.DefaultSize,
                                                    0)
        open_local_log_file_sizer.Add(self.open_local_log_file_button, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        menu_panel_sizer.Add(open_local_log_file_sizer, 1, wx.ALL | wx.EXPAND, 5)

        self.show_parser_warnings_checkBox = wx.CheckBox(self.menu_panel, wx.ID_ANY, u"Show parser warnings",
                                                         wx.DefaultPosition, wx.DefaultSize, 0)
        self.show_parser_warnings_checkBox.SetValue(True)
        menu_panel_sizer.Add(self.show_parser_warnings_checkBox, 0, wx.ALL, 5)

        self.menu_panel.SetSizer(menu_panel_sizer)
        self.menu_panel.Layout()
        menu_panel_sizer.Fit(self.menu_panel)
        self.main_sizer.Add(self.menu_panel, 1, wx.EXPAND, 5)

        self.SetSizer(self.main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.new_connection_url_textCtrl.Bind(wx.EVT_TEXT, self.OnNewConnectionUrlText)
        self.save_new_connection_button.Bind(wx.EVT_BUTTON, self.OnSaveNewConnectionButton)
        self.saved_connections_listBox.Bind(wx.EVT_LISTBOX, self.OnSelectConnection)
        self.saved_connections_listBox.Bind(wx.EVT_LISTBOX_DCLICK, self.OnConnectionDClick)
        self.fetch_button.Bind(wx.EVT_BUTTON, self.OnFetchButton)
        self.fetch_all_button.Bind(wx.EVT_BUTTON, self.OnFetchAllButton)
        self.open_log_button.Bind(wx.EVT_BUTTON, self.OnOpenLogUrlButton)
        self.open_local_log_file_button.Bind(wx.EVT_BUTTON, self.OnOpenLogFileButton)
        None

    def _init_filter_attributes_panel(self):
        self.menu_panel.Hide()
        self.filter_attributes_panel = wx.Panel(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                                wx.BORDER_THEME | wx.TAB_TRAVERSAL)
        # self.filter_attributes_panel.Hide()

        filter_attributes_panel_sizer = wx.BoxSizer(wx.VERTICAL)

        time_sizer = wx.StaticBoxSizer(wx.StaticBox(self.filter_attributes_panel, wx.ID_ANY, u"Time"), wx.HORIZONTAL)

        self.start_time_staticText = wx.StaticText(time_sizer.GetStaticBox(), wx.ID_ANY, u"From", wx.DefaultPosition,
                                                   wx.DefaultSize, 0)
        self.start_time_staticText.Wrap(-1)

        time_sizer.Add(self.start_time_staticText, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.start_time_datePicker = wx.adv.DatePickerCtrl(time_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                                           wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT)
        time_sizer.Add(self.start_time_datePicker, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.start_time_timePicker = wx.adv.TimePickerCtrl(time_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                                           wx.DefaultPosition, wx.DefaultSize, 0)
        time_sizer.Add(self.start_time_timePicker, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.end_time_staticText = wx.StaticText(time_sizer.GetStaticBox(), wx.ID_ANY, u"To", wx.DefaultPosition,
                                                 wx.DefaultSize, 0)
        self.end_time_staticText.Wrap(-1)

        time_sizer.Add(self.end_time_staticText, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.end_time_datePicker = wx.adv.DatePickerCtrl(time_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                                         wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT)
        time_sizer.Add(self.end_time_datePicker, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.end_time_timePicker = wx.adv.TimePickerCtrl(time_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultDateTime,
                                                         wx.DefaultPosition, wx.DefaultSize, wx.adv.DP_DEFAULT)
        time_sizer.Add(self.end_time_timePicker, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        filter_attributes_panel_sizer.Add(time_sizer, 1, wx.ALL | wx.EXPAND, 5)

        log_level_sizer = wx.StaticBoxSizer(wx.StaticBox(self.filter_attributes_panel, wx.ID_ANY, u"Log level"),
                                            wx.HORIZONTAL)

        self.log_level_info_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"INFO",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        self.log_level_info_checkBox.SetValue(True)
        log_level_sizer.Add(self.log_level_info_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_level_error_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"ERROR",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        self.log_level_error_checkBox.SetValue(True)
        log_level_sizer.Add(self.log_level_error_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_level_warn_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"WARN",
                                                   wx.DefaultPosition, wx.DefaultSize, 0)
        log_level_sizer.Add(self.log_level_warn_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_level_trace_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"TRACE",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        log_level_sizer.Add(self.log_level_trace_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_level_debug_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"DEBUG",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        log_level_sizer.Add(self.log_level_debug_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.log_level_fatal_checkBox = wx.CheckBox(log_level_sizer.GetStaticBox(), wx.ID_ANY, u"FATAL",
                                                    wx.DefaultPosition, wx.DefaultSize, 0)
        log_level_sizer.Add(self.log_level_fatal_checkBox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        filter_attributes_panel_sizer.Add(log_level_sizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        instance_sizer = wx.StaticBoxSizer(
            wx.StaticBox(self.filter_attributes_panel, wx.ID_ANY, u"Instance name (optional)"), wx.VERTICAL)

        self.instance_staticText = wx.StaticText(instance_sizer.GetStaticBox(), wx.ID_ANY, u"Enter instance name",
                                                 wx.DefaultPosition, wx.DefaultSize, 0)
        self.instance_staticText.Wrap(-1)

        instance_sizer.Add(self.instance_staticText, 0, wx.ALL, 5)

        self.instance_textCtrl = wx.TextCtrl(instance_sizer.GetStaticBox(), wx.ID_ANY, wx.EmptyString,
                                             wx.DefaultPosition, wx.DefaultSize, 0)
        self.instance_textCtrl.SetToolTip(u"123")

        instance_sizer.Add(self.instance_textCtrl, 0, wx.ALL | wx.EXPAND, 5)

        self.instance_list_staticText = wx.StaticText(instance_sizer.GetStaticBox(), wx.ID_ANY,
                                                      u"or choose from the list below", wx.DefaultPosition,
                                                      wx.DefaultSize, 0)
        self.instance_list_staticText.Wrap(-1)

        instance_sizer.Add(self.instance_list_staticText, 0, wx.ALL, 5)

        instance_listBoxChoices = [u"12", u"5ihgcjhcj", u"yfylfili", u"ilhifiydhd", u"gfdgsfgsfh", u"sfghsfghsghsfs",
                                   u"fsf2222", u"gfdgdfgdf", u"dfgdfgdfgs", u"tg4g45g45g", u"54g45g45g45",
                                   u"brtgbrtbrtbrtb", u"trbwrgbgngfngfn", u"fgrfbrgbrtthetr", u"fgerth25hhw45h6",
                                   u"iygpiygpiyvf", u"iugpugp9uu", u"lvuyckugucljh", u"fggsgsss"]
        self.instance_listBox = wx.ListBox(instance_sizer.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                           instance_listBoxChoices,
                                           wx.LB_ALWAYS_SB | wx.LB_MULTIPLE | wx.LB_NEEDED_SB | wx.LB_SORT)
        instance_sizer.Add(self.instance_listBox, 0, wx.ALL | wx.EXPAND, 5)

        filter_attributes_panel_sizer.Add(instance_sizer, 1, wx.ALIGN_CENTER | wx.ALL | wx.EXPAND, 5)

        self.apply_filters_button = wx.Button(self.filter_attributes_panel, wx.ID_ANY, u"Apply filters",
                                              wx.DefaultPosition, wx.DefaultSize, 0)
        filter_attributes_panel_sizer.Add(self.apply_filters_button, 0, wx.ALIGN_CENTER | wx.ALL | wx.SHAPED, 5)

        self.filter_attributes_panel.SetSizer(filter_attributes_panel_sizer)
        self.filter_attributes_panel.Layout()
        filter_attributes_panel_sizer.Fit(self.filter_attributes_panel)
        self.main_sizer.Add(self.filter_attributes_panel, 1, wx.EXPAND, 5)

        self.SetSizer(self.main_sizer)
        self.Layout()

        self.Centre(wx.BOTH)

        self.apply_filters_button.Bind(wx.EVT_BUTTON, self.OnApplyFiltersButton)

    def collect_filter_attributes(self):

        wx_start_date = self.start_time_datePicker.GetValue()
        wx_start_time = self.start_time_timePicker.GetValue()
        wx_end_date = self.end_time_datePicker.GetValue()
        wx_end_time = self.end_time_timePicker.GetValue()

        log_level = []
        if self.log_level_info_checkBox.GetValue(): log_level.append('INFO')
        if self.log_level_error_checkBox.GetValue(): log_level.append('ERROR')
        if self.log_level_warn_checkBox.GetValue(): log_level.append('WARN')
        if self.log_level_trace_checkBox.GetValue(): log_level.append('TRACE')
        if self.log_level_debug_checkBox.GetValue(): log_level.append('DEBUG')
        if self.log_level_fatal_checkBox.GetValue(): log_level.append('FATAL')

        attributes = gu.create_filters(wx_start_date, wx_start_time, wx_end_date, wx_end_time, log_level)
        return attributes

    # Virtual event handlers, overide them in your derived class
    def OnNewConnectionUrlText(self, event):
        url = self.new_connection_url_textCtrl.GetValue()

        self.new_connection_alias_textCtrl.SetValue(gu.make_alias_name(url))

    def OnSaveNewConnectionButton(self, event):
        event.Skip()

    def OnSelectConnection(self, event):
        event.Skip()

    def OnConnectionDClick(self, event):
        event.Skip()

    def OnFetchButton(self, event):
        event.Skip()

    def OnFetchAllButton(self, event):
        event.Skip()

    def OnOpenLogFileButton(self, event):

        with wx.FileDialog(self, "Open TXT file", wildcard="TXT files (*.txt)|*.txt",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return  # the user changed their mind

            # Proceed loading the file chosen by the user
            pathname = fileDialog.GetPath()
            show_warnings = self.show_parser_warnings_checkBox.GetValue()

            self.log = gu.try_parse_log_file(pathname)

            wx.StatusBar.SetStatusText(self.main_statusBar, f'{pathname} has been successfully parsed')
            self._init_filter_attributes_panel()
        event.Skip()

    def OnOpenLogUrlButton(self, event):
        event.Skip()

    def OnApplyFiltersButton(self, event):

        attributes = self.collect_filter_attributes()
        filtered_list = util.filter_events(self.log, attributes)
        for log_event in filtered_list:
            print(log_event.timestamp, log_event.log_level, log_event.instance, log_event.message)
        print('Opening results...')
        results = ResultsFrame(None, filtered_list)
        results.Show()
        event.Skip()


def run():
    app = wx.App()
    frm = MainFrame(None)
    frm.Show()
    app.MainLoop()
