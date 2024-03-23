try:
  import usocket as socket
except:
  import socket
from boot import led, analogPin, relay
import time

def web_page(turnOnValue, analogValue, hysteresis):
  if led.value() == 1:
    gpio_state="ON"
  else:
    gpio_state="OFF"

  print(turnOnValue, analogValue, hysteresis)
  
  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>Wait for a while againAgain</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p>Analog value: <strong>""" + str(analogValue) + """</strong></p><p><a href="/?led=on"><button class="button">ON</button></a></p>
  <p><a href="/?led=off"><button class="button button2">OFF</button></a></p><p>Turn on value: <strong>""" + str(turnOnValue) + """</strong></p>
  </p><p>Hysteresis: <strong>""" + str(hysteresis) + """</strong></p><form><label for="fname">Turn on:</label><br>
  <input type="text" id="turnOn" name="turnOn" value=""" + str(turnOnValue) + """><br><br>
  <input type="text" id="hysteresis" name="hysteresis" value=""" + str(hysteresis) + """><br><br>
  <input type="submit" value="Submit"></form></body></html>"""
  
  print(html)
  return html
def webApp():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.settimeout(5)
    s.bind(('', 80))
    s.listen(5)

    turnOnValue=500
    analogValue=analogPin.read()
    hysteresis=10
    while True:
        try:
          conn, addr = s.accept()
          print('Got a connection from %s' % str(addr))
          request = conn.recv(1024)
          request = str(request)
          print('Content = %s' % request)
          led_on = request.find('/?led=on')
          led_off = request.find('/?led=off')
          if led_on == 6:
            print('LED ON')
            led.value(1)
          if led_off == 6:
            print('LED OFF')
            led.value(0)
          if request.find('turnOn=')>-1:
            startIndex=request.find('turnOn=')
            temp=request[startIndex+7:]
            temp=temp.split("&")
            turnOnValue=int(temp[0])
            print(turnOnValue)
          if request.find('hysteresis=')>-1:
            startIndex=request.find('hysteresis=')
            temp=request[startIndex+11:]
            temp=temp.split()
            hysteresis=int(temp[0])
            print(hysteresis)
          response = web_page(turnOnValue, analogValue, hysteresis)
          conn.send('HTTP/1.1 200 OK\n')
          conn.send('Content-Type: text/html\n')
          conn.send('Connection: close\n\n')
          conn.sendall(response)
          conn.close()
        except Exception as e:
            print('Accept exception')
            print(e)
            
        analogValue=analogPin.read()
        
        if analogValue>=turnOnValue:
            relay.value(1)
        elif analogValue<turnOnValue-hysteresis:
            relay.value(0)
    return True
