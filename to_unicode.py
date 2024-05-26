import unicodedata
from femiber.models import Cases
from femiber import db, app


def remove_special_characters(text):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')


with app.app_context():
    cases = Cases.query.all()

    for case in cases:
        case.case_summary_unidecode = remove_special_characters(case.case_summary)
        case.excerpt_unidecode = remove_special_characters(case.excerpt)
        db.session.commit()
