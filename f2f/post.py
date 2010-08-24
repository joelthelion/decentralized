

class Post:
    "Represents either posts or comments."
    def __init__(self):
        #URL the post links to. Unused in the case of a comment
        self.url=u""
        #Title of the post: ununsed(?) in the case of a comment
        self.title=u""
        #Content of the post
        self.content=u""
        #Votes received so far concerning the post
        self.votes=[]
        #Date of the first reception of this post 
        self.reception_date=0
        #ID of the parent post
        self.parent=u""
        #Nickname of the post's original author
        self.author=u""
    def pretty_print(self):
        return self.url + " : " + self.title + " (" + self.author + ")\n" + self.content
    "Return a unique identifier for the post"
    def get_id(self):
        return 0
