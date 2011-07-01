from wombatdb import db
class Asset(db.Model):

    def create_db():
        __tablename__ = 'assets'
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.Text, default=u'Unnamed Asset')
        used_by = db.Column(db.Integer, db.ForeignKey('collections.id'))

    def __init__(self,name,tags):
        self.name = name
        self.tags = tags
