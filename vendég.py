
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
tv1 = Device("Digitális menütábla 1", "TV-PT")
tv2 = Device("Digitális menütábla 2", "TV-PT")

# Kapcsolatok hozzáadása
terminal1.add_connection(ap)
terminal2.add_connection(ap)
ap.add_connection(switch)
switch.add_connection(tv1)
switch.add_connection(tv2)

# Hálózat létrehozása és megjelenítése
network = Network()
network.add_device(terminal1)
network.add_device(terminal2)
network.add_device(ap)
network.add_device(switch)
network.add_device(tv1)
network.add_device(tv2)

network.display_network()

# Több rendelés leadása mindkét terminálról
def rendelest_indit_mindket_terminal():
    orders = ["Hamburger", "Pizza", "Gyros", "Saláta"]

    # Függvény egy terminál rendeléseinek kezelésére
    def rendelest_valaszt(terminal_name, terminal_device, target_device):
        selected_orders = []
        print(f"\nRendelés leadása {terminal_name} számára:")
        while len(selected_orders) < 5:
            print("\nVálasztható rendelési lehetőségek:")
            for i, order in enumerate(orders, start=1):
                print(f"{i}. {order}")
            print("0. Rendelés befejezése")

            try:
                choice = int(input(f"{terminal_name}: Válaszd ki a rendelés számát: ")) - 1
                if choice == -1:
                    print("Rendelés befejezve.")
                    break
                elif 0 <= choice < len(orders):
                    selected_orders.append(orders[choice])
                    print(f"Hozzáadva a rendelés: {orders[choice]}")
                else:
                    print("Érvénytelen választás, próbáld újra!")
            except ValueError:
                print("Érvénytelen bemenet, számot adj meg!")

        print(f"\n{terminal_name} kiválasztott rendelések:")
        for order in selected_orders:
            print(f"- {order}")
            terminal_device.send_data(f"Rendelés: {order}", target_device)

    # Rendelés Terminal 1 számára
    rendelest_valaszt("Terminal 1", terminal1, tv1)

    # Rendelés Terminal 2 számára
    rendelest_valaszt("Terminal 2", terminal2, tv2)

# Rendelések indítása mindkét terminálról
rendelest_indit_mindket_terminal()
