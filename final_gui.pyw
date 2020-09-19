# reference : https://www.jianshu.com/p/2b79012c0228
# original author ex2tron

import cv2
import pyarcface as pyarc
import public_func as pub_func
import time
import mask_detect_cnn_predict as mask_predict
import tkinter as tk
from PIL import Image, ImageTk
from tkinter.filedialog import askdirectory
import tkinter.messagebox
import os
import os.path
from datetime import datetime
from threading import Thread
from filetrans import SFTP


def exiting():
    global capture
    pyarc.ASFDeactivate()
    capture.release()
    # del capture
    if fileflag:
        global file
        file.flush()
        file.close()

def start():
    try:
        register()
        monitoring()
    except Exception as e:
        print(e)


def selectpath():
    if not stop_ask_for_path:
        path_ = askdirectory()
        path_var.set(path_)

def sync(path):
    pics = []
    files = os.listdir(path)
    for each in files:
        for name in ['jpg', 'jpeg', 'bmp', 'png']:
            if name in each.split('.')[-1].lower():
                pics.append(each)
    for each in pics:
        temp = pub_func.hashs(path + '/' + each)
        os.rename(path + '/' + each, path + '/' + temp + '.' + each.split('.')[-1])
    pics = []
    files = os.listdir(path)
    for each in files:
        for name in ['jpg', 'jpeg', 'bmp', 'png']:
            if name in each.split('.')[-1].lower():
                pics.append(each)
    sftp = SFTP()
    sftplistdir = sftp.listdir()
    downloadlist = [i for i in sftplistdir if i not in pics]
    uploadlist = [i for i in pics if i not in sftplistdir]
    for each in downloadlist:
        sftp.download('/'+each, path + '/' + each)
        lb.insert(tk.END, 'Successfully download a face file from cloud')
        time.sleep(0.5)
    for each in uploadlist:
        sftp.upload(path + '/' + each, '/' + each)
        lb.insert(tk.END, 'Successfully upload a face file to cloud')
        time.sleep(0.5)

def realtimesync():
    time.sleep(1)
    uploadlist = []
    for each in os.listdir(realpath):
        if len(each.split('.')[0]) != 32:
            for name in ['jpg', 'jpeg', 'bmp', 'png']:
                if name in each.split('.')[-1].lower():
                    temp = pub_func.hashs(realpath + '/' +each)
                    os.rename(realpath + '/' + each, realpath + '/' + temp + '.' + each.split('.')[-1])
                    uploadlist.append(temp + '.' + each.split('.')[-1])
    sftp = SFTP()
    for each in uploadlist:
        sftp.upload(realpath + '/' + each, '/' + each)
        lb.insert(tk.END, 'Successfully upload a face file to cloud')

def register():
    global file
    global fileflag
    global registered_num
    global log
    global logflag
    global realpath
    registered_num = 0
    fileflag = False
    logflag = False
    path = path_var.get()
    path = path.strip()
    realpath = path[:]
    if path == '注册脸文件夹，可留空':
        realpath = None
        return None
    if path == '':
        path = './SWJTUArcFace'
        realpath = path[:]
        path_var.set(path)
    if not os.path.exists(path) and path != './SWJTUArcFace':
        tkinter.messagebox.showerror('错误','路径不存在')
        realpath = None
        return None
    else:
        if path == './SWJTUArcFace' and not os.path.exists(path):
            os.mkdir(path)
        if not os.path.exists(path + '/' + 'FacePool'):
            tkinter.messagebox.showwarning('警告','FacePool不存在, 将自动创建')
            os.mkdir(path + '/' + 'FacePool')
    sync(path)
    pics = os.listdir(path + '/FacePool')
    for each in pics:
        os.remove(path + '/FacePool/' + each)
    pics = os.listdir(path)
    for each in pics:
        flag = False
        for name in ['jpg', 'jpeg', 'bmp', 'png']:
            if name in each.split('.')[-1].lower():
                flag = True
                break
        if flag:
            img = cv2.imread(path+ '/' + each)
            print(path + '/' + each)
            multires = pyarc.ASFDetectFaces(img, pyarc.CVIMGMODE)
            singlelist = pub_func.multiinfo2singleinfolist(multires)
            for single in singlelist:
                feature = pyarc.ASFFaceFeatureExtract(img, single, pyarc.CVIMGMODE)
                if type(feature) != int:
                    faceidlist.append(feature)
                    faceimg = img[single.faceRect.top:single.faceRect.bottom, single.faceRect.left:single.faceRect.right]
                    cv2.imwrite(path + '/FacePool/' + str(len(faceidlist) - 1) + '.' + each.split('.')[-1],faceimg)
                    facerecord.append(1)
                    lb.insert(tk.END, 'a new object registered, called NO.%d'%(len(faceidlist) - 1))
    registered_num = len(faceidlist)
    file = open(path + '/' + 'detail_log.txt', 'a')
    file.write('-'*20 + '\n')
    file.write('Start logging at: ' + time.ctime())
    file.write('\n')
    file.flush()
    fileflag = True

    log = open(path + '/' + 'log.txt','a')
    log.write('-'*20 + '\n')
    log.write('Start logging at: ' + time.ctime())
    log.write('\n')
    log.flush()
    logflag = True
                    


