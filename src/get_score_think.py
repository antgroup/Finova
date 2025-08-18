import argparse
import os
import re
import ast
import pandas as pd
from sklearn.metrics import accuracy_score
from utils.file_utils import save_json
from utils.math_grader import math_equal
import json

def accuracy_score_NER(answers, predictions):
    """
    针对提槽的评测集
    """
    data_count = 0
    correct_count = 0
    losse_count = 0

    for answer, prediction in zip(answers, predictions):
        data_count += 1
        try:
            if answer != "":
                ans = json.loads(answer)
            else:
                ans = []
            if prediction != "":
                pre = json.loads(prediction)
            else:
                pre = []
        except Exception as e:
            continue
        if len(ans) == 0 and len(pre) == 0:
            correct_count += 1
            losse_count += 1
        elif len(ans) != 0 and len(pre) != 0:   
            correct = 0
            for a in pre:
                for b in ans:
                    try:
                        if a["type"] == b["type"]:
                            if a["content"] == b["content"] or b["content"] in a["content"]:
                                correct += 1
                                break
                    except Exception as e:
                        continue
            if correct == len(pre):
                correct_count += 1
    return correct_count / data_count


def accuracy_score_CEHUA(answers, predictions):
    """
    针对策划的评测集
    """
    data_count = 0
    correct_count = 0

    def is_superset(list_a, list_b):
        return set(list_a).issuperset(set(list_b))

    for answer, prediction in zip(answers, predictions):
        data_count += 1 
        try:     
            if is_superset(ast.literal_eval(prediction), ast.literal_eval(answer)):
                correct_count += 1
        except Exception as e:
            continue
    return correct_count / data_count

def accuracy_score_YITU(answers, predictions):
    """
    针对意图的评测集
    """
    data_count = 0
    correct_count = 0
    for answer, prediction in zip(answers, predictions):
        data_count += 1 
        try:
            answer = sorted(ast.literal_eval(answer))
            prediction = sorted(ast.literal_eval(prediction))
            if answer == prediction:
                correct_count += 1
        except Exception as e:
            continue
    return correct_count / data_count

def accuracy_score_CotEval(answers, predictions):
    """
    针对复杂金融的评测集
    """
    data_count = 0
    correct_count = 0
    for answer, prediction in zip(answers, predictions):
        data_count += 1 
        if len(answer) == 1:
            if answer == prediction:
                correct_count += 1
        else:
            if ";" in answer:
                answer = answer.split(";")
                prediction = prediction.split(";")
                if len(answer) == len(prediction):
                    flag = True
                    for ans, pre in zip(answer, prediction):
                        if not math_equal(ans, pre):
                            flag = False
                            break
                    if flag:
                        correct_count += 1
            else:
                if "A" in answer or "B" in answer or "C" in answer or "D" in answer:
                    answer = answer.split()
                    prediction = prediction.split(";")
                    if len(answer) == len(prediction):
                        if set(answer) == set(prediction):
                            correct_count += 1
                else:
                    if math_equal(answer, prediction):
                        correct_count += 1
    return correct_count / data_count


def extract_yn(response: str) -> str:
    choices = ["是", "否", "对", "错"]

    if response == '':
        return ""

    # 普通匹配
    patterns = [
        (r'([是对])[ ？]*正确', 1),
        (r'([否错])[ ？]*错误', 1),
        (r'([是对])', 1),
        (r'([否错])', 1)
    ]
    first_match = None  
    try:
        first_position = len(response)  
    except Exception as e:
        response = ""
        first_position = 0

    for pattern, idx in patterns:
        for m in re.finditer(pattern, response):
            answer = m.group(idx)
            position = m.start(idx)  

            if answer in choices and position < first_position:
                first_match = answer
                first_position = position  
    # 推理匹配
    think_patterns = [
        (r'boxed\{\\text\{([是否])\}\}', 1), 
        (r'boxed\{([是否])\}', 1), 
        (r'<answer>([否错])</answer>', 1), 
        (r'<answer>([是对])</answer>', 1), 
        (r'\*\*([是对])\*\*', 1), 
        (r'\*\*([否错])\*\*', 1), 
        (r'\n([是对])', 1), 
        (r'\n([否错])', 1)
        ]

    first_position = len(response) 
    for pattern, idx in think_patterns:
        for m in re.finditer(pattern, response):
            answer = m.group(idx)
            position = m.start(idx)  
            if answer != "":
                return answer

    return first_match if first_match is not None else ""

