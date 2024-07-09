from locust import User, task, constant


class MyScript(User):
    weight = 2                  # Weightage to each task
    wait_time = constant(1)     #pacing time or wait time between each task

    @task
    def launch(self):
        print("Launching the URl")

    @task
    def search(self):
        print("searching")

    @task
    def launch(self):
        print("Launching the URL2")

    @task
    def search2(self):
        print("Searching2")