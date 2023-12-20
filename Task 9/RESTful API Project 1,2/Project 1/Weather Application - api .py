''' Project 1 description

For this project I used the main.py from our lecture. I added WeatherAPI class to add the logic by which 
the program gets temperature of the specified city. The user have chance to specify the interested name of the city. After running this py file in the terminal, user will see input place where he/she can provide city name, for example; Armenia, New York, etc. After pressing enter user will see the message from server about the temperature. I want to note that in the message there is one character which is because of encoding issues that I could not overcome, here you can see message example in case of Armenia; Temperature in Armenia: 17.1Â°C. '''

# to view the app locally, after running the py file, go to the following
# http://localhost:8000/api


import urllib3
import requests
import http.server
import socketserver
import json

custom_pool_manager = urllib3.PoolManager()

url = 'http://api.openweathermap.org/data/2.5/weather'

# sign up to get  your API key:
api_key = 'e57621d66bd221d6c00eb0cd398d7e3a'


class WeatherAPI:
    def get_temperature(self, city):
        try:
            params = {
                'q': city,
                'appid': api_key,
                'units': 'metric'  # Request temperature in Celsius
            }

            response = custom_pool_manager.request('GET', url, fields=params)

            if response.status == 200:
                weather_data = json.loads(response.data.decode('utf-8'))
                temperature = weather_data['main']['temp']
                return temperature
            else:
                return None  # Handle errors by returning None

        except Exception as e:
            print('Error:', e)
            return None
            
data_storage = {}
class MyHandler(http.server.BaseHTTPRequestHandler):
  def do_GET(self):
    if self.path == '/api':
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()

      try: 
        city = input('Enter city name: ')
        weather_api = WeatherAPI()
        temperature = weather_api.get_temperature(city)
        if temperature is not None:
               self.wfile.write(f'Temperature in {city}: {temperature}°C'.encode())

        else:
                self.wfile.write(b'Error getting temperature')

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
