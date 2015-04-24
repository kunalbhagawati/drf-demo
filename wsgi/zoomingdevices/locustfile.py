from locust import HttpLocust, TaskSet, task
import random, string


# def login(l):
#     l.client.request("/admin", {"username": "admin", "password": "admin123"})


# def listDevices(l):
#     l.client.request("/devices")


# def retrieveDevice(l):
#     l.client.request("/devices/{0}".format(random.randint(1, 10)))


# class FetchBehaviour(TaskSet):
#     tasks = {listDevices: 2, retrieveDevice: 1}

#     def on_start(self):
#         login(self)


# class WebsiteUser(HttpLocust):
#     task_set = FetchBehaviour
#     min_wait = 100
#     max_wait = 1000


# from locust import HttpLocust, TaskSet, task


class LoadTest(TaskSet):

    @task(1)
    def get_all(self):
        self.client.request(
                method="GET",
                url="/devices",
                headers={
                    "Authorization": "Basic YWRtaW46YWRtaW4xMjM=",
                    "Content-Type": "application/json"})

    @task(2)
    def get_one(self):
        self.client.request(
                method="GET",
                url="/devices/{0}".format(random.randint(1, 10)),
                headers={
                    "Authorization": "Basic YWRtaW46YWRtaW4xMjM=",
                    "Content-Type": "application/json"})

    @task(1)
    def search_by_name(self):
        q = (''.join(random.choice(string.lowercase)
                for i in range(random.randint(1, 5))))
        self.client.request(
                method="GET",
                url="/devices/?search={0}".format(q),
                headers={
                    "Authorization": "Basic YWRtaW46YWRtaW4xMjM=",
                    "Content-Type": "application/json"})


class User(HttpLocust):
    task_set = LoadTest
    min_wait = 50
    max_wait = 1000
