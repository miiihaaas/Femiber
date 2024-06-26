from femiber import app, db
from sqlalchemy.ext.hybrid import hybrid_property
from unidecode import unidecode


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    standard_name = db.Column(db.String(255))
    wikidata = db.Column(db.String(255))
    recorded_names = db.Column(db.String(255))
    about = db.Column(db.Text)
    chapters_rubrics = db.Column(db.String(350))
    people_filter = db.Column(db.String(255))
    cases = db.relationship('Cases', backref='cases_people', lazy=True)


class Cases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)
    consang_kinship = db.Column(db.String(255))
    religion = db.Column(db.String(255))
    religion_flag = db.Column(db.String(255))
    traits = db.Column(db.String(255))
    partnership = db.Column(db.String(255))
    motherhood = db.Column(db.String(255))
    physical_violence = db.Column(db.String(255))
    passing_away = db.Column(db.String(255))
    case_summary = db.Column(db.Text)
    case_summary_unidecode = db.Column(db.Text)
    excerpt = db.Column(db.Text)
    excerpt_unidecode = db.Column(db.Text)
    reference = db.Column(db.String(255))
    notes = db.Column(db.Text)
    
    # @hybrid_property
    # def case_summary_unidecoded(self):
    #     return unidecode(self.case_summary)

    # @hybrid_property
    # def consang_kinship_unidecoded(self):
    #     return unidecode(self.consang_kinship)

with app.app_context():
    db.create_all()
    db.session.commit()