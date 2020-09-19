from PIL import Image
import os.path
import cv2
# from ctypes import *
import arc_struct
import hashlib

def transpictype(path, type_name):
    I = Image.open(path)
    out_path = os.path.dirname(path)
    out_path += os.path.splitext(os.path.basename(path)[0])
    out_path += '.' + type_name
    I.save(out_path)


class Pic:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.imageData = None

class ASFSingleComprehensiveInfo2:
    def __init__(self):
        self.singleinfo = arc_struct.ASFSingleFaceInfo()
        self.age = -9
        self.gender = -9
        self.isLive = -9
        self.roll = -9
        self.yaw = -9
        self.pitch = -9
        self.status = -9


def load_image(file_path):
    img = cv2.imread(file_path)
    sp = img.shape
    img = cv2.resize(img, (sp[1] // 4 * 4, sp[0]// 4 * 4))  # 四字节对齐
    image = Pic()
    image.width = img.shape[1]
    image.height = img.shape[0]
    image.imageData = img
    return image


def pack_image(img):
    sp = img.shape
    img = cv2.resize(img, (sp[1] // 4 * 4, sp[0]// 4 * 4))  # 四字节对齐
    image = Pic()
    image.width = img.shape[1]
    image.height = img.shape[0]
    image.imageData = img
    return image


def multiinfo2singleinfolist(multi):
    num = multi.faceNum
    single_list = []
    for _ in range(num):
        temp = arc_struct.ASFSingleFaceInfo()
        temp.faceRect = multi.faceRect[_]
        temp.faceOrient = multi.faceOrient[_]
        single_list.append(temp)
    return single_list


def allinfo2siglecomprehensiveinfo(multifaceinfo, ageinfo, genderinfo, livenessinfo, face3dangle):
    num = multifaceinfo.faceNum
    single_list = []
    for _ in range(num):
        temp = arc_struct.ASFSingleComprehensiveInfo()
        temp.faceRect = multifaceinfo.faceRect[_]
        temp.faceOrient = multifaceinfo.faceOrient[_]
        if ageinfo is not None and type(ageinfo) != int:
            temp.age = ageinfo.ageArray[_]
        if genderinfo is not None and type(genderinfo) != int:
            temp.gender = genderinfo.genderArray[_]
        if livenessinfo is not None and type(livenessinfo) != int:
            temp.isLive = livenessinfo.isLive[_]
        if face3dangle is not None and type(face3dangle) != int:
            temp.roll = face3dangle.roll[_]
            temp.yaw = face3dangle.yaw[_]
            temp.pitch = face3dangle.pitch[_]
            temp.status = face3dangle.status[_]
        single_list.append(temp)
    return single_list

def allinfo2siglecomprehensiveinfo2(multifaceinfo, ageinfo, genderinfo, livenessinfo, face3dangle):
    num = multifaceinfo.faceNum
    single_list = []
    for _ in range(num):
        temp = ASFSingleComprehensiveInfo2()
        temp.single = arc_struct.ASFSingleFaceInfo()
        temp.single.faceRect = multifaceinfo.faceRect[_]
        temp.single.faceOrient = multifaceinfo.faceOrient[_]
        if ageinfo is not None and type(ageinfo) != int:
            temp.age = ageinfo.ageArray[_]
        if genderinfo is not None and type(genderinfo) != int:
            temp.gender = genderinfo.genderArray[_]
        if livenessinfo is not None and type(livenessinfo) != int:
            temp.isLive = livenessinfo.isLive[_]
        if face3dangle is not None and type(face3dangle) != int:
            temp.roll = face3dangle.roll[_]
            temp.yaw = face3dangle.yaw[_]
            temp.pitch = face3dangle.pitch[_]
            temp.status = face3dangle.status[_]
        single_list.append(temp)
    return single_list



'''
<
版权声明：本文为CSDN博主「pan_jinquan」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/guyuealian/article/details/103498851
>
'''

def draw_text(img, point, text, drawType="custom"):
    '''
    :param img:
    :param point:
    :param text:
    :param drawType: custom or custom
    :return:
    '''
    fontScale = 0.4
    thickness = 5
    text_thickness = 1
    bg_color = (255, 0, 0)
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    if drawType == "custom":
        text_size, baseline = cv2.getTextSize(str(text), fontFace, fontScale, thickness)
        text_loc = (point[0], point[1] + text_size[1])
        cv2.rectangle(img, (text_loc[0] - 2 // 2, text_loc[1] - 2 - baseline),
                      (text_loc[0] + text_size[0], text_loc[1] + text_size[1]), bg_color, -1)
        # draw score value
        cv2.putText(img, str(text), (text_loc[0], text_loc[1] + baseline), fontFace, fontScale,
                    (255, 255, 255), text_thickness, 8)
    elif drawType == "simple":
        cv2.putText(img, '%d' % (text), point, fontFace, 0.5, (255, 0, 0))
    return img
 
 
def draw_text_line(img, point, text_line: str, drawType="custom"):
    '''
    :param img:
    :param point:
    :param text:
    :param drawType: custom or custom
    :return:
    '''
    fontScale = 0.4
    thickness = 5
    fontFace = cv2.FONT_HERSHEY_SIMPLEX
    # fontFace=cv2.FONT_HERSHEY_SIMPLEX
    text_line = text_line.split("\n")
    # text_size, baseline = cv2.getTextSize(str(text_line), fontFace, fontScale, thickness)
    text_size, baseline = cv2.getTextSize(str(text_line), fontFace, fontScale, thickness)
    for i, text in enumerate(text_line):
        if text:
            draw_point = [point[0], point[1] + (text_size[1] + 2 + baseline) * i]
            img = draw_text(img, draw_point, text, drawType)
    return img
'''
</
版权声明：本文为CSDN博主「pan_jinquan」的原创文章，遵循 CC 4.0 BY-SA 版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/guyuealian/article/details/103498851
>
'''


def hashs(fineName, hashs_type="md5", block_size=64 * 1024):
        """ Support md5(), sha1(), sha224(), sha256(), sha384(), sha512(), blake2b(), blake2s(),
        sha3_224, sha3_256, sha3_384, sha3_512, shake_128, and shake_256
        """
        with open(fineName, 'rb') as file:
                hash = hashlib.new(hashs_type, b"")
                while True:
                        data = file.read(block_size)
                        if not data:
                                break
                        hash.update(data)
        return hash.hexdigest()
