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


from collections import Counter

# Data Structure: a list of dictionaries
ammo_data = []

# 1. Manual input function
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

        duplicate_found = any(
            entry['manufacturer'].lower() == manufacturer.lower() and
            entry['name'].lower() == name.lower()
            for entry in ammo_data
        )

        if duplicate_found:
            print(f"❌ Entry with manufacturer '{manufacturer}' and name '{name}' already exists. Skipping entry.\n")
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
        print("✅ Entry added! Wirte done to exit.\n")


# 2. Merge Sort (by single or multi-key)
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

# 3. Search function
def search_data(keyword):
    results = [item for item in ammo_data if keyword.lower() in str(item).lower()]
    for r in results:
        print(r)

# 4. Display function
def display_data():
    if not ammo_data:
        print("No data to display.")
        return
    print("\nID | LeadFree | Manufacturer | Name | Caliber | BulletWeight | Grain | J@0m | J@150m | V@0m | V@150m")
    for item in ammo_data:
        print(f"{item['ID']} | {item['lead_free']} | {item['manufacturer']} | {item['name']} | {item['caliber']} | {item['bullet_weight']} | {item['grain']} | {item['j_0m']} | {item['j_150m']} | {item['v_0m']} | {item['v_150m']}")

# 5. Average grain per caliber
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



# 7. Most common caliber and bullet weight
def most_common():
    if not ammo_data:
        print("❌ No data available. Please enter or upload ammunition data first.")
        return

    calibers = [item['caliber'] for item in ammo_data]
    weights = [item['bullet_weight'] for item in ammo_data]

    if calibers:
        common_caliber = Counter(calibers).most_common(1)[0]
        print(f"✅ Most common caliber: {common_caliber[0]} ({common_caliber[1]}x)")
    else:
        print("❌ No caliber data available.")

    if weights:
        common_weight = Counter(weights).most_common(1)[0]
        print(f"✅ Most common bullet weight: {common_weight[0]} ({common_weight[1]}x)")
    else:
        print("❌ No bullet weight data available.")


# 10. Main loop
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
        print("\nAvailable sort keys:")
        print("lead_free, manufacturer, name, caliber, bullet_weight, grain, j_0m, j_150m, v_0m, v_150m")

        keys = input("Enter keys separated by comma (e.g., lead_free,caliber,v_150m): ").split(',')
        keys = [k.strip() for k in keys if k.strip()] 

        valid_keys = ['lead_free', 'manufacturer', 'name', 'caliber',
                      'bullet_weight', 'grain', 'j_0m', 'j_150m', 'v_0m', 'v_150m']

        if all(k in valid_keys for k in keys):
            ammo_data = merge_sort(ammo_data, keys)  
            print("✅ Sorted by multiple keys:", ', '.join(keys))
            display_data()  
            input("\nPress Enter to return to menu...")  
        else:
            print("❌ Invalid key(s). Please only use valid field names.")
            input("Press Enter to return to menu...")
        print("❌ Invalid key(s). Please only use valid field names.")
        input("Press Enter to return to menu...")

        display_data()
    elif choice == '7':
        most_common()
    elif choice == '8':
        print("Exiting program. Thanks for using the Ammunition Database!")
        break
    else:
        print("Invalid choice.")
