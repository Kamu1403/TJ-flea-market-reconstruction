#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
from api.utils import *
from api import api_blue
from item.models import Item_type, Item_state

@api_blue.route("/generate_order",methods=["PUT"])
def generate_order():
    return make_response_json(404,"NOT FOUND")