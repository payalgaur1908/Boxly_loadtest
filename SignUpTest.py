from locust import HttpUser, TaskSet, between, task
from faker import Faker
import random
import logging

fake = Faker()
signup_url = "http://eb-boxly-ecs-alb-1362902103.eu-west-1.elb.amazonaws.com/api/users/user_signup"
build_crm = "http://eb-boxly-ecs-alb-1362902103.eu-west-1.elb.amazonaws.com/api/organization/build_my_crm"
websites = [
    "https://trulydental.ie/",
    "https://smilecareclinic.in/",
    "https://www.drleah.co.uk/",
    "https://www.reckonsys.com/",
]

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserBehavior(TaskSet):

    def on_start(self):
        """This function is called when a Locust user starts before any task is scheduled"""
        self.token = None
        self.signup()
        if self.token:
            self.build_crm_method()
        else:
            logger.error("Token not found, skipping build_crm_method call.")

    @task
    def signup(self):
        # Generate fake user data
        username = fake.user_name()
        email = fake.email()
        password = fake.password()

        # Send a POST request to the signup endpoint
        response = self.client.post(
            signup_url,
            json={"first_name": username, "email": email, "password": password},
        )

        # Extract the token from the response
        if response.status_code == 201:
            response_json = response.json()
            self.token = response_json.get("token")
            logger.info(f"Signup successful, token obtained: {self.token}")
        else:
            logger.error(f"Signup failed with status code: {response.status_code}")

    @task
    def build_crm_method(self):
        if self.token:
            # Send a POST request to a protected endpoint using the token
            payload = {
                "website_link": random.choice(websites),
                "timezone": "Asia/Kolkata",
                "country": "IN",
                "crm_built_type": 2,
            }
            response = self.client.post(
                build_crm,
                headers={"Authorization": f"Bearer {self.token}"},
                json=payload,
            )
            if response.status_code == 201:
                logger.info("build_crm_method call successful.")
            else:
                logger.error(
                    f"build_crm_method call failed with status code: {response.status_code}"
                )
        else:
            logger.error("Token not available, cannot call build_crm_method.")


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 5)