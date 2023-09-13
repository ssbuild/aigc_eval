# -*- coding: utf-8 -*-
# @Time:  19:04
# @Author: tk
# @File：struct_match
import json
from typing import Any, List, Union, Tuple, Callable, Optional, Dict

import aigc_evals
import aigc_evals.metrics
from aigc_evals.api import CompletionFn
from aigc_evals.prompt.base import is_chat_prompt
from aigc_evals.record import record_match


class Element(object):
    def __init__(self,value: str):
        self.key,self.value  = value.split('_',1)

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

class StructMatch(aigc_evals.Eval):
    def __init__(
        self,
        completion_fns: List[CompletionFn],
        samples_jsonl: str,
        *args,
        max_tokens: int = 500,
        **kwargs,
    ):
        super().__init__(completion_fns, *args, **kwargs)
        assert len(completion_fns) == 1, "Match only supports one completion fn"
        self.max_tokens = max_tokens
        self.samples_jsonl = samples_jsonl

    def _evaluate(self,
                  sample: Dict,
                  expect: Dict,
                  ):
        """评测函数
        """
        R,T = [],[]
        for k,v in sample.items():
            RESULT = R
            if isinstance(v, dict):
                RESULT.extend([k + _ for _ in list(v.values()) if _])
            elif isinstance(v, list):
                for _ in v:
                    if not isinstance(_,dict):
                        continue
                    RESULT.extend([k + '_' +  value for value in list(_.values()) if value])
            else:
                if v:
                    RESULT.append(v)

        for k, v in expect.items():
            RESULT = T
            if isinstance(v, dict):
                RESULT.extend([k + _ for _ in list(v.values()) if _])
            elif isinstance(v, list):
                for _ in v:
                    if not isinstance(_, dict):
                        continue
                    RESULT.extend([k + '_' + value for value in list(_.values()) if value])
            else:
                if v:
                    RESULT.append(v)

        R = set([Element(i) for i in R])
        T = set([Element(i) for i in T])
        tp = len(R & T)
        fp = len(R) - tp
        fn = len(T) - tp

        return tp, fp, fn

    def eval_sample(self, sample: Any, *_):
        assert isinstance(sample, dict), "sample must be a dict"
        assert "input" in sample, "sample must have an 'input' key"
        assert "ideal" in sample, "sample must have an 'ideal' key"
        assert isinstance(sample["ideal"], dict) or isinstance(
            sample["ideal"], dict
        ), "sample['ideal'] must be dict"

        prompt = sample["input"]


        result = self.completion_fn(
            prompt=prompt,
        )
        sampled = result.get_completions()[0]

        try:
            jd = json.loads(sampled.strip())

        except:
            jd = {}
            pass

        tp, fp, fn = self._evaluate(sample=jd, expect=sample["ideal"])

        result = {
            "index" : sample.get("id",None),
            # "prompt": prompt,
            "sampled": sampled,
            "tp": tp,
            "fp": fp,
            "fn": fn,
        }
        result["expected"] = json.dumps(sample["ideal"],ensure_ascii=False)
        aigc_evals.record.record_sampling(prompt, sampled, index=sample.get("id",None))
        aigc_evals.record.record_metrics(**result)

    def run(self, recorder):
        samples = self.get_samples()
        self.eval_all_samples(recorder, samples)
        events = recorder.get_events("metrics")
        tp = sum(int(event.data["tp"]) for event in events)
        fp = sum(int(event.data["fp"]) for event in events)
        fn = sum(int(event.data["fn"]) for event in events)
        precision,recall = tp / (tp + fp + 1e-10),tp / (tp + fn + 1e-10)
        f1 = 2*(precision*recall)/(precision+recall +1e-10)
        return {
            "precision": precision,
            "recall": recall,
            "f1": f1,
        }
