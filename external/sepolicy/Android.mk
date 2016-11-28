LOCAL_PATH:= $(call my-dir)

include $(CLEAR_VARS)

# SELinux policy version.
# Must be <= /sys/fs/selinux/policyvers reported by the Android kernel.
# Must be within the compatibility range reported by checkpolicy -V.
POLICYVERS ?= 30

MLS_SENS=1
MLS_CATS=1024

ifdef BOARD_SEPOLICY_REPLACE
$(error BOARD_SEPOLICY_REPLACE is no longer supported; please remove from your BoardConfig.mk or other .mk file.)
endif

ifdef BOARD_SEPOLICY_IGNORE
$(error BOARD_SEPOLICY_IGNORE is no longer supported; please remove from your BoardConfig.mk or other .mk file.)
endif

ifdef BOARD_SEPOLICY_UNION
$(warning BOARD_SEPOLICY_UNION is no longer required - all files found in BOARD_SEC_SEPOLICY_DIRS are implicitly unioned; please remove from your BoardConfig.mk or other .mk file.)
endif

# Builds paths for all policy files found in BOARD_SEPOLICY_DIRS.
# $(1): the set of policy name paths to build
build_policy = $(foreach type, $(1), $(wildcard $(addsuffix /$(type), $(LOCAL_PATH) $(BOARD_SEC_SEPOLICY_DIRS))))

sepolicy_build_files := security_classes \
                        initial_sids \
                        access_vectors \
                        global_macros \
                        neverallow_macros \
                        mls_macros \
                        mls \
                        policy_capabilities \
                        te_macros \
                        attributes \
                        ioctl_macros \
                        *.te \
                        roles \
                        users \
                        initial_sid_contexts \
                        fs_use \
                        genfs_contexts \
                        port_contexts

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := sepolicy
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

sepolicy_policy.conf := $(intermediates)/policy.conf
$(sepolicy_policy.conf): PRIVATE_MLS_SENS := $(MLS_SENS)
$(sepolicy_policy.conf): PRIVATE_MLS_CATS := $(MLS_CATS)
$(sepolicy_policy.conf) : $(call build_policy, $(sepolicy_build_files))
	@mkdir -p $(dir $@)
	$(hide) m4 -D mls_num_sens=$(PRIVATE_MLS_SENS) -D mls_num_cats=$(PRIVATE_MLS_CATS) \
		-D target_build_variant=$(TARGET_BUILD_VARIANT) \
		-s $^ > $@
	$(hide) sed '/dontaudit/d' $@ > $@.dontaudit

$(LOCAL_BUILT_MODULE) : $(sepolicy_policy.conf) $(HOST_OUT_EXECUTABLES)/checkpolicy $(HOST_OUT_EXECUTABLES)/typeofparse.py $(HOST_OUT_EXECUTABLES)/negationShrink $(HOST_OUT_EXECUTABLES)/addAttrsToPolicy $(HOST_OUT_EXECUTABLES)/addAttrToTypeFile $(HOST_OUT_EXECUTABLES)/attributeinfo $(HOST_OUT_EXECUTABLES)/attrListToTypeDef $(HOST_OUT_EXECUTABLES)/compareBinPolicies $(HOST_OUT_EXECUTABLES)/domainsFromPattern $(HOST_OUT_EXECUTABLES)/negationPatterns $(HOST_OUT_EXECUTABLES)/patternToAttr $(HOST_OUT_EXECUTABLES)/policyFixWhitespace $(HOST_OUT_EXECUTABLES)/typeDefLine $(HOST_OUT_EXECUTABLES)/seinfo.sh 
	@mkdir -p $(dir $@)
	$(hide) $(HOST_OUT_EXECUTABLES)/policyFixWhitespace $< > $<.tmp
	$(hide) mv $<.tmp $<
	$(hide) python $(HOST_OUT_EXECUTABLES)/typeofparse.py -o $<.tmp $<
	$(hide) mv $<.tmp $<
	$(hide) echo Minimizing binary policy size:
	$(hide) time $(HOST_OUT_EXECUTABLES)/negationShrink -o $< -B $<
	$(hide) python $(HOST_OUT_EXECUTABLES)/typeofparse.py -o $<.dontaudit.tmp $<.dontaudit
	$(hide) mv $<.dontaudit.tmp $<.dontaudit
	$(hide) $(HOST_OUT_EXECUTABLES)/checkpolicy -M -c $(POLICYVERS) -o $@ $<
	$(hide) $(HOST_OUT_EXECUTABLES)/checkpolicy -M -c $(POLICYVERS) -o $(dir $<)/$(notdir $@).dontaudit $<.dontaudit

