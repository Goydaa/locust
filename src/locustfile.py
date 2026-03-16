from locust import HttpUser, task, between 
import random 
 
class BlogUser(HttpUser): 
    # Virtual blog user 
    # On start, gets list of all posts 
    # Then in 70%% cases views list, in 30%% - views single post 
    wait_time = between(1, 5)  # user thinks 1-5 seconds 
 
    def on_start(self): 
        # Executed when each user starts 
        response = self.client.get("/posts") 
        if response.status_code == 200: 
            self.posts_list = response.json()  # save posts list 
            print(f"User {self} loaded {len(self.posts_list)} posts") 
        else: 
            self.posts_list = [] 
            print(f"Error loading posts: {response.status_code}") 
 
    @task(7) 
    def get_all_posts(self): 
        # View list of all posts (frequent action) 
        self.client.get("/posts") 
 
    @task(3) 
    def get_single_post(self): 
        # View single post (rare action) 
        if self.posts_list:  # if list is loaded 
            # choose random post from real existing ones 
            post_id = random.choice(self.posts_list)['id'] 
        else:  # if something went wrong 
            post_id = random.randint(1, 100)  # take random number 
        self.client.get(f"/posts/{post_id}") 
