LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)

LOCAL_MODULE := checkseapp
LOCAL_MODULE_TAGS := optional
LOCAL_C_INCLUDES := external/selinux/libsepol/include/
LOCAL_CFLAGS := -DLINK_SEPOL_STATIC -Wall -Werror
LOCAL_SRC_FILES := check_seapp.c
LOCAL_STATIC_LIBRARIES := libsepol
LOCAL_CXX_STL := none

include $(BUILD_HOST_EXECUTABLE)

###################################
include $(CLEAR_VARS)

LOCAL_MODULE := checkfc
LOCAL_MODULE_TAGS := optional
LOCAL_C_INCLUDES := external/selinux/libsepol/include \
                    external/libselinux/include
LOCAL_CFLAGS := -Wall -Werror
LOCAL_SRC_FILES := checkfc.c
LOCAL_STATIC_LIBRARIES := libsepol libselinux
LOCAL_CXX_STL := none

include $(BUILD_HOST_EXECUTABLE)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := insertkeys.py
LOCAL_SRC_FILES := insertkeys.py
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)
###################################
include $(CLEAR_VARS)

LOCAL_MODULE := sepolicy-check
LOCAL_MODULE_TAGS := optional
LOCAL_C_INCLUDES := external/selinux/libsepol/include
LOCAL_CFLAGS := -Wall -Werror
LOCAL_SRC_FILES := sepolicy-check.c
LOCAL_STATIC_LIBRARIES := libsepol
LOCAL_CXX_STL := none

include $(BUILD_HOST_EXECUTABLE)

###################################
include $(CLEAR_VARS)

LOCAL_MODULE := typeofparse.py
LOCAL_SRC_FILES := typeofparse.py
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)


##################################
include $(CLEAR_VARS)

LOCAL_MODULE := seinfo.sh
LOCAL_SRC_FILES := seinfo.sh
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := negationShrink
LOCAL_SRC_FILES := negationShrink
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := addAttrsToPolicy
LOCAL_SRC_FILES := addAttrsToPolicy
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := addAttrToTypeFile
LOCAL_SRC_FILES := addAttrToTypeFile
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := attributeinfo
LOCAL_SRC_FILES := attributeinfo
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := attrListToTypeDef
LOCAL_SRC_FILES := attrListToTypeDef
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := compareBinPolicies
LOCAL_SRC_FILES := compareBinPolicies
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := domainsFromPattern
LOCAL_SRC_FILES := domainsFromPattern
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := negationPatterns
LOCAL_SRC_FILES := negationPatterns
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := patternToAttr
LOCAL_SRC_FILES := patternToAttr
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := policyFixWhitespace
LOCAL_SRC_FILES := policyFixWhitespace
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := typeDefLine
LOCAL_SRC_FILES := typeDefLine
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)


##################################
include $(CLEAR_VARS)

LOCAL_MODULE := md5sum.py
LOCAL_SRC_FILES := md5sum.py
LOCAL_MODULE_CLASS := EXECUTABLES
LOCAL_IS_HOST_MODULE := true
LOCAL_MODULE_TAGS := optional

include $(BUILD_PREBUILT)

include $(call all-makefiles-under,$(LOCAL_PATH))
