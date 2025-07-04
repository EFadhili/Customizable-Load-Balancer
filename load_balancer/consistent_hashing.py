import hashlib

class ConsistentHashing:
    def __init__(self, num_servers=3, num_slots=512, num_virtual=9):
        self.num_servers = num_servers
        self.num_slots = num_slots
        self.num_virtual = num_virtual
        self.hash_ring = dict()
        self.sorted_keys = []
        self.servers = {}

        # Initialize servers in hash ring
        for server_id in range(1, num_servers + 1):
            self.add_server(f"Server {server_id}")

    def hash_function(self, key):
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    def add_server(self, server_name):
        self.servers[server_name] = []
        for virtual_id in range(self.num_virtual):
            key = f"{server_name}-virtual-{virtual_id}"
            hash_key = self.hash_function(key)
            self.hash_ring[hash_key] = server_name
            self.sorted_keys.append(hash_key)
            self.servers[server_name].append(hash_key)

        self.sorted_keys.sort()

    def remove_server(self, server_name):
        if server_name in self.servers:
            for key in self.servers[server_name]:
                self.hash_ring.pop(key, None)
                self.sorted_keys.remove(key)
            del self.servers[server_name]

    def get_server(self, request_id):
        hash_key = self.hash_function(request_id)
        for key in self.sorted_keys:
            if hash_key <= key:
                return self.hash_ring[key]
        return self.hash_ring[self.sorted_keys[0]]  # Wrap around

    def get_all_servers(self):
        return list(self.servers.keys())
