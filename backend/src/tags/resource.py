from flask_restx import Namespace, reqparse

from backend.models.measurement import Tags
from backend.src.base_resource import BaseResource
from backend.src.tags.schema import TagsSchema
from backend.src.utils import schema_to_swagger

ns = Namespace('tags', description='Tags operations')
tags = ns.model('Tag', schema_to_swagger(TagsSchema))


@ns.route('/')
class TagsResource(BaseResource):
    schema = TagsSchema()
    model = Tags
    parser = reqparse.RequestParser()


    @ns.doc('list_tags')
    @ns.marshal_list_with(tags)
    def get(self):
        query = self.resource_with_query_params()
        return self.schema.dump(obj=query, many=True)