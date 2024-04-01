import json
from flask import Blueprint, jsonify, render_template_string
from femiber.models import People, Cases
from flask import render_template, redirect, url_for, flash, request
from femiber import db
from sqlalchemy import or_, and_, not_
from itertools import chain


main = Blueprint('main', __name__)

def filter_cases(filter_people_value, filter_consang_kinship_value, filter_religion_value, filter_religion_flag_value,
                filter_traits_value, filter_partnership_value, filter_motherhood_value,
                filter_physical_violence_value, filter_passing_away_value):
    query = Cases.query  # Početni upit sa svim zapisima
    filters = []  # Lista filtera koje ćemo primenjivati redom

    # Dodavanje filtera u listu, preskačemo prazne filtere
    
    if filter_people_value:
        if filter_people_value[0] == "individual":
            people_filters = Cases.cases_people.has(People.people_filter.contains("individual"))
            print(f'{people_filters=}')
            filters.append(people_filters)
        elif filter_people_value[0] == "groups":
            people_filters = Cases.cases_people.has(People.people_filter.contains("groups"))
            filters.append(people_filters)
        elif filter_people_value[0] == "name":
            people_filters = Cases.cases_people.has(not_(People.people_filter.contains("groups")) & not_(People.people_filter.contains("individual")))
            filters.append(people_filters)
        else:
            print('nije prošao individual')

    if filter_consang_kinship_value:
        consang_filters = [Cases.consang_kinship.contains(value) for value in filter_consang_kinship_value]
        filters.append(or_(*consang_filters))
    if filter_religion_value:
        religion_filters = [Cases.religion.contains(value) for value in filter_religion_value]
        filters.append(or_(*religion_filters))
    if filter_religion_flag_value:
        religion_flag_filters = [Cases.religion_flag.contains(value) for value in filter_religion_flag_value]
        filters.append(or_(*religion_flag_filters))
    if filter_traits_value:
        traits_filters = [Cases.traits.contains(value) for value in filter_traits_value]
        filters.append(or_(*traits_filters))
    if filter_partnership_value:
        partnership_filters = [Cases.partnership.contains(value) for value in filter_partnership_value]
        filters.append(or_(*partnership_filters))
    if filter_motherhood_value:
        motherhood_filters = [Cases.motherhood.contains(value) for value in filter_motherhood_value]
        filters.append(or_(*motherhood_filters))
    if filter_physical_violence_value:
        physical_violence_filters = [Cases.physical_violence.contains(value) for value in filter_physical_violence_value]
        filters.append(or_(*physical_violence_filters))
    if filter_passing_away_value:
        passing_away_filters = [Cases.passing_away.contains(value) for value in filter_passing_away_value]
        filters.append(or_(*passing_away_filters))

    # Primena filtera redom na početni upit
    query = query.filter(and_(*filters))
    unique_people_list = list(set([record.cases_people.people_filter for record in query.all()]))

    unique_kinships_list = list(set([string for record in query.all() for string in json.loads(record.consang_kinship)]))
    unique_religion_list = list(set([string for record in query.all() for string in json.loads(record.religion)]))
    unique_religion_flag_list = list(set([string for record in query.all() for string in json.loads(record.religion_flag)]))
    unique_traits_list = list(set([string for record in query.all() for string in json.loads(record.traits)]))
    unique_partnership_list = list(set([string for record in query.all() for string in json.loads(record.partnership)]))
    unique_motherhood_list = list(set([string for record in query.all() for string in json.loads(record.motherhood)]))
    unique_violence_list = list(set([string for record in query.all() for string in json.loads(record.physical_violence)]))
    unique_passing_away_list = list(set([string for record in query.all() for string in json.loads(record.passing_away)]))

    filtered_cases = query.all()
    
    return filtered_cases, unique_people_list, unique_kinships_list, unique_religion_list, unique_religion_flag_list, unique_traits_list, unique_partnership_list, unique_motherhood_list, unique_violence_list, unique_passing_away_list


