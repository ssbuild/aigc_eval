# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/9/7 16:34
import json
from typing import Any, List

from aigc_evals.record import record_event, record_metrics, record_sampling
from sacrebleu.metrics.bleu import BLEU
import aigc_evals
import aigc_evals.metrics
from aigc_evals.api import CompletionFn
from aigc_evals.prompt.base import is_chat_prompt
from rouge import Rouge

class RougeMatch(aigc_evals.Eval):
    def __init__(
        self,
        completion_fns: List[CompletionFn],
        samples_jsonl: str,
        *args,
        max_tokens: int = 500,
        num_few_shot: int = 0,
        few_shot_jsonl: str = None,
        threshold=30,
        **kwargs,
    ):
        super().__init__(completion_fns, *args, **kwargs)
        assert len(completion_fns) == 1, "Translate only supports one completion fn"
        self.max_tokens = max_tokens
        self.samples_jsonl = samples_jsonl
        self.threshold = threshold
        self.num_few_shot = num_few_shot
        if self.num_few_shot > 0:
            assert few_shot_jsonl is not None, "few shot requires few shot sample dataset"
            self.few_shot_jsonl = few_shot_jsonl
            self.few_shot = aigc_evals.get_jsonl(self.few_shot_jsonl)

        self.rouge = Rouge()

    def eval_sample(self, sample: Any, *_):
        prompt = sample["input"]
        expected = sample["ideal"]
        if self.num_few_shot > 0:
            assert is_chat_prompt(sample["input"]), "few shot requires chat prompt"
            prompt = sample["input"][:-1]
            for s in self.few_shot[: self.num_few_shot]:
                prompt += s["sample"]
            prompt += sample["input"][-1:]

        if isinstance(expected, tuple):
            expected = list(expected)
        elif not isinstance(expected, list):
            expected = [expected]

        result = self.completion_fn(
            prompt=prompt,
            max_tokens=self.max_tokens,
        )
        sampled = result.get_completions()[0]


        rouge = self.rouge.get_scores([sampled], [expected[0]])[0]


        record_metrics(rouge=json.dumps(rouge,ensure_ascii=True), index=sample.get("id",None))

        record_sampling(
            prompt=prompt, sampled=sampled,expected=expected[0], index=sample.get("id",None)
        )




    def run(self, recorder):
        samples = self.get_samples()
        self.eval_all_samples(recorder, samples)
        events = recorder.get_events("sampling")

        sampled = list(map(lambda e: e.data["sampled"], events))
        expected = list(map(lambda e: e.data["expected"], events))

        rouge = self.rouge.get_scores(sampled, expected,avg=True)

        return {
            "rouge": rouge,
        }