def monitoring():
    global stop_ask_for_path
    global capture
    stop_ask_for_path = True
    path = path_var.get()
    path = path.strip()
    capture = cv2.VideoCapture(cam_num)
    rectangle_colour = ([0,0,0], [0,0,255])
    i = 0
    net = mask_predict.Net()
    net.load()
    # while loop produce every frame
    text_display = 'Unknown object'
    while True:
        log_write = False
        t0 = time.time()
        ret, frame = capture.read()
        fresh_frame = frame.copy()
        if frame is None or frame.sum() == 0:
            pass
        #choose some frames to get detail
        if i % 10 == 0:
            timing = 'ON     '
            multires = pyarc.ASFDetectFaces(frame, pyarc.CVIMGMODE)
            pyarc.ASFProcess(frame, multires, pyarc.CVIMGMODE)
            genderinfo = pyarc.ASFGetGender()
            ageinfo = pyarc.ASFGetAge()
            face3dangle = pyarc.ASFGetFace3DAngle()
            livenessinfo = pyarc.ASFGetLivenessScore()
            singlecomprehensiveinfolist = pub_func.allinfo2siglecomprehensiveinfo2(multires, ageinfo, genderinfo,
                                                                                  livenessinfo,
                                                                                  face3dangle)
            #singleinfolist = pub_func.multiinfo2singleinfolist(multires)
            try:
                for each in singlecomprehensiveinfolist:
                    each_single = each.single
                    each_feature = pyarc.ASFFaceFeatureExtract(fresh_frame, each_single, pyarc.CVIMGMODE)
                    # cv2.imwrite('temp.jpg', fresh_frame)
                    position = each.single.faceRect
                    left = position.left
                    right = position.right
                    up = position.top
                    down = position.bottom



                    
                    img = frame[up:down, left:right]
                    if img.sum != 0:
                        img = cv2.resize(img, (64, 64))
                        ismasked = net.predict(img)
                    if type(each_feature) != int or type(each_feature) != float:
                        for i, faceid in enumerate(faceidlist):
                            confidentlevel = pyarc.ASFFaceFeatureCompare(each_feature, faceid)
                            if 0.5 <= confidentlevel <= 1.0:
                                idnum = faceidlist.index(faceid)
                                if facerecord[i]:
                                    log_write = True
                                    facerecord[i] = 0
                                break
                        else:
                            faceidlist.append(each_feature)
                            idnum = len(faceidlist) - 1
                            cv2.imwrite(path + '/' + str(len(faceidlist) - 1) + '.jpg', fresh_frame)
                            faceimg = fresh_frame[up:down, left:right]
                            cv2.imwrite(path + '/FacePool/' + str(len(faceidlist) - 1) + '.jpg',faceimg)
                            threading = Thread(target=realtimesync)
                            threading.start()
                            lb.insert(tk.END, 'a new object detected, called NO.%d'%(len(faceidlist) - 1))
                            facerecord.append(0)
                            log_write = True
                    else:
                        idnum = -1
                        lb.insert(tk.END, 'low confident')
                        print(each_feature)
                    if idnum == -1:
                        text_display = 'low confident'
                    elif idnum < registered_num:  
                        text_display = 'registered'
                    else:
                        text_display = 'Unknown object'
                    texting = 'faceOrient:%d\nage:%d\ngender:%d\nisLive:%d\nroll:%d\nyaw:%d\npitch:%d\nstatus:%d\nismasked:%d\nidnum:%d\n' % (
                                each.single.faceOrient, each.age, each.gender, each.isLive, each.roll, each.yaw, each.pitch, each.status, ismasked, idnum)
                    if fileflag:
                        file.write(texting.replace('\n', ','))
                        file.write('time:'+datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                        file.write('\n')
                        file.flush()
                    if logflag:
                        if log_write:
                            log.write(texting.replace('\n', ','))
                            log.write('time:'+datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3])
                            log.write('\n')
                            log.flush()
                            log_write = False
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    frame = pub_func.draw_text_line(frame, (left, up), text_display)



                    if ismasked:
                        square_color = rectangle_colour[0]
                    else:
                        square_color = rectangle_colour[1]
                    #  Northwest to Northeast
                    #  Southwest to Southeast
                    for i in range(left, right + 1):
                        frame[up][i] = square_color
                        frame[down][i] = square_color
                    #  Northwest to Southwest
                    #  Northeast to Southeast
                    for i in range(up, down + 1):
                        frame[i][left] = square_color
                        frame[i][right] = square_color
                        
            except Exception as e:
                print(e)
                #cv2.imwrite('temp.jpg', frame)

        #other frame using previous result
        else:
            timing = 'OFF    '
            multi = pyarc.ASFDetectFaces(frame, pyarc.CVIMGMODE)
            singleinfolist = pub_func.multiinfo2singleinfolist(multi)
            try:
                for each in singleinfolist:
                    position = each.faceRect
                    left = position.left
                    right = position.right
                    up = position.top
                    down = position.bottom
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    frame = pub_func.draw_text_line(frame, (left, up), text_display)




                    if ismasked:
                        square_color = rectangle_colour[0]
                    else:
                        square_color = rectangle_colour[1]
                    #  Northwest to Northeast
                    #  Southwest to Southeast
                    for i in range(left, right + 1):
                        frame[up][i] = square_color
                        frame[down][i] = square_color
                    #  Northwest to Southwest
                    #  Northeast to Southeast
                    for i in range(up, down + 1):
                        frame[i][left] = square_color
                        frame[i][right] = square_color
            except Exception as e:
                print(e)
                
        t1 = time.time()
        timing += '%.2f/fps' % (1/(t1 - t0 + 0.0001))
        frame = pub_func.draw_text(frame, (0,0), timing)
        #cv2.imshow('Stream media', frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        showimg=Image.fromarray(frame)
        showimg=ImageTk.PhotoImage(showimg)

        canvas.create_image(0,0,anchor='nw',image=showimg)
        root.update_idletasks()
        root.update()
    
