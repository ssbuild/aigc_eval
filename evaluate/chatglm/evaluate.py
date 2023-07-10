# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/7/10 16:42

import torch
from deep_training.data_helper import ModelArguments,DataHelper
from transformers import HfArgumentParser
from aigc_zoo.model_zoo.chatglm.llm_model import MyTransformer, ChatGLMTokenizer, LoraArguments, setup_model_profile, \
    ChatGLMConfig
class NN_DataHelper(DataHelper):pass

train_info_args = {
    'data_backend': 'parquet',
    # 预训练模型路径
    'model_type': 'chatglm',
    'model_name_or_path': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4',
    'config_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4/config.json',
    'tokenizer_name': '/data/nlp/pre_models/torch/chatglm/chatglm-6b-int4',
    'use_fast_tokenizer': False,
    'do_lower_case': None,
}


class Engine_API:
    def init(self):
        train_info_args['seed'] = None
        parser = HfArgumentParser((ModelArguments,))
        (model_args,) = parser.parse_dict(train_info_args, allow_extra_keys=True)

        setup_model_profile()

        dataHelper = NN_DataHelper(model_args)
        tokenizer: ChatGLMTokenizer
        tokenizer, config, _, _ = dataHelper.load_tokenizer_and_config(tokenizer_class_name=ChatGLMTokenizer,
                                                                       config_class_name=ChatGLMConfig)
        assert tokenizer.eos_token_id == 130005
        config.initializer_weight = False

        pl_model = MyTransformer(config=config, model_args=model_args, torch_dtype=torch.float16, )

        model = pl_model.get_llm_model()
        if not model.quantized:
            # 按需修改，目前只支持 4/8 bit 量化 ， 可以保存量化模型
            model.half().quantize(4).cuda()
        else:
            # 已经量化
            model.half().cuda()
        model = model.eval()

        self.model = model
        self.tokenizer = tokenizer

    def infer(self,input,**kwargs):
        default_kwargs = dict(
            history=[], max_length=2048,
            eos_token_id=self.model.config.eos_token_id,
            do_sample=True, top_p=0.7, temperature=0.95,
        )
        kwargs.update(default_kwargs)
        response, history = self.model.chat(self.tokenizer, query=input,  **kwargs)
        return response

if __name__ == '__main__':
    api_client = Engine_API()
    api_client.init()
    text_list = [
        "写一个诗歌，关于冬天",
        "晚上睡不着应该怎么办",
    ]
    for input in text_list:
        response = api_client.infer(input)
        print("input", input)
        print("response", response)


