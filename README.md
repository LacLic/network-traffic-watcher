# network-traffic-watcher

powered by Python, using subprocess, Django and so on

to return a realtime network traffic information page with Django and Echart

-----

# Install

Run in Linux.

## clone the repo

```
cd ~
mkdir github_repo
cd github_repo
git clone https://github.com/LacLic/network-traffic-watcher
```

## run tcpdump

```
cd network-traffic-watcher
python3 tcpdump.py
```

then wait for echo

## run manage.py at the same time

If you are using command-line Linux, you can use ```screen```.

```
cd ~/github_repo/network-traffic-watcher
python3 manage.py runserver 0.0.0.0:11451
```

and then, you can see it on website ```localhost:11451/index/``` or ```[Yourserver IP]:11451/index/```

~~My demo: ```nw.laclic.ink:11451/index/```~~(no longer used)