# init
cam_num = 'test.avi'
capture = cv2.VideoCapture(cam_num)
ret, frame = capture.read()
height, width = frame.shape[:-1]
del capture
stop_ask_for_path = False

print(height, width)

faceidlist = []
facerecord = []

appid, sdkkey = "HTuiwqWmNdJ8EYp7q49H1KW3GT41vwmoLxSWcZM9eHDN", "6hG1AUuvdmHVeBSvMhEyJDv47FsGBjJCfWjRD92Xi64A"
pyarc.ASFSetPath()
pyarc.ASFSetLicence(appid, sdkkey)
pyarc.ASFAllActivate()

root = tk.Tk()
root.geometry("1067x561+200+200")
root.iconbitmap('icon.ico')
root.title('ArcFace Webcam Monitor - SWJTU')
canvas = tk.Canvas(root,width=width,height=height)


path_var = tk.StringVar()
path_box = tk.Entry(root, textvariable = path_var, validate="focusin", validatecommand=selectpath)
path_box.insert(tk.END, '注册脸文件夹，可留空')


start_button = tk.Button(root, text='开始监控', command=start)


lb = tk.Listbox(root, width=40)
scr = tk.Scrollbar(root)

lb.config(yscrollcommand=scr.set)
scr.config(command=lb.yview)
scr.pack(side=tk.RIGHT, fill=tk.Y)
lb.pack(side=tk.RIGHT, fill=tk.Y)
canvas.pack()
path_box.pack()
start_button.pack()

root.mainloop()
