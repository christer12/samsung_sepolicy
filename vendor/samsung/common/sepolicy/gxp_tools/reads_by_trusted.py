obj_read = open("../gxp_outs/reads_by_trusted.out", 'w')


trusted_list = ['../mediaserver.te', '../init.te', '../zygote.te', '../adbd.te', '../clatd.te', '../debuggerd.te', '../fingerprintd.te', '../gatekeeperd.te', '../gpsd.te', '../healthd.te', '../hostapd.te', '../installd.te', '../kernel.te', '../keystore.te', '../lmkd.te', '../logd.te', '../mdnsd.te', '../netd.te', '../perfprofd.te', '../rild.te', '../sdcardd.te', '../ueventd.te', '../vold.te', '../watchdogd.te', '../binderservicedomain.te', '../bootanim.te', '../drmserver.te', '../mediaserver.te', '../runas.te', '../servicemanager.te', '../surfaceflinger.te', '../su.te', '../system_server.te', '../tee.te', '../toolbox.te']

read_ops = [' accept ',' acceptfrom ',' access ',' acquire_svc ',' copy ',' dccp_recv ',' debug ',' entrypoint ',' execute ',' execute_no_trans ',' export ',' forward_in ',' get_property ',' getattr ',' getcap ',' getfocus ',' getgrp ',' gethost ',' getopt ',' getpgid ',' getpwd ',' getsched ',' getserv ',' getsession ',' getstat ',' ingress ',' install_module ',' list_child ',' list_property ',' listen ',' load_module ',' manage ',' mounton ',' nlmsg_read ',' nlmsg_readpriv ',' polmatch ',' ptrace ',' query ',' quotaget ',' quotaon ',' rawip_recv ',' read ',' receive ',' record ',' recv ',' recv_msg ',' recvfrom ',' relabelfrom ',' rmdir ',' saver_getattr ',' search ',' share ',' shmemgrp ',' shmemhost ',' shmempwd ',' shmemserv ',' swapon ',' tcp_recv ',' udp_recv ',' unix_read ',' use ',' view ', ' accept}',' acceptfrom}',' access}',' acquire_svc}',' copy}',' dccp_recv}',' debug}',' entrypoint}',' execute}',' execute_no_trans}',' export}',' forward_in}',' get_property}',' getattr}',' getcap}',' getfocus}',' getgrp}',' gethost}',' getopt}',' getpgid}',' getpwd}',' getsched}',' getserv}',' getsession}',' getstat}',' ingress}',' install_module}',' list_child}',' list_property}',' listen}',' load_module}',' manage}',' mounton}',' nlmsg_read}',' nlmsg_readpriv}',' polmatch}',' ptrace}',' query}',' quotaget}',' quotaon}',' rawip_recv}',' read}',' receive}',' record}',' recv}',' recv_msg}',' recvfrom}',' relabelfrom}',' rmdir}',' saver_getattr}',' search}',' share}',' shmemgrp}',' shmemhost}',' shmempwd}',' shmemserv}',' swapon}',' tcp_recv}',' udp_recv}',' unix_read}',' use}',' view}',' accept;',' acceptfrom;',' access;',' acquire_svc;',' copy;',' dccp_recv;',' debug;',' entrypoint;',' execute;',' execute_no_trans;',' export;',' forward_in;',' get_property;',' getattr;',' getcap;',' getfocus;',' getgrp;',' gethost;',' getopt;',' getpgid;',' getpwd;',' getsched;',' getserv;',' getsession;',' getstat;',' ingress;',' install_module;',' list_child;',' list_property;',' listen;',' load_module;',' manage;',' mounton;',' nlmsg_read;',' nlmsg_readpriv;',' polmatch;',' ptrace;',' query;',' quotaget;',' quotaon;',' rawip_recv;',' read;',' receive;',' record;',' recv;',' recv_msg;',' recvfrom;',' relabelfrom;',' rmdir;',' saver_getattr;',' search;',' share;',' shmemgrp;',' shmemhost;',' shmempwd;',' shmemserv;',' swapon;',' tcp_recv;',' udp_recv;',' unix_read;',' use;',' view;']



for trusted in trusted_list: 
	with open(trusted) as f:
		for line in f:
			if line.startswith('allow '):
				if any(op in line for op in read_ops):
				#if any(op in line for op in read_ops):
					#print(line)
			        	obj_read.write(line)


