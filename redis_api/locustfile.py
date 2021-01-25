from locust import HttpUser, task, between


# class UserBehavior(TaskSet):
#     @task
#     def predict(self):
#         self.client.post('/predict', files={'input_text': "i love you"})


# class WebsiteUser(HttpUser):
#     task_set = UserBehavior
#     min_wait = 500
#     max_wait = 5000
    
class WebsiteUser(HttpUser):
    wait_time = between(500, 5000)
      
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        pass

    def on_stop(self):
        """ on_stop is called when the TaskSet is stopping """
        pass
          
    @task(1)
    def predict(self):
        self.client.post("/predict", json={"input": [{"input_text": "love you"}]})
        
    @task(2)
    def hello_world(self):
        self.client.get("http://0.0.0.0:8032")



