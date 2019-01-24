ps ajx|grep start_pool|grep -v grep|cut -c 7-12|xargs kill -9