built_sepolicy := $(LOCAL_BUILT_MODULE)
sepolicy_policy.conf :=

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := sepolicy.recovery
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := eng

include $(BUILD_SYSTEM)/base_rules.mk

sepolicy_policy_recovery.conf := $(intermediates)/policy_recovery.conf
$(sepolicy_policy_recovery.conf): PRIVATE_MLS_SENS := $(MLS_SENS)
$(sepolicy_policy_recovery.conf): PRIVATE_MLS_CATS := $(MLS_CATS)
$(sepolicy_policy_recovery.conf) : $(call build_policy, $(sepolicy_build_files))
	@mkdir -p $(dir $@)
	$(hide) m4 -D mls_num_sens=$(PRIVATE_MLS_SENS) -D mls_num_cats=$(PRIVATE_MLS_CATS) \
		-D target_build_variant=$(TARGET_BUILD_VARIANT) \
		-D target_recovery=true \
		-s $^ > $@

$(LOCAL_BUILT_MODULE) : $(sepolicy_policy_recovery.conf) $(HOST_OUT_EXECUTABLES)/checkpolicy $(HOST_OUT_EXECUTABLES)/typeofparse.py $(HOST_OUT_EXECUTABLES)/negationShrink $(HOST_OUT_EXECUTABLES)/addAttrsToPolicy $(HOST_OUT_EXECUTABLES)/addAttrToTypeFile $(HOST_OUT_EXECUTABLES)/attributeinfo $(HOST_OUT_EXECUTABLES)/attrListToTypeDef $(HOST_OUT_EXECUTABLES)/compareBinPolicies $(HOST_OUT_EXECUTABLES)/domainsFromPattern $(HOST_OUT_EXECUTABLES)/negationPatterns $(HOST_OUT_EXECUTABLES)/patternToAttr $(HOST_OUT_EXECUTABLES)/policyFixWhitespace $(HOST_OUT_EXECUTABLES)/typeDefLine $(HOST_OUT_EXECUTABLES)/seinfo.sh 
	@mkdir -p $(dir $@)
	$(hide) $(HOST_OUT_EXECUTABLES)/policyFixWhitespace $< > $<.tmp
	$(hide) mv $<.tmp $<
	$(hide) python $(HOST_OUT_EXECUTABLES)/typeofparse.py -o $<.tmp $<
	$(hide) mv $<.tmp $<

	$(hide) echo Minimizing binary policy size:
	$(hide) time $(HOST_OUT_EXECUTABLES)/negationShrink -o $< -B $<
	
	$(hide) $(HOST_OUT_EXECUTABLES)/checkpolicy -M -c $(POLICYVERS) -o $@ $<

built_sepolicy_recovery := $(LOCAL_BUILT_MODULE)
sepolicy_policy_recovery.conf :=

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := general_sepolicy.conf
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := tests

include $(BUILD_SYSTEM)/base_rules.mk

exp_sepolicy_build_files :=\
  $(wildcard $(addprefix $(LOCAL_PATH)/, $(sepolicy_build_files)))

$(LOCAL_BUILT_MODULE): PRIVATE_MLS_SENS := $(MLS_SENS)
$(LOCAL_BUILT_MODULE): PRIVATE_MLS_CATS := $(MLS_CATS)
$(LOCAL_BUILT_MODULE): $(exp_sepolicy_build_files)
	mkdir -p $(dir $@)
	$(hide) m4 -D mls_num_sens=$(PRIVATE_MLS_SENS) -D mls_num_cats=$(PRIVATE_MLS_CATS) \
		-D target_build_variant=user \
		-s $^ > $@
	$(hide) sed '/dontaudit/d' $@ > $@.dontaudit

GENERAL_SEPOLICY_POLICY.CONF = $(LOCAL_BUILT_MODULE)

exp_sepolicy_build_files :=

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := file_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

