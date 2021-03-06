from flask import Flask, render_template, request
from queries import query_get_last_date_of_lost_objects, query_get_all_nature, query_get_lost_object_with_conditions, \
    query_get_lat_long_name_train_station, query_get_all_lost_object_with_conditions
from get_data_to_rdf import get_data_to_rdf_object

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home_app():
    input_path_owl_file = '../data/train_station_context.owl'
    path_owl_file = '../data/output_context.owl'
    get_data_to_rdf_object(input_path_owl_file, path_owl_file)
    last = query_get_last_date_of_lost_objects(path_owl_file)
    last_object = last[0]
    last_date = last[1]
    last_place = last[2]

    markers = query_get_lat_long_name_train_station(path_owl_file)

    return render_template('home.html',
                           l_nature_windows=query_get_all_nature(path_owl_file),
                           last_date=last_date[:10],
                           last_hour=((last_date.split('T')[1])[:8]),
                           last_place=last_place,
                           last_object=last_object,
                           markers=markers
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

        if nature_obj == 'All' and zipcode != '':
            query_final = query_get_all_lost_object_with_conditions(path_owl_file, zipcode, hasRecoveredDate)
        elif nature_obj != 'All' and zipcode != '':
            query_final = query_get_lost_object_with_conditions(path_owl_file, nature_obj, zipcode, hasRecoveredDate)
        elif nature_obj == 'All' and zipcode == '':
            query_final = query_get_all_lost_object_with_conditions(path_owl_file, 'zipcode', hasRecoveredDate)
        else:
            query_final = query_get_lost_object_with_conditions(path_owl_file, nature_obj, 'zipcode', hasRecoveredDate)
        verif_df = len(query_final)
        return render_template('result.html', df_result=[query_final.to_html(classes='d')], len_df=verif_df)


if __name__ == '__main__':
    app.run()
