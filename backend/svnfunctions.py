import pysvn


class SVNfunctions:
    def checkout_repo(self,link):
        client = pysvn.Client()
        client.checkout(link,'./repository')

    def update_copy(self):
        client = pysvn.Client()
        client.update('./repository')

    def get_url(self):
        client = pysvn.Client()
        entry = client.info('.')
        return entry.url

    def get_dir_content(self,updated_link):
        client = pysvn.Client()
        entry_list = client.ls('.')
        return entry_list
