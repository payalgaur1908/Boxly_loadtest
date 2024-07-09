import random

from locust import TaskSet, task, constant, HttpUser

"""
TaskSet is the class of locust. As of now we have just defined a taskset which we have to implement but we are not telling 
 the locust to run the test for that we have to define the httpUser package.
"""


class HttpCat(TaskSet):

    @task
    def get_status(self):
        self.client.get("/200")
        print("Get status of 200")

    @task
    def get_random_statuscode(self):
        status_Code = [100, 101, 103, 105, 110, 201, 203, 204, 205, 210, 300, 301, 304, 400, 401, 404, 701, 703]
        random_url = str(random.choice(status_Code))
        res = self.client.get(random_url)
        print("Random status code")

    @task
    class MyAnotherHttpCat(TaskSet):

        @task
        def get_500_status(self):
            self.client.get("/500")
            print("Get status of 500")


class LoadTest(HttpUser):
    host = "https://http.cat"
    tasks = [TaskSet]
    wait_time = constant(1)
