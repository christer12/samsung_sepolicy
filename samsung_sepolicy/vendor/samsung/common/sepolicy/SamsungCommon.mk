# For SE Android
# policies for samsung common

# SE Policy version for SPOTA update
# SS_POLICYVER Should be increased when update sepolicy by spota
# Version 'A' means MSC policy
SS_POLICYVER := 0013
POLICY_REVISION := SEPF_SECMOBILE_$(PLATFORM_VERSION)_$(SS_POLICYVER)

# Factory binary: file_contexts(fc_digest) must be different with nonFactory
ifeq ($(SEC_FACTORY_BUILD),true) 
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/factory
endif

# Samsung common domain
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/sec_common

# Model and BSP Policy
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/BSP/bsp_qcom_v2/bsp/common \
	vendor/samsung/common/sepolicy/BSP/bsp_qcom_v2/qcom_common \
	vendor/samsung/common/sepolicy/BSP/bsp_marvell \
	vendor/samsung/common/sepolicy/BSP/bsp_sprd

# TODO : move to sepolicy directory
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/model
	
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/knox_common

BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/qcom_common \
	vendor/samsung/common/sepolicy/slsi_common \
	vendor/samsung/common/sepolicy/marvell_common \
	vendor/samsung/common/sepolicy/sprd_common

# 3rd party configuration
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/3rd/vmware \
	vendor/samsung/common/sepolicy/3rd/mcafee \
	

# samsung policy
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy

# Carrier policy
BOARD_SEC_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/carrier/carrier_att \
	vendor/samsung/common/sepolicy/carrier/carrier_spr \
	vendor/samsung/common/sepolicy/carrier/carrier_tfntmo \
	vendor/samsung/common/sepolicy/carrier/carrier_vzw \
	vendor/samsung/common/sepolicy/carrier/carrier_kor \
	vendor/samsung/common/sepolicy/carrier/carrier_jpn \

# Specific case
ifdef SEC_BUILD_CONF_CSC_CUSTOMERS
	# ATT ENG MODEL
	ifneq ($(filter ATT, $(SEC_BUILD_CONF_CSC_CUSTOMERS)),)
		ifeq ($(TARGET_BUILD_VARIANT), eng)
		BOARD_SEC_SEPOLICY_DIRS += \
			vendor/samsung/common/sepolicy/eng/carrier_att
		endif
	endif

	# LDU MODEL
	ifneq ($(filter PAP OZH, $(SEC_BUILD_CONF_CSC_CUSTOMERS)),)
		BOARD_SEC_SEPOLICY_DIRS += \
			vendor/samsung/common/sepolicy/carrier/carrier_ldu
	endif
endif
