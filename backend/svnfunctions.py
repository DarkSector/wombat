import pysvn


class SVNfunctions:
    def checkout_repo(self,link,local_link):
        client = pysvn.Client()
        client.checkout(link,local_link)

    def update_copy(self):
        client = pysvn.Client()
        client.update('./repository')

    def get_url(self):
        client = pysvn.Client()
        entry = client.info('./repository')
        return entry.url

    def get_dir_content(self,updated_link):
        client = pysvn.Client()
        entry_list = client.ls('.')
        return entry_list

    def get_revision_no(self):
        client = pysvn.Client()
        rev_no = client.info('./repository').revision.number
        return rev_no
