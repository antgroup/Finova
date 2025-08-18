from utils.dataloader import load_coteval, load_biaoda, load_cehua, load_safety, load_yitu, load_ner, load_dataset_all

dataset = load_yitu("../data")
print("*"*30)
print("意图测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_ner("../data")
print("*"*30)
print("提槽测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_cehua("../data")
print("*"*30)
print("策划测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_biaoda("../data")
print("*"*30)
print("表达测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_coteval("../data")
print("*"*30)
print("复杂金融整体测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_safety("../data")
print("*"*30)
print("整体测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])

dataset = load_dataset_all("../data")
print("*"*30)
print("整体测评集总数：" + str(len(dataset)))
print("单个样例：")
print(dataset[0])