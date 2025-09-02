import os
import requests

class NotionClient:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY")
        self.database_id = os.getenv("NOTION_DATABASE_ID")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def add_course(self, course):
        estado = "Activo" if course["available"] == "Yes" else "Inactivo"
        payload = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Nombre": {
                    "title": [{
                        "text": {"content": course["name"] or "Sin nombre"}
                    }]
                },
                "Estado": {
                    "select": {"name": estado}
                },
                "Semestre/Trimestre": {
                    "rich_text": [{
                        "text": {"content": course["term"]}
                    }]
                },
                "Tiempo": {
                    "date": {"start": course["created"]}
                },
                "Profesor (a)": {
                    "rich_text": [{
                        "text": {"content": course["instructor_name"]}
                    }]
                },
                "Correo Profesor": {
                    "email": course["instructor_email"] or None
                }
            }
        }

        resp = requests.post("https://api.notion.com/v1/pages", headers=self.headers, json=payload)
        if resp.status_code != 200:
            print("❌ Error al crear curso en Notion:", resp.text)
        else:
            print("✅ Curso agregado:", course["name"])