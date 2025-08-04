from app.tool_interface import ToolService

class Greeter(ToolService):
    name = "Greeter"
    description = "Demo greeter tool"
    direct_return = False
    def execute(self, params: str):
        if params == "":
            params = "World"

        return f"Hello {params}!"