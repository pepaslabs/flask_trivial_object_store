#!/usr/bin/env python

# object_store.py: a trivial, unauthenticated object store, written in Python/Flask.
# copyright jason pepas, released under the MIT license.
# see https://github.com/pepaslabs/flask_trivial_object_store

import hashlib
import re
import os

import flask
app = flask.Flask(__name__)

valid_hex_regex = '[0-9a-f]'
valid_md5_regex = '%s{32}' % valid_hex_regex
valid_md5_pattern = re.compile('^%s$' % valid_md5_regex)

#app.config['DATADIR'] = '/var/www/object_store/objects/'
app.config['DATADIR'] = '/tmp/'

@app.route("/objects", methods=['POST'])
def POST_object():
	object = flask.request.files.values()[0]
	if not object:
		flask.abort(400)
	data = object.stream.read()
	hash_id = md5(data)
	path = os.path.join(app.config['DATADIR'], hash_id)
	with open(path, 'w') as fp:
		fp.write(data)
	response = flask.make_response()
	response.headers['Location'] = '/objects/%s' % hash_id
	return response

@app.route("/objects/<hash_id>")
def GET_object(hash_id, methods=['GET']):
    if hash_id_is_sane(hash_id) == False:
    	flask.abort(400)
    return flask.send_from_directory(app.config['DATADIR'], hash_id, mimetype='application/octet-stream')

def md5(data):
    return hashlib.md5(data).hexdigest()

def hash_id_is_sane(hash_id):
    if valid_md5_pattern.match(hash_id) is None:
    	return False

if __name__ == "__main__":
    app.run(debug=True)
