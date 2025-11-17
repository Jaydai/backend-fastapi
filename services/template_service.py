from domains.entities import TemplateTitle
from dtos import TemplateTitleResponseDTO
from repositories import TemplateRepository
from utils import localize_object

class TemplateService:
    @staticmethod
    def get_all_templates_title() -> list[TemplateTitleResponseDTO]:
        # TODO: Implement logic in needed for this function
        templates = TemplateRepository.get_all_templates_title()
        print("TEMPLATES IN SERVICE", templates)
        return [
            # TODO: localize fields
            TemplateTitleResponseDTO(**localize_object(template, "fr", ["title"]))
            for template in templates
        ]