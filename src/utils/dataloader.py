import json
import os

def load_dataset_NER(path):
    dataset = []
    with open(path, mode="r", encoding="utf-8") as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "NER"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] =  data["from"]
        dataset.append(details)
    return dataset

def load_dataset_YITU(path):
    dataset = []
    with open(path, mode="r", encoding="utf-8") as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "YITU"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] = data["from"]
        dataset.append(details)
    return dataset

def load_dataset_CEHUA(path):
    dataset = []
    with open(path, mode='r') as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "CEHUA"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] = data["from"]
        dataset.append(details)
    return dataset

def load_dataset_BIAODA(path):
    dataset = []
    with open(path, mode='r') as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "BIAODA"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] = data["from"]
        dataset.append(details)
    return dataset

def load_dataset_CotEval(path):
    dataset = []
    with open(path, mode='r') as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "CotEval"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] = data["from"]
        dataset.append(details)
    return dataset

def load_dataset_Safety(path):
    dataset = []
    with open(path, mode='r') as f:
        data_list = json.load(f)
    for data in data_list:
        details = {}
        details["subject"] = "Safety"
        details["prompt"] = data["prompt"]
        details["answer"] = data["ground_truth"]
        details["from"] = data["from"]
        dataset.append(details)
    return dataset

def load_yitu(path):
    dataset = load_dataset_YITU(os.path.join(path, "Agent", "金融意图识别.json"))
    return dataset

def load_ner(path):
    dataset = load_dataset_NER(os.path.join(path, "Agent", "金融NER.json"))
    return dataset

def load_cehua(path):
    dataset = load_dataset_CEHUA(os.path.join(path, "Agent", "金融工具策划.json"))
    return dataset

def load_biaoda(path):
    dataset = load_dataset_BIAODA(os.path.join(path, "Agent", "金融表达.json"))
    return dataset

def load_coteval(path):
    dataset = load_dataset_CotEval(os.path.join(path, "Reasoning", "复杂金融问题.json"))
    return dataset

def load_safety(path):
    dataset = load_dataset_Safety(os.path.join(path, "ComplianceSafety", "安全合规.json"))
    return dataset

def load_dataset_all(path):
    dataset_all = load_dataset_YITU(os.path.join(path, "Agent", "金融意图识别.json"))
    dataset_all.extend(load_dataset_NER(os.path.join(path, "Agent", "金融NER.json")))
    dataset_all.extend(load_dataset_CEHUA(os.path.join(path, "Agent", "金融工具策划.json")))
    dataset_all.extend(load_dataset_BIAODA(os.path.join(path, "Agent", "金融表达.json")))
    dataset_all.extend(load_dataset_CotEval(os.path.join(path, "Reasoning", "复杂金融问题.json")))
    dataset_all.extend(load_dataset_Safety(os.path.join(path, "ComplianceSafety", "安全合规.json")))
    return dataset_all

DATASET_CONFIG = {
    'yitu': load_dataset_YITU,
    'ner': load_dataset_NER,
    'cehua': load_dataset_CEHUA,
    'biaoda': load_dataset_BIAODA,
    'coteval': load_dataset_CotEval,
    'safety': load_dataset_Safety,
    'all': load_dataset_all
}

def load_dataset(path, dataset_type):
    dataset_type = dataset_type.lower()
    if dataset_type not in DATASET_CONFIG:
        raise ValueError(f"不支持的数据集类型: {dataset_type}")
    return DATASET_CONFIG[dataset_type](path)

if __name__ == "__main__":
    dataset = load_dataset("/ossfs/workspace/test/FinBench/data", "all")
    print(len(dataset))



        

            
