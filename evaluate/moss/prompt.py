# -*- coding: utf-8 -*-
# @Author  : ssbuild
# @Time    : 2023/7/11 10:41

import os
import re
import typing
from tqdm import tqdm
from evaluate.prompt.prompt import EvaluateBuilderBase
from evaluate.moss.infer import Engine_API

class EvaluateBuilder(EvaluateBuilderBase):
    def __init__(self,choices, model_name, k):
        super().__init__(choices, model_name, k)
        self.api_client: typing.Optional[Engine_API] = None

    def init(self):
        self.api_client = Engine_API()
        self.api_client.init()
        A = self.api_client.tokenizer.encode("A", bos=False, eos=False)[0]
        B = self.api_client.tokenizer.encode("B", bos=False, eos=False)[0]
        C = self.api_client.tokenizer.encode("C", bos=False, eos=False)[0]
        D = self.api_client.tokenizer.encode("D", bos=False, eos=False)[0]
        self.choices_ids = [A,B,C,D]

    def eval_subject(self, subject_name, test_df, dev_df=None, few_shot=False, cot=False, save_result_dir=None):
        correct_num = 0
        if save_result_dir:
            if few_shot:
                result = []
            score = []
        if few_shot:
            history = self.generate_few_shot_prompt(subject_name, dev_df, cot=cot)
        else:
            history = []
        answers = list(test_df['answer'])
        for row_index, row in tqdm(test_df.iterrows(), total=len(test_df)):
            question = self.format_example(row, include_answer=False, cot=cot)
            if few_shot:
                response, _ = self.api_client.infer(question, do_sample=False, history=history)
                response = response.strip()
                # For ChatGLM, we use answer extraction in answer-only mode too.
                ans, direct_extract = self.extract_cot_answer(row, response)
            else:  # zero-shot by extracting answer from distribution
                ans = self.generate_dist(question, do_sample=False, max_length=2048,history=history)
            if ans == answers[row_index]:
                correct_num += 1
                correct = 1
            else:
                correct = 0
            if save_result_dir:
                if few_shot:
                    result.append(response)
                score.append(correct)
        correct_ratio = 100 * correct_num / len(answers)

        if save_result_dir:
            if few_shot:
                test_df['model_output'] = result
            test_df['correctness'] = score
            test_df.to_csv(os.path.join(save_result_dir, f'{subject_name}_test.csv'))

        return correct_ratio

    def generate_few_shot_prompt(self, subject, dev_df, cot=False):
        message = []
        k = self.k
        if self.k == -1:
            k = dev_df.shape[0]
        message.append(self.format_example(dev_df.iloc[0, :], cot=cot,
                                           add_prompt=f"以下是中国关于{subject}考试的单项选择题，请选出其中的正确答案。\n\n"))
        for i in range(1, k):
            message.append(self.format_example(dev_df.iloc[i, :], cot=cot))
        return message

    def format_example(self, line, include_answer=True, cot=False, add_prompt=''):
        example = add_prompt + line['question']
        # print(example)
        for choice in self.choices:
            example += f'\n{choice}. {line[f"{choice}"]}'
        example += '\n答案：'
        if include_answer:
            if cot:
                ans = "让我们一步一步思考，\n" + line["explanation"] + f"\n所以答案是{line['answer']}。"
            else:
                ans = line["answer"]
            m = (example, ans)
            return m
        return example

    def extract_cot_answer(self, line, gen_ans):
        m = re.findall(r'所以答案是(.+?)。', gen_ans, re.M)
        if len(m) > 0 and m[-1] in self.choices:
            return m[-1], True
        answer_patterns = [
            r'([ABCD])是正确的',
            r'选项([ABCD])正确',
            r'答案为([ABCD])',
            r'答案是([ABCD])',
            r'答案([ABCD])',
            r'选择([ABCD])',
            r'答案：([ABCD])',
            r'选择答案([ABCD])'
        ]
        # RE extraction
        for answer_pattern in answer_patterns:
            m = re.search(answer_pattern, gen_ans, re.M)
            if m:
                answer = m.group(1)
                return answer, False
        # only containing one choice-character
        m = re.findall(r'[ABCD]', gen_ans, re.M)
        if len(m) == 1:
            answer = m[0]
            return answer, False
        answer_word_counter = 0
        # only containing one choice-context
        for c in self.choices:
            if str(line[f'{c}']) in gen_ans:
                answer = c
                answer_word_counter += 1
        if answer_word_counter == 1:
            return answer, False
        return '-', False

    def generate_dist(self, query, history, num_beams=1, max_length=2048,
                      do_sample=False, top_p=0.7, temperature=0.95, logits_processor=None, **kwargs):
        if history is None:
            history = []

        gen_kwargs = {"num_beams": num_beams, "do_sample": do_sample, "top_p": top_p, "max_length": max_length,
                      "temperature": temperature, "logits_processor": logits_processor, **kwargs}

        scores = self.api_client.infer(query,return_dict_in_generate=True, output_scores=True,history=history, **gen_kwargs)
        score = scores[0].tolist()



        choice_score = [score[self.choices_ids[0]], score[self.choices_ids[1]],
                        score[self.choices_ids[2]], score[self.choices_ids[3]]]
        ranked_index = [index for index, value in
                        sorted(list(enumerate(choice_score)), key=lambda x: x[1], reverse=True)]
        return self.choices[ranked_index[0]]