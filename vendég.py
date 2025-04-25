
class Device:
    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.connections = []

    def add_connection(self, device):
        if device not in self.connections:
            self.connections.append(device)
            device.connections.append(self)

    def send_data(self, data, target_device, visited=None):
        if visited is None:
            visited = set()
        visited.add(self)

        if target_device in self.connections:
            print(f"{self.name} küld adatot {target_device.name} eszköznek: {data}")
            target_device.receive_data(data)
        else:
            print(f"{self.name} adatot továbbít: {data}")
            for connection in self.connections:
                if connection not in visited:
                    connection.send_data(data, target_device, visited)

    def receive_data(self, data):
        print(f"{self.name} fogad adatot: {data}")


class Network:
    def __init__(self):
        self.devices = []

    def add_device(self, device):
        self.devices.append(device)

    def display_network(self):
        for device in self.devices:
            print(f"{device.name} ({device.device_type})")
            for connection in device.connections:
                print(f"  -> {connection.name} ({connection.device_type})")


# Hálózati eszközök létrehozása
terminal1 = Device("Rendelő Terminal 1", "TabletPC-PT")
terminal2 = Device("Rendelő Terminal 2", "TabletPC-PT")
ap = Device("Light Weight Access Point", "AP")
switch = Device("2960-24TT Switch3", "Switch")
cloud1 = Device("Cloud1", "Cloud-PT")
cloud2 = Device("Cloud2", "Cloud-PT")
tv1 = Device("Digitális menütábla 1", "TV-PT")
tv2 = Device("Digitális menütábla 2", "TV-PT")

# Kapcsolatok hozzáadása
terminal1.add_connection(ap)
terminal2.add_connection(ap)
ap.add_connection(switch)
switch.add_connection(cloud1)
switch.add_connection(cloud2)
cloud1.add_connection(tv1)
cloud2.add_connection(tv2)

# Hálózat létrehozása és megjelenítése
network = Network()
network.add_device(terminal1)
network.add_device(terminal2)
network.add_device(ap)
network.add_device(switch)
network.add_device(cloud1)
network.add_device(cloud2)
network.add_device(tv1)
network.add_device(tv2)

network.display_network()

# Rendelési funkció terminálonként
def rendelest_indit_terminalonként():
    orders = ["Hamburger", "Pizza", "Gyros", "Saláta"]

    # Függvény a rendelés leadásához egy terminál számára
    def rendelest_valaszt(terminal_name):
        while True:
            print(f"\nRendelés leadása {terminal_name} számára:")
            for i, order in enumerate(orders, start=1):
                print(f"{i}. {order}")
            try:
                choice = int(input(f"{terminal_name}: Válaszd ki a rendelés számát: ")) - 1
                if 0 <= choice < len(orders):
                    return orders[choice]
                else:
                    print("Érvénytelen választás! Próbáld újra.")
            except ValueError:
                print("Érvénytelen bemenet! Számot adj meg.")

    # Rendelés Terminal 1 számára
    selected_order1 = rendelest_valaszt("Terminal 1")
    print(f"Terminal 1 kiválasztott rendelése: {selected_order1}")
    terminal1.send_data(f"Rendelés: {selected_order1}", tv1)

    # Rendelés Terminal 2 számára
    selected_order2 = rendelest_valaszt("Terminal 2")
    print(f"Terminal 2 kiválasztott rendelése: {selected_order2}")
    terminal2.send_data(f"Rendelés: {selected_order2}", tv2)

# Felhasználói választás terminálonként
rendelest_indit_terminalonként()
