import pysvn


class SVNfunctions:
    def checkout_repo(self,link):
        client = pysvn.Client()
        client.checkout(link,'./repository')
