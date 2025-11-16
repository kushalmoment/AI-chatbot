from pyngrok import ngrok
import time

# Set your ngrok auth token if you have one (optional but recommended for persistent tunnels)
# ngrok.set_auth_token("YOUR_AUTH_TOKEN")

# Start ngrok tunnel to port 5000
tunnel = ngrok.connect("5000")
public_url = tunnel.public_url
print(f"Ngrok tunnel established at: {public_url}")

# Keep the tunnel open
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    if tunnel.public_url:
        ngrok.disconnect(tunnel.public_url)
    print("Ngrok tunnel closed.")
