
import socket as so

# import requests
# r = requests.get('http://myip.ipip.net', timeout=6).text
# print(r)

a=so.gethostname()
print(a)

# soc=so.socket()
# print(so.gethostbyaddr('218.106.117.247'))
print(so.gethostbyname(so.gethostname()))
# print(so.gethostbyname())
# print(so.gethostbyaddr())
# print(so.gethostbyaddr(so.gethostname()))


