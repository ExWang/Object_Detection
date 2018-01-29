# coding=utf-8
import sys
import MySQLdb
import wx
from PIL import Image

import viewer_back

'''
处理数据库类
'''
WIN_WIDTH = 1440
WIN_HEIGHT = 900

sql_func1_master = 'select distinct(id_img),cam,time_date,time_time from caption_info'

path_img_source = 'getpicture/CaptureImg/output/camera/'
path_caping_source = 'capTest'

action_hash = {'standing': 1, 'stands': 1, 'sitting': 2, 'sits': 2, 'walking': 4, 'walks': 4, 'calling': 5, 'calls': 5,
               'bending': 7, 'bends': 7, 'squatting': 11, 'squats': 11}


def WxBitmapToPilImage(myBitmap):
    return WxImageToPilImage(WxBitmapToWxImage(myBitmap))


def WxBitmapToWxImage(myBitmap):
    return wx.ImageFromBitmap(myBitmap)


def PilImageToWxBitmap(myPilImage):
    return WxImageToWxBitmap(PilImageToWxImage(myPilImage))


def WxImageToWxBitmap(myWxImage):
    return myWxImage.ConvertToBitmap()


def WxImageToWxBitmap(myWxImage):
    return myWxImage.ConvertToBitmap()


def PilImageToWxImage(myPilImage):
    (x, y) = myPilImage.size
    # print x, y
    width2c = 215
    hight2c = 215
    x_s = width2c
    y_s = int((width2c / float(x)) * y)
    if y_s > hight2c:
        x_s2 = int((hight2c / float(y_s)) * x_s)
        y_s2 = hight2c
    else:
        x_s2 = x_s
        y_s2 = y_s
    myPilImage = myPilImage.resize((x_s2, y_s2), Image.ANTIALIAS)
    myWxImage = wx.Image(myPilImage.size[0], myPilImage.size[1])
    myWxImage.SetData(myPilImage.convert('RGB').tobytes())
    return myWxImage


class MyShowInfo_1(wx.Frame):
    def __init__(self, parent, ToShow):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='详细信息', pos=wx.DefaultPosition,
                          size=wx.Size(300, 150), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.ms_panel = wx.Panel(self, size=wx.Size(300, 150))
        self.SetMaxSize((300, 150))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.ms_staticText1 = wx.StaticText(self.ms_panel, wx.ID_ANY, ToShow)
        bSizer1.Add(self.ms_staticText1, 1, wx.EXPAND | wx.ALL, 10)

        self.ms_button2 = wx.Button(self.ms_panel, wx.ID_ANY, "返回", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.ms_button2, 0, wx.CENTER | wx.BOTTOM | wx.TOP, 10)
        self.ms_button2.Bind(wx.EVT_BUTTON, self.CloseThis)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def CloseThis(self, event):
        self.Close()

    def __del__(self):
        pass


class MyShowInfo_2(wx.Frame):
    def __init__(self, parent, ToShow):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='详细信息', pos=wx.DefaultPosition,
                          size=wx.Size(400, 450), style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        self.ms_panel = wx.Panel(self, size=wx.Size(400, 450))

        self.SetMaxSize((400, 450))

        self.SetSizeHints(wx.DefaultSize, wx.DefaultSize)

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        self.ms_staticText1 = wx.StaticText(self.ms_panel, wx.ID_ANY, ToShow)
        bSizer1.Add(self.ms_staticText1, 1, wx.EXPAND | wx.ALL, 10)

        self.ms_button2 = wx.Button(self.ms_panel, wx.ID_ANY, "返回", wx.DefaultPosition, wx.DefaultSize, 0)
        bSizer1.Add(self.ms_button2, 0, wx.CENTER | wx.BOTTOM | wx.TOP, 10)
        self.ms_button2.Bind(wx.EVT_BUTTON, self.CloseThis)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

    def CloseThis(self, event):
        self.Close()

    def __del__(self):
        pass


