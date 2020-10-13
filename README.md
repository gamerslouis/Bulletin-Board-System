# Bulletin-Board-System
- NCTU 108B網程設學期專案
- 這是一個極簡易的 BBS 系統，在hw1和hw2可使用telnet來連線，在hw3、hw4中需要使用client來連線，並搭配aws bucket和redis作為儲存和快取服務

### How to run
+ Runserver
	```shell=
	cd server
	python3 runserver.py 8888
	```

+ Client dependency install
	```shell=
	pip3 install boto3
	```

+ Redis required
    + default server: 10.0.8.1:6379
    + 可更改client/command/Subscribe.py

+ Runclient
	```
	cd client
	python3 bbs.py 8888
	```


