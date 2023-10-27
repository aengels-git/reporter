class PDFHeader:
    def __init__(self,
                    title="",
                    author="",
                    toc = False,
                    toc_depth = 3):
        self.title = title
        self.author = author
        self.toc = toc
        self.toc_depth = toc_depth

    def create(self):
        header = ["---\n",
                    "title: '{}'\n".format(self.title),
                    "author: '{}'\n".format(self.author),
                    "format:\n",
                    "".ljust(2)+"pdf:\n",
                    "".ljust(4)+"toc: {}\n".format(self.toc),
                    "".ljust(4)+"toc-depth: {}\n".format(self.toc_depth),
                    "---\n"
                    ]
        output = "".join(i for i in header)
        return output

