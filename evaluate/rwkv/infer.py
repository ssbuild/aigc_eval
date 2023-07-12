# -*- coding: utf-8 -*-
# @Time:  20:45
# @Author: tk
# @File：evaluate
import torch
from deep_training.data_helper import ModelArguments, DataArguments, DataHelper
from transformers import HfArgumentParser
from aigc_zoo.model_zoo.rwkv4.llm_model import MyTransformer, RwkvConfig, set_model_profile
from aigc_zoo.utils.llm_generate import Generate
from evaluate.constant_map import train_info_args
class NN_DataHelper(DataHelper):pass



class Engine_API:
    def init(self,model_name):
        parser = HfArgumentParser((ModelArguments,))
        (model_args,) = parser.parse_dict(train_info_args[model_name], allow_extra_keys=True)

        # 可以自行修改 RWKV_T_MAX  推理最大长度
        set_model_profile(RWKV_T_MAX=2048, RWKV_FLOAT_MODE='16')

        dataHelper = NN_DataHelper(model_args)
        tokenizer, config, _, _ = dataHelper.load_tokenizer_and_config(config_kwargs={"torch_dtype": torch.float16},
                                                                       config_class_name=RwkvConfig)

        pl_model = MyTransformer(config=config, model_args=model_args, torch_dtype=torch.float16)
        model = pl_model.get_llm_model()

        model.requires_grad_(False)
        model.eval().half().cuda()

        self.model = model
        self.tokenizer = tokenizer

    def infer(self,input,**kwargs):
        default_kwargs = dict(
            max_length=2018,
            eos_token_id=self.model.config.eos_token_id,
            pad_token_id=self.model.config.eos_token_id,
            do_sample=False, top_p=0.7, temperature=0.95,
        )
        default_kwargs.update(kwargs)
        response = Generate.generate(self.model,
                                     tokenizer=self.tokenizer,
                                     query=input,**default_kwargs)
        return response


if __name__ == '__main__':
    api_client = Engine_API()
    api_client.init("rwkv-4-raven-3b-v12-Eng49%-Chn49%-Jpn1%-Other1%")
    text_list = [
        "你是谁?",
        "你会干什么?",
    ]
    for input in text_list:
        response = api_client.infer(input)
        print('input', input)
        print('output', response)