from github import GitHub
from panel.models import Token
class GitHub:
    def __init__(self, username):
        self.username = username

    def removeUser(self):
        GITHUB_TOKEN = Token.objects.values().get(key='GITHUB_TOKEN')['value']
        g = GitHub(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('cognizance-amrita')
        if org.has_in_members(ghuser):
            org.remove_from_members(ghuser)

    def addUser(self):
        GITHUB_TOKEN = Token.objects.values().get(key='GITHUB_TOKEN')['value']
        g = GitHub(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('cognizance-amrita')
        if not org.has_in_members(ghuser):
            org.add_to_members(ghuser, 'member')

    def checkIfUserExists(self):
        GITHUB_TOKEN = Token.objects.values().get(key='GITHUB_TOKEN')['value']
        g = GitHub(GITHUB_TOKEN)
        ghuser = g.get_user(self.username)
        org = g.get_organization('cognizance-amrita')
        if org.has_in_members(ghuser):
            return True
        else:
            return False
