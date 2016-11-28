# Board specific SELinux policy variable definitions
BOARD_SEPOLICY_DIRS += \
	vendor/samsung/common/sepolicy/BSP/bsp_sprd

BOARD_SEPOLICY_UNION += \
	adbd.te \
	bluetooth.te \
	bootanim.te \
	debuggerd.te \
	device.te \
	dex2oat.te \
	drmserver.te \
	engpc.te \
	file.te \
	file_contexts \
	genfs_contexts \
	hostapd.te \
	init.te \
	kernel.te \
	mediaserver.te \
	netd.te \
	nvitemd.te \
	platform_app.te \
	radio.te \
	recovery.te \
	refnotify.te \
	rild.te \
	sdcardd.te \
	service_contexts \
	shell.te \
	srtd.te \
	surfaceflinger.te \
	system_app.te \
	system_server.te \
	ueventd.te \
	untrusted_app.te \
	wcnd.te \
	wpa.te \
	zram.te \
	zygote.te
