# Re-execute the class definitions after environment reset

# Re-defining classes after reset, now with proper inheritance usage

# Base class
class Ammunition:
    def __init__(self, id, lead_free, manufacturer, name, caliber, bullet_weight, grain, j_0m, j_150m, v_0m, v_150m):
        self.id = id
        self.lead_free = lead_free
        self.manufacturer = manufacturer
        self.name = name
        self.caliber = caliber
        self.bullet_weight = bullet_weight
        self.grain = grain
        self.j_0m = j_0m
        self.j_150m = j_150m
        self.v_0m = v_0m
        self.v_150m = v_150m

    def __str__(self):
        return (f"{self.id} | {self.lead_free} | {self.manufacturer} | {self.name} | "
                f"{self.caliber} | {self.bullet_weight} | {self.grain} | "
                f"{self.j_0m} | {self.j_150m} | {self.v_0m} | {self.v_150m}")

# Subclass for rifle ammunition
class RifleAmmunition(Ammunition):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "Rifle"

    def __str__(self):
        return f"{super().__str__()} | Type: {self.type}"

# Class to manage database
class AmmunitionDatabase:
    def __init__(self):
        self.ammo_list = []

    def add_ammunition(self, ammo: Ammunition):
        for entry in self.ammo_list:
            if (entry.manufacturer.lower() == ammo.manufacturer.lower() and
                entry.name.lower() == ammo.name.lower()):
                print("❌ Duplicate found.")
                return False
        self.ammo_list.append(ammo)
        print("✅ Entry added.")
        return True

    def display_all(self):
        if not self.ammo_list:
            print("No data to display.")
            return
        print("\nID | LeadFree | Manufacturer | Name | Caliber | BulletWeight | Grain | J@0m | J@150m | V@0m | V@150m")
        for ammo in self.ammo_list:
            print(ammo)

    def average_grain(self):
        from collections import defaultdict
        calibers = defaultdict(list)
        for ammo in self.ammo_list:
            calibers[ammo.caliber].append(ammo.grain)
        for cal, grains in calibers.items():
            avg = sum(grains) / len(grains)
            print(f"{cal}: {avg:.2f}")

    def most_common(self):
        from collections import Counter
        calibers = [ammo.caliber for ammo in self.ammo_list]
        weights = [ammo.bullet_weight for ammo in self.ammo_list]
        if calibers:
            common_cal = Counter(calibers).most_common(1)[0]
            print(f"Most common caliber: {common_cal[0]} ({common_cal[1]}x)")
        if weights:
            common_wt = Counter(weights).most_common(1)[0]
            print(f"Most common bullet weight: {common_wt[0]} ({common_wt[1]}x)")

# Ammunition sorter
class AmmunitionSorter:
    @staticmethod
    def merge_sort(data, keys):
        if len(data) <= 1:
            return data
        mid = len(data) // 2
        left = AmmunitionSorter.merge_sort(data[:mid], keys)
        right = AmmunitionSorter.merge_sort(data[mid:], keys)
        return AmmunitionSorter.merge(left, right, keys)

    @staticmethod
    def merge(left, right, keys):
        result = []
        while left and right:
            l_val = tuple(getattr(left[0], k) for k in keys)
            r_val = tuple(getattr(right[0], k) for k in keys)
            if l_val <= r_val:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result += left + right
        return result

# Ammunition search
class AmmunitionSearch:
    @staticmethod
    def search(data, keyword):
        return [ammo for ammo in data if keyword.lower() in str(ammo).lower()]

# Main input logic using inheritance
def manual_input(ammo_db):
    print("Enter ammunition data (type 'done' anytime to stop):")
    allowed_calibers = ['.308', '30-06 Springfield', '300 Win Mag', '243']
    rifle_calibers = ['.308', '30-06 Springfield', '300 Win Mag', '243']
    next_id = len(ammo_db.ammo_list) + 1

    while True:
        lead_free = input("Is the bullet lead free? (yes/no): ").strip().lower()
        if lead_free == 'done':
            break
        if lead_free not in ['yes', 'no']:
            print("Please enter 'yes' or 'no'.")
            continue

        manufacturer = input("Manufacturer: ")
        if manufacturer.lower() == 'done':
            break

        name = input("Product name: ")
        if name.lower() == 'done':
            break

        print("Select caliber from the following:")
        for i, cal in enumerate(allowed_calibers, 1):
            print(f"{i}. {cal}")
        cal_choice = input("Enter number: ")
        if cal_choice.lower() == 'done':
            break
        if not cal_choice.isdigit() or not (1 <= int(cal_choice) <= len(allowed_calibers)):
            print("Invalid selection. Please enter a number from the list.")
            continue
        caliber = allowed_calibers[int(cal_choice) - 1]

        try:
            bullet_weight = float(input("Bullet weight: ").replace(',', '.'))
            grain = float(input("Grain: ").replace(',', '.'))
            j_0m = float(input("Energy at 0 m: ").replace(',', '.'))
            j_150m = float(input("Energy at 150 m: ").replace(',', '.'))
            v_0m = float(input("Speed at 0 m: ").replace(',', '.'))
            v_150m = float(input("Speed at 150 m: ").replace(',', '.'))
        except ValueError:
            print("Invalid input! Use numbers with '.' or ',' for decimal values.")
            continue

        if caliber in rifle_calibers:
            ammo = RifleAmmunition(str(next_id), lead_free, manufacturer, name, caliber,
                                   bullet_weight, grain, j_0m, j_150m, v_0m, v_150m)
        else:
            ammo = Ammunition(str(next_id), lead_free, manufacturer, name, caliber,
                              bullet_weight, grain, j_0m, j_150m, v_0m, v_150m)

        if ammo_db.add_ammunition(ammo):
            next_id += 1



# Create the database instance
ammo_db = AmmunitionDatabase()

# Menu system – would run interactively (uncomment for actual use)
while True:
     print("\n" + "="*50)
     print("      🔍 Ammunition Database – Main Menu")
     print("="*50)
     print(" 1. ➕ Manual input")
     print(" 2. 🔀 Sort data")
     print(" 3. 🔎 Search data")
     print(" 4. 📋 Display all entries")
     print(" 5. 📊 Average grain per caliber")
     print(" 6. 🧮 Multi-column sort")
     print(" 7. 📈 Most common caliber & bullet weight")
     print(" 8. 🚪 Exit")
     print("="*50)

     choice = input("Please enter your choice (1–8): ")

     if choice == '1':
         manual_input(ammo_db)
     elif choice == '2':
         key = input("Sort by (e.g., grain): ").strip()
         ammo_db.ammo_list = AmmunitionSorter.merge_sort(ammo_db.ammo_list, [key])
         ammo_db.display_all()
     elif choice == '3':
         term = input("Search term: ")
         results = AmmunitionSearch.search(ammo_db.ammo_list, term)
         for r in results:
             print(r)
     elif choice == '4':
         ammo_db.display_all()
     elif choice == '5':
         ammo_db.average_grain()
     elif choice == '6':
         keys = input("Enter keys (comma-separated): ").split(',')
         keys = [k.strip() for k in keys if k.strip()]
         ammo_db.ammo_list = AmmunitionSorter.merge_sort(ammo_db.ammo_list, keys)
         ammo_db.display_all()
     elif choice == '7':
         ammo_db.most_common()
     elif choice == '8':
         break
     else:
         print("Invalid choice.")