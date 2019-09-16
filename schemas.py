# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema
)

from gl_const import *


class NodeSchema(Schema):
    i = fields.Integer(required=True)
    j = fields.Integer(required=True)
    t = fields.Integer()


class SearchSchema(Schema):
    start = fields.Nested(
        NodeSchema,
        required=True
    )

    goal = fields.Nested(
        NodeSchema,
        required=True
    )


class MapSchema(Schema):
    cellsize = fields.Float(
        missing=1.0,
        validate=validate.Range(min=0.01)
    )

    width = fields.Integer(required=True)

    @validates_schema
    def validate_width(self, data, **kwargs):
        for i in range(len(data['grid'])):
            if data['width'] != len(data['grid'][i]):
                raise ValidationError('Invalid width!')

    height = fields.Integer(required=True)

    @validates_schema
    def validate_height(self, data, **kwargs):
        if data['height'] != len(data['grid']):
            raise ValidationError('Invalid height!')

    grid = fields.List(
        fields.List(
            fields.String(
                validate=validate.OneOf(['.', '*'])
            ),
            required=True,
            validate=validate.Length(min=1)
        ),
        required=True,
        validate=validate.Length(min=1),
    )

    searches = fields.List(
        fields.Nested(
            SearchSchema
        )
    )

    @validates_schema
    def validate_searches(self, data, **kwargs):
        for search in data['searches']:
            if not -1 < search['start']['i'] < data['height'] or not -1 < search['start']['j'] < data['width']:
                raise ValidationError('Invalid start!')
            if data['grid'][search['start']['i']][search['start']['j']] == '*':
                raise ValidationError('Start is an obstacle!')
            if not -1 < search['goal']['i'] < data['height'] or not -1 < search['goal']['j'] < data['width']:
                raise ValidationError('Invalid goal!')
            if data['grid'][search['goal']['i']][search['goal']['j']] == '*':
                raise ValidationError('Goal is an obstacle!')


class OptionsSchema(Schema):
    searchtype = fields.String(
        required=True,
        validate=validate.OneOf(['astar', 'sipp'])
    )

    metrictype = fields.String(
        required=True,
        validate=validate.OneOf([EUCL, DIAG, MANH, CHEB])
    )

    breakingties = fields.String(
        missing='g-min',
        validate=validate.OneOf([G_MIN, G_MAX])
    )

    hweight = fields.Float(
        missing=1.0,
        validate=validate.Range(min=0.01)
    )

    allowdiagonal = fields.Boolean(missing=False)


class InputSchema(Schema):
    map = fields.Nested(
        MapSchema,
        required=True
    )

    options = fields.Nested(
        OptionsSchema,
        required=True
    )


input_schema = InputSchema()


class SearchResultSchema(Schema):
    pathfound = fields.Boolean(required=True)

    numberofsteps = fields.Integer(required=True)

    pathtime = fields.Integer(required=True)

    pathlength = fields.Integer(required=True)

    pathlength_scaled = fields.Integer(required=True)

    lppath = fields.List(
        fields.Nested(
            NodeSchema
        ),
        required=True
    )

    hppath = fields.List(
        fields.Nested(
            NodeSchema
        ),
        required=True
    )

    time = fields.Float(required=True)


class OutputSchema(Schema):
    search_results = fields.List(
        fields.Nested(
            SearchResultSchema,
        ),
        required=True
    )


output_schema = OutputSchema()
