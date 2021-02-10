#!/usr/bin/env python3
"""
08:18:39.506290 IP 172.19.128.1.54239 > 172.19.137.44.38797: tcp 62
08:18:39.555459 IP 172.19.128.1.54239 > 172.19.137.44.38797: tcp 0
08:18:39.560364 IP 172.19.128.1.53 > 172.19.137.44.40162: UDP, length 278
08:18:39.581865 IP 172.19.128.1.53 > 172.19.137.44.40162: UDP, length 179
08:18:39.631127 IP 13.107.5.93.443 > 172.19.137.44.39216: tcp 0
08:18:39.637724 IP 172.19.128.1.54239 > 172.19.137.44.38797: tcp 55
08:18:39.679623 IP 172.19.128.1.54239 > 172.19.137.44.38797: tcp 0
08:18:39.681551 IP 13.107.5.93.443 > 172.19.137.44.39216: tcp 1436
"""
"""
[('172.19.128.1.54238', 'tcp', '0')]
[('172.19.128.1.54238', 'tcp', '0')]
[('172.19.128.1.53', 'UDP', '260')]
[('172.19.128.1.53', 'UDP', '207')]
[('172.19.128.1.54238', 'tcp', '0')]
[('172.19.128.1.54238', 'tcp', '0')]
"""
"""
{'172.19.128.1': 20548, '111.221.29.254': 12393, '13.229.188.59': 4552}
"""

from func_timeout import func_set_timeout
import func_timeout.exceptions
import subprocess
class Tcpdump(): # return a process
    def __init__(self):
        self.__local_ip__ = self.__get_host_ip__()
        self.process = self.__tcpdump__()
        self.total = {}
        self.time = ''

    def __get_host_ip__(self):
        import socket
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip

    def __tcpdump__(self):
        cmd1 = [f'tcpdump -q -n dst {self.__local_ip__}']
        # cmd1 = [f'tcpdump -q -n dst {local_ip}']
        p1 = subprocess.Popen(cmd1,stdout=subprocess.PIPE,encoding='utf-8',shell=True,stderr=subprocess.STDOUT) # dst: destination 接收方, src: source 发送方

        cmd2 = ['grep', '--line-buffered', '-a', '-o', '-E' , '.*IP.*']
        p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE, stdin=p1.stdout,bufsize=0)
        
        return p2

    def __parseEcho__(self,echo):
        import re
        pattern = re.compile(  # Regex
        r'([0-9]*?:[0-9]*?:[0-9]*?)\..*?IP ([0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}).*?: ([a-zA-Z][a-zA-Z][a-zA-Z]).*?([0-9][0-9]*)', re.S) # items[0]: source ip 发送方ip，[1]: protocal(previous 3 letters) 协议名（显示前三个字母），[2]: package length 包长度
        items = re.findall(pattern, echo)
        return items[0][0],items[0][1],items[0][2],int(items[0][3]) # src ip, port, protocol, length(str)

    def __readTemp__(self):
        with open('tempo/temp','r') as temp_fio:
            temp_text = temp_fio.read().split()
            return int(temp_text[0]), int(temp_text[1]) # now, roop_range


    @func_set_timeout(10)
    def __readOut__(self,now):
        while True:
            echo = self.process.stdout.readline().strip().decode('utf-8')
            try:
                self.time, ip, protocol, lenth = self.__parseEcho__(echo)  # local: 172.19.143.195
            except Exception:
                continue

            print(self.time, ip, protocol, lenth)
            try:
                self.total[ip] += lenth
            except KeyError:
                self.total[ip] = lenth

            print(self.total, now)

    def readOut(self):
        import json
        now, roop_range = self.__readTemp__()
        cnt = 0
        while True:
            cnt += 1
            if cnt == 60:
                self.time = ''
                self.total = {}
            try:
                self.__readOut__(now)
            except func_timeout.exceptions.FunctionTimedOut:
                # print('------\n pwn!\n------')
                pass
            now = (now+1) % roop_range
            with open(f'tempo/temp', 'w') as mark_fio:
                mark_fio.write(f"{str(now)} {str(roop_range)}")
                mark_fio.close()
            with open(f'tempo/temp{now}','w') as fio:
                json.dump(self.total,fio)
                fio.write('\n' + self.time)
                fio.close()

tcpdump = Tcpdump()
tcpdump.readOut()
