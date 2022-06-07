from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api()

#create my data base
motors = {
    1: {"name": "Suzuki", "model": "DL650"},
    2: {"name": "BMW", "model": "R1200"}
}

parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("model", type=str)

class MAIN(Resource):
    def get(self, motors_id):  #return JSON file
        if motors_id == 0:
            return motors
        else:
            return motors[motors_id]

    def delete(self, motors_id):
        del motors[motors_id]
        return motors

    def post(self, motors_id):
        motors[motors_id] = parser.parse_args()
        return motors

    def put(self, motors_id):
        motors[motors_id] = parser.parse_args()
        return motors


api.add_resource(MAIN, '/api/motors/<int:motors_id>') #tracking URL
api.init_app(app)

if __name__ == "__main__":
    app.run(debug=True, port=3032, host='127.0.0.1')