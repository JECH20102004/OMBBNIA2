from app.sync.blackboard import BlackboardClient
from app.sync.notion import NotionClient

def sync_blackboard_to_notion():
    bb = BlackboardClient()
    notion = NotionClient()
    courses = bb.get_courses_with_instructors()

    for course in courses:
        notion.add_course(course)

if __name__ == "__main__":
    sync_blackboard_to_notion()