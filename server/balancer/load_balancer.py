import aiohttp
from aiohttp import web
import asyncio

# List of backend server URLs
backend_servers = [
    "http://127.0.0.1:5001",
    "http://127.0.0.1:5002",
    "http://127.0.0.1:5003",
    "http://127.0.0.1:5004",
    "http://127.0.0.1:5005"
]

# Simple round-robin index tracker
current_index = 0

async def proxy_handler(request):
    global current_index
    # Select backend using round-robin
    backend = backend_servers[current_index]
    current_index = (current_index + 1) % len(backend_servers)
    
    # Construct the target URL: use the same path and query string from the request
    target_url = backend + str(request.rel_url)
    
    # Forward the request to the selected backend
    async with aiohttp.ClientSession() as session:
        try:
            async with session.request(
                method=request.method,
                url=target_url,
                headers={key: value for key, value in request.headers.items() if key != 'Host'},
                data=await request.read()
            ) as resp:
                # Read response data
                response_body = await resp.read()
                # Create a response to send back to the client
                return web.Response(
                    status=resp.status,
                    body=response_body,
                    headers=resp.headers
                )
        except Exception as e:
            # In a real-world scenario, you would include better error handling and logging
            return web.Response(status=502, text=f"Bad Gateway: {e}")

# Create the aiohttp application and add a catch-all route
app = web.Application()
app.router.add_route('*', '/{tail:.*}', proxy_handler)

if __name__ == '__main__':
    web.run_app(app, host="0.0.0.0", port=5000)
