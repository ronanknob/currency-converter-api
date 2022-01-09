input_schema = {
    "type" : "object",
    "properties" : {
        "origin_currency" : {"type" : "string", "minLength": 3, "maxLength": 3},
        "destination_currency" : {"type" : "string", "minLength": 3, "maxLength": 3},
        "value" : {"type" : "number"},
    },
    "required": ["origin_currency", "destination_currency", "value"]
}