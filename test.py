import tkinter as tk
import tkinter.filedialog
import cv2
import mediapipe as mp
import time
import matplotlib.pyplot as plt
import xlrd # 解析excel
import xlwt
import numpy as np
from tkinter import messagebox


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic


# 以下代码提取一副单帧运动画面多识别的Results内的33个关节点的坐标，并以二维数据返回。
def KineDataGenerateFromVideo(paraResults):
    # 将33个关键点坐标汇总
    import numpy as np

    coords = np.array(paraResults.pose_world_landmarks.landmark)

    # 汇总所有点的XYZ坐标
    def get_x(each):
        return each.x

    def get_y(each):
        return each.y

    def get_z(each):
        return each.z

    # 分别获取关键点XYZ坐标
    points_x = np.array(list(map(get_x, coords)))
    points_y = np.array(list(map(get_y, coords)))
    points_z = np.array(list(map(get_z, coords)))

    paraKineData=np.zeros((1, 100))


    for i in range(1, 34):      #循环至34后不执行即结束，因此i最大取33
        paraKineData[0, (i - 1) * 3 + 1] = points_x[i-1]
        paraKineData[0, (i - 1) * 3 + 2] = points_y[i-1]
        paraKineData[0, (i - 1) * 3 + 3] = points_z[i-1]

    return paraKineData

# ------以上代码提取一副单帧运动画面多识别的Results内的33个关节点的坐标，并以二维数据返回。


# 以下代码定义视频关节点识别和播放函数
def BodyJointIdentifyAndDisplay(capGlobal):
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_holistic = mp.solutions.holistic

    videoPicNum = 0

    with (mp_holistic.Holistic(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as holistic):

        paraKineDatas = np.zeros((0, 100))
        while capGlobal.isOpened():
            success, image = capGlobal.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # 如果视频播放结束，则结束循环
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            videoPicNum = videoPicNum + 1  # 当前处理的视频帧号
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = holistic.process(image)

            # 画图
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            mp_drawing.draw_landmarks(
                image,
                results.pose_landmarks,
                mp_holistic.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing_styles
                .get_default_pose_landmarks_style())

            mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

            #cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
            cv2.imshow('MediaPipe Holistic', image)

            paraKineData=KineDataGenerateFromVideo(results)
            paraKineDatas=np.append(paraKineDatas,paraKineData,axis=0)

            #varKineDatas_global=np.append(varKineDatas_global,paraKineData,axis=0)#添加整行元素，axis=1添加整列元素

    return paraKineDatas
# --------以上代码定义视频关节点识别和播放函数


# region  以下代码定义菜单映射函数
def onRightClick(event):
    # 弹出菜单
    menu.post(event.x_root, event.y_root)


def mnuOpenCampEvent():
    cap = cv2.VideoCapture(0)
    global varKineDatasGlobal
    varKineDatasGlobal = BodyJointIdentifyAndDisplay(cap)


# 以下代码定义点击”打开视频“菜单的响应函数
def mnuOpenVideoEvent():
    ss = tkinter.filedialog.askopenfilename(title='请选择一个文件', initialdir=r'D:\PythonProject', filetypes=[("mov文件", ".mov"), ("avi文件", ".avi"), ("All Files", '*')], defaultextension='.tif', multiple=False)
    cap = cv2.VideoCapture(ss)  # 读取视频
    global varKineDatasGlobal
    varKineDatasGlobal = BodyJointIdentifyAndDisplay(cap)
    # varKineDatasGlobal=np.append(varKineDatasGlobal,varData,axis=0)
    print('aaaaaaaaaa')
# ----------以上代码定义点击”打开视频“菜单的响应函数


def mnuCloseCampAndVideoEvent():
    return


# 运动学数据导出函数
def mnuKineDataExportEvent():
    if varKineDatasGlobal == None:
        messagebox.showinfo('信息提示', '您尚未选择视频信息')
        return
    else:
        fileNameStr = tkinter.filedialog.asksaveasfilename()    # 创建Excel文件和sheeet工作簿
        writebook = xlwt.Workbook(encoding='utf-8')  # 生成excel文件并设置编码为utf8
        sheet1 = writebook.add_sheet('Sheet1', cell_overwrite_ok=True)  # 创建第一个sheet 表单
        # 行号
        for i in range(1, len(varKineDatasGlobal[0])+1):
            # 列号
            for j in range(1, 100):
                sheet1.write(i, j, varKineDatasGlobal[i, j])  # 第i行第j列

        writebook.save(fileNameStr)    # 保存ExcelBook.save('path/文件名称.xls')
        messagebox.showinfo('信息提示', '数据已成功导出')
# endregion 以上代码定义菜单映射函数

# region   窗口的界面设计
# 创建主窗口


root = tk.Tk()
root.title("同济大学人工智能关节点识别软件")
root.geometry('1200x900+50+50')

# 创建菜单
menu = tk.Menu(root, tearoff=0)

# 添加菜单项

submenu1 = tk.Menu(menu, tearoff=0)
submenu2 = tk.Menu(menu, tearoff=0)
submenu3 = tk.Menu(menu, tearoff=0)
submenu4 = tk.Menu(menu, tearoff=0)
submenu5 = tk.Menu(menu, tearoff=0)

submenu1.add_command(label="打开摄像头", command=mnuOpenCampEvent)
submenu1.add_command(label="打开已有视频", command=mnuOpenVideoEvent)
submenu1.add_command(label="关闭视频/摄像头", command=mnuCloseCampAndVideoEvent)
submenu1.add_command(label="运动学数据导出", command=mnuKineDataExportEvent)
submenu1.add_separator()
submenu1.add_command(label="退出系统", command=root.quit)
menu.add_cascade(label="文件", menu=submenu1)

submenu2.add_command(label="关节点识别")
submenu2.add_command(label="运动学参数计算")
menu.add_cascade(label="采集", menu=submenu2)


submenu3.add_command(label="采样频率设置")
submenu3.add_command(label="视频起止点设置")
menu.add_cascade(label="设置", menu=submenu3)

submenu4.add_command(label="关节点坐标值优化")
submenu4.add_command(label="运动学参数优化")
menu.add_cascade(label="优化", menu=submenu4)

submenu5.add_command(label="使用指南")
submenu5.add_command(label="关于")
menu.add_cascade(label="帮助", menu=submenu5)

menu.add_separator()

# 设置菜单的样式
menu.config(bg="gray", fg="white", font=("Courier", 12))

# 绑定快捷键
root.bind_all("<Control-d>", lambda event: root.quit())

# 绑定鼠标右键事件
root.bind("<Button-3>", onRightClick)

# 进入消息循环
root.config(menu=menu)
root.mainloop()

# endregion  窗口的界面设计
