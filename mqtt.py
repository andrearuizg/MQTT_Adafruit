# Example of using the MQTT client class to subscribe to and publish feed values.
# Author: Tony DiCola

# Import standard python modules.
import random
import sys
import time
import RPi.GPIO as GPIO
import subprocess

# Import Adafruit IO MQTT client.
from Adafruit_IO import MQTTClient

# Set to your Adafruit IO key.
# Remember, your key is a secret,
# so make sure not to publish it when you publish this code!
ADAFRUIT_IO_KEY = 'your_key'

# Set to your Adafruit IO username.
# (go to https://accounts.adafruit.com to find your username)
ADAFRUIT_IO_USERNAME = 'your_username'

# Set to the ID of the feed to subscribe to for updates.
FEED_ID_C = 'temperatura'
FEED_ID_S = 'led'

#Definir pin 24 en BCM o 5 en WiPi
ledPin = 17

# GPIO BCM
GPIO.setmode(GPIO.BCM) 
# Definirlo como salida
GPIO.setup(ledPin, GPIO.OUT)

# Led OFF - estado inicial
GPIO.output(ledPin, GPIO.LOW)

# Define callback functions which will be called when certain events happen.
def connected(client):
    # Connected function will be called when the client is connected to Adafruit IO.
    # This is a good place to subscribe to feed changes.  The client parameter
    # passed to this function is the Adafruit IO MQTT client so you can make
    # calls against it easily.
    print('Connected to Adafruit IO!  Listening for {0} and {1} changes...'.format(FEED_ID_C, FEED_ID_S))
    # Subscribe to changes on a feed named DemoFeed.
    client.subscribe(FEED_ID_S)

def disconnected(client):
    # Disconnected function will be called when the client disconnects.
    print('Disconnected from Adafruit IO!')
    sys.exit(1)
    
def subscribe(client, userdata, mid, granted_qos):
    # This method is called when the client subscribes to a new feed.
    print('Subscribed to {0} with QoS {1}'.format(FEED_ID_S, granted_qos[0]))
    
def message(client, feed_id, payload):
    # Message function will be called when a subscribed feed has a new value.
    # The feed_id parameter identifies the feed, and the payload parameter has
    # the new value.
    print('Feed {0} received new value: {1}'.format(feed_id, payload))
    if payload == "ON":
    	print("LED ON")
    	GPIO.output(ledPin, GPIO.HIGH) # Led ON
    else:
    	print("LED OFF")
    	GPIO.output(ledPin, GPIO.LOW) # Led OFF


# Create an MQTT client instance.
client = MQTTClient(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Setup the callback functions defined above.
client.on_connect    = connected
client.on_disconnect = disconnected
client.on_message    = message
client.on_subscribe  = subscribe

# Connect to the Adafruit IO server.
client.connect()

# Now the program needs to use a client loop function to ensure messages are
# sent and received.  There are a few options for driving the message loop,
# depending on what your program needs to do.

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_background()
# Now send new values every 10 seconds.
print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
while True:
	temperatura = subprocess.run(["cat","/sys/bus/w1/devices/28-030797943f92/temperature"],stdout=subprocess.PIPE,text=True)
	temperatura = str(int(temperatura.stdout)/1000)
	print('Publishing {0} to {1}.'.format(temperatura,FEED_ID_C))
	client.publish(FEED_ID_C, temperatura)
	time.sleep(10)

# Another option is to pump the message loop yourself by periodically calling
# the client loop function.  Notice how the loop below changes to call loop
# continuously while still sending a new message every 10 seconds.  This is a
# good option if you don't want to or can't have a thread pumping the message
# loop in the background.
#last = 0
#print('Publishing a new message every 10 seconds (press Ctrl-C to quit)...')
#while True:
#   # Explicitly pump the message loop.
#   client.loop()
#   # Send a new message every 10 seconds.
#   if (time.time() - last) >= 10.0:
#       value = random.randint(0, 100)
#       print('Publishing {0} to DemoFeed.'.format(value))
#       client.publish('DemoFeed', value)
#       last = time.time()

# The last option is to just call loop_blocking.  This will run a message loop
# forever, so your program will not get past the loop_blocking call.  This is
# good for simple programs which only listen to events.  For more complex programs
# you probably need to have a background thread loop or explicit message loop like
# the two previous examples above.
#client.loop_blocking()
