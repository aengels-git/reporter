class TextChunk:
    def __init__(self,
                 content="",
                 level=0):
        self.content = content
        self.level = level

    def create(self):
        txt = "\n" + "".ljust(self.level,"#") + f" {self.content}\n"
        return txt
