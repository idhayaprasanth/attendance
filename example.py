from pyngrok import ngrok
import time
import os
from pyngrok import ngrok

os.environ["NGROK_PATH"] = "C:\\path\\to\\ngrok.exe"
ngrok.set_auth_token("2duL8cK7vAI45HlSNp8EJWsa2ZS_5yVSyfi2dDsE1YbzbtZmY")

# Set the ngrok authentication token
ngrok.set_auth_token("2duL8cK7vAI45HlSNp8EJWsa2ZS_5yVSyfi2dDsE1YbzbtZmY")

# Start a HTTP tunnel to a local web server
http_tunnel = ngrok.connect(addr="http://localhost:8000", proto="http")

try:
    print("Public URL:", http_tunnel.public_url)

    # Keep the tunnel open indefinitely
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # Close the ngrok tunnel when the script is interrupted
    ngrok.disconnect(http_tunnel.public_url)
    print("Tunnel closed.")
