from models.measurement import Measurement
from src.base_resource import BaseResource
from src.utils import schema_to_swagger
from src.measurement.schema import MeasurementSchema
from flask_restx import Namespace, reqparse

ns = Namespace('measurements', description='Measurement operations')
measurement = ns.model('Measurement', schema_to_swagger(MeasurementSchema))


@ns.route('/')
class MeasurementResource(BaseResource):
    model = Measurement
    schema = MeasurementSchema()
    parser = reqparse.RequestParser()

    @ns.doc('list_measurements')
    @ns.marshal_list_with(measurement)
    @ns.expect(parser)
    def get(self):
        query = self.resource_with_query_params()
        return self.schema.dump(obj=query, many=True)
