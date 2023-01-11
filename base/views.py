from fastapi.templating import Jinja2Templates


class BaseTemplateView:
    templates = Jinja2Templates(directory="dashboard/templates")

    def list(self, request, data):
        return self.templates.TemplateResponse(
            name="list.html", context={"request": request, "data": data}
        )
