
#Imports
from abc import ABC, abstractmethod 
import time  
import matplotlib.pyplot as plt
import pandas as pd


# AbstractAmmunition class
class AbstractAmmunition(ABC):
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

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def get_sort_key(self, key):
        pass

# Ammunition 
class Ammunition(AbstractAmmunition):
    def __str__(self):
        return (f"{self.id} | {self.lead_free} | {self.manufacturer} | {self.name} | "
                f"{self.caliber} | {self.bullet_weight} | {self.grain} | "
                f"{self.j_0m} | {self.j_150m} | {self.v_0m} | {self.v_150m}")
    
    def get_sort_key(self, key):
        return getattr(self, key)


# Subclass for rifle ammunition
class RifleAmmunition(Ammunition):
    def __init__(self, *args):
        super().__init__(*args)
        self.type = "Rifle"

    def __str__(self):
        return f"{super().__str__()} | Type: {self.type}"
    
    def get_sort_key(self, key):
        if key == 'caliber':
            return f"R-{getattr(self, key)}"  # gives Rifle ammo higher sorting priority
        return getattr(self, key)

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

# Ammunition sorter (using polymorphism)
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
            l_val = tuple(left[0].get_sort_key(k) for k in keys)
            r_val = tuple(right[0].get_sort_key(k) for k in keys)
            if l_val <= r_val:
                result.append(left.pop(0))
            else:
                result.append(right.pop(0))
        result += left + right
        return result
    

# Ammunition search 
class AmmunitionSearch:
    @staticmethod
    def search_loop(data, keyword):
        start = time.perf_counter()
        result = [ammo for ammo in data if keyword.lower() in str(ammo).lower()]
        end = time.perf_counter()
        print(f"⏱️ Loop Search took {end - start:.6f} seconds.")
        return result

    @staticmethod
    def search_recursive(data, keyword, index=0, result=None, timer_start=None):
        if result is None:
            result = []
            timer_start = time.perf_counter()
        if index >= len(data):
            print(f"⏱️ Recursive Search took {time.perf_counter() - timer_start:.6f} seconds.")
            return result
        if keyword.lower() in str(data[index]).lower():
            result.append(data[index])
        return AmmunitionSearch.search_recursive(data, keyword, index + 1, result, timer_start)

    @staticmethod
    def filter_by_logic(data):
        print("Filtering using logical conditions...")
        print("You will now define the conditions:")
        try:
            energy_threshold = float(input("Minimum energy at 0m (e.g., 2000): "))
            speed_threshold = float(input("Minimum speed at 0m (e.g., 800): "))
        except ValueError:
            print("Invalid input.")
            return []

        print("\nApplied Logic:\n(Lead-Free == True AND J@0m > threshold) OR (Speed@0m > threshold)")
        start = time.perf_counter()
        result = []
        for ammo in data:
            condition_1 = (ammo.lead_free == 'yes') and (ammo.j_0m > energy_threshold)
            condition_2 = ammo.v_0m > speed_threshold
            if condition_1 or condition_2:
                result.append(ammo)
        end = time.perf_counter()
        print(f"⏱️ Truth Table Filter took {end - start:.6f} seconds.")
        return result

# Timing NR. 10 
def visualize_timings():
    methods = ['Loop Search', 'Recursive Search', 'Truth Table']
    times = []

    data = ammo_db.ammo_list
    keyword = "Ammo-999"

    # Measure Loop Search
    start = time.perf_counter()
    AmmunitionSearch.search_loop(data, keyword)
    times.append(time.perf_counter() - start)

    # Measure Recursive Search
    start = time.perf_counter()
    AmmunitionSearch.search_recursive(data, keyword)
    times.append(time.perf_counter() - start)

    # Measure Truth Table Filter
    start = time.perf_counter()
    AmmunitionSearch.filter_by_logic(data)
    times.append(time.perf_counter() - start)

    plt.bar(methods, times, color='skyblue')
    plt.ylabel("Time in seconds")
    plt.title("Algorithm Performance Comparison")
    plt.show()


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

# CSV Data import
def load_ammunition_from_csv(filepath, ammo_db):
    df = pd.read_csv(filepath, sep=';', engine='python')
    df = df.dropna(axis=1, how='all')  # leere Spalten entfernen
    df.columns = [col.strip().lower().replace(' ', '_') for col in df.columns]

    for i, row in df.iterrows():
        try:
            ammo = RifleAmmunition(
                str(i + 1),
                'yes' if 'lead' in row.get('name', '').lower() else 'no',
                row['manufacturer'],
                row['name'],
                str(row['caliber']),
                float(str(row['bullet_weight']).strip().replace(',', '.')),
                float(str(row['grain']).strip().replace(',', '.')),
                float(str(row['j_0m']).strip().replace(',', '.')),
                float(str(row['j_150m']).strip().replace(',', '.')),
                float(str(row['v_0m']).strip().replace(',', '.')),
                float(str(row['v_150m']).strip().replace(',', '.'))
            )
            ammo_db.add_ammunition(ammo)
        except Exception as e:
            print(f"⚠️ Error on row {i + 1}: {e}")

