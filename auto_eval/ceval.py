#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import os
from utils import build_ceval_data, env_setting, get_registry_path
env_setting()

registry_path = get_registry_path()

# 数据路径
data_path = r'../assets/ceval_data'
# 构建数据
subjects = build_ceval_data(data_path,registry_path,few_shot=5)


model = "langchain/chat_model/chatglm2-6b-int4"
data_type = "ceval"

# 评估主题
for subject in subjects:
    run_string = 'exec_aigc_evals {} match_{}_{} --registry_path={}'.format(
        model,
        data_type,
        subject,
        registry_path
    )
    #启动评估脚本
    os.system(run_string)
    # # How to process the log events generated by oaieval
    # events = "/tmp/evallogs/{log_name}"
    #
    # with open(events, "r") as f:
    #     events_df = pd.read_json(f, lines=True)
    #
    # matches_df = events_df[events_df.type == "match"].reset_index(drop=True)
    # matches_df = matches_df.join(pd.json_normalize(matches_df.data))
    # matches_df.correct.value_counts().plot.bar(title="Correctness of generated answers", xlabel="Correctness", ylabel="Count")
    #
    #
    # # In[ ]:
    #
    #
    # # Inspect samples
    # for i, r in pd.json_normalize(events_df[events_df.type == "sampling"].data).iterrows():
    #     print(f"Prompt: {r.prompt}")
    #     print(f"Sampled: {r.sampled}")
    #     print("-" * 25)

