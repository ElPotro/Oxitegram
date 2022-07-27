import network, time, urequests   # Cómo se trabaja con APIs hay que manejar esta libreria que ya la tiene machine para peticiones de recursos en APIs
from machine import Pin, ADC, I2C
from utelegram import Bot  # Utilizamos el módulo utelegram para que funcione
from ssd1306 import SSD1306_I2C
import framebuf
from time import sleep
import framebuf # Módulo para visualizar imagenes en pbm

TOKEN = 'N° del bot de telegram suministrado'
bot = Bot(TOKEN)
led = Pin(2, Pin.OUT)

ancho = 128
alto = 64

i2c = I2C(0, scl=Pin(22), sda=Pin(21))
oled = SSD1306_I2C(ancho, alto, i2c)
#Modulo para conectar a Telegram
class Telebot():
    def __init__ (self):   
            
        def conectaWifi (red, password):
              global miRed
              miRed = network.WLAN(network.STA_IF)     
              if not miRed.isconnected():              #Si no está conectado…
                  miRed.active(True)                   #activa la interface
                  miRed.connect(red, password)         #Intenta conectar con la red
                  print('Conectando a la red', red +"…")
                  timeout = time.time ()
                  while not miRed.isconnected():           #Mientras no se conecte..
                      if (time.ticks_diff (time.time (), timeout) > 10):
                          return False
              return True

        if conectaWifi ("Nombre de la red", "Contraseña de la red"):

            print ("Conexión exitosa!")
            print('Datos de la red (IP/netmask/gw/Dns):', miRed.ifconfig())    
            
            @bot.add_message_handler('Hola')
            def help(update):
            update.reply('Escriba on para encender y off para apagar el led')

            #print(i2c.scan()) 

            @bot.add_message_handler('On')
            def on(update):
                led.on()
                update.reply('LED is on')

            @bot.add_message_handler('Off')
            def off(update):
                led.off()
                update.reply('LED is off')
               
            bot.start_loop()
                
                
        else:
               print ("Imposible conectar")
               miRed.active (False)
               
print("soy el metodo conectar")