class MyShowFunc_1(wx.Frame):
    def __init__(self, parent):
        print 'Came to func1'

        camera_list = ['ALL', '200', '201', '202']

        self.con = MySQLdb.connect("localhost", "root", "123456", "human_caption", unix_socket="/tmp/mysql.sock")
        # 使用cursor()方法获取操作游标
        self.cursor = self.con.cursor()

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='全部监控图像检索', size=(1440, 900))

        # win2 = wx.Frame(None, title='全部监控图像检索', size=(1440, 900))
        # self.SetMaxSize((1440, 900))
        # self.SetMinSize((1440, 900))
        self.bkg2 = wx.Panel(self, size=wx.Size(1440, 900))

        self.ImgList = []
        self.path_img_source_f1 = path_img_source  # from global
        self.ImgPos = 0
        self.ImgTotal = 0

        self.Button_query_f1 = wx.Button(self.bkg2, label='查询')
        self.Button_query_f1.Bind(wx.EVT_BUTTON, self.GetFunc1)
        self.Button_detail_f1 = wx.Button(self.bkg2, label=' 详细信息 ')
        self.Button_detail_f1.Bind(wx.EVT_BUTTON, self.GetPicInfo)
        self.Button_return_f1 = wx.Button(self.bkg2, label=' 返回系统 ')
        self.Button_return_f1.Bind(wx.EVT_BUTTON, self.CloseThisWin)

        self.Label_camera_f1 = wx.StaticText(self.bkg2, label=' 相机: ')
        self.Label_date_f1 = wx.StaticText(self.bkg2, label=' 日期: ')
        self.Label_time_f1 = wx.StaticText(self.bkg2, label=' 时间: ')
        self.Label_pic_num = wx.StaticText(self.bkg2, label=' 0/0 ')

        self.Input_date_f1 = wx.TextCtrl(self.bkg2)
        self.Input_time_f1 = wx.TextCtrl(self.bkg2)

        self.ComboBox_camera_f1 = wx.ComboBox(self.bkg2, choices=camera_list)
        self.ComboBox_camera_f1.SetSelection(0)

        # image next button
        self.bmp_0 = wx.Image("img_next_png.png", wx.BITMAP_TYPE_PNG)
        bmp_0_w = self.bmp_0.GetWidth()
        bmp_0_h = self.bmp_0.GetHeight()
        self.bmp_0 = self.bmp_0.Scale(width=bmp_0_w * 0.5, height=bmp_0_h * 0.6)
        self.bmp_0 = self.bmp_0.ConvertToBitmap()
        self.BT_next_Button = wx.BitmapButton(self.bkg2, bitmap=self.bmp_0)
        self.BT_next_Button.Bind(wx.EVT_BUTTON, self.GetNextPic)

        # image preview button
        self.bmp_0 = wx.Image("img_prev_png.png", wx.BITMAP_TYPE_PNG)
        bmp_0_w = self.bmp_0.GetWidth()
        bmp_0_h = self.bmp_0.GetHeight()
        self.bmp_0 = self.bmp_0.Scale(width=bmp_0_w * 0.5, height=bmp_0_h * 0.6)
        self.bmp_0 = self.bmp_0.ConvertToBitmap()
        self.BT_prev_Button = wx.BitmapButton(self.bkg2, bitmap=self.bmp_0)
        self.BT_prev_Button.Bind(wx.EVT_BUTTON, self.GetPrevPic)

        # image to show area
        self.pic_im_init_f1 = wx.Image("wx03.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.pic_im_now_f1 = wx.Image("wx03.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.image_show_f1 = wx.StaticBitmap(self.bkg2, bitmap=self.pic_im_init_f1)

        hbox_query = wx.BoxSizer()
        hbox_query.Add(self.Label_camera_f1, proportion=0, flag=wx.CENTER, border=10)
        hbox_query.Add(self.ComboBox_camera_f1, proportion=0, flag=wx.CENTER | wx.RIGHT, border=10)
        hbox_query.Add(self.Label_date_f1, proportion=0, flag=wx.CENTER, border=10)
        hbox_query.Add(self.Input_date_f1, proportion=1, flag=wx.CENTER | wx.RIGHT, border=10)
        hbox_query.Add(self.Label_time_f1, proportion=0, flag=wx.CENTER, border=10)
        hbox_query.Add(self.Input_time_f1, proportion=1, flag=wx.CENTER, border=10)
        hbox_query.Add(self.Button_query_f1, proportion=0, flag=wx.CENTER | wx.LEFT, border=10)

        self.hbox_show = wx.BoxSizer()
        self.hbox_show.Add(self.BT_prev_Button, proportion=0, flag=wx.LEFT | wx.EXPAND, border=10)
        self.hbox_show.Add(self.image_show_f1, proportion=1, flag=wx.EXPAND | wx.CENTER, border=10)
        self.hbox_show.Add(self.BT_next_Button, proportion=0, flag=wx.RIGHT | wx.EXPAND, border=10)

        hbox_operations = wx.BoxSizer()
        hbox_operations.Add(self.Label_pic_num, proportion=0, flag=wx.CENTER | wx.RIGHT, border=30)
        hbox_operations.Add(self.Button_detail_f1, proportion=0, flag=wx.CENTER, border=10)
        hbox_operations.Add(self.Button_return_f1, proportion=0, flag=wx.CENTER | wx.LEFT, border=10)

        vbox_all = wx.BoxSizer(wx.VERTICAL)
        vbox_all.Add(hbox_query, proportion=0, flag=wx.CENTER | wx.TOP, border=10)
        vbox_all.Add(self.hbox_show, proportion=1, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=5)
        vbox_all.Add(hbox_operations, proportion=0, flag=wx.CENTER | wx.BOTTOM, border=10)

        self.bkg2.SetSizer(vbox_all)
        self.Layout()

    def CloseThisWin(self, event):
        print 'Leaving Function 1'
        self.cursor.close()
        self.con.close()
        self.Close()

    def GetFunc1(self, event):
        camera = self.ComboBox_camera_f1.GetValue()
        date = self.Input_date_f1.GetValue()
        time = self.Input_time_f1.GetValue()

        if camera == '' or camera == 'ALL':
            sql_camera = 'cam IS NULL or cam IS NOT NULL'
        else:
            sql_camera = 'cam=' + str(camera)

        if date == '' or date == 'ALL':
            sql_date = 'time_date IS NULL or time_date IS NOT NULL'
        else:
            sql_date = 'time_date=' + date

        if time == '' or time == 'ALL':
            sql_time = 'time_time IS NULL or time_time IS NOT NULL'
        else:
            sql_time = 'time_time=' + time

        sql_final = sql_func1_master + ' where (' + sql_camera + ')and(' + sql_date + ')and(' + sql_time + ')'
        self.Label_pic_num.SetLabel('1 / ' + str(self.ImgTotal))
        print sql_final
        self.cursor = self.con.cursor()
        self.cursor.execute(sql_final)
        result = self.cursor.fetchall()
        self.cursor.close()
        self.ImgList = result
        self.ImgTotal = len(result)
        self.ImgPos = 0
        show_path = self.path_img_source_f1 + self.ImgList[0][1] + '/' + self.ImgList[0][0]
        self.ShowPic(show_path)
        print result
        print len(result)

    def ShowPic(self, pic_path):
        self.pic_im_now_f1 = wx.Image(pic_path, wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        self.image_show_f1.SetBitmap(self.pic_im_now_f1)
        self.image_show_f1.Refresh()
        self.hbox_show.Layout()

    def GetNextPic(self, event):
        if self.ImgPos < (self.ImgTotal - 1):
            self.ImgPos = self.ImgPos + 1
            self.Label_pic_num.SetLabel(str(self.ImgPos + 1) + ' / ' + str(self.ImgTotal))
            path_in = self.path_img_source_f1 + self.ImgList[self.ImgPos][1] + '/' + self.ImgList[self.ImgPos][0]
            self.ShowPic(path_in)
        else:
            warn = wx.MessageBox("已经是最后一张了！", 'Attention', style=wx.OK | wx.CENTER)

    def GetPrevPic(self, event):
        if self.ImgPos > 0:
            self.ImgPos = self.ImgPos - 1
            self.Label_pic_num.SetLabel(str(self.ImgPos + 1) + ' / ' + str(self.ImgTotal))
            path_in = self.path_img_source_f1 + self.ImgList[self.ImgPos][1] + '/' + self.ImgList[self.ImgPos][0]
            self.ShowPic(path_in)
        else:
            ret = wx.MessageBox("已经是第一张了！", 'Attention', style=wx.OK | wx.CENTER)

    def GetPicInfo(self, event):

        ThisInfo = self.ImgList[self.ImgPos]
        ShowStr = '\n 名称 : ' + ThisInfo[0] + '\n 相机 : ' + ThisInfo[1] + '\n 捕捉日期 : ' + str(
            ThisInfo[2]) + '\n 捕捉时间 : ' + str(ThisInfo[3])

        PicInfo = MyShowInfo_1(self, ShowStr)
        PicInfo.Show()

    def __del__(self):
        pass


# -------------------------------------------------------------


class MyShowFunc_2(wx.Frame):
    def __init__(self, parent):
        print 'Came to func2'

        self.find_result_len = 0
        self.page_now = 0
        self.page_total = 0
        self.find_result = ()

        # Some List for ComboBoxes

        self.sex_list = ['ALL', 'Male', 'Female']
        self.camera_list = ['ALL', '200', '201', '202']
        self.color_list_master = ['ALL', 'blue', 'gray', 'brown', 'purple', 'yellow', 'pink', 'black', 'green',
                                  'striped', 'white', 'red',
                                  "plaid"]
        self.color_list_slave = ['', 'blue', 'gray', 'brown', 'purple', 'yellow', 'pink', 'black', 'green', 'striped',
                                 'white', 'red',
                                 "plaid"]
        self.action_hash = {'standing': 1, 'stands': 1, 'sitting': 2, 'sits': 2, 'walking': 4, 'walks': 4, 'calling': 5,
                            'calls': 5,
                            'bending': 7, 'bends': 7, 'squatting': 11, 'squats': 11}
        self.action_list_master = ['ALL', 'stand', 'sit', 'walk', 'call', 'bend', 'squat']
        self.action_list_slave = ['', 'stand', 'sit', 'walk', 'call', 'bend', 'squat']
        self.action_index = ['', '1', '2', '4', '5', '7', '11']

        self.con = MySQLdb.connect("localhost", "root", "123456", "human_caption", unix_socket="/tmp/mysql.sock")
        # 使用cursor()方法获取操作游标
        self.cursor = self.con.cursor()

        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='行人监控检索', size=(1440, 900))

        # win2 = wx.Frame(None, title='全部监控图像检索', size=(1440, 900))
        # self.SetMaxSize((1440, 900))
        # self.SetMinSize((1440, 900))
        self.bkg3 = wx.Panel(self, size=wx.Size(1440, 900))

        # 创建ComboBox
        self.ComboBox_sex = wx.ComboBox(self.bkg3, choices=self.sex_list)
        self.ComboBox_sex.SetSelection(0)
        self.ComboBox_camera = wx.ComboBox(self.bkg3, choices=self.camera_list)
        self.ComboBox_camera.SetSelection(0)
        self.ComboBox_color_m = wx.ComboBox(self.bkg3, choices=self.color_list_master)
        self.ComboBox_color_m.SetSelection(0)
        self.ComboBox_color_s0 = wx.ComboBox(self.bkg3, choices=self.color_list_slave)
        self.ComboBox_color_s0.SetSelection(0)
        self.ComboBox_color_s1 = wx.ComboBox(self.bkg3, choices=self.color_list_slave)
        self.ComboBox_color_s1.SetSelection(0)
        self.ComboBox_action_m = wx.ComboBox(self.bkg3, choices=self.action_list_master)
        self.ComboBox_action_m.SetSelection(0)
        self.ComboBox_action_s0 = wx.ComboBox(self.bkg3, choices=self.action_list_slave)
        self.ComboBox_action_s0.SetSelection(0)

        # 事件绑定
        self.ComboBox_color_m.Bind(wx.EVT_COMBOBOX, self.set_color_other)
        self.ComboBox_color_s0.Bind(wx.EVT_COMBOBOX, self.set_color_other)
        self.ComboBox_color_s1.Bind(wx.EVT_COMBOBOX, self.set_color_other)
        self.ComboBox_action_m.Bind(wx.EVT_COMBOBOX, self.set_action_other)
        self.ComboBox_action_s0.Bind(wx.EVT_COMBOBOX, self.set_action_other)

        # 创建按钮控件
        # self.helpButton = wx.Button(self.bkg3, label='帮助')
        # self.helpButton.Bind(wx.EVT_BUTTON, help)
        self.QueryButton = wx.Button(self.bkg3, label='查询')
        self.QueryButton.Bind(wx.EVT_BUTTON, self.query)
        self.ClearButton = wx.Button(self.bkg3, label='清除')
        self.ClearButton.Bind(wx.EVT_BUTTON, self.clear_id)

        self.ReturnButton = wx.Button(self.bkg3, label='返回系统')
        self.ReturnButton.Bind(wx.EVT_BUTTON, self.CloseThisWin)

        # 创建可编辑（输入）文本框控件
        self.Input_date = wx.TextCtrl(self.bkg3)
        self.Input_time = wx.TextCtrl(self.bkg3)

        # 创建静态（不可编辑）文本框控件
        self.Label_camera = wx.StaticText(self.bkg3, label=' 相机 :')
        self.Label_sex = wx.StaticText(self.bkg3, label=' 性别 :')
        self.Label_color = wx.StaticText(self.bkg3, label=' 颜色 :')
        self.Label_action = wx.StaticText(self.bkg3, label=' 动作 :')
        self.Label_date = wx.StaticText(self.bkg3, label=' 日期 : ')
        self.Label_time = wx.StaticText(self.bkg3, label=' 时间 : ')

        self.Label_total_pics = wx.StaticText(self.bkg3, label='共0个检索结果')
        self.Label_now_page = wx.StaticText(self.bkg3, label='当前0/0页')

        imgbox_thresh_w = 230
        imgbox_thresh_h = 230
        # pic0 = wx.Image("wx01.jpg", wx.BITMAP_TYPE_JPEG).ConvertToBitmap()
        pil_img_file = Image.open("wx01.jpg")
        pic0 = WxImageToWxBitmap(PilImageToWxImage(pil_img_file))
        self.Img_box0 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box1 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box2 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box3 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box4 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box5 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box6 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))
        self.Img_box7 = wx.BitmapButton(self.bkg3, bitmap=pic0, size=(imgbox_thresh_w, imgbox_thresh_h))

        self.Img_box0.Bind(wx.EVT_BUTTON, self.show_0)
        self.Img_box1.Bind(wx.EVT_BUTTON, self.show_1)
        self.Img_box2.Bind(wx.EVT_BUTTON, self.show_2)
        self.Img_box3.Bind(wx.EVT_BUTTON, self.show_3)
        self.Img_box4.Bind(wx.EVT_BUTTON, self.show_4)
        self.Img_box5.Bind(wx.EVT_BUTTON, self.show_5)
        self.Img_box6.Bind(wx.EVT_BUTTON, self.show_6)
        self.Img_box7.Bind(wx.EVT_BUTTON, self.show_7)

        labbox_thresh_w = 150
        labbox_thresh_h = 80
        self.lab_box0 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box1 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box2 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box3 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box4 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box5 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box6 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))
        self.lab_box7 = wx.StaticText(self.bkg3, size=(labbox_thresh_w, labbox_thresh_h))

        # page next button
        self.bmp_0 = wx.Image("img_next_png.png", wx.BITMAP_TYPE_PNG)
        bmp_0_w = self.bmp_0.GetWidth()
        bmp_0_h = self.bmp_0.GetHeight()
        self.bmp_0 = self.bmp_0.Scale(width=bmp_0_w * 0.5, height=bmp_0_h * 0.6)
        self.bmp_0 = self.bmp_0.ConvertToBitmap()
        self.BT_next_Button = wx.BitmapButton(self.bkg3, bitmap=self.bmp_0)
        self.BT_next_Button.Bind(wx.EVT_BUTTON, self.GetNextPage)

        # page preview button
        self.bmp_0 = wx.Image("img_prev_png.png", wx.BITMAP_TYPE_PNG)
        bmp_0_w = self.bmp_0.GetWidth()
        bmp_0_h = self.bmp_0.GetHeight()
        self.bmp_0 = self.bmp_0.Scale(width=bmp_0_w * 0.5, height=bmp_0_h * 0.6)
        self.bmp_0 = self.bmp_0.ConvertToBitmap()
        self.BT_prev_Button = wx.BitmapButton(self.bkg3, bitmap=self.bmp_0)
        self.BT_prev_Button.Bind(wx.EVT_BUTTON, self.GetPrevPage)

        ### 窗口布局配置

        hbox_con = wx.BoxSizer()
        hbox_con.Add(self.ClearButton, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        hbox_con.Add(self.QueryButton, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        # hbox_con.Add(self.helpButton, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)

        # 图片在数据库内编号 和 摄像机 布局
        hbox_cam = wx.BoxSizer()
        hbox_cam.Add(self.Label_camera, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT | wx.CENTER, border=5)
        hbox_cam.Add(self.ComboBox_camera, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)

        # 时间查询 按日期 按时间 布局
        hbox_datetime = wx.BoxSizer()
        hbox_datetime.Add(self.Label_date, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=5)
        hbox_datetime.Add(self.Input_date, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)
        hbox_datetime.Add(self.Label_time, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL | wx.LEFT, border=5)
        hbox_datetime.Add(self.Input_time, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)

        # 性别查询 布局
        hbox_sex = wx.BoxSizer()
        hbox_sex.Add(self.Label_sex, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=5)
        hbox_sex.Add(self.ComboBox_sex, proportion=1, flag=wx.EXPAND | wx.LEFT, border=5)

        # 颜色查询 布局
        hbox_color = wx.BoxSizer()
        hbox_color.Add(self.Label_color, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=5)
        hbox_color.Add(self.ComboBox_color_m, proportion=2, flag=wx.EXPAND | wx.LEFT, border=5)
        hbox_color.Add(self.ComboBox_color_s0, proportion=2, flag=wx.EXPAND | wx.LEFT, border=5)
        hbox_color.Add(self.ComboBox_color_s1, proportion=2, flag=wx.EXPAND | wx.LEFT, border=5)

        # 动作查询 布局
        hbox_action = wx.BoxSizer()
        hbox_action.Add(self.Label_action, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=5)
        hbox_action.Add(self.ComboBox_action_m, proportion=2, flag=wx.EXPAND | wx.LEFT, border=5)
        hbox_action.Add(self.ComboBox_action_s0, proportion=2, flag=wx.EXPAND | wx.LEFT, border=5)

        # 布局以上 布局box
        hbox_line1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_line1.Add(hbox_cam, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox_line1.Add(hbox_datetime, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox_line1.Add(hbox_sex, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        hbox_line2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox_line2.Add(hbox_color, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)
        hbox_line2.Add(hbox_action, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        inputvbox = wx.BoxSizer(wx.VERTICAL)
        inputvbox.Add(hbox_line1, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        inputvbox.Add(hbox_line2, proportion=0, flag=wx.EXPAND | wx.ALL, border=1)
        inputvbox.Add(hbox_con, proportion=0, flag=wx.ALIGN_RIGHT, border=1)

        # 用于显示图像的布局
        ib0 = wx.BoxSizer(wx.VERTICAL)
        ib1 = wx.BoxSizer(wx.VERTICAL)
        ib2 = wx.BoxSizer(wx.VERTICAL)
        ib3 = wx.BoxSizer(wx.VERTICAL)
        ib4 = wx.BoxSizer(wx.VERTICAL)
        ib5 = wx.BoxSizer(wx.VERTICAL)
        ib6 = wx.BoxSizer(wx.VERTICAL)
        ib7 = wx.BoxSizer(wx.VERTICAL)

        ib0.Add(self.Img_box0, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib0.Add(self.lab_box0, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib1.Add(self.Img_box1, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib1.Add(self.lab_box1, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib2.Add(self.Img_box2, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib2.Add(self.lab_box2, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib3.Add(self.Img_box3, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib3.Add(self.lab_box3, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib4.Add(self.Img_box4, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib4.Add(self.lab_box4, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib5.Add(self.Img_box5, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib5.Add(self.lab_box5, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib6.Add(self.Img_box6, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib6.Add(self.lab_box6, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        ib7.Add(self.Img_box7, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        ib7.Add(self.lab_box7, proportion=0, flag=wx.CENTER | wx.TOP | wx.BOTTOM, border=10)

        imgbox_0 = wx.BoxSizer()
        imgbox_0.Add(ib0, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_0.Add(ib1, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_0.Add(ib2, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_0.Add(ib3, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        imgbox_1 = wx.BoxSizer()
        imgbox_1.Add(ib4, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_1.Add(ib5, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_1.Add(ib6, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)
        imgbox_1.Add(ib7, proportion=0, flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=20)

        self.imgvbox = wx.BoxSizer(wx.VERTICAL)
        self.imgvbox.Add(imgbox_0, proportion=0, flag=wx.CENTER, border=5)
        self.imgvbox.Add(imgbox_1, proportion=0, flag=wx.CENTER, border=5)

        pagebox = wx.BoxSizer(wx.HORIZONTAL)
        pagebox.Add(self.BT_prev_Button, proportion=0, flag=wx.LEFT | wx.EXPAND, border=10)
        pagebox.Add(self.imgvbox, proportion=1, flag=wx.ALL | wx.CENTER, border=10)
        pagebox.Add(self.BT_next_Button, proportion=0, flag=wx.RIGHT | wx.EXPAND, border=10)

        self.statusbox = wx.BoxSizer(wx.HORIZONTAL)
        self.statusbox.Add(self.Label_total_pics, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.statusbox.Add(self.Label_now_page, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)
        self.statusbox.Add(self.ReturnButton, proportion=0, flag=wx.ALL | wx.ALIGN_CENTER_VERTICAL, border=5)

        # 总布局
        finalvbox = wx.BoxSizer(wx.VERTICAL)
        finalvbox.Add(inputvbox, proportion=0, flag=wx.ALL | wx.EXPAND, border=10)
        finalvbox.Add(pagebox, proportion=1, flag=wx.CENTER | wx.EXPAND, border=5)
        finalvbox.Add(self.statusbox, proportion=0, flag=wx.CENTER, border=5)

        self.bkg3.SetSizer(finalvbox)
        self.Layout()

    def get_show_info(self, btid):
        hole_str = self.find_result[self.page_now * 8 + btid]
        dbinfo_idp = str(hole_str[0])
        dbinfo_camera = hole_str[1]
        dbinfo_date = str(hole_str[2])
        dbinfo_time = str(hole_str[3])
        dbinfo_imgid = hole_str[4]
        img_left = hole_str[5]
        img_right = hole_str[6]
        img_top = hole_str[7]
        img_bottom = hole_str[8]
        dbinfo_sex = hole_str[9]
        dbinfo_color = hole_str[10]
        dbinfo_action = hole_str[11]
        dbinfo_captions = hole_str[12]

        captions_this = dbinfo_captions.split('.')

        actions_this = dbinfo_action.split(',')
        dbinfo_action = ''
        for action_this in actions_this:
            dbinfo_action = dbinfo_action + self.action_list_master[self.action_index.index(action_this)] + ','
        dbinfo_action = dbinfo_action[:-1]

        part_a = 'ID:' + dbinfo_idp + '\n相机:' + dbinfo_camera + '\n捕捉日期:' + dbinfo_date + '\n捕捉时间:' + dbinfo_time
        part_b = '\n父图像名称:' + dbinfo_imgid + '\n性别:' + dbinfo_sex + '\n颜色:' + dbinfo_color + '\n动作:' + dbinfo_action
        part_c = '\n说明:'
        code_num = 1
        limit_cap = len(captions_this)
        for caption_this in range(0, limit_cap - 1):
            part_c = part_c + '\n' + str(code_num) + ' : ' + captions_this[caption_this]
            code_num += 1
        total = part_a + part_b + part_c
        print total
        return total

    def get_abstract_info(self, infid):
        hole_str = self.find_result[infid]
        dbinfo_sex = hole_str[9]
        dbinfo_color = hole_str[10]
        dbinfo_action = hole_str[11]

        actions_this = dbinfo_action.split(',')
        dbinfo_action = ''
        for action_this in actions_this:
            dbinfo_action = dbinfo_action + self.action_list_master[self.action_index.index(action_this)] + ','
        dbinfo_action = dbinfo_action[:-1]

        part_b = '性别:' + dbinfo_sex + '\n颜色:' + dbinfo_color + '\n动作:' + dbinfo_action

        return part_b

    def show_0(self, event):
        btid = 0
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_1(self, event):
        btid = 1
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_2(self, event):
        btid = 2
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_3(self, event):
        btid = 3
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_4(self, event):
        btid = 4
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_5(self, event):
        btid = 5
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_6(self, event):
        btid = 6
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    def show_7(self, event):
        btid = 7
        ShowStr = self.get_show_info(btid)
        PicInfo = MyShowInfo_2(self, ShowStr)
        PicInfo.Show()

    # 查询函数
    def query(self, event):
        # 获取控件中内容
        camera = self.ComboBox_camera.GetValue()
        sex = self.ComboBox_sex.GetValue()
        date = self.Input_date.GetValue()
        time = self.Input_time.GetValue()

        # Load ComboBoxes
        color_select_m = self.ComboBox_color_m.GetValue()
        color_select_s0 = self.ComboBox_color_s0.GetValue()
        color_select_s1 = self.ComboBox_color_s1.GetValue()
        print 'Color:master---->', color_select_m, 'slave0---->', color_select_s0, 'slave1---->', color_select_s1
        action_select_m = self.ComboBox_action_m.GetValue()
        action_select_s0 = self.ComboBox_action_s0.GetValue()
        print 'Action:master---->', action_select_m, 'slave0---->', action_select_s0

        # 判断查询条件

        if camera == '' or camera == 'ALL':
            sql_camera = 'cam IS NULL or cam IS NOT NULL'
        else:
            sql_camera = 'cam=' + str(camera)

        if sex == 'ALL':
            sql_sex = 'sex IS NULL or sex IS NOT NULL'
        else:
            sql_sex = 'sex=\"' + sex + "\""

        if date == '':
            sql_date = 'time_date IS NULL or time_date IS NOT NULL'
        else:
            sql_date = 'time_date=\"' + date + "\""

        if time == '':
            sql_time = 'time_time IS NULL or time_time IS NOT NULL'
        else:
            sql_time = 'time_time=\"' + time + "\""

        if color_select_m == 'ALL':
            sql_color = 'color IS NULL or color IS NOT NULL'
        else:
            sql_color = 'color like \'%' + color_select_m + '%\' and color like \'%' + color_select_s0 + '%\' and color like \'%' + color_select_s1 + '%\''

        if action_select_m == 'ALL':
            sql_action = 'action_id IS NULL or action_id IS NOT NULL'
        else:
            action_select_m = self.action_index[self.action_list_master.index(action_select_m)]
            action_select_s0 = self.action_index[self.action_list_slave.index(action_select_s0)]
            print 'Action:master---->', action_select_m, 'slave0---->', action_select_s0

            sql_ac_0 = 'action_id like \'%,' + action_select_m + '\' or action_id like \'' + action_select_m + ',%\' or action_id like \'%' + action_select_m + '%\' or action_id like \'' + action_select_m + '\''
            sql_ac_1 = 'action_id like \'%,' + action_select_s0 + '\' or action_id like \'' + action_select_s0 + ',%\' or action_id like \'%' + action_select_s0 + '%\' or action_id like \'' + action_select_s0 + '\''
            sql_action = '(' + sql_ac_0 + ') and (' + sql_ac_1 + ')'
            # 'action_id like \'%' + action_select_m + '%\' and color like \'%' + action_select_s0 + '%\''

        # 根据条件拼接查询语句，并执行查询
        sql = "select * from caption_info where (" + sql_camera + ") and (" + sql_sex + ") and (" + sql_color + ") and (" + sql_action + ") and ( " + sql_date + ") and (" + sql_time + ")"
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        self.find_result = result
        print '++++++++++++++', type(result), type(self.find_result)
        print result
        print self.find_result
        pil_img_file = Image.open("null.jpg")
        picnull = WxImageToWxBitmap(PilImageToWxImage(pil_img_file))
        self.Img_box0.SetBitmap(bitmap=picnull)
        self.Img_box1.SetBitmap(bitmap=picnull)
        self.Img_box2.SetBitmap(bitmap=picnull)
        self.Img_box3.SetBitmap(bitmap=picnull)
        self.Img_box4.SetBitmap(bitmap=picnull)
        self.Img_box5.SetBitmap(bitmap=picnull)
        self.Img_box6.SetBitmap(bitmap=picnull)
        self.Img_box7.SetBitmap(bitmap=picnull)
        self.imgvbox.Layout()
        self.lab_box0.SetLabel('')
        self.lab_box1.SetLabel('')
        self.lab_box2.SetLabel('')
        self.lab_box3.SetLabel('')
        self.lab_box4.SetLabel('')
        self.lab_box5.SetLabel('')
        self.lab_box6.SetLabel('')
        self.lab_box7.SetLabel('')

        # 按照自定规则打印出每一条内容
        device_count = 1

        # 输出检索页数和结果个数
        self.find_result_len = len(result)
        self.Label_total_pics.SetLabel('共' + str(self.find_result_len) + '个检索结果')
        self.page_now = 0
        self.page_total = int((self.find_result_len - 1) / 8)
        self.Label_now_page.SetLabel('当前' + str(self.page_now + 1) + '/' + str(self.page_total + 1) + '页')
        self.statusbox.Layout()

        now_pic = self.page_now * 8
        limit_pic = now_pic + 8
        for row in result:
            dbinfo_idp = row[0]
            dbinfo_camera = row[1]
            dbinfo_date = row[2]
            dbinfo_time = row[3]
            dbinfo_imgid = row[4]
            img_left = row[5]
            img_right = row[6]
            img_top = row[7]
            img_bottom = row[8]
            dbinfo_sex = row[9]
            dbinfo_color = row[10]
            dbinfo_action = row[11]
            dbinfo_captions = row[12]

            path_img_to_cut = path_img_source + dbinfo_camera + '/' + dbinfo_imgid
            pil_img = Image.open(path_img_to_cut)
            box = [img_left, img_top, img_right, img_bottom]
            pil_img = pil_img.crop(box)
            pic_this = WxImageToWxBitmap(PilImageToWxImage(pil_img))
            result_len = self.find_result_len
            if (now_pic < limit_pic) and (now_pic % 8) == 0:
                self.Img_box0.SetBitmap(bitmap=pic_this)
                self.lab_box0.SetLabel(self.get_abstract_info(now_pic))
                print 'Img_box0 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 1:
                self.Img_box1.SetBitmap(bitmap=pic_this)
                self.lab_box1.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box1.SetBitmap(bitmap=pic_this)
                print 'Img_box1 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 2:
                self.Img_box2.SetBitmap(bitmap=pic_this)
                self.lab_box2.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box2.SetBitmap(bitmap=pic_this)
                print 'Img_box2 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 3:
                self.Img_box3.SetBitmap(bitmap=pic_this)
                self.lab_box3.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box3.SetBitmap(bitmap=pic_this)
                print 'Img_box3 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 4:
                self.Img_box4.SetBitmap(bitmap=pic_this)
                self.lab_box4.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box4.SetBitmap(bitmap=pic_this)
                print 'Img_box4 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 5:
                self.Img_box5.SetBitmap(bitmap=pic_this)
                self.lab_box5.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box5.SetBitmap(bitmap=pic_this)
                print 'Img_box5 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 6:
                self.Img_box6.SetBitmap(bitmap=pic_this)
                self.lab_box6.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box6.SetBitmap(bitmap=pic_this)
                print 'Img_box6 get pic'
            if (now_pic < limit_pic) and (now_pic % 8) == 7:
                self.Img_box7.SetBitmap(bitmap=pic_this)
                self.lab_box7.SetLabel(self.get_abstract_info(now_pic))
                self.Img_box7.SetBitmap(bitmap=pic_this)
                print 'Img_box7 get pic'
            if now_pic == limit_pic:
                break
            now_pic = now_pic + 1
            print now_pic

            device_count = device_count + 1
        self.imgvbox.Layout()

    # 清除所有输入框函数
    def clear_id(self, id):
        self.Input_date.Clear()
        self.Input_time.Clear()
        self.ComboBox_sex.SetSelection(0)
        self.ComboBox_camera.SetSelection(0)
        self.ComboBox_color_m.SetSelection(0)
        self.ComboBox_action_m.SetSelection(0)
        self.find_result = ()
        pil_img_file = Image.open("null.jpg")
        picnull = WxImageToWxBitmap(PilImageToWxImage(pil_img_file))
        self.Img_box0.SetBitmap(bitmap=picnull)
        self.Img_box1.SetBitmap(bitmap=picnull)
        self.Img_box2.SetBitmap(bitmap=picnull)
        self.Img_box3.SetBitmap(bitmap=picnull)
        self.Img_box4.SetBitmap(bitmap=picnull)
        self.Img_box5.SetBitmap(bitmap=picnull)
        self.Img_box6.SetBitmap(bitmap=picnull)
        self.Img_box7.SetBitmap(bitmap=picnull)
        self.lab_box0.SetLabel('')
        self.lab_box1.SetLabel('')
        self.lab_box2.SetLabel('')
        self.lab_box3.SetLabel('')
        self.lab_box4.SetLabel('')
        self.lab_box5.SetLabel('')
        self.lab_box6.SetLabel('')
        self.lab_box7.SetLabel('')
        self.imgvbox.Layout()

        self.find_result_len = 0

    def GetNextPage(self, event):
        if (self.page_now < self.page_total) and ((self.page_now + 1) * 8 <= self.find_result_len):
            self.page_now = self.page_now + 1
            now_pic_l = self.page_now * 8
            limit_pic = now_pic_l + 8

            # 输出检索页数和结果个数
            self.Label_now_page.SetLabel('当前' + str(self.page_now + 1) + '/' + str(self.page_total + 1) + '页')
            self.statusbox.Layout()

            pil_img_file = Image.open("null.jpg")
            picnull = WxImageToWxBitmap(PilImageToWxImage(pil_img_file))
            self.Img_box0.SetBitmap(bitmap=picnull)
            self.Img_box1.SetBitmap(bitmap=picnull)
            self.Img_box2.SetBitmap(bitmap=picnull)
            self.Img_box3.SetBitmap(bitmap=picnull)
            self.Img_box4.SetBitmap(bitmap=picnull)
            self.Img_box5.SetBitmap(bitmap=picnull)
            self.Img_box6.SetBitmap(bitmap=picnull)
            self.Img_box7.SetBitmap(bitmap=picnull)

            self.lab_box0.SetLabel('')
            self.lab_box1.SetLabel('')
            self.lab_box2.SetLabel('')
            self.lab_box3.SetLabel('')
            self.lab_box4.SetLabel('')
            self.lab_box5.SetLabel('')
            self.lab_box6.SetLabel('')
            self.lab_box7.SetLabel('')

            for now_pic in range(now_pic_l, limit_pic):
                row = self.find_result[now_pic]
                dbinfo_camera = row[1]
                dbinfo_imgid = row[4]
                img_left = row[5]
                img_right = row[6]
                img_top = row[7]
                img_bottom = row[8]

                path_img_to_cut = path_img_source + dbinfo_camera + '/' + dbinfo_imgid
                pil_img = Image.open(path_img_to_cut)
                box = [img_left, img_top, img_right, img_bottom]
                pil_img = pil_img.crop(box)
                pic_this = WxImageToWxBitmap(PilImageToWxImage(pil_img))
                result_len = self.find_result_len
                if (now_pic < limit_pic) and (now_pic % 8) == 0:
                    self.Img_box0.SetBitmap(bitmap=pic_this)
                    self.lab_box0.SetLabel(self.get_abstract_info(now_pic))
                    print 'Img_box0 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 1:
                    self.Img_box1.SetBitmap(bitmap=pic_this)
                    self.lab_box1.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box1.SetBitmap(bitmap=pic_this)
                    print 'Img_box1 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 2:
                    self.Img_box2.SetBitmap(bitmap=pic_this)
                    self.lab_box2.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box2.SetBitmap(bitmap=pic_this)
                    print 'Img_box2 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 3:
                    self.Img_box3.SetBitmap(bitmap=pic_this)
                    self.lab_box3.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box3.SetBitmap(bitmap=pic_this)
                    print 'Img_box3 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 4:
                    self.Img_box4.SetBitmap(bitmap=pic_this)
                    self.lab_box4.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box4.SetBitmap(bitmap=pic_this)
                    print 'Img_box4 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 5:
                    self.Img_box5.SetBitmap(bitmap=pic_this)
                    self.lab_box5.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box5.SetBitmap(bitmap=pic_this)
                    print 'Img_box5 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 6:
                    self.Img_box6.SetBitmap(bitmap=pic_this)
                    self.lab_box6.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box6.SetBitmap(bitmap=pic_this)
                    print 'Img_box6 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 7:
                    self.Img_box7.SetBitmap(bitmap=pic_this)
                    self.lab_box7.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box7.SetBitmap(bitmap=pic_this)
                    print 'Img_box7 get pic'
                if now_pic == limit_pic:
                    break
                now_pic = now_pic + 1

            self.imgvbox.Layout()
        else:
            ret = wx.MessageBox("已经是最后一页了！", 'Attention', style=wx.OK | wx.CENTER)

        print 'Next'

    def GetPrevPage(self, event):
        if self.page_now > 0:
            self.page_now = self.page_now - 1

            # 输出检索页数和结果个数
            self.Label_now_page.SetLabel('当前' + str(self.page_now + 1) + '/' + str(self.page_total + 1) + '页')
            self.statusbox.Layout()

            now_pic_l = self.page_now * 8
            limit_pic = now_pic_l + 8

            pil_img_file = Image.open("null.jpg")
            picnull = WxImageToWxBitmap(PilImageToWxImage(pil_img_file))
            self.Img_box0.SetBitmap(bitmap=picnull)
            self.Img_box1.SetBitmap(bitmap=picnull)
            self.Img_box2.SetBitmap(bitmap=picnull)
            self.Img_box3.SetBitmap(bitmap=picnull)
            self.Img_box4.SetBitmap(bitmap=picnull)
            self.Img_box5.SetBitmap(bitmap=picnull)
            self.Img_box6.SetBitmap(bitmap=picnull)
            self.Img_box7.SetBitmap(bitmap=picnull)

            self.lab_box0.SetLabel('')
            self.lab_box1.SetLabel('')
            self.lab_box2.SetLabel('')
            self.lab_box3.SetLabel('')
            self.lab_box4.SetLabel('')
            self.lab_box5.SetLabel('')
            self.lab_box6.SetLabel('')
            self.lab_box7.SetLabel('')

            for now_pic in range(now_pic_l, limit_pic):
                row = self.find_result[now_pic]
                dbinfo_camera = row[1]
                dbinfo_imgid = row[4]
                img_left = row[5]
                img_right = row[6]
                img_top = row[7]
                img_bottom = row[8]

                path_img_to_cut = path_img_source + dbinfo_camera + '/' + dbinfo_imgid
                pil_img = Image.open(path_img_to_cut)
                box = [img_left, img_top, img_right, img_bottom]
                pil_img = pil_img.crop(box)
                pic_this = WxImageToWxBitmap(PilImageToWxImage(pil_img))
                result_len = self.find_result_len
                if (now_pic < limit_pic) and (now_pic % 8) == 0:
                    self.Img_box0.SetBitmap(bitmap=pic_this)
                    self.lab_box0.SetLabel(self.get_abstract_info(now_pic))
                    print 'Img_box0 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 1:
                    self.Img_box1.SetBitmap(bitmap=pic_this)
                    self.lab_box1.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box1.SetBitmap(bitmap=pic_this)
                    print 'Img_box1 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 2:
                    self.Img_box2.SetBitmap(bitmap=pic_this)
                    self.lab_box2.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box2.SetBitmap(bitmap=pic_this)
                    print 'Img_box2 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 3:
                    self.Img_box3.SetBitmap(bitmap=pic_this)
                    self.lab_box3.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box3.SetBitmap(bitmap=pic_this)
                    print 'Img_box3 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 4:
                    self.Img_box4.SetBitmap(bitmap=pic_this)
                    self.lab_box4.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box4.SetBitmap(bitmap=pic_this)
                    print 'Img_box4 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 5:
                    self.Img_box5.SetBitmap(bitmap=pic_this)
                    self.lab_box5.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box5.SetBitmap(bitmap=pic_this)
                    print 'Img_box5 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 6:
                    self.Img_box6.SetBitmap(bitmap=pic_this)
                    self.lab_box6.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box6.SetBitmap(bitmap=pic_this)
                    print 'Img_box6 get pic'
                if (now_pic < limit_pic) and (now_pic % 8) == 7:
                    self.Img_box7.SetBitmap(bitmap=pic_this)
                    self.lab_box7.SetLabel(self.get_abstract_info(now_pic))
                    self.Img_box7.SetBitmap(bitmap=pic_this)
                    print 'Img_box7 get pic'
                if now_pic == limit_pic:
                    break
                now_pic = now_pic + 1

            self.imgvbox.Layout()
        else:
            ret = wx.MessageBox("已经是第一页了！", 'Attention', style=wx.OK | wx.CENTER)
        print 'Prev'

    def set_color_other(self, event):
        if self.ComboBox_color_m.GetValue() == 'ALL':
            self.ComboBox_color_s0.SetSelection(0)
            self.ComboBox_color_s1.SetSelection(0)

    def set_action_other(self, event):
        if self.ComboBox_action_m.GetValue() == 'ALL':
            self.ComboBox_action_s0.SetSelection(0)

    def CloseThisWin(self, event):
        print 'Leaving Function 2'
        self.cursor.close()
        self.con.close()
        self.Close()

    def __del__(self):
        pass


# 帮助函数 用于打印该程序的帮助信息
def help(event):
    contents.Clear()  # clear before print
    contents.AppendText("======== Help =======\n")
    contents.AppendText("|     This is a demo     |\n")
    contents.AppendText("| Date input example: 20170803 ---> 2017-08-03 |\n")
    contents.AppendText("| Time input example: 194704 ---> 19:47:04 |\n")
    contents.AppendText("====================\n")


def close_win(event):
    print 'Debug from org'
    # win.MenuBar
    win.Close()

    # app2 = wx.App()
    win2 = wx.Frame(None, title='Sub window', size=(800, 600))
    bkg2 = wx.Panel(win2)
    bb = wx.BoxSizer()
    showButton2 = wx.Button(bkg2, label='ALL')
    bb.Add(showButton2, proportion=0, flag=wx.EXPAND, border=5)
    bkg2.SetSizer(bb)
    win2.Show()
    # app2.MainLoop()
    ShowStr = 'Fucker\n' + 'Test\n'
    ss = MyShowInfo_1(win2, ShowStr)
    ss.Show()


class MyShowFunc_main_surv(wx.Frame):
    def __init__(self, parent):
        print 'Came to Surveillance Function '
        self.MAIN_WIDTH = 490
        self.MAIN_HEIGHT = 200
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='行人检索系统 V1.0', size=(self.MAIN_WIDTH, self.MAIN_HEIGHT))
        self.bkg3 = wx.Panel(self, size=wx.Size(self.MAIN_WIDTH, self.MAIN_HEIGHT))
        self.SetMaxSize((self.MAIN_WIDTH, self.MAIN_HEIGHT))
        self.Center()

        # image function button
        bmp_m = wx.Image("func01.png", wx.BITMAP_TYPE_PNG)
        bmp_m_w = bmp_m.GetWidth()
        bmp_m_h = bmp_m.GetHeight()
        rew = bmp_m_w * 0.1
        reh = bmp_m_h * 0.1
        print rew, reh
        bmp_m = bmp_m.Scale(width=rew, height=reh)
        bmp_m = bmp_m.ConvertToBitmap()
        self.BT_func1_Button = wx.BitmapButton(self.bkg3, bitmap=bmp_m, pos=(30, 50 - 20), size=(200, 100))
        self.LAB_func1 = wx.StaticText(self.bkg3, label='全部监控图像检索', pos=(70, 160 - 20))
        self.BT_func1_Button.Bind(wx.EVT_BUTTON, self.Function1_start)

        bmp_m = wx.Image("func02.png", wx.BITMAP_TYPE_PNG)
        bmp_m_w = bmp_m.GetWidth()
        bmp_m_h = bmp_m.GetHeight()
        rew = bmp_m_w * 0.085
        reh = bmp_m_h * 0.085
        print rew, reh
        bmp_m = bmp_m.Scale(width=rew, height=reh)
        bmp_m = bmp_m.ConvertToBitmap()
        self.BT_func2_Button = wx.BitmapButton(self.bkg3, bitmap=bmp_m, pos=(255, 50 - 20), size=(200, 100))
        self.LAB_func2 = wx.StaticText(self.bkg3, label='行人监控检索', pos=(310, 160 - 20))
        self.BT_func2_Button.Bind(wx.EVT_BUTTON, self.Function2_start)

    def Function1_start(self, event):
        win_1 = MyShowFunc_1(self)
        win_1.Show()

    def Function2_start(self, event):
        win_2 = MyShowFunc_2(self)
        win_2.Show()

    def CloseThisWin(self, event):
        print 'Leaving Function Surveillance'
        self.Close()

    def __del__(self):
        pass


class MyShowFunc_Caption_Demo(wx.Frame):
    def __init__(self, parent):
        print 'Came to Image Caption Function'
        # 窗口和绘制区域创建
        cap_W = 700
        cap_H = 550
        self.img_show_heigh = 300.0
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title='图像描述V0_1', size=(cap_W, cap_H))
        self.bkg4 = wx.Panel(self, size=wx.Size(cap_W, cap_H))
        self.Center()
        self.SetMaxSize((cap_W, cap_H+100))
        self.SetMinSize((cap_W, cap_H))

        # 参数设定
        self.selected_Path = "capTest/000370.jpg"
        self.ImgList = []
        self.ImgPos = 0
        self.ImgTotal = 0

        # 控件创建
        self.Button_browse = wx.Button(self.bkg4, label=' 浏览 ')
        self.Button_caption = wx.Button(self.bkg4, label=' 生成图像描述 ')
        self.Button_openImg = wx.Button(self.bkg4, label=' 打开图片 ')

        self.Label_path = wx.StaticText(self.bkg4, label=' 路径: ')
        self.Label_caption = wx.StaticText(self.bkg4, label=' 图像描述: ')

        self.Text_path = wx.TextCtrl(self.bkg4, value=self.selected_Path)
        self.Text_caption = wx.TextCtrl(self.bkg4, value='描述', style=wx.TE_MULTILINE | wx.HSCROLL)

        try:
            path_init_image = self.Text_path.GetValue()
            print path_init_image
            self.pic_im_init_f4 = wx.Image(path_init_image, wx.BITMAP_TYPE_JPEG)
            bmp_m_w = self.pic_im_init_f4.GetWidth()*0.1*10
            bmp_m_h = self.pic_im_init_f4.GetHeight()*0.1*10
            print bmp_m_w, bmp_m_h
            rew = self.img_show_heigh * (bmp_m_w / bmp_m_h)
            reh = self.img_show_heigh
            print rew, reh
            self.pic_im_init_f4 = self.pic_im_init_f4.Scale(width=rew, height=reh)
            self.pic_im_init_f4 = self.pic_im_init_f4.ConvertToBitmap()
            self.image_show_f4 = wx.StaticBitmap(self.bkg4, bitmap=self.pic_im_init_f4)
        finally:
            print 'Load init image success!'

        # 控件绑定
        self.Button_browse.Bind(wx.EVT_BUTTON, self.myBrowser)
        self.Button_openImg.Bind(wx.EVT_BUTTON, self.myOpener)
        self.Button_caption.Bind(wx.EVT_BUTTON, self.myCaption)

        # 控件布局
        self.hbox_path = wx.BoxSizer()
        self.hbox_path.Add(self.Label_path, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=10)
        self.hbox_path.Add(self.Text_path, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        self.hbox_path.Add(self.Button_browse, proportion=0, flag=wx.ALIGN_CENTER_VERTICAL, border=10)

        self.vbox_imageopbt = wx.BoxSizer(wx.VERTICAL)
        self.vbox_imageopbt.Add(self.Button_openImg, proportion=0, flag=wx.TOP | wx.ALIGN_RIGHT, border=10)
        self.vbox_imageopbt.Add(self.Button_caption, proportion=0, flag=wx.TOP | wx.BOTTOM, border=10)

        self.hbox_imageview = wx.BoxSizer()
        self.hbox_imageview.Add(self.image_show_f4, proportion=1, flag=wx.EXPAND | wx.CENTER, border=10)
        self.hbox_imageview.Add(self.vbox_imageopbt, proportion=0, flag=wx.RIGHT, border=0)

        vbox_all = wx.BoxSizer(wx.VERTICAL)
        vbox_all.Add(self.hbox_path, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox_all.Add(self.hbox_imageview, proportion=0, flag=wx.EXPAND | wx.ALL, border=10)
        vbox_all.Add(self.Label_caption, proportion=0, flag=wx.TOP | wx.BOTTOM, border=5)
        vbox_all.Add(self.Text_caption, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, border=10)

        self.bkg4.SetSizer(vbox_all)
        self.Layout()

    def myBrowser(self, event):
        fileDlg = wx.FileDialog(self, '请选择要描述的图像文件')
        if fileDlg.ShowModal() == wx.ID_OK:
            self.selected_Path = fileDlg.GetPath()
            self.Text_path.Clear()
            self.Text_path.AppendText(self.selected_Path)
            print 'File path: ', self.selected_Path
        fileDlg.Destroy()

    def myOpener(self, event):
        print 'Open image: ', self.selected_Path
        try:
            # fileKind = self.selected_Path.split('.')[-1]
            # if fileKind == 'jpg' | 'JPG':
            #     self.pic_im_init_f4 = wx.Image(self.selected_Path, wx.BITMAP_TYPE_JPEG)
            # elif fileKind == 'png' | 'PNG':
            #     self.pic_im_init_f4 = wx.Image(self.selected_Path, wx.BITMAP_TYPE_PNG)

            self.pic_im_init_f4 = wx.Image(self.selected_Path, wx.BITMAP_TYPE_ANY)
            bmp_m_w = self.pic_im_init_f4.GetWidth()*0.1*10
            bmp_m_h = self.pic_im_init_f4.GetHeight()*0.1*10
            print bmp_m_w, bmp_m_h
            rew = self.img_show_heigh * (bmp_m_w / bmp_m_h)
            reh = self.img_show_heigh
            print rew, reh
            self.pic_im_init_f4 = self.pic_im_init_f4.Scale(width=rew, height=reh)
            self.pic_im_init_f4 = self.pic_im_init_f4.ConvertToBitmap()
            self.image_show_f4.SetBitmap(self.pic_im_init_f4)
            self.hbox_imageview.Layout()
        finally:
            print 'Load image success!'

    def myCaption(self, event):
        str_cap = ''
        try:
            str_cap = viewer_back.getCaption(self.selected_Path)
        finally:
            print 'Caption end'
        self.Text_caption.Clear()
        self.Text_caption.AppendText(str_cap)

    def CloseThisWin(self, event):
        print 'Leaving Function Image Caption'
        self.Close()

    def __del__(self):
        pass


def Function_main_surveillance_start(event):
    win_m_s = MyShowFunc_main_surv(bkg_m_m)
    win_m_s.Show()

def Function_main_caption_start(event):
    win_m_c = MyShowFunc_Caption_Demo(bkg_m_m)
    win_m_c.Show()


# 主函数
if __name__ == '__main__':
    MAIN_OF_MAIN_WIDTH = 320
    MAIN_OF_MAIN_HEIGHT = 180
    try:
        app_m = wx.App()

        print 'Func Surv Main Frame Opened'
        print 'Main Frame Opened'
        win_m_m = wx.Frame(None, title='图像描述应用演示系统 V0.1')
        win_m_m.SetMaxSize((MAIN_OF_MAIN_WIDTH, MAIN_OF_MAIN_HEIGHT))
        win_m_m.Center()
        bkg_m_m = wx.Panel(win_m_m)

        # 控件创建
        BT_main_func1 = wx.Button(bkg_m_m, label='图像描述功能', pos=(30, 20), size=(120, 140))
        BT_main_func2 = wx.Button(bkg_m_m, label='行人检索功能', pos=(170, 20), size=(120, 140))

        # 控件绑定
        BT_main_func1.Bind(wx.EVT_BUTTON, Function_main_caption_start)
        BT_main_func2.Bind(wx.EVT_BUTTON, Function_main_surveillance_start)

        win_m_m.Show()

        app_m.MainLoop()

    finally:

        print 'Main Frame Closed'
