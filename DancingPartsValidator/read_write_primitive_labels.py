import json
from validator.utils import dictionary_ops as do

dict_file = "validator/primitives/primitive_labels.json"

dic = {
    1:"box",
    2:"cylinder",
    3:"ellipsoid"
}

do.save_dict(dict_file, dic)

dic = do.load_dict(dict_file)
print dic


