from ctypes import *

c_ubyte_p = POINTER(c_ubyte)
memcpy = cdll.msvcrt.memcpy
malloc = cdll.msvcrt.malloc
malloc.restype = c_void_p
free = cdll.msvcrt.free


class MRECT(Structure):  # 人脸框
    _fields_ = [(u'left', c_int32),
                (u'top', c_int32),
                (u'right', c_int32),
                (u'bottom', c_int32)]


class ASFVersion(Structure):  # 版本信息 版本号 构建日期 版权说明
    _fields_ = [
        ('Version', c_char_p),
        ('BuildDate', c_char_p),
        ('CopyRight', c_char_p)]


class ASFSingleFaceInfo(Structure):  # 单人脸信息 人脸框 人脸角度 only for image
    _fields_ = [
        ('faceRect', MRECT),
        ('faceOrient', c_int32)]


class ASFMultiFaceInfo(Structure):  # 多人脸信息 人脸框数组 人脸角度数组 人脸数 only for image
    _fields_ = [
        (u'faceRect', POINTER(MRECT)),
        (u'faceOrient', POINTER(c_int32)),
        (u'faceNum', c_int32)]


class ASFFaceFeature(Structure):  # 人脸特征 人脸特征 人脸特征长度
    _fields_ = [
        ('feature', c_void_p),   # c_void_p
        ('featureSize', c_int32)]


class ASFAgeInfo(Structure):  # 年龄
    _fields_ = [
        (u'ageArray', POINTER(c_int32)),   # c_void_p
        (u'num', c_int32)]


class ASFGenderInfo(Structure):  # 性别
    _fields_ = [
        (u'genderArray', POINTER(c_int)),   # c_void_p
        (u'num', c_int32)]


class ASFFace3DAngle(Structure):  # 人脸角度信息
    _fields_ = [
        ('roll', POINTER(c_float)),  
        ('yaw', POINTER(c_float)),  
        ('pitch', POINTER(c_float)),   
        ('status', POINTER(c_int32)), 
        ('num', POINTER(c_int32))]  


class ASFLivenessThreshold(Structure):  # 活体阈值
    _fields_ = [
        (u'thresholdmodel_BGR', c_float),
        (u'thresholdmodel_IR', c_float)]  # c_int32


class ASFLivenessInfo(Structure):  # 活体信息
    _fields_ = [
        (u'isLive', POINTER(c_int32)),  # c_void_p
        (u'num', c_int32)]

class ASFSingleComprehensiveInfo(Structure):   # 综合信息
    _fields_ = [
        ('faceRect', MRECT),
        ('faceOrient', c_int32),
        ('age', c_int32),
        ('gender', c_int32),
        ('isLive', c_int32),
        ('roll', c_float),  
        ('yaw', c_float),  
        ('pitch', c_float),   
        ('status', c_int32)
        ]
class ASFSingleComprehensiveInfo2(Structure):   # 综合信息2
    _fields_ = [
        ('single',ASFSingleFaceInfo),
        #('faceRect', MRECT),
        #('faceOrient', c_int32),
        ('age', c_int32),
        ('gender', c_int32),
        ('isLive', c_int32),
        ('roll', c_float),  
        ('yaw', c_float),  
        ('pitch', c_float),   
        ('status', c_int32)
        ]
