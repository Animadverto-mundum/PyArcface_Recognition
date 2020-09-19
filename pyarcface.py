import arc_func
import os.path
from arc_struct import *
import public_func as pub_func
from ctypes import *

app_id = None
sdk_key = None
engine = 0
PATHMODE = 0
CVIMGMODE = 1

dft_face_dll_path = os.path.dirname(__file__) + r"/ArcFaceV3/lib/X64/libarcsoft_face.dll"
dft_face_engine_dll_path = os.path.dirname(__file__) + r"/ArcFaceV3/lib/X64/libarcsoft_face_engine.dll"
c_ubyte_p = POINTER(c_ubyte)
memcpy = cdll.msvcrt.memcpy
malloc = cdll.msvcrt.malloc
malloc.restype = c_void_p
free = cdll.msvcrt.free

combined_mask = arc_func.ASF_AGE | \
                arc_func.ASF_GENDER | \
                arc_func.ASF_FACE3DANGLE | \
                arc_func.ASF_LIVENESS


def ASFSetPath(face_dll_path=dft_face_dll_path, face_engine_dll_path=dft_face_engine_dll_path):
    arc_func.setpath(face_dll_path, face_engine_dll_path)
    arc_func.setfunc()

def ASFSetLicence(appid, sdkkey):
    global app_id
    global sdk_key
    app_id = appid.encode('utf-8')
    sdk_key = sdkkey.encode('utf-8')


def ASFAllActivate(mask=arc_func.ASF_FACE_DETECT | \
                        arc_func.ASF_FACE_RECOGNITION | \
                        arc_func.ASF_AGE | \
                        arc_func.ASF_GENDER | \
                        arc_func.ASF_FACE3DANGLE | \
                        arc_func.ASF_LIVENESS):
    global engine
    ret = arc_func.activate(app_id, sdk_key)  # activate
    if ret == 0 or ret == 90114:
        pass  # print("Engine activated")
    else:
        return ret  # print("Engine NOT activated, Error code:", ret)

    engine = c_void_p()
    ret = arc_func.init_engine(arc_func.ASF_DETECT_MODE_IMAGE,
                               arc_func.ArcSoftFaceOrientPriority.ASF_OP_0_ONLY.value[0],
                               30, 10, mask, byref(engine))
    if ret == 0:
        pass
    else:
        return ret  # print("Engine NOT Initialised, Error code:", ret)


def ASFDetectFaces(inputpara, mode=PATHMODE):
    if mode == PATHMODE:
        image = pub_func.load_image(inputpara)
    elif mode == CVIMGMODE:
        image = pub_func.pack_image(inputpara)
    else:
        return 100000
    image_bytes = bytes(image.imageData)
    image_ubytes = cast(image_bytes, c_ubyte_p)
    detect_faces = ASFMultiFaceInfo()  # create a object to contain the result
    ret = arc_func.detect_face(
        engine,
        image.width,
        image.height,
        arc_func.ASVL_PAF_RGB24_B8G8R8,
        image_ubytes,
        byref(detect_faces)
    )  # introduce c function referring to manual #3.5.5 ASFDetectFaces

    if ret == 0:
        copy_detect_faces = ASFMultiFaceInfo()
        copy_detect_faces.faceNum = detect_faces.faceNum
        copy_detect_faces.faceRect = cast(malloc(sizeof(MRECT) * copy_detect_faces.faceNum), POINTER(MRECT))
        copy_detect_faces.faceOrient = cast(malloc(sizeof(c_int32)), POINTER(c_int32))
        memmove(copy_detect_faces.faceRect, detect_faces.faceRect, sizeof(MRECT) * copy_detect_faces.faceNum)
        memmove(copy_detect_faces.faceOrient, detect_faces.faceOrient, sizeof(c_int32))
        return copy_detect_faces
    else:
        return ret
    '''
    if progress ends successfully, return result object
    else return the error code, referring to manual#4.2
    '''


def ASFFaceFeatureExtract(inputpara, single, mode=PATHMODE):
    if mode == PATHMODE:
        image = pub_func.load_image(inputpara)
    elif mode == CVIMGMODE:
        image = pub_func.pack_image(inputpara)
    else:
        return 100000
    feature = ASFFaceFeature()
    image_bytes = bytes(image.imageData)
    image_ubytes = cast(image_bytes, c_ubyte_p)
    ret = arc_func.extract_feature(
        engine,
        int(image.width),
        int(image.height),
        arc_func.ASVL_PAF_RGB24_B8G8R8,
        image_ubytes,
        byref(single),
        byref(feature),
    )
    if ret == 0:
        copy_feature = ASFFaceFeature()
        copy_feature.featureSize = feature.featureSize
        copy_feature.feature = malloc(feature.featureSize)
        memmove(copy_feature.feature, feature.feature, feature.featureSize)
        return copy_feature 
    else:
        return ret



def ASFFaceFeatureCompare(feature_0, feature_1):
    confidenceLevel = c_float()
    ret = arc_func.compare_feature(
        engine,
        byref(feature_0),
        byref(feature_1),
        byref(confidenceLevel),
    )
    if ret == 0:
        return confidenceLevel.value
    else:
        return int(ret)


def ASFProcess(inputpara, multi, mode=PATHMODE):
    if mode == PATHMODE:
        image = pub_func.load_image(inputpara)
    elif mode == CVIMGMODE:
        image = pub_func.pack_image(inputpara)
    else:
        return 100000
    image_bytes = bytes(image.imageData)
    image_ubytes = cast(image_bytes, c_ubyte_p)
    ret = arc_func.process(
        engine,
        image.width,
        image.height,
        arc_func.ASVL_PAF_RGB24_B8G8R8,
        image_ubytes,
        byref(multi),
        combined_mask,
    )
    return ret
    '''
    return the error code
    CAUTION:if next 3 function is called, this function need to be called first
    '''


def ASFGetGender():
    gender = ASFGenderInfo()
    ret = arc_func.get_gender(engine, byref(gender))
    if ret == 0:
        return gender
    else:
        return ret
    '''
    if progress ends successfully, return result object
    else return the error code, referring to manual#4.2
    '''


def ASFGetAge():
    age = ASFAgeInfo()
    ret = arc_func.get_age(engine, byref(age))
    if ret == 0:
        return age
    else:
        return ret
    '''
    if progress ends successfully, return result object
    else return the error code, referring to manual#4.2
    '''


def ASFGetFace3DAngle():
    angle = ASFFace3DAngle()
    ret = arc_func.get_3d_angle(engine, byref(angle))
    if ret == 0:
        return angle
    else:
        return ret
    '''
    if progress ends successfully, return result object
    else return the error code, referring to manual#4.2
    '''


def ASFGetLivenessScore():
    liveness = ASFLivenessInfo()
    ret = arc_func.get_liveness_score(engine, byref(liveness))
    if ret == 0:
        return liveness
    else:
        return ret
    '''
    if progress ends successfully, return result object
    else return the error code, referring to manual#4.2
    '''


def ASFDeactivate():
    ret = arc_func.de_activate(engine)
    return ret
    '''
    de-activate the engine
    '''
