import grpc
from protos import tool_pb2_grpc as tool_grpc
from protos import tool_pb2 as tool_pb

    
def run():

    with grpc.insecure_channel("localhost:5000", options=(('grpc.enable_http_proxy', 0),)) as channel:
        stub = tool_grpc.ToolkitStub(channel)

        # Request output from tool
        describe_request = tool_pb.DescribeRequest()
        tool_list = stub.DescribeTools(describe_request)
        print("Available Tools: ")

        for i, tool in enumerate(tool_list.tools):
            print(f"{i}. {tool.name}")

        tool_id = input("Choose a tool to use: ")
        input_params = input("String input into tool: ")
        tool_request = tool_pb.ToolRequest(name=tool_list.tools[int(tool_id)].name, params=input_params)
        tool_response = stub.ExecuteTool(tool_request)
        print(tool_response.message)
    
if __name__ == "__main__":
    run()
    