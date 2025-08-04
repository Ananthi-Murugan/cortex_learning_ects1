import grpc
from protos import tool_pb2_grpc as tool_grpc
from protos import tool_pb2 as tool_pb
from google.protobuf.struct_pb2 import Value


def run():
    with grpc.insecure_channel(
        "[::]:5000", options=(("grpc.enable_http_proxy", 0),)
    ) as channel:
        stub = tool_grpc.ToolkitStub(channel)

        # Request output from tool
        auth = tool_pb.Auth(user_context={"full_name": Value(string_value="John Doe")})
        describe_request = tool_pb.DescribeRequest(
            source_toolkit="cortex-tool-template", auth=auth
        )
        tool_list: tool_pb.ToolList = stub.DescribeTools(describe_request)
        print("Available Tools: ")

        for i, tool in enumerate(tool_list.tools):
            print(f"{i}. {tool.name}")

        tool_id = input("Choose a tool to use: ")
        input_params = input("String input into tool: ")
        tool_request = tool_pb.ToolRequestV2(
            name=tool_list.tools[int(tool_id)].name,
            auth=auth,
            input=input_params,
        )
        tool_response: tool_pb.ToolResponseV2 = stub.ExecuteTool(tool_request)
        print(tool_response.output)


if __name__ == "__main__":
    run()
