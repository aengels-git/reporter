class CodeChunk:
    def __init__(self,
                 content="",
                 include = True,
                 echo = False,
                 output = True,
                 error = False,
                 warning  = False,
                 evaluate = True):
        self.content = content
        self.include = CodeChunk.bool_to_str(include)
        self.echo = CodeChunk.bool_to_str(echo)
        self.output = CodeChunk.bool_to_str(output)
        self.error = CodeChunk.bool_to_str(error)
        self.warning = CodeChunk.bool_to_str(warning)
        self.eval = CodeChunk.bool_to_str(evaluate)
            
    @staticmethod
    def bool_to_str(boolean):
        if boolean:
            return "true"
        else:
            return "false"
        
    def create(self):
        chunk = ["\n```{python}\n",
                    "#| eval: {}\n".format(self.eval),
                    "#| echo: {}\n".format(self.echo),
                    "#| output: {}\n".format(self.output),
                    "#| warning: {}\n".format(self.warning),
                    "#| error: {}\n".format(self.error),
                    "#| include: {}\n".format(self.include),
                    "{}\n".format(self.content),
                    "```"
                    ]
        output = "".join(i for i in chunk)
        return output