def extract_answer_json(response: str) -> str:
    if response == '':
        return ""
    
    patterns = [
            (r'<answer>[\s\S]*?(\[[\s\S]*?\])[\s\S]*?</answer>', 1),
            (r'json(\[[\s\S]*\])', 1),
            (r'<answer>【工具S】([\s\S]*?)【工具E】', 1),
            (r'</think>[\s\S]*?【工具S】([\s\S]*?)【工具E】', 1),
            (r'【工具S】([\s\S]*?)【工具E】', 1),
            (r'<example>\n(.+)\n</example>', 1),
            (r'</think>[\s\S]*?json\s*(\[[\s\S]*\])', 1),
            (r'\`\`\`json(\[[\s\S]*?\])\n', 1),
            (r'json(\[[\s\S]*\])', 1),
            (r'json\s*(\[[\s\S]*\])', 1),
            (r'<answer>[\s\S]*?(\[[\s\S]*\])[\s\S]*</answer>', 1),
            (r'</think>[\s\S]*?(\[[\s\S]*\])[\s\S]*', 1),
            (r'<answer>([\s\S]+)</answer>', 1),
            (r'(\[[\s\S]*\])', 1),
        ]   
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            if answer != "":
                return answer

    return ""

def extract_answer_multi(response: str) -> str:
    if response == '':
        return ""
    
    patterns = [
            (r'<answer>[\s\S]*boxed\{\{(.*)\}\}[\s\S]*</answer>', 1),
            (r'<answer>[\s\S]*boxed\{(.*)\}[\s\S]*</answer>', 1),
            (r'<answer>([\s\S]+)</answer>', 1),
            (r'boxed\{\{(.*)\}\}', 1),
            (r'boxed\{(.*)\}', 1),
            ]   
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            if answer != "":
                return answer

    return ""

def extract_answer_list(response: str) -> str:
    if response == '':
        return ""
    patterns = [
            (r'```[\s\S]*(\[.*\])', 1),
            (r'boxed\{\\text\{([.*])\}\}', 1),
            (r'<answer>[\s\S]*boxed\{\{(.*)\}\}[\s\S]*</answer>', 1),
            (r'<answer>[\s\S]*boxed\{(.*)\}[\s\S]*</answer>', 1),
            (r'<answer>(\[[\s\S]+?\])</answer>', 1),
            (r'<answer>([\s\S]+)</answer>', 1),
            (r'boxed\{\{(.*)\}\}', 1),
            (r'boxed\{(.*)\}', 1),
            (r'</think>[\s\S]*?(\[[\s\S]*\])', 1),
            ]   
    for pattern, idx in patterns:
        m = re.search(pattern, response, re.M)
        if m:
            answer = m.group(idx)
            if answer != "":
                return answer

    return "[]"

EXTRACTOR_MAP = {
    'agent-提槽': extract_answer_json,
    'agent-策划': extract_answer_json,
    'agent-表达': extract_yn,
    '安全': extract_yn,
    '合规': extract_yn,
    'agent-意图': extract_answer_list,
    'reasoning-数学/代码': extract_answer_multi,
    'reasoning-复杂金融': extract_answer_multi
}

TASK_ACCURACY_FUNCTIONS_MAP = {
    'NER': accuracy_score_NER,
    'CEHUA': accuracy_score_CEHUA,
    'CotEval': accuracy_score_CotEval,
    'YITU': accuracy_score_YITU,
    'Safety': accuracy_score,
    'BIAODA': accuracy_score
}

def get_score(args):
    model_name = args.model_name
    result_path = args.result_path

    if not os.path.exists(result_path):
        os.makedirs(result_path)

    ga_result_path = os.path.join(result_path, f'{model_name}_ga.csv')
    df = pd.read_csv(ga_result_path)
    sid_set = set()
    for index, row in df.iterrows():
        # 正则提取正确选项
        sid = row["subject"]
        sid_set.add(sid)
        df.at[index, f'{model_name}_extract'] = EXTRACTOR_MAP[row['from']](row[f'{model_name}_answer'])

    df.to_csv(os.path.join(result_path, f'{model_name}_result.csv'), index=False)

    # 计算 accuracy
    task_acc = {}
    sid_list = list(sid_set)
    sid_list.sort()
    for task in sid_list:
        task_df = df[df["subject"] == task]
        acc = TASK_ACCURACY_FUNCTIONS_MAP[task](task_df['answer'].tolist(), task_df[f'{model_name}_extract'].tolist())
        print(f'{task}: {acc}')
        task_acc[task] = acc

    save_json(task_acc, os.path.join(result_path, f'{model_name}_score.json'))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', required=True, type=str)
    parser.add_argument('--result_path', required=True, type=str)
    parser.add_argument('--dataset_name', required=True, type=str)
    args = parser.parse_args()
    get_score(args)