ALL_FC_FILES := $(call build_policy, file_contexts)

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE):  $(ALL_FC_FILES) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $(ALL_FC_FILES) > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc $(PRIVATE_SEPOLICY) $@

built_fc := $(LOCAL_BUILT_MODULE)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := general_file_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := tests

include $(BUILD_SYSTEM)/base_rules.mk

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE) : $(addprefix $(LOCAL_PATH)/, file_contexts) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $< > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc $(PRIVATE_SEPOLICY) $@

GENERAL_FILE_CONTEXTS := $(LOCAL_BUILT_MODULE)

##################################
include $(CLEAR_VARS)
LOCAL_MODULE := seapp_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

seapp_contexts.tmp := $(intermediates)/seapp_contexts.tmp
$(seapp_contexts.tmp): $(call build_policy, seapp_contexts)
	@mkdir -p $(dir $@)
	$(hide) m4 -s $^ > $@

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE) : $(seapp_contexts.tmp) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkseapp
	@mkdir -p $(dir $@)
	$(HOST_OUT_EXECUTABLES)/checkseapp -p $(PRIVATE_SEPOLICY) -o $@ $<

built_sc := $(LOCAL_BUILT_MODULE)
seapp_contexts.tmp :=

##################################
include $(CLEAR_VARS)
LOCAL_MODULE := general_seapp_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := tests

include $(BUILD_SYSTEM)/base_rules.mk

general_seapp_contexts.tmp := $(intermediates)/general_seapp_contexts.tmp
$(general_seapp_contexts.tmp): $(addprefix $(LOCAL_PATH)/, seapp_contexts)
	@mkdir -p $(dir $@)
	$(hide) m4 -s $^ > $@

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE) : $(general_seapp_contexts.tmp) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkseapp
	@mkdir -p $(dir $@)
	$(HOST_OUT_EXECUTABLES)/checkseapp -p $(PRIVATE_SEPOLICY) -o $@ $<

GENERAL_SEAPP_CONTEXTS := $(LOCAL_BUILT_MODULE)
general_seapp_contexts.tmp :=

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := property_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

ALL_PC_FILES := $(call build_policy, property_contexts)

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE):  $(ALL_PC_FILES) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $(ALL_PC_FILES) > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc -p $(PRIVATE_SEPOLICY) $@

built_pc := $(LOCAL_BUILT_MODULE)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := general_property_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := tests

include $(BUILD_SYSTEM)/base_rules.mk

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE) : $(addprefix $(LOCAL_PATH)/, property_contexts) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $< > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc -p $(PRIVATE_SEPOLICY) $@

GENERAL_PROPERTY_CONTEXTS := $(LOCAL_BUILT_MODULE)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := service_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

ALL_SVC_FILES := $(call build_policy, service_contexts)

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE):  $(ALL_SVC_FILES) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $(ALL_SVC_FILES) > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc -p $(PRIVATE_SEPOLICY) $@

built_svc := $(LOCAL_BUILT_MODULE)

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := general_service_contexts
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := tests

include $(BUILD_SYSTEM)/base_rules.mk

$(LOCAL_BUILT_MODULE): PRIVATE_SEPOLICY := $(built_sepolicy)
$(LOCAL_BUILT_MODULE) : $(addprefix $(LOCAL_PATH)/, service_contexts) $(built_sepolicy) $(HOST_OUT_EXECUTABLES)/checkfc
	@mkdir -p $(dir $@)
	$(hide) m4 -s $< > $@
	$(hide) $(HOST_OUT_EXECUTABLES)/checkfc -p $(PRIVATE_SEPOLICY) $@

GENERAL_SERVICE_CONTEXTS := $(LOCAL_BUILT_MODULE)

##################################
ifeq ($(SEC_SELINUX), true)
include $(CLEAR_VARS)

LOCAL_MODULE := publiccert.pem
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

ifeq ($(TARGET_BUILD_VARIANT), eng)	
   ALL_PEM_FILES := $(call build_policy, publiccert_eng.pem)
else
   ALL_PEM_FILES := $(call build_policy, publiccert.pem)
endif

$(LOCAL_BUILT_MODULE) : $(ALL_PEM_FILES)
	@mkdir -p $(dir $@)
	@cp -f $(ALL_PEM_FILES) $@ 
