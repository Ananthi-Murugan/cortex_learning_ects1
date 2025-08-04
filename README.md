# Cortex Tool Server Template

This repo contains a GRPC toolkit server which is necessary for integration with any Cortex agent in order to interact with external tools.

## Tool Interface Overview

In order for a Cortex model to interact with external functionality, the server that will need to act as a tool server by implementing the accepted tool interface. The modle toolkit configuration that will direct the model to interact with the tool server.
- The tool server exposes 2 main RPCs:
  -	`DescribeTools`: Provides a list of available tools with names and descriptions. An agent uses this to see what tools it can use and how they work.
  -	`ExecuteTool`: Executes a requested tool and returns the response. An agent will call this RPC to use a tool.
- All tool servers must adhere to the expected GRPC prototype for compatibility, but the underlying architecture for how to describe, track, and execute tools is up to the developer.

## Creating a GRPC Toolkit Server

TODO: update this with backstage docs

## Hosting a GRPC Toolkit Server on CATS

Follow these steps to set up the server on the CATS DEV cluster (similar steps apply for the PROD cluster):

Follow these steps to set up the server on the CATS DEV cluster (similar steps apply for the PROD cluster):
1. Create a new project or modify an existing project in the [CATS repository]( https://github.com/EliLillyCo/LRL_light_k8s_infra_apps_test/tree/main) for your new server. See the CATS documentation for more help.
2. Modify your namespace YAML to add an `sg-rule` allowing ingress from the `llm-dev` namespace on your exposed port. Refer to [SG Rule Docs]( https://github.com/EliLillyCo/LRL_light_k8s_infra_apps/blob/main/examples/sg-rule.md) for details.
```json
"ingress_rules" : [{
	"namespace_allow_from": "llm-dev",
	"port": 50051
}]
```
3. Add an automated GitHub workflow or a manual script to build and push your container. See the CATS documentation or the CATS team for help.
4. After a few minutes, the server will be deployed on the CATS server and should be reachable from the `llm-dev` namespace. Optionally, test to check the deployment is set up correctly by running a `curl` command from `llm-dev` to your server. If set up correctly, the response should indicate the connection is not allowed due to GRPC not supporting curl. If not, curl will hang.
```bash
curl http://[service-name].[namespace-name].svc.cluster.local:50051
```

## Agent and Toolkit Configuration on Cortex

TODO: Update this with current cortex configuration

Follow these steps to set up an agent and toolkit on the CATS DEV cluster deployment of Cortex (set up on a different deployment requires hosting the server on the respective CATS cluster):

1. Go to the Cortex docs page: <https://chat.apps-d.lrl.lilly.com/docs>.
2. In the `/manage/toolkit_config` endpoint, create a new toolkit, filling the server field with the server address and port. Do not include `http://`, as it is automatically added. Ensure to include the name of the new model in the `auth_models` list.
```json
"server" : "[service-name].[namespace-name].svc.cluster.local:50051"
"auth_models": [ "new-model-name" ]
```
3. In the `/manage/config` endpoint, create a new model. Ensure the toolkit's name is added to the `toolkits` list, and to include the "tool-chain" in the chain section of the config.
```json
"chain": [{"chain_class": "tool-chain", "model_iteration": 1,"order": 1}],
"toolkits": ["new-toolkit-name"]
```
4. The new agent and toolkit should have been successfully created. If everything is set up correctly the model should be able to answer prompts related to the provided tools and use them correctly. If the model isn’t working, here are potential problems:
   - Is your model working for non-tool related prompts? Then the tool server is correctly connected but the execution of certain tools are likely causing an error. Check the tool execution on the toolkit server. Use the `/manage/{toolkit_config}/toolkit_execute` to test specific tools from Cortex.
   - Is your model always returning an error to any prompt? Then the tool server is not correctly connected. Use the `/manage/{toolkit_config}/toolkit_describe` to check the health of your toolkit server.
   - Does the describe endpoint not work? Then the llm-dev namespace is unable to find and connect to your tool server. Double check the address of the toolkit config. Try to curl to the GRPC server from the llm-dev namespace. Double check the exposed ports on the GRPC server and the sg rules.
   - Is your toolkit server not deploying on CATS? Double check to see if the CATS configuration is correct. Run your container locally to check it can deploy correct. Reach out to the CATS team if problems persist.
  
## Understanding Tool Commands

Tool commands enable an agent to initiate functionality indirectly, providing a layer of security, especially for sensitive operations like database writes. Commands allow the agent to formulate requests through tools, and these commands are returned directly in the Cortex model response as metadata. External services leveraging the Cortex API can extract and execute these commands with additional protection measures. Although optional, this functionality enhances security and reliability in certain scenarios and can be implemented in tools as needed.

### Implementation Details:

- **Flexibility**: Implementing a command requires only a command name and associated data.
- **Example**: The `ChangeWellData` command in `grpc-server/tools.py` illustrates its usage.

### Example Workflow:

1. An agent executes the `ChangeWellData` tool to modify data in a database.
2. Instead of directly modifying the data (which could lead to errors), a command is constructed with the appropriate parameters.
3. The command is included in the `ToolResponse`, along with a success message.
4. The agent reads only the message from the `ToolResponse` while the command is saved.
5. Upon the agent's completion and returning a final response, the Cortex model response includes the command as metadata.
   ```json
   {
	   "message": "Successfully changed well data.",
	   "command_request": [{
		   "command": "changeWellData",
		   "data": "{'Barcode': 'P12345', 'ContainerData': {'A1': [0, null]}}"
	   }]
   }
   ```
6. The script utilizing the Cortex API parses the `command_request` and can execute it with added protection measures, such as manual confirmation from the user.
