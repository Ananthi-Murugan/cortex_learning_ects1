from concurrent import futures
from typing import (Dict, List)
import logging

import grpc
from protos import tool_pb2_grpc as tool_grpc
from protos import tool_pb2 as tool_pb
from app.tool_interface import ToolService
from app.tools import *

TOOL_DICT: Dict[str, ToolService] = {}

# Servicer to listen to client requests and send back responses 
class ToolkitServicer(tool_grpc.ToolkitServicer):
    def DescribeTools(self, request, context):
        logging.info("DescribeTools Request Made")
        logging.info(request)
        
        tool_list = tool_pb.ToolList(tools=[tool.gen_proto_message() for tool in TOOL_DICT.values()])
        return tool_list

    def ExecuteTool(self, request, context):
        logging.info("ExecuteTool Request Made")
        logging.info(request)
        
        commands=[]
        try:
            response = TOOL_DICT[request.name].execute(request.params)
            if (type(response) is dict):
                message = response['message']
                for command in response['commands']:
                    commands.append(tool_pb.Command(command=command["command"], data=command["data"]))
            else:
                message = response
        except Exception as e:
            logging.error(e)
            message = f"An unknown error occured while executing {request.name}: {e}"
        
        logging.info(message)
        return tool_pb.ToolResponse(message=message, commands=commands)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tool_grpc.add_ToolkitServicer_to_server(ToolkitServicer(), server)

    server.add_insecure_port("[::]:5000")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    # Decide what tools to host here:
    tool_list: List[ToolService] = [
        Greeter()
    ]

    logging.basicConfig(level=logging.DEBUG)
    logging.info("Init GRPC server")

    # Create the tool dict, to reference tools by name:
    TOOL_DICT = {tool.name: tool for tool in tool_list}
    serve()
    
