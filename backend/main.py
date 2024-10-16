from flask import Flask
from flask_cors import CORS
from flask_restx import Api
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.measurement.resource import ns as MeasurementNamespace
from src.tags.resource import ns as TagsNamespace
from src.analytics.resource import ns as AnalyticsResource

app = Flask(__name__)
CORS(app)
api = Api(app, version='1.0', title='Measurements API',
    description='A simple Measurements API. \n To fully use each endpoint use query parameters. Each endpoint can'
                ' be filtered by columns described in models plus optional operator: eq, ne, lt, le, gt, ge.\n'
                'For example: /measurements?energy=eq:0.2 .\n You can also query the minimal and maximal value of each column'
                ' just use column name as argument value. \nFor example: /measurements?max=energy',
)
api.add_namespace(MeasurementNamespace)
api.add_namespace(TagsNamespace)
api.add_namespace(AnalyticsResource)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)