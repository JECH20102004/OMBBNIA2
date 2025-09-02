import requests
import os
from typing import List, Dict

class BlackboardClient:
    def __init__(self):
        self.client_id = os.getenv("BLACKBOARD_CLIENT_ID")
        self.client_secret = os.getenv("BLACKBOARD_CLIENT_SECRET")
        self.domain = os.getenv("BLACKBOARD_DOMAIN")
        self.token = self.get_token()

    def get_token(self):
        auth = (self.client_id + ":" + self.client_secret).encode("utf-8")
        headers = {
            "Authorization": "Basic " + auth.hex(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        resp = requests.post(f"https://{self.domain}/learn/api/public/v1/oauth2/token",
                             data="grant_type=client_credentials", headers=headers)
        resp.raise_for_status()
        return resp.json()["access_token"]

    def get_courses(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"https://{self.domain}/learn/api/public/v1/courses"
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json().get("results", [])

    def get_instructor_for_course(self, course_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        user_resp = requests.get(
            f"https://{self.domain}/learn/api/public/v1/courses/{course_id}/users", headers=headers)
        user_resp.raise_for_status()
        users = user_resp.json().get("results", [])

        instructors = [u for u in users if "instructor" in u["courseRoleId"].lower()]
        if not instructors:
            return {"name": "", "email": ""}

        instructor_id = instructors[0]["userId"]
        instructor_resp = requests.get(
            f"https://{self.domain}/learn/api/public/v1/users/{instructor_id}", headers=headers)
        instructor_resp.raise_for_status()
        data = instructor_resp.json()
        full_name = f"{data['name'].get('given', '')} {data['name'].get('family', '')}".strip()
        email = data.get("contact", {}).get("email", "")
        return {"name": full_name, "email": email}

    def get_courses_with_instructors(self) -> List[Dict]:
        courses = self.get_courses()
        result = []
        for course in courses:
            instructor = self.get_instructor_for_course(course["id"])
            result.append({
                "name": course.get("name"),
                "available": course.get("availability", {}).get("available", "No"),
                "term": course.get("term", {}).get("id", "N/A"),
                "created": course.get("created"),
                "instructor_name": instructor["name"],
                "instructor_email": instructor["email"]
            })
        return result