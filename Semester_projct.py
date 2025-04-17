# Full Project Implementation: Social Media Post Analysis System




# ---- Class Definition ----


class SocialMediaPost:
    def __init__(self, post_id: int, content: str, likes: int, viral: bool, controversial: bool, logic_expr: str):
        self.post_id = post_id
        self.content = content
        self.likes = likes
        self.viral = viral
        self.controversial = controversial
        self.logic_expr = logic_expr
        self.logic_result = self.evaluate_expression()

    def evaluate_expression(self) -> bool:
        if self.logic_expr == "p ∧ q":
            return self.viral and self.controversial
        elif self.logic_expr == "p ∨ q":
            return self.viral or self.controversial
        elif self.logic_expr == "¬q":
            return not self.controversial
        elif self.logic_expr == "p → q":
            return not self.viral or self.controversial
        elif self.logic_expr == "p ↔ q":
            return self.viral == self.controversial
        return False

    def get_summary(self) -> tuple:
        return (self.post_id, self.likes, self.logic_expr, self.logic_result, self.content)

    def print_truth_table(self):
        print(f"\nTruth Table for expression '{self.logic_expr}'")
        print("p (viral) | q (controversial) | Result")
        for p in [True, False]:
            for q in [True, False]:
                temp = SocialMediaPost(self.post_id, "", 0, p, q, self.logic_expr)
                print(f"{p:<9} | {q:<16} | {temp.logic_result}")






# ---- Sorting Algorithms ----




# Insertion Sort (Loop)
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

# Merge Sort (Recursion)
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
        a = left[0]
        b = right[0]
        if (a.likes > b.likes) or (a.likes == b.likes and a.logic_result and not b.logic_result):
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    return result + left + right

# ---- Display Functions ----

def display_posts(posts):
    print("\nSorted Posts:")
    for post in posts:
        print(f"{post.post_id}. '{post.content}' | Likes: {post.likes} | Logic: {post.logic_expr} = {post.logic_result}")

def show_truth_table(posts, post_id):
    for post in posts:
        if post.post_id == post_id:
            post.print_truth_table()
            return

# ---- Sample Dataset (list + tuple + dict included) ----

posts_list = [
    SocialMediaPost(1, "Funny cat video", 120, True, False, "p ∧ q"),
    SocialMediaPost(2, "Politics debate", 90, True, True, "p ∧ q"),
    SocialMediaPost(3, "Travel tips", 150, True, False, "p → q"),
    SocialMediaPost(4, "Meme collection", 120, False, True, "p ∨ q"),
    SocialMediaPost(5, "AI news", 130, True, True, "¬q"),
    SocialMediaPost(6, "Piano playlist", 75, False, False, "p ↔ q")
]

# tuple: storing available expressions
logic_options = ("p ∧ q", "p ∨ q", "¬q", "p → q", "p ↔ q")

# dictionary: mapping post ID to content
post_dict = {post.post_id: post.content for post in posts_list}

# ---- Simple Console Menu Logic (print only version) ----

def run_final_project_simulation():
    print("=== SOCIAL MEDIA POST ANALYSIS TOOL ===")
    print("Initial Posts:")
    display_posts(posts_list)

    sorted_by_insertion = insertion_sort(posts_list[:])
    print("\n--- Sorted by Insertion Sort ---")
    display_posts(sorted_by_insertion)

    sorted_by_merge = merge_sort(posts_list[:])
    print("\n--- Sorted by Merge Sort ---")
    display_posts(sorted_by_merge)

    print("\n--- Displaying Truth Table for Post ID 2 ---")
    show_truth_table(posts_list, 2)

    print("\n--- Logic Expressions Available ---")
    for expr in logic_options:
        print(f"- {expr}")

    print("\n--- Post Dictionary (ID to Content) ---")
    for pid, text in post_dict.items():
        print(f"{pid}: {text}")

run_final_project_simulation()
