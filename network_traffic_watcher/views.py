
from django.shortcuts import render
import json

def chart(request):
    with open('tempo/temp','r') as fio:
        roop = fio.read().split()
        fio.close()
        now = int(roop[0])
        roop_range = int(roop[1])

    with open(f'tempo/temp{now}','r') as fio:
        data = fio.readlines()
        traffics = eval(data[0])
        traffics = sorted(traffics.items(), key=lambda x : x[1], reverse=True)
        fio.close()

        times = [data[1],]
        IPs = []
        flows = {}
        cnt = 0
        for traffic in traffics:
            cnt += 1
            if cnt==10:
                break
            IPs.append(traffic[0])
            flows[traffic[0]] = [traffic[1],]
    
    for useless in range(1,roop_range):
        now = (now+7) % roop_range
        with open(f'tempo/temp{now}','r') as fio:
            data = fio.readlines()
            times.insert(0,data[1])
            temp = eval(data[0])
            fio.close()
            for ip in IPs:
                try:
                    flows[ip].insert(0,temp[ip])
                except Exception:
                    flows[ip].insert(0,0)

    lst = list(flows.values())
    print(lst)

    return render(request, 'chart.html', {'times': times,'IPs': IPs,'flows': list(flows.values())})
