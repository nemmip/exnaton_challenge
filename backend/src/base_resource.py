from flask_restx import Resource
from sqlalchemy import text
from werkzeug.exceptions import BadRequest

from models.session import get_session
from flask import request
import re
import operator


class BaseResource(Resource):
    model = None
    schema = None
    __additional_query_args = ["min", "max"]
    __operators = {
        'eq': operator.eq,
        'ne': operator.ne,
        'lt': operator.lt,
        'le': operator.le,
        'gt': operator.gt,
        'ge': operator.ge,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.session = get_session()
        self.__model_columns = self.model.__table__.columns.keys() if self.model else []

    def resource_with_query_params(self):
        args = request.args.keys()
        query = None
        if len(args):
            self.check_query_params([*args])
            column_matches, additional_args_matches = self._get_matches(args)
            if column_matches:
                filter_args = [self._get_filter_args(col) for col in column_matches]
                query = self.session.query(self.model).filter(*filter_args)
            elif additional_args_matches:
                # always return one record
                sql_execution = self.session.execute(text(f"""
                SELECT {additional_args_matches[0]}({request.args.get(additional_args_matches[0])})
                FROM {self.model.__tablename__}"""))
                for el in sql_execution:
                    filter_args = getattr(self.model, request.args.get(additional_args_matches[0])) == el[0]
                    query = self.session.query(self.model).filter(filter_args)
        else:
            query = self.session.query(self.model)
        return query.all()

    def check_query_params(self, args: list):
        for arg in args:
            if not (arg in self.__additional_query_args or arg in self.__model_columns):
                raise BadRequest("Invalid query parameter")
            if arg in self.__additional_query_args and request.args.get(arg) not in self.__model_columns:
                raise BadRequest(f"{arg} should point to the {self.model.__name__} columns")
        args_str = ','.join(args)
        re_additional_args = self._create_list_regex(self.__additional_query_args)
        count_matches = len(re.findall(re_additional_args, args_str))
        if count_matches > 1:
            raise BadRequest(f"You can only use once per query {','.join(self.__additional_query_args)}")

    def _create_list_regex(self, items: list):
        return '|'.join(re.escape(item) for item in items)

    def _get_matches(self, args):
        re_additional_args = self._create_list_regex(self.__additional_query_args)
        re_column_args = self._create_list_regex(self.__model_columns)
        re_pattern = f"({re_column_args})|({re_additional_args})"
        matches = re.findall(re_pattern, ' '.join(args))

        column_matches = [match[0] for match in matches if match[0]]
        additional_args_matches = [match[1] for match in matches if match[1]]
        return column_matches, additional_args_matches

    def _get_filter_args(self, col):
        argument = request.args.get(col).split(':', maxsplit=1)
        if argument[0] not in self.__operators.keys():
            return getattr(self.model, col) == argument[0]

        return self.__operators[argument[0]](getattr(self.model, col), argument[1])