endif

##################################
ifeq ($(SEC_SELINUX), true)
include $(CLEAR_VARS)

LOCAL_MODULE := audit_filter_table
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_OUT_ETC)/security

include $(BUILD_SYSTEM)/base_rules.mk

AUDIT_FILTER_FILE := $(call build_policy, audit_filter_table)

$(LOCAL_BUILT_MODULE) : $(AUDIT_FILTER_FILE)
	@mkdir -p $(dir $@)
	@cp -f $(AUDIT_FILTER_FILE) $@ 
endif

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := authorize.xml
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_OUT_ETC)/security

include $(BUILD_SYSTEM)/base_rules.mk

ALL_AUTH_FILES := $(call build_policy, authorize.xml)

$(LOCAL_BUILT_MODULE) : $(ALL_AUTH_FILES)
	@mkdir -p $(dir $@)
	@cp -f $(ALL_AUTH_FILES) $@ 

##################################
include $(CLEAR_VARS)

LOCAL_MODULE := mac_permissions.xml
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_OUT_ETC)/security

include $(BUILD_SYSTEM)/base_rules.mk

### correct signing key for PBS User Build
ifdef SEC_RELEASE_KEY_DIR
ifeq ($(SEC_RELEASE_KEY_DIR),)
SEC_BUILD_SEPOLICY_SIGN := eng
else
SEC_BUILD_SEPOLICY_SIGN := $(TARGET_BUILD_VARIANT)
endif
else
SEC_BUILD_SEPOLICY_SIGN := eng
endif

# Build keys.conf
mac_perms_keys.tmp := $(intermediates)/keys.tmp
$(mac_perms_keys.tmp) : $(call build_policy, keys.conf)
	@mkdir -p $(dir $@)
	$(hide) m4 -s $^ > $@

ALL_MAC_PERMS_FILES := $(call build_policy, $(LOCAL_MODULE))

$(LOCAL_BUILT_MODULE) : $(mac_perms_keys.tmp) $(HOST_OUT_EXECUTABLES)/insertkeys.py $(ALL_MAC_PERMS_FILES)
	@mkdir -p $(dir $@)
	$(hide) DEFAULT_SYSTEM_DEV_CERTIFICATE="$(dir $(DEFAULT_SYSTEM_DEV_CERTIFICATE))" \
		$(HOST_OUT_EXECUTABLES)/insertkeys.py -t $(SEC_BUILD_SEPOLICY_SIGN) -c $(TOP) $< -o $@ $(ALL_MAC_PERMS_FILES)

built_mac_perms := $(LOCAL_BUILT_MODULE)
mac_perms_keys.tmp :=
##################################
ifeq ($(SEC_SELINUX), true)
include $(CLEAR_VARS)

LOCAL_MODULE := sepolicy_version
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk

ifndef POLICY_REVISION
POLICY_REVISION := UNDEFINED_POLICY
endif

ALL_POLICY_FILES := $(built_sepolicy) $(built_sc) $(built_pc) $(built_fc) $(built_mac_perms) $(built_svc)

$(LOCAL_BUILT_MODULE) : $(ALL_POLICY_FILES) $(HOST_OUT_EXECUTABLES)/md5sum.py 
	@mkdir -p $(dir $@)
	$(HOST_OUT_EXECUTABLES)/md5sum.py -r $(POLICY_REVISION) -o $@ $(ALL_POLICY_FILES)
else
include $(CLEAR_VARS)

LOCAL_MODULE := selinux_version
LOCAL_MODULE_CLASS := ETC
LOCAL_MODULE_TAGS := optional
LOCAL_MODULE_PATH := $(TARGET_ROOT_OUT)

include $(BUILD_SYSTEM)/base_rules.mk
$(LOCAL_BUILT_MODULE) : $(built_sepolicy) $(built_pc) $(built_fc) $(built_sc) $(built_svc)
	@mkdir -p $(dir $@)
	$(hide) echo -n $(BUILD_FINGERPRINT) > $@
endif
##################################

build_policy :=
sepolicy_build_files :=
built_sepolicy :=
built_sc :=
built_fc :=
built_pc :=
built_svc :=
built_mac_perms := 

include $(call all-makefiles-under,$(LOCAL_PATH))
