# Client side vs Server side 
# URL uniform resource locator https://example.com/api
# REST API GET POST PUT(PATCH) DELETE

# Flask 
# requests third-party library pip install 
# http.server, urllib & urllib3, socketserver 
# Form Data 
# netstat -vanp tcp | grep 8000

import urllib3
import requests
import http.server
import socketserver
import json
# OSI Application layer

custom_pool_manager = urllib3.PoolManager()

url = 'http://api.openweathermap.org/geo/1.0/direct'


api_key = '5e7523329fe5639e8087bac0ea8f1d37'

params = {
  'q': ('New York', 'NY', 'US'),
  'limit': 1,
  'appid': api_key

}
# res = requests.get(url, params=params)

data_storage = {}
class MyHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/api':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()

      try: 
        res = custom_pool_manager.request('GET', url, fields=params)
        res_bytes = json.dumps(data_storage).encode()
        current_data = json.loads(res.data.decode('utf-8'))
        self.wfile.write(res.data)

      except urllib3.exceptions.HTTPError as e:
        print('HTTPError', e)
        self.wfile.write(b'File not found')

  def do_POST(self):
    global data_storage;
    if self.path == '/api/post':
      content_lngth = int(self.headers['Content-length'])
      post_data = self.rfile.read(content_lngth)
      try:
        post_json = json.loads(post_data.decode('utf-8'))
        self.send_response(201)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        data_storage.update(post_json)
      
        self.wfile.write(b'File was recieved')
      except ValueError:
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Invalid JSON or URL')        

if __name__ == '__main__':
  PORT = 8000
  with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print(f"Our server serving on port {PORT}")
    httpd.serve_forever()
