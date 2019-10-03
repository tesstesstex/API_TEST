from flask import Flask, jsonify, request
import bleach

app = Flask(__name__)

TOKEN = 'YOUR_TOKEN'


@app.route('/api/item', methods=['GET'])
def get_item():
    item = {"item_name": 'hogehoge'}

    return jsonify(item)


@app.route('/api/v1/user', methods=['POST'])
def add_user():
    # check token
    header = request.headers.get('Authorization', None)
    _, token = header.split()
    if token != TOKEN:
        return jsonify({'Forbidden': 'Access is denied'}), 403

    # method check
    if request.method != 'POST':
        return jsonify({'Method Not Allowed': 'Method is invalid.'}), 405

    # create new user
    new_user = {}
    for key in request.form.keys():
        new_user[key] = bleach.clean(request.form.get(key))

    # save uploaded file into data folder
    for file in request.files:
        if file is None:
            break
        upload_file = request.files.get(file)
        upload_path = 'data/%s' % upload_file.filename
        upload_file.save(upload_path)
        new_user[file] = upload_file.filename

    return jsonify(new_user)


if __name__ == '__main__':
    app.run(debug=True)
