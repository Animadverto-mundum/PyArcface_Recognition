from arc_struct import *
from ctypes import *
from enum import Enum


def setpath(face_dll_path, face_engine_dll_path):
    face_dll = CDLL(face_dll_path)
    face_engine_dll = CDLL(face_engine_dll_path)
    globals().update(locals())


ASF_DETECT_MODE_VIDEO = 0x00000000
ASF_DETECT_MODE_IMAGE = 0xFFFFFFFF

ASF_NONE = 0x00000000
ASF_FACE_DETECT = 0x00000001
ASF_FACE_RECOGNITION = 0x00000004
ASF_AGE = 0x00000008
ASF_GENDER = 0x00000010
ASF_FACE3DANGLE = 0x00000020
ASF_LIVENESS = 0x00000080
ASF_IR_LIVENESS = 0x00000400

ASVL_PAF_RGB24_B8G8R8 = 0x201


class ArcSoftFaceOrientPriority(Enum):
    ASF_OP_0_ONLY = 0x1,
    ASF_OP_90_ONLY = 0x2,
    ASF_OP_270_ONLY = 0x3,
    ASF_OP_180_ONLY = 0x4,
    ASF_OP_0_HIGHER_EXT = 0x5,

def setfunc():
    # face_engine_dll = 0
    # 3.5.3 to activate the engine
    activate = face_engine_dll.ASFActivation
    activate.restype = c_int32
    activate.argtypes = (c_char_p, c_char_p)

    # 3.5.4 to initialise the engine
    init_engine = face_engine_dll.ASFInitEngine
    init_engine.restype = c_int32
    init_engine.argtypes = (c_long, c_int32, c_int32, c_int32, c_int32, POINTER(c_void_p))

    # 3.5.5 to recognise the faces in given image
    detect_face = face_engine_dll.ASFDetectFaces
    detect_face.restype = c_int32
    detect_face.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte), POINTER(ASFMultiFaceInfo))

    # 3.5.6 to recognise the faces in given image with structure parameter
    # NOT available

    # 3.5.7 to extract feature of SINGLE face
    # NOT available
    extract_feature = face_engine_dll.ASFFaceFeatureExtract
    extract_feature.restype = c_int32
    extract_feature.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte),
                                POINTER(ASFSingleFaceInfo), POINTER(ASFFaceFeature))

    # 3.5.8 to extract feature of SINGLE face with structure parameter
    extract_feature_ex = face_engine_dll.ASFFaceFeatureExtractEx
    extract_feature_ex.restype = c_int32
    extract_feature_ex.argtypes = (c_void_p, POINTER(c_ubyte),
                                POINTER(ASFSingleFaceInfo), POINTER(ASFFaceFeature))


    # 3.5.9 to compare 2 faces and return similarity percentage
    # NOT available
    compare_feature = face_engine_dll.ASFFaceFeatureCompare
    compare_feature.restype = c_int32
    compare_feature.argtypes = (c_void_p, POINTER(ASFFaceFeature),
                                POINTER(ASFFaceFeature), POINTER(c_float))

    # 3.5.10 to set liveness threshold value with default RGB：0.5   IR：0.7
    set_liveness_param = face_engine_dll.ASFSetLivenessParam
    set_liveness_param.restype = c_int32
    set_liveness_param.argtypes = (c_void_p, POINTER(ASFLivenessThreshold))

    # 3.5.11 to recognise face feature
    # UNKNOWN MANUAL DESCRIPTION
    # NOT available
    process = face_engine_dll.ASFProcess
    process.restype = c_int32
    process.argtypes = (c_void_p, c_int32, c_int32, c_int32, POINTER(c_ubyte),
                        POINTER(ASFMultiFaceInfo), c_int32)

    # 3.5.13 to get the age of faces
    # NOT available
    get_age = face_engine_dll.ASFGetAge
    get_age.restype = c_int32
    get_age.argtypes = (c_void_p, POINTER(ASFAgeInfo))


    # 3.5.14 to get the gender of faces
    # NOT available
    get_gender = face_engine_dll.ASFGetGender
    get_gender.restype = c_int32
    get_gender.argtypes = (c_void_p, POINTER(ASFGenderInfo))


    # 3.5.15 to get the spacial 3d angle
    # NOT available
    get_3d_angle = face_engine_dll.ASFGetFace3DAngle
    get_3d_angle.restype = c_int32
    get_3d_angle.argtypes = (c_void_p, POINTER(ASFFace3DAngle))


    # 3.5.16 to evaluate the liveness of faces
    # NOT available
    get_liveness_score = face_engine_dll.ASFGetLivenessScore
    get_liveness_score.restype = c_int32
    get_liveness_score.argtypes = (c_void_p, POINTER(ASFLivenessInfo))

    # 3.5.21 de-activate the engine
    # NOT available
    de_activate = face_engine_dll.ASFUninitEngine
    de_activate.restype = c_int32
    de_activate.argtypes = (c_void_p,)
    globals().update(locals())
