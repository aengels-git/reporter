class HtmlHeader:
    def __init__(self,
                    title="",
                    author="",
                    theme="default",
                    toc = False,
                    toc_depth = 3,
                    toc_expand = 2,
                    toc_location = "left"):
        self.title = title
        self.author = author
        self.theme = theme
        self.toc = toc
        self.toc_depth = toc_depth
        self.toc_expand = toc_expand
        self.toc_location = toc_location
        self.available_themes = ["default","bootstrap","cerulean","cosmo","darkly","flatly","journal","lumen",
                                    "paper","readable","sandstone","simplex","spacelab","united","yeti"]
    def create(self):
        header = ["---\n",
                    "title: '{}'\n".format(self.title),
                    "author: '{}'\n".format(self.author),
                    "format:\n",
                    "".ljust(2)+"html:\n",
                    "".ljust(4)+"embed-resources: true\n",
                    "".ljust(4)+"theme: {}\n".format(self.theme),
                    "".ljust(4)+"toc: {}\n".format(self.toc),
                    "".ljust(4)+"toc-depth: {}\n".format(self.toc_depth),
                    "".ljust(4)+"toc-expand: {}\n".format(self.toc_expand),
                    "".ljust(4)+"toc-location: {}\n".format(self.toc_location),
                    "---\n"
                    ]
        output = "".join(i for i in header)
        return output

