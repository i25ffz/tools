1. 一台 root 手机，取 lib 目录备用：adb pull /system/lib
2. 找配套的 gdb & gdbserver
3. adb forward tcp:5039 tcp:5039
4. 启动应用并得到 pid，进入手机 target shell，attach 进程： ./gdbserver --attach :5039 $pid
5. 在 host 运行 gdb 并执行：
	target remote :5039 //连接远端的 gdbserver
	set solib-search-path /home/martin/workspace/tudoo/gdb_hm/lib //设置库的搜索路径
	handle SIG33 nostop noprint pass // ignore SIG33
	b glShaderSource //设置断点
	continue //不解释
	x/5a $sp //以16进制查看 sp 寄存器后面的5个地址
	x/32s 0x5f679ff0 // 根据函数原型，	
	x/s (char*)(*((int*)$sp+1))
	x/8s *((int*)$sp+1)
