from locust import User, task, HttpUser, constant


class MyReqRes(HttpUser):
    host = "https://reqres.in/"
    wait_time = constant(1)

    @task
    def get_users(self):
        res = self.client.get("/api/users?page=2")  # 200 response
        print(res.text)
        print(res.status_code)
        print(res.headers)


    def create_user(self):
        res1 = self.client.post("/api/users", data='''{name: "morpheus", job: "leader"}''')  # API and placeholder 201 request
        print(res1.text)
        print(res1.status_code)
        print(res1.headers)