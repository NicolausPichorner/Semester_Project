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

import csv

# 1. Data Structure: a list of dictionaries
ammo_data = []

# 2. Manual input function
def manual_input():
    print("Enter ammunition data (type 'done' to stop):")
    while True:
        post_id = input("ID: ")
        if post_id.lower() == 'done':
            break
        ammo = {
            'ID': post_id,
            'lead_free': input("Lead free (yes/no): "),
            'manufacturer': input("Manufacturer: "),
            'name': input("Name: "),
            'caliber': input("Caliber: "),
            'bullet_weight': float(input("Bullet Weight: ")),
            'grain': float(input("Grain: ")),
            'j_0m': float(input("0 m (J): ")),
            'j_150m': float(input("150 m (J): ")),
            'v_0m': float(input("0 m (m/s): ")),
            'v_150m': float(input("150 m (m/s): "))
        }
        ammo_data.append(ammo)

# 3. File upload function
def file_upload(filename):
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['bullet_weight'] = float(row['bullet_weight'])
            row['grain'] = float(row['grain'])
            row['j_0m'] = float(row['j_0m'])
            row['j_150m'] = float(row['j_150m'])
            row['v_0m'] = float(row['v_0m'])
            row['v_150m'] = float(row['v_150m'])
            ammo_data.append(row)

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

# 8. Remove duplicates by ID
def remove_duplicates():
    unique = {}
    for item in ammo_data:
        unique[item['ID']] = item
    print(f"Removed {len(ammo_data) - len(unique)} duplicates.")
    global ammo_data
    ammo_data = list(unique.values())

# 9. Most common caliber and bullet weight
def most_common():
    from collections import Counter
    calibers = [item['caliber'] for item in ammo_data]
    weights = [item['bullet_weight'] for item in ammo_data]
    print("Most common caliber:", Counter(calibers).most_common(1)[0])
    print("Most common bullet weight:", Counter(weights).most_common(1)[0])

# 10. Main loop
while True:
    print("""
    1. Manual input
    2. Upload from file
    3. Sort data
    4. Search data
    5. Display data
    6. Average grain per caliber
    7. Multi-column sort
    8. Remove duplicates
    9. Most common values
    10. Exit
    """)
    choice = input("Choose: ")

    if choice == '1':
        manual_input()
    elif choice == '2':
        filename = input("CSV file name: ")
        file_upload(filename)
    elif choice == '3':
        key = input("Sort by key: ")
        ammo_data = merge_sort(ammo_data, [key])
    elif choice == '4':
        term = input("Search term: ")
        search_data(term)
    elif choice == '5':
        display_data()
    elif choice == '6':
        average_grain_per_caliber()
    elif choice == '7':
        keys = input("Enter keys separated by comma (e.g., lead_free,caliber,v_150m): ").split(',')
        ammo_data = merge_sort(ammo_data, keys)
    elif choice == '8':
        remove_duplicates()
    elif choice == '9':
        most_common()
    elif choice == '10':
        print("Exiting program.")
        break
    else:
        print("Invalid choice.")
