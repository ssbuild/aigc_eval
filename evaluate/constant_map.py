# -*- coding: utf-8 -*-
# @Time:  18:46
# @Author: tk
# @File：constant_map


train_info_args = {
    "baichuan-7B":{
        'model_type': 'baichuan',
        'model_name_or_path': '/data/nlp/pre_models/torch/baichuan/baichuan-7B',
        'config_name': '/data/nlp/pre_models/torch/baichuan/baichuan-7B/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/baichuan/baichuan-7B',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },

    "Baichuan-13B-Chat":
    {
        'model_type': 'baichuan',
        'model_name_or_path': '/data/nlp/pre_models/torch/baichuan/Baichuan-13B-Chat',
        'config_name': '/data/nlp/pre_models/torch/baichuan/Baichuan-13B-Chat/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/baichuan/Baichuan-13B-Chat',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    "chatglm-6b":{
        'model_type': 'chatglm',
        'model_name_or_path': '/data/nlp/pre_models/torch/chatglm/chatglm-6b',
        'config_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    "chatglm-6b-int4":{
        'model_type': 'chatglm',
        'model_name_or_path': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4',
        'config_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    "chatglm-6b-int8":{
        'model_type': 'chatglm',
        'model_name_or_path': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int8',
        'config_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int8/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int8',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    "chatglm2-6b-int4" : {
        'model_type': 'chatglm2',
        'model_name_or_path': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b-int4',
        'config_name': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b-int4/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b-int4',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    "chatglm2-6b": {
        'model_type': 'chatglm2',
        'model_name_or_path': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b',
        'config_name': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/chatglm2/chatglm2-6b',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    'bloom-560m': {
        'model_type': 'bloom',
        'model_name_or_path': '/data/nlp/pre_models/torch/bloom/bloom-560m',
        'config_name': '/data/nlp/pre_models/torch/bloom/bloom-560m/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/bloom/bloom-560m',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    'bloom-1b7': {
        'model_type': 'bloom',
        'model_name_or_path': '/data/nlp/pre_models/torch/bloom/bloom-1b7',
        'config_name': '/data/nlp/pre_models/torch/bloom/bloom-1b7/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/bloom/bloom-1b7',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },
    'opt-350m': {
        'model_type': 'opt',
        'model_name_or_path': '/data/nlp/pre_models/torch/opt/opt-350m',
        'config_name': '/data/nlp/pre_models/torch/opt/opt-350m/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/opt/opt-350m',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },

    'llama-7b-hf': {
        'model_type': 'llama',
        'model_name_or_path': '/data/nlp/pre_models/torch/llama/llama-7b-hf',
        'config_name': '/data/nlp/pre_models/torch/llama/llama-7b-hf/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/llama/llama-7b-hf',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },

    'moss-moon-003-sft-int4':{
        'model_type': 'moss',
        'model_name_or_path': '/data/nlp/pre_models/torch/moss/moss-moon-003-sft-int4',
        'config_name': '/data/nlp/pre_models/torch/moss/moss-moon-003-sft-int4/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/moss/moss-moon-003-sft-int4',
        'use_fast_tokenizer': False,
        'do_lower_case': None,
    },

    # 中英日语
    "rwkv-4-raven-3b-v12-Eng49%-Chn49%-Jpn1%-Other1%": {
        'model_type': 'rwkv',
        'model_name_or_path': '/data/nlp/pre_models/torch/rwkv_gf/rwkv-4-raven-3b-v12',
        'config_name': '/data/nlp/pre_models/torch/rwkv_gf/rwkv-4-raven-3b-v12/config.json',
        'tokenizer_name': '/data/nlp/pre_models/torch/rwkv_gf/rwkv-4-raven-3b-v12',
        'use_fast_tokenizer': True,
        'do_lower_case': None,
    },

}