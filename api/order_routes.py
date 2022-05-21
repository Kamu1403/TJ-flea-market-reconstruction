#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue


@api_blue.route("/change_order_status", methods=["PUT"])
def generate_order():
    data = request.get_json()
    print(data['order_id'])
    print(data['state'])

    return make_response_json(404, "NOT FOUND")
