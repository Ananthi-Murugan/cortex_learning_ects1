from protos import tool_pb2

class ToolService():
    """ Interface for creating tools that can be used by client via GRPC """
    name: str
    description: str
    direct_return: bool

    def execute(self, params: str) -> str:
        """ Empty execute function to be implemented """
        raise NotImplementedError('Method not implemented!')
    
    def gen_proto_message(self) -> tool_pb2.AgentTool:
        """ Return the proto message associate with the tool """
        return tool_pb2.AgentTool(name=self.name, description=self.description, direct_return=self.direct_return)
