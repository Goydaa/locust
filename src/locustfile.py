from locust import HttpUser, task, between 
import random 
 
class BlogUser(HttpUser): 
    Виртуальный пользователь блога. 
    При заходе на сайт получает список всех постов. 
    Потом в 70% случаев смотрит список, в 30% - читает конкретный пост. 
    wait_time = between(1, 5)  # пользователь думает 1-5 секунд 
 
    def on_start(self): 
        """Выполняется при старте каждого пользователя""" 
        response = self.client.get("/posts") 
        if response.status_code == 200: 
            self.posts_list = response.json()  # сохраняем список постов 
            print(f"Пользователь {self} загрузил {len(self.posts_list)} постов") 
        else: 
            self.posts_list = [] 
            print(f"Ошибка загрузки списка постов: {response.status_code}") 
 
    @task(7) 
    def get_all_posts(self): 
        """Посмотреть список всех постов (частое действие)""" 
        self.client.get("/posts") 
 
    @task(3) 
    def get_single_post(self): 
        """Посмотреть конкретный пост (редкое действие)""" 
        if self.posts_list:  # если список загружен 
            # выбираем случайный пост из реально существующих 
            post_id = random.choice(self.posts_list)['id'] 
        else:  # если что-то пошло не так 
            post_id = random.randint(1, 100)  # берем случайное число 
        self.client.get(f"/posts/{post_id}") 
