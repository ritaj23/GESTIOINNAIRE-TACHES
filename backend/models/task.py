class Task:
    def __init__(self, title, description, owner, collaborators=[]):
        self.title = title
        self.description = description
        self.owner = owner
        self.collaborators = collaborators
        self.completed = False
