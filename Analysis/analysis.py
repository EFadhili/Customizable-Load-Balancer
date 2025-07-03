import asyncio
import aiohttp
from collections import Counter
import matplotlib.pyplot as plt

URL = "http://127.0.0.1:5000/home"  # Load Balancer Endpoint
NUM_REQUESTS = 5000  # Total Requests to Send

async def send_request(session):
    try:
        async with session.get(URL) as response:
            try:
                # Try to decode JSON response
                json_resp = await response.json()
                server_message = json_resp.get("message", "")
            except Exception:
                # Fallback for non-JSON response
                text = await response.text()
                server_message = f"Non-JSON: {text[:50]}"  # Limit text length
            return server_message
    except Exception as e:
        return f"Error: {e}"

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session) for _ in range(NUM_REQUESTS)]
        responses = await asyncio.gather(*tasks)

        # Count responses
        counter = Counter(responses)
        print("\nRequest Distribution:\n")
        for server, count in counter.items():
            print(f"{server}: {count} requests")

        # Plot Bar Chart
        plt.figure(figsize=(10, 6))
        plt.bar(counter.keys(), counter.values(), color='skyblue')
        plt.xticks(rotation=45, ha='right')
        plt.title("Load Distribution Among Servers")
        plt.xlabel("Server")
        plt.ylabel("Number of Requests")
        plt.tight_layout()
        plt.savefig("load_distribution.png")
        print("\nChart saved as 'load_distribution.png'.")

if __name__ == '__main__':
    asyncio.run(main())
