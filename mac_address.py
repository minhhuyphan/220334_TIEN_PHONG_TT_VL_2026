import uuid

mac = uuid.getnode()
mac_address = ':'.join(f'{(mac >> i) & 0xff:02x}' for i in range(40, -1, -8))
print("=" * 40)
print(f"  MAC Address: {mac_address}")
print("=" * 40)
