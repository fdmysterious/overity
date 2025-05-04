"""
LSTM Init
=========

**Created**: 2025-03-15

- Author 1 (author1@mail.com)
- Author 2 (author2@mail.com): Role

Blahblahbalh
"""

#from keras.models import load_model

import logging

import verity.api as vapi

vapi.init()

log = logging.getLogger("My Method")


#with vapi.describe_arguments() as vargs:
#    vargs.add_argument("input_model", help="Test input model")
#    vargs.add_flag("optional", help="Test flag")
#
#
#input_model = vapi.argument("input_model")

model_file, model_info = vapi.model_use("sru_binary_model_pruned_15_97-v0_1")

log.info(f"Use model: {model_info.name}!")
log.info(f"Model format: {model_info.exchange_format}")

log.info(f"-> Model extracted to: {model_file}")

# Try save model back
with vapi.model_package("test_output_model", model_info.exchange_format, model_info.target) as vpkg:
    vpkg.model_file_path.write_bytes(model_file.read_bytes())

# Done :)