# CSV save data
def save_ammunition_to_csv(filepath, ammo_db):
    data = [{
        'ID': ammo.id,
        'LeadFree': ammo.lead_free,
        'Manufacturer': ammo.manufacturer,
        'Name': ammo.name,
        'Caliber': ammo.caliber,
        'BulletWeight': ammo.bullet_weight,
        'Grain': ammo.grain,
        'J@0m': ammo.j_0m,
        'J@150m': ammo.j_150m,
        'V@0m': ammo.v_0m,
        'V@150m': ammo.v_150m
    } for ammo in ammo_db.ammo_list]
    df = pd.DataFrame(data)
    df.to_csv(filepath, sep=';', index=False)
    print(f"✅ Saved {len(df)} entries to CSV.")




#Dummy Data Generator
import random

def generate_dummy_data(ammo_db, count=5000):
    calibers = ['.308', '30-06 Springfield', '300 Win Mag', '243']
    manufacturers = ['Hornady', 'Winchester', 'Remington', 'Federal']
    for i in range(1, count + 1):
        lead_free = random.choice(['yes', 'no'])
        manufacturer = random.choice(manufacturers)
        name = f"Ammo-{i}"
        caliber = random.choice(calibers)
        bullet_weight = random.uniform(9.0, 15.0)
        grain = random.uniform(130, 180)
        j_0m = random.uniform(1800, 3200)
        j_150m = j_0m * 0.7
        v_0m = random.uniform(750, 950)
        v_150m = v_0m * 0.8
        if caliber in calibers:
            ammo = RifleAmmunition(str(i), lead_free, manufacturer, name, caliber,
                                   bullet_weight, grain, j_0m, j_150m, v_0m, v_150m)
        else:
            ammo = Ammunition(str(i), lead_free, manufacturer, name, caliber,
                              bullet_weight, grain, j_0m, j_150m, v_0m, v_150m)
        ammo_db.add_ammunition(ammo)

# Dummy-Daten generieren
generate_dummy_data(ammo_db, count=5000)


# Menu system – would run interactively (uncomment for actual use)
while True:
    print("\n" + "=" * 50)
    print("      🔍 Ammunition Database – Main Menu")
    print("=" * 50)
    print(" 1. ➕ Manual input")
    print(" 2. 🔀 Sort data")
    print(" 3. 🔎 Search data")
    print(" 4. 📋 Display all entries")
    print(" 5. 📊 Average grain per caliber")
    print(" 6. 🧮 Multi-column sort")
    print(" 7. 📈 Most common caliber & bullet weight")
    print(" 8. ⚙️ Logical filter (Truth Table Logic)")
    print(" 9. 📊 Visualize timings")
    print("10. 📂 Load from CSV")
    print("11. 💾 Save to CSV")
    print("12. 🚪 Exit")
    print("=" * 50)

    choice = input("Please enter your choice (1–9): ")

    if choice == '1':
        manual_input(ammo_db)

    elif choice == '2':
        key = input("Sort by (e.g., grain): ").strip()
        ammo_db.ammo_list = AmmunitionSorter.merge_sort(ammo_db.ammo_list, [key])
        ammo_db.display_all()

    elif choice == '3':
        term = input("Search term: ")
        method = input("Use (1) Loop or (2) Recursion for search? ")
        if method == '1':
            results = AmmunitionSearch.search_loop(ammo_db.ammo_list, term)
        elif method == '2':
            results = AmmunitionSearch.search_recursive(ammo_db.ammo_list, term)
        else:
            print("Invalid search method.")
            results = []
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
        results = AmmunitionSearch.filter_by_logic(ammo_db.ammo_list)
        if results:
            print("\nFiltered Ammunition:")
            for r in results:
                print(r)
        else:
            print("No results matched your logical conditions.")

    elif choice == '9':
        visualize_timings()

    elif choice == '10':
        path = input("Enter CSV filepath (or press Enter for 'Ammunition1.csv'): ").strip()
        if not path:
            path = "Ammunition1.csv"
        load_ammunition_from_csv(path, ammo_db)

    elif choice == '11':
        path = input("Enter filename to save (or press Enter for 'export.csv'): ").strip()
        if not path:
            path = "export.csv"
        save_ammunition_to_csv(path, ammo_db)

    elif choice == '12':
        break

    else:
        print("Invalid choice.")
