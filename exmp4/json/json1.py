import json

with open("sample-data.json") as f:
    data = json.load(f)

print("Interface Status")
print("=" * 80)
print(f"{'DN':50} {'Description':20} {'Speed':7} {'MTU':6}")
print("-" * 80)

for item in data["imdata"]:
    obj = next(iter(item.values()))
    attr = obj["attributes"]

    dn = attr.get("dn", " ")
    descr = attr.get("")
    speed = attr.get("speed", " ")
    mtu = attr.get("mtu", " ")

    print(f"{dn:50} {descr if descr else 'None':20} {speed:7} {mtu:6}")