@main.route("/", methods=['GET', 'POST'])
@main.route("/home", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        # get checked options
        filter_consang_kinship_value = request.form.getlist('kinship')
        filter_religion_value = request.form.getlist('religion')
        filter_religion_flag_value = request.form.getlist('religion_flag')
        filter_traits_value = request.form.getlist('trait')
        filter_partnership_value = request.form.getlist('partnership')
        filter_motherhood_value = request.form.getlist('motherhood')
        filter_physical_violence_value = request.form.getlist('violence')
        filter_passing_away_value = request.form.getlist('passing_away')
        print(f'{filter_consang_kinship_value=}')
        print(f'{filter_religion_value=}')
        print(f'{filter_religion_flag_value=}')
        print(f'{filter_traits_value=}')
        print(f'{filter_partnership_value=}')
        print(f'{filter_motherhood_value=}')

        filtered_cases, unique_people_list, unique_kinships_list, unique_religion_list, unique_religion_flag_list, unique_traits_list, unique_partnership_list, unique_motherhood_list, unique_violence_list, unique_passing_away_list = filter_cases(filter_consang_kinship_value, filter_religion_value, filter_religion_flag_value,
                                                                                                                                                                                                        filter_traits_value, filter_partnership_value, filter_motherhood_value,
                                                                                                                                                                                                        filter_physical_violence_value, filter_passing_away_value)
        # Možete iterirati kroz rezultate ili ih obraditi na drugi način
        print('-------------------------------------------------------------------------------------------------------------------------------')
        for case in filtered_cases:
            print(case.id, case.consang_kinship, case.religion, case.religion_flag,
                case.traits, case.partnership, case.motherhood, case.physical_violence, case.passing_away)
        print('-------------------------------------------------------------------------------------------------------------------------------')
        print(f'home|post > {unique_people_list=}')
        print('END OF TESTING')
        
        return render_template('home.html',
                                unique_kinships_list=unique_kinships_list,
                                unique_religion_list=unique_religion_list,
                                unique_religion_flag_list=unique_religion_flag_list,
                                unique_traits_list=unique_traits_list,
                                unique_partnership_list=unique_partnership_list,
                                unique_motherhood_list=unique_motherhood_list,
                                unique_violence_list=unique_violence_list,
                                unique_passing_away_list=unique_passing_away_list)
    else:
        people = People.query.all()
        
        #! Primer korišćenja funkcije za filtriranje - treba da se dobije iz HTML fajla selektovane vrednosti u obliku liste
        filter_people_value = []
        filter_consang_kinship_value = []  # Promenljiva vrednost filtera za consang_kinship
        filter_religion_value = []  # Promenljiva vrednost filtera za religion
        filter_religion_flag_value = []  # Promenljiva vrednost filtera za religion_flag
        filter_traits_value = []  # Promenljiva vrednost filtera za traits
        filter_partnership_value = []  # Promenljiva vrednost filtera za partnership
        filter_motherhood_value = []  # Promenljiva vrednost filtera za motherhood
        filter_physical_violence_value = []  # Promenljiva vrednost filtera za physical_violence
        filter_passing_away_value = []  # Promenljiva vrednost filtera za passing_away

        filtered_cases, unique_people_list, unique_kinships_list, unique_religion_list, unique_religion_flag_list, unique_traits_list, unique_partnership_list, unique_motherhood_list, unique_violence_list, unique_passing_away_list = filter_cases(filter_people_value, filter_consang_kinship_value, filter_religion_value, filter_religion_flag_value,
                                                                                                                                                                                                                filter_traits_value, filter_partnership_value, filter_motherhood_value,
                                                                                                                                                                                                                filter_physical_violence_value, filter_passing_away_value)

        # Možete iterirati kroz rezultate ili ih obraditi na drugi način
        print('-------------------------------------------------------------------------------------------------------------------------------')
        for case in filtered_cases:
            print(case.id, case.consang_kinship, case.religion, case.religion_flag,
                case.traits, case.partnership, case.motherhood, case.physical_violence, case.passing_away)
        print('-------------------------------------------------------------------------------------------------------------------------------')
        print(f'home|else > {unique_people_list=}')
        print('END OF TESTING')
        
        
        #! Ovo su sve moguće vrednosti filtera koje se učitavaju na početku
        # unique_kinships_list = ['mothers', 'father', 'brother(s)', 'sister(s)', 'others', 'none']
        # unique_religion_list = ['Christian', 'Jewish', 'Muslim', 'uncertain']
        # unique_religion_flag_list = ['act/attitude', 'explicit', 'implicit', 'lack', 'probably', 'saint']
        # unique_motherhood_list = ['children', 'pregnacy', 'no children', 'unclear']
        # unique_traits_list = ['intellectual', 'moral', 'physical']
        # unique_partnership_list = ['liaison', 'marriage', 'marriage arrangment', 'unclear', 'none']
        # unique_violence_list = ['assult', 'murder', 'captivity', 'mouring', 'rape']
        # unique_passing_away_list = ['death', 'funeral', 'resting place', 'translation']


        return render_template('home.html',
                                people=people,
                                unique_kinships_list=unique_kinships_list,
                                unique_religion_list=unique_religion_list,
                                unique_religion_flag_list=unique_religion_flag_list,
                                unique_traits_list=unique_traits_list,
                                unique_partnership_list=unique_partnership_list,
                                unique_motherhood_list=unique_motherhood_list,
                                unique_violence_list=unique_violence_list,
                                unique_passing_away_list=unique_passing_away_list,
                                filter_people_value=None, #! da nema preselektovanu opciju people
                                filtered_cases=filtered_cases)


@main.route('/update_fiters', methods=["POST"])
def update_filters():
    # get checked options
    filter_people_value = request.form.getlist('people')
    filter_consang_kinship_value = request.form.getlist('kinship')
    filter_religion_value = request.form.getlist('religion')
    filter_religion_flag_value = request.form.getlist('religion_flag')
    filter_traits_value = request.form.getlist('trait')
    filter_partnership_value = request.form.getlist('partnership')
    filter_motherhood_value = request.form.getlist('motherhood')
    filter_physical_violence_value = request.form.getlist('violence')
    filter_passing_away_value = request.form.getlist('passing_away')
    print(f'{filter_people_value=}')
    print(f'{filter_consang_kinship_value=}')
    print(f'{filter_religion_value=}')
    print(f'{filter_religion_flag_value=}')
    print(f'{filter_traits_value=}')
    print(f'{filter_partnership_value=}')
    print(f'{filter_motherhood_value=}')
    print(f'{filter_physical_violence_value=}')
    print(f'{filter_passing_away_value=}')
    
    filtered_cases, unique_people_list, unique_kinships_list, unique_religion_list, unique_religion_flag_list, unique_traits_list, unique_partnership_list, unique_motherhood_list, unique_violence_list, unique_passing_away_list = filter_cases(filter_people_value, filter_consang_kinship_value, filter_religion_value, filter_religion_flag_value,
                                                                                                                                                                                                filter_traits_value, filter_partnership_value, filter_motherhood_value,
                                                                                                                                                                                                filter_physical_violence_value, filter_passing_away_value)
    print('-------------------------------------------------------------------------------------------------------------------------------')
    for case in filtered_cases:
        print(case.id, case.consang_kinship, case.religion, case.religion_flag,
            case.traits, case.partnership, case.motherhood, case.physical_violence, case.passing_away)
    print('-------------------------------------------------------------------------------------------------------------------------------')
    print(f'update_filters > {unique_people_list=}')
    print('END OF TESTING')
    
    if any(filter_people_value + filter_consang_kinship_value + filter_religion_value + filter_religion_flag_value + filter_traits_value + filter_partnership_value + filter_motherhood_value + filter_physical_violence_value + filter_passing_away_value):
        criteria_options = True
    else:
        criteria_options = False
    
    return render_template('home.html',
                        filtered_cases=filtered_cases,
                        unique_kinships_list=unique_kinships_list,
                        unique_religion_list=unique_religion_list,
                        unique_religion_flag_list=unique_religion_flag_list,
                        unique_traits_list=unique_traits_list,
                        unique_partnership_list=unique_partnership_list,
                        unique_motherhood_list=unique_motherhood_list,
                        unique_violence_list=unique_violence_list,
                        unique_passing_away_list=unique_passing_away_list,
                        
                        filter_people_value=filter_people_value,
                        filter_consang_kinship_value=filter_consang_kinship_value,
                        filter_religion_value=filter_religion_value,
                        filter_religion_flag_value=filter_religion_flag_value,
                        filter_traits_value=filter_traits_value,
                        filter_partnership_value=filter_partnership_value,
                        filter_motherhood_value=filter_motherhood_value,
                        filter_physical_violence_value=filter_physical_violence_value,
                        filter_passing_away_value=filter_passing_away_value,
                        
                        criteria_options=criteria_options
                        )


@main.route('/contact')
def contact():
    return render_template('contact.html')


@main.route('/database_codebook')
def database_codebook():
    return render_template('database_codebook.html')