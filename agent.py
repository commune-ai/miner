import commune as c

class Agent(c.Module):

    def __init__(self, name='agent', 
                    network='commune', 
                    network_module='subnet', 
                    link_fns=None, 
                    tools=['module.cmd', 'module.find_object_paths']):

        self.set_network(network=network, network_module=network_module, link_fns=link_fns)
        self.set_tools(tools=tools)
        self.set_model()
        
    def set_model(self, model='model.openrouter'):
        self.model = c.module(model)()

    def set_network(self, network='all', network_module = 'subnet', link_fns=None):
        self.network_module= c.module(network_module)(network=network)
        link_fns = link_fns or self.network_module.fns()
        for fn in link_fns:
            setattr(self, fn, getattr(self.network_module, fn))

    @property
    def networks(self):
        return list(self.network_module.state.keys())

    def find_objects(self, path='./'):
        return c.find_object_paths(path)

    def set_tools(self, tools=['module.cmd', 'module.find_object_paths']):
        tool_schema = {}
        for tool in tools:
            print(tool)
        
            if '.' in tool:
                module = '.'.join(tool.split('.')[:-1])
                module = c.module(module)
                fn = tool.split('.')[-1]
            else:
                module = self
                fn = tool
            fn_obj = getattr(module, fn)
            fn_schema = c.fn_schema(fn_obj)
            tool_schema[tool] = fn_schema
        subnet_schema = self.network_module.schema()
        self.tool_schema = tool_schema
        self.tool_schema.update(subnet_schema)

            
        return tool_schema


    def ask(self, text, **kwargs):

        instructions = [
            'FOLLOW THE TEXT USING THE TOOLS, ONLY USE THE TOOLS ',
            'ONLY RESPOND IN THE OUTPUT_FORMAT ',
            'IF YOU ARE USING A TOOL YOU CANNOT POST A RESULT',
            'DO NOT POST A RESULT IF YOU ARE USING A TOOL AND DO', 
            'DO NOT USE A TOOL IF YOU ARE POSTING A RESULT',
            'DO NOT REPOND OUTSIDE OF THE OUTPUT FORMAT',
            'YOU WILL BE PENALIZED IF YOU DO NOT FOLLOW THE INSTRUCTIONS', 
            'IF NONE OF THE TOOLS CAN BE USED, YOU CAN POST A RESULT',


        ]

        prompt = {
            'input': text,
            'output': {
                'tool_execution_plan': [{'tool': 'str', 'params': 'dict'}], 
                'result': 'None',
                'memory': 'None' 
            },
            'instructions': instructions,
            'tools': self.tool_schema,


        }

        return self.model.generate(c.python2str(prompt), **kwargs)


    