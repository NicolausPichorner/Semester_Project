# what should the code do?
# Database About Ammunition Types
# ID, lead or lead free, Manufacturer, Name, Caliber, Bullet Weight, Grain, 0 m / j, 150 m / j, 0 m / s, 150 m /s
# upload data throug manually input or file upload
# sort through merge sort 
# What it should do?
# 1. Upload data through manual input or file upload
# 2. Sort data through merge sort
# 3. Search through the data
# 4. Display data in a table format
# 6. find average grain weight per caliber 
# 7. sort more then 1 colum for example lead free - caliber - 150 m / s 
# 9. dubble check for duplicates and say if there are any and remove them 
# 10. find the most common caliber and bullet weight
# 11. exit 

# Ammunition Database Program (based on your slides knowledge)
# Features: manual/file input, merge sort, search, display, average, multi-column sort, duplicate removal, stats
# Ammunition Database Program (based on your slides knowledge)
# Features: manual/file input, merge sort, search, display, average, multi-column sort, duplicate removal, stats

import csv
from collections import Counter

# 1. Data Structure: a list of dictionaries
ammo_data = []

# 2. Manual input function
def manual_input():
    print("Enter ammunition data (type 'done' anytime to stop):")
    allowed_calibers = ['.308', '30-06 Springfield', '300 Win Mag', '243']
    next_id = len(ammo_data) + 1

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
            bullet_weight = float(input("Bullet weight (e.g., 9.7): ").replace(',', '.'))
            grain = float(input("Grain (e.g., 150 or 150.5): ").replace(',', '.'))
            j_0m = float(input("Energy at 0 m (Joules): ").replace(',', '.'))
            j_150m = float(input("Energy at 150 m (Joules): ").replace(',', '.'))
            v_0m = float(input("Speed at 0 m (m/s): ").replace(',', '.'))
            v_150m = float(input("Speed at 150 m (m/s): ").replace(',', '.'))
        except ValueError:
            print("Invalid input! Use numbers with '.' or ',' for decimal values.")
            continue

        ammo = {
            'ID': str(next_id),
            'lead_free': lead_free,
            'manufacturer': manufacturer,
            'name': name,
            'caliber': caliber,
            'bullet_weight': bullet_weight,
            'grain': grain,
            'j_0m': j_0m,
            'j_150m': j_150m,
            'v_0m': v_0m,
            'v_150m': v_150m
        }

        ammo_data.append(ammo)
        next_id += 1
        print("✅ Entry added!\n")

# 4. Merge Sort (by single or multi-key)
def merge_sort(data, keys):
    if len(data) <= 1:
        return data
    mid = len(data) // 2
    left = merge_sort(data[:mid], keys)
    right = merge_sort(data[mid:], keys)
    return merge(left, right, keys)

def merge(left, right, keys):
    result = []
    while left and right:
        l_val = tuple(left[0][k] for k in keys)
        r_val = tuple(right[0][k] for k in keys)
        if l_val <= r_val:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    result += left + right
    return result

# 5. Display function
def display_data():
    if not ammo_data:
        print("No data to display.")
        return
    print("\nID | LeadFree | Manufacturer | Name | Caliber | BulletWeight | Grain | J@0m | J@150m | V@0m | V@150m")
    for item in ammo_data:
        print(f"{item['ID']} | {item['lead_free']} | {item['manufacturer']} | {item['name']} | {item['caliber']} | {item['bullet_weight']} | {item['grain']} | {item['j_0m']} | {item['j_150m']} | {item['v_0m']} | {item['v_150m']}")

# 6. Search function
def search_data(keyword):
    results = [item for item in ammo_data if keyword.lower() in str(item).lower()]
    for r in results:
        print(r)

# 7. Average grain per caliber
def average_grain_per_caliber():
    calibers = {}
    for item in ammo_data:
        cal = item['caliber']
        if cal not in calibers:
            calibers[cal] = []
        calibers[cal].append(item['grain'])
    for cal in calibers:
        avg = sum(calibers[cal]) / len(calibers[cal])
        print(f"Average grain for {cal}: {avg:.2f}")

# 8. Remove duplicates by full entry
def remove_duplicates():
    global ammo_data
    seen = []
    unique = []
    for item in ammo_data:
        if item not in seen:
            seen.append(item)
            unique.append(item)
    removed = len(ammo_data) - len(unique)
    ammo_data = unique
    print(f"Removed {removed} exact duplicate(s).")

# 9. Most common caliber and bullet weight
def most_common():
    calibers = [item['caliber'] for item in ammo_data]
    weights = [item['bullet_weight'] for item in ammo_data]
    print("Most common caliber:", Counter(calibers).most_common(1)[0])
    print("Most common bullet weight:", Counter(weights).most_common(1)[0])

# 10. Main loop
while True:
    print("""
    1. Manual input
    2. Sort data
    3. Search data
    4. Display data
    5. Average grain per caliber
    6. Multi-column sort
    7. Remove duplicates
    8. Most common values
    9. Exit
    """)
    choice = input("Choose: ")

    if choice == '1':
        manual_input()
    elif choice == '2':
        if not ammo_data:
            print("❌ No data available to sort. Please add or upload data first.\n")
            continue

        print("\nAvailable sort keys:")
        print("lead_free, manufacturer, name, caliber, bullet_weight, grain, j_0m, j_150m, v_0m, v_150m")
        key = input("Enter one field to sort by: ").strip()

        valid_keys = ['lead_free', 'manufacturer', 'name', 'caliber',
                      'bullet_weight', 'grain', 'j_0m', 'j_150m', 'v_0m', 'v_150m']

        if key in valid_keys:
            ammo_data = merge_sort(ammo_data, [key])
            print(f"✅ Sorted by '{key}'. Sorted list:\n")
            display_data()
            input("\nPress Enter to return to menu...")
        else:
            print("❌ Invalid key. Please try again.\n")
    elif choice == '3':
        term = input("Search term: ")
        search_data(term)
    elif choice == '4':
        display_data()
    elif choice == '5':
        average_grain_per_caliber()
    elif choice == '6':
        keys = input("Enter keys separated by comma (e.g., lead_free,caliber,v_150m): ").split(',')
        ammo_data = merge_sort(ammo_data, keys)
        print("✅ Sorted by multiple keys.")
        display_data()
    elif choice == '7':
        remove_duplicates()
    elif choice == '8':
        most_common()
    elif choice == '9':
        print("Exiting program. Thanks for using the Ammunition Database!")
        break
    else:
        print("Invalid choice.")
