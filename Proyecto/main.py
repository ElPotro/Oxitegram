import urequests
import telegramM
import pulsimetro
from utelegram import Bot
from telegramM import *
from pulsimetro import Pulso
from machine import Timer, I2C, Pin, ADC
from ssd1306 import SSD1306_I2C
from time import sleep
import time, network  #Importamos el módulo de tiempo time https://docs.python.org/es/3/library/time.html
import framebuf # Módulo para visualizar imagenes en pbm
from utime import ticks_diff, ticks_us
from max30102 import MAX30102, MAX30105_PULSE_AMP_MEDIUM

TOKEN = 'N° del token del bot suministrado por telegram'
bot = Bot(TOKEN)

pin_0 = Pin(18, Pin.OUT)
pin_1 = Pin(5, Pin.OUT)
pin_2 = Pin(17, Pin.OUT)
pin_3 = Pin(16, Pin.OUT)


ancho = 128
alto = 64
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  #Definimos los pines de la OLED SCL y SDA para ssd1306 y sh1106(otra)
oled = SSD1306_I2C(ancho, alto, i2c)


# telegram
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
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
    
else:
       print ("Imposible conectar")
       miRed.active (False)       
       
def telegram_bot_sendtext(bot_message):

    bot_token = 'N° del token del bot suministrado por telegram'
    bot_chatID = 'ID de la cuenta telegram donde se enviará el mensaje de retorno'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = urequests.get(send_text)

    return response.json()





def buscar_icono(ruta):
    dibujo = open(ruta, "rb")  # Abrir en modo lectura de bits https://python-intermedio.readthedocs.io/es/latest/open_function.html
    dibujo.readline() # metodo para ubicarse en la primera linea de los bist
    xy = dibujo.readline() # ubicarnos en la segunda linea
    x = int(xy.split()[0])  # split  devuelve una lista de los elementos de la variable solo 2 elemetos
    y = int(xy.split()[1])
    icono = bytearray(dibujo.read())  # guardar en matriz de bites
    dibujo.close()
    return framebuf.FrameBuffer(icono, x, y, framebuf.MONO_HLSB)  #Utilizamos el metodo MONO_HLSB

print(i2c.scan())

oled.blit(buscar_icono("areandina/OXITEGRAM.pbm"), 0, 0) # ruta y sitio de ubicación del directorio
oled.show()  #mostrar en la oled
time.sleep(3) # Espera de 3 segundos
oled.fill(0)
oled.show()
 
oled.text("Bienvenidos", 0, 10)
oled.text("Sistema", 0, 30)
oled.text("OXITEGRAM", 0, 50)
oled.show()
time.sleep(4)
 
oled.fill(1)
oled.show()
time.sleep(2)
oled.fill(0)
oled.show()

while True:
    oled.fill(0)
    '''conversion_factor = 100 / (65535)
    val= int(oledC.datos.sensor.pop_ir_from_storage())'''
    #oxigeno = float (oledC.datos.sensor.pop_ir_from_storage()*conversion_factor)
    oled.text("************",0,0)    
    oled.text("Lectura",10,10)
    #oled.text(str(val),10,20)
    oled.text("oxigeno",10,30)                
    #oled.text(str(oxigeno),0,40)
    oled.text("************",0,50)
    oled.show()
    
    #print("oxigeno =", oxigeno)
    time.sleep(0.25)
                
    temporiza = Timer(0)
    def desborde (Timer):
        
        #apagado de leds
        pin_0.off()
        pin_1.off()
        pin_2.off()
        pin_3.off()
        
        
        if oledC.datos >= 20 and oledC.datos <= 29 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("20%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 20% = Hipoxia severa")
            
        elif oledC.datos >= 30 and oledC.datos <= 39 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("30%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 30% = Hipoxia severa")
            
        elif oledC.datos >= 40 and oledC.datos <= 49 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("40%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 40% = Hipoxia severa")
            
        elif oledC.datos >= 50 and oledC.datos <= 59 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.text("Nivel de SPO2",10,30)                
            oled.text("50%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 50% = Hipoxia severa")
            
        elif oledC.datos >= 60 and oledC.datos <= 69 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("60%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 60% = Hipoxia severa")
            
        elif oledC.datos >= 70 and oledC.datos <= 79 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("70%",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 70% = Hipoxia severa")
            
        elif oledC.datos >= 80 and oledC.datos <= 85 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("80-85 %",0,40)
            oled.text("Hipoxia severa",0,50)
            oled.show()
            pin_1.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 80-85% = Hipoxia severa")
            
        elif oledC.datos >= 86 and oledC.datos <= 89 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)                
            oled.text("86-89 %",0,40)
            oled.text("Hipoxia Moderada",0,50)
            oled.show()
            pin_2.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 86-89% = Hipoxia Moderada")
            
        elif oledC.datos >= 90 and oledC.datos <= 92 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)              
            oled.text("90-92 %",0,40)
            oled.text("Hipoxia Leve",0,50)
            oled.show()
            pin_2.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 90-92% = Hipoxia Leve")
            
        elif oledC.datos >= 93 and oledC.datos <= 100 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel de SPO2",10,30)              
            oled.text("93-100 %",0,40)
            oled.text("Normal",0,50)
            pin_3.on()
            test = telegram_bot_sendtext("Nivel de SPO2 - 93-100% = Normal")
            
        elif oledC.datos >= 101 :
            print("% SP02={:02} ".format(oledC.datos))
            oled.fill(0)
            oled.text("Nivel erroneo",10,30)              
            oled.text("Fuera de rango",0,40)
            oled.text("Error",0,50)
            
            
            
        else:
            oled.fill(0)
            oled.text("Bienvenido.",10,30)                
            oled.text("Ubicar dedo",15,40)
            oled.text("En espera...",15,50)
            oled.show()
            pin_0.on()
            print("Sin muestras...", oledC.datos)
            test = telegram_bot_sendtext("Sin muestras...")
     
                
    #______________________
    temporiza.init(period=1000,mode=Timer.PERIODIC,callback=desborde)
    #_______________________
    oledC = Pulso()
    oledC.muestra()
    print("salio")