
# https://circuitpython.org/board/yd_esp32_s3_n16r8/
import socketpool
import wifi
import ipaddress
from os import listdir
from neopixel import NeoPixel
from board import NEOPIXEL

# DEFINITIONS
AP_SSID = 		"HP_LASERJET"
AP_PASSWORD = 	"12345678"
AP_IP = 		"10.1.1.1"
AP_MASK = 		"255.255.255.0"

# TURN OFF RGB LED
pixel = NeoPixel(NEOPIXEL, 1, auto_write=True) # GPIO48
pixel[0] = (0, 0, 0)

# EXTERNAL LIBRARIES
try:
    from adafruit_httpserver import Server, Request, Response, GET #adafruit-circuitpython-httpserver
except ImportError as e:
    raise ImportError("This requires adafruit-circuitpython-httpserver library.") from e

# INIT NET
ipv4 = ipaddress.IPv4Address(AP_IP)
netmask = ipaddress.IPv4Address(AP_MASK)
gateway = ipaddress.IPv4Address(AP_IP)

print("Creating access point...")
wifi.radio.set_ipv4_address_ap(ipv4=ipv4, netmask=netmask, gateway=gateway)
wifi.radio.start_ap(ssid=AP_SSID, password=AP_PASSWORD, authmode=[wifi.AuthMode.WPA2, wifi.AuthMode.PSK])
print(f"Created access point {AP_SSID}")

# Create /static directory if it doesn't exist
try:
    listdir("/static")
except OSError as e:
    raise OSError("Please create a /static directory on the CIRCUITPY drive.") from e

# HTTP SERVER
pool = socketpool.SocketPool(wifi.radio)
server = Server(pool, "/static/document/en/ps5/", debug=True)
@server.route("/<path:path>", GET)
def static(request: Request, path: str):
    return FileResponse(request, path, "/static")
server.serve_forever(str(wifi.radio.ipv4_address_ap), 80)
