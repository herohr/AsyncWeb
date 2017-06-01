from orm import BaseModel, Field


class Article(BaseModel):
    __tablename__ = "article"
    id = Field('id', is_primary=True)
    title = Field('title')
    url = Field('url')
    author = Field('author')
    author_id = Field("author_id")
    time_write = Field("time_write")
    time_last_update = Field('time_last_update')

    def __init__(self, **kwargs):
        self.id = kwargs.get('id', None)
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.author = kwargs.get('author')
        self.author_id = kwargs.get('author_id')
        self.time_write = kwargs.get('time_write')
        self.time_last_update = kwargs.get('time_last_update')

    def __str__(self):
        return "id:{}, title:{}, author: {}".format(self.id, self.title, self.author)

    def __repr__(self):
        return self.__str__()
