import pandas as pd
from flask import Flask, render_template, request
from queries import *
from get_data_to_rdf import get_data_to_rdf_object, get_data_to_rdf_train_station


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_app():
    input_path_owl_file = 'C:/Users/tinou/PycharmProjects/web_datamining_and_semantics/data/train_station_context.owl'
    path_owl_file = 'C:/Users/tinou/PycharmProjects/web_datamining_and_semantics/data/output_context.owl'
    get_data_to_rdf_object(input_path_owl_file, path_owl_file)
    last = query_get_last_date_of_lost_objects(path_owl_file)
    last_date = last[0]
    last_place = last[1]

    return render_template('home.html',
                           l_nature_windows=query_get_all_nature(path_owl_file),
                           last_date=last_date[:10],
                           last_hour=((last_date.split('T')[1])[:8]),
                           last_place=last_place
           )


@app.route('/result/', methods=['GET', 'POST'])
def result_page():
    path_owl_file = './data/output_context.owl'
    hasRecoveredDate = ''
    if request.method == 'POST':
        nature_obj = request.form.get('nature_selected')
        print(f'nature: {nature_obj}')
        zipcode = str(request.form.get('zipcode_selected'))
        print(f'zipcode: {zipcode}')
        b_recovered_date = request.form.get('rdate_selected')
        print(f'recovered_date: {b_recovered_date}')

        if nature_obj != '' and zipcode != '':
            query_final = query_get_lost_object_with_conditions(path_owl_file, nature_obj, zipcode, hasRecoveredDate)
            print('only nature')
        elif nature_obj == '' and zipcode != '':
            query_final = query_get_lost_object_with_conditions(path_owl_file, 'nature', zipcode, hasRecoveredDate)
            print('only nature')
        elif nature_obj != '' and zipcode == '':
            query_final = query_get_lost_object_with_conditions(path_owl_file, nature_obj, 'zipcode', hasRecoveredDate)
            print('only zipcode')
        else:
            query_final = query_get_lost_object_with_conditions(path_owl_file, 'nature', 'zipcode', hasRecoveredDate)
            print('both')
        verif_df = len(query_final)
        return render_template('result.html', df_result=[query_final.to_html(classes='d')], len_df=verif_df)


if __name__ == '__main__':
    app.run()
