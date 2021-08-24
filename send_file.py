
import requests

url = 'http://127.0.0.1:8080/upload-file'
files = {'files[]': open('/Users/lucasrahn/misc/server/allure/AS-archive.tar.gz','rb')}

r = requests.post(url, files=files)
print(r)



