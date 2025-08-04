from app.tool_interface import ToolService
from protos import tool_pb2 as tool_pb2


class Greeter(ToolService):
    name = "Greeter"
    description = "Demo greeter tool"
    direct_return = False

    def execute(self, input: str, auth: tool_pb2.Auth):
        if auth is None:
            raise ValueError("auth is required")

        full_name = auth.user_context.get("full_name").string_value
        if full_name is None or full_name == "":
            raise ValueError("User full name is required")

        message = f"Hello {full_name}!"

        if input == "":
            input = "Congrats on your first Cortex Toolkit!"

        message += f" {input}"
        return message
