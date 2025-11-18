from core.supabase import supabase
from domains.entities import TemplateTitle

class TemplateRepository:
    @staticmethod
    def get_all_templates_title() -> list[TemplateTitle]:
        print("HELLLLLLLLLLLLLLLLLLOOOOOOOOOOOOO")
        response = supabase.table("prompt_templates").select("id, title").execute()
        print("HELLLLLLLLLLLLLLLLLLOOOOOOOOOOOOO", response)
        return [TemplateTitle(**item) for item in response.data]