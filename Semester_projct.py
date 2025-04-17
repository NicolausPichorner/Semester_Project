import time

# ---- Class Definitions ----

class SocialMediaPost:
    def __init__(self, post_id, content, likes, viral, controversial, logic_expr):
        self.post_id = post_id
        self.content = content
        self.likes = likes
        self.viral = viral
        self.controversial = controversial
        self.logic_expr = logic_expr
        self.logic_result = self.evaluate_expression()

    def evaluate_expression(self):
        try:
            expr = self.logic_expr.replace("∧", "and").replace("∨", "or").replace("¬", "not ")
            expr = expr.replace("→", "(not self.viral or self.controversial)").replace("↔", "(self.viral == self.controversial)")
            return eval(expr, {}, {"self": self})
        except Exception:
            return False

    def display_truth_table(self):
        table = []
        for p in [True, False]:
            for q in [True, False]:
                self.viral = p
                self.controversial = q
                result = self.evaluate_expression()
                table.append((p, q, result))
        return table

    def __str__(self):
        return f"Post ID: {self.post_id} | Likes: {self.likes} | Logic: {self.logic_expr} = {self.logic_result} | Content: {self.content}"


# ---- Sorting Algorithms ----

# Insertion Sort (loop-based)
def insertion_sort(posts):
    for i in range(1, len(posts)):
        key = posts[i]
        j = i - 1
        while j >= 0 and (posts[j].likes < key.likes or
                          (posts[j].likes == key.likes and not posts[j].logic_result and key.logic_result)):
            posts[j + 1] = posts[j]
            j -= 1
        posts[j + 1] = key
    return posts

# Merge Sort (recursive)
def merge_sort(posts):
    if len(posts) <= 1:
        return posts
    mid = len(posts) // 2
    left = merge_sort(posts[:mid])
    right = merge_sort(posts[mid:])
    return merge(left, right)

def merge(left, right):
    result = []
    while left and right:
        if (left[0].likes > right[0].likes or
            (left[0].likes == right[0].likes and left[0].logic_result and not right[0].logic_result)):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right


# ---- Search Algorithm ----

def search_by_keyword(posts, keyword):
    return [post for post in posts if keyword.lower() in post.content.lower()]


# ---- Performance Analysis ----

def measure_sorting_time(sort_func, posts):
    start_time = time.time()
    sorted_posts = sort_func(posts[:])
    end_time = time.time()
    duration = end_time - start_time
    return sorted_posts, duration


# ---- Sample Dataset ----

default_posts = [
    SocialMediaPost(1, "Cats dancing under moonlight", 120, True, False, "viral ∧ controversial"),
    SocialMediaPost(2, "Politics today: chaos or clarity?", 90, True, True, "viral ∧ controversial"),
    SocialMediaPost(3, "Top 10 travel destinations", 150, True, False, "viral → controversial"),
    SocialMediaPost(4, "Memes that broke the internet", 120, False, True, "viral ∨ controversial"),
    SocialMediaPost(5, "AI taking over the world?", 130, True, True, "¬controversial"),
    SocialMediaPost(6, "Peaceful piano for work", 75, False, False, "viral ↔ controversial"),
]


# ---- User Interaction ----

def display_menu():
    print("\n==== SOCIAL MEDIA POST ANALYSIS SYSTEM ====")
    print("1. Show all posts")
    print("2. Sort by Insertion Sort")
    print("3. Sort by Merge Sort")
    print("4. Search by keyword")
    print("5. Show truth table of a post")
    print("6. Exit")
    return input("Choose an option (1-6): ")

def display_posts(posts):
    for post in posts:
        print(post)

def run_system(posts):
    while True:
        choice = display_menu()
        if choice == "1":
            display_posts(posts)
        elif choice == "2":
            sorted_posts, duration = measure_sorting_time(insertion_sort, posts)
            print(f"\nSorted with Insertion Sort (Time: {duration:.6f}s):")
            display_posts(sorted_posts)
        elif choice == "3":
            sorted_posts, duration = measure_sorting_time(merge_sort, posts)
            print(f"\nSorted with Merge Sort (Time: {duration:.6f}s):")
            display_posts(sorted_posts)
        elif choice == "4":
            keyword = input("Enter keyword to search for: ")
            found = search_by_keyword(posts, keyword)
            print(f"\nFound {len(found)} posts:")
            display_posts(found)
        elif choice == "5":
            post_id = int(input("Enter Post ID to show its truth table: "))
            for post in posts:
                if post.post_id == post_id:
                    table = post.display_truth_table()
                    print(f"\nTruth Table for expression: {post.logic_expr}")
                    print("Viral | Controversial | Result")
                    for row in table:
                        print(f"{row[0]}     | {row[1]}          | {row[2]}")
        elif choice == "6":
            print("Exiting... Bye!")
            break
        else:
            print("Invalid choice. Please select a number between 1 and 6.")


# ---- Start Application ----

run_system(default_posts)
