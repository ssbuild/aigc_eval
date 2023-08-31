#!/usr/bin/env python
# coding: utf-8

# get_ipython().system('curl -O https://people.eecs.berkeley.edu/~hendrycks/data.tar')
# get_ipython().system('tar -xf data.tar')
# data_path = "data"
import os
import sys
sys.path.append(os.path.dirname(__file__))
import pandas as pd
from utils import build_mmlu_data, env_setting, get_registry_path, get_output_path

env_setting()

registry_path = get_registry_path()
output_path = get_output_path()
data_path = r'F:\nlpdata_2023\openai\evals\data'

data_type = "mmlu"
# 构建数据
subjects = build_mmlu_data(data_path,registry_path,data_type = data_type,few_shot=5)
model = "langchain/chat_model/chatglm2-6b-int4"



# 评估主题
for subject in subjects:
    log_path = os.path.join(output_path,data_type)
    os.makedirs(log_path,exist_ok=True)
    log_file = os.path.join(log_path, subject + '.log')
    record_path = os.path.join(log_path, subject + '.event')
    run_string = 'exec_aigc_evals {} match_{}_{} --debug=1 --registry_path={} --log_to_file={} --record_path={}'.format(
        model,
        data_type,
        subject,
        registry_path,
        log_file,
        record_path
    )
    #启动评估脚本
    ret = os.system(run_string)
    if ret != 0:
        break
    # # How to process the log events generated by oaieval

    # with open(record_path, "r") as f:
    #     events_df = pd.read_json(f, lines=True)
    #
    # # matches_df = events_df[events_df.type == "match"].reset_index(drop=True)
    # # matches_df = matches_df.join(pd.json_normalize(matches_df.data))
    # # matches_df.correct.value_counts().plot.bar(title="Correctness of generated answers", xlabel="Correctness", ylabel="Count")
    #
    #
    # for i, r in pd.json_normalize(events_df[events_df.type == "sampling"].data).iterrows():
    #     print(f"expected: {r.expected}")
    #     print(f"Sampled: {r.sampled}")
    #     print("-" * 25)

