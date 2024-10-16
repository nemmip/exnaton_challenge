from flask_restx import Namespace, reqparse
from sqlalchemy import text

from backend.models import table_obj, Measurement
from backend.src.analytics.schema import AnalyticsSchema
from backend.src.base_resource import BaseResource
from backend.src.utils import schema_to_swagger

ns = Namespace('analytics', description='Analytics operations')
analytics = ns.model('Analytics', schema_to_swagger(AnalyticsSchema))
parser = reqparse.RequestParser()
parser.add_argument('field_name', type=str, help='Enter existing field name')
parser.add_argument('operation', type=str, help='Supported operations: avg')
parser.add_argument('tags_id', type=str, help='Enter proper tags id')
parser.add_argument('date', type=str, help='Enter date (optional)')


class AnalyticsResource(BaseResource):
    schema = AnalyticsSchema()


@ns.route('/measurement')
@ns.expect(parser)
class MeasurementAnalyticsResource(AnalyticsResource):
    model = Measurement
    def get(self):
        args = parser.parse_args()
        sql_text_query = f"""
                        SELECT {args['operation']}({args['field_name']})
                        FROM {self.model.__tablename__}"""
        if len(args['tags_id']):
            sql_text_query += f" WHERE tags_id = {args['tags_id']}"
            if args.get('date', None):
                sql_text_query += f" AND timestamp::date = date '{args['date']}'"

        sql_execution = self.session.execute(text(sql_text_query))
        data = [self.schema.dump({
            "operation": args['operation'],
            "field_name": args['field_name'],
            "class_name": self.model.__tablename__,
            "operation_value": el[0]
        }) for el in sql_execution]
        return data
