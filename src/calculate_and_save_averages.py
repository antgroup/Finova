import json
import argparse

def calculate_and_save_averages(args):
    model_name = args.model_name
    result_path = args.result_path
    # 动态生成文件路径
    score_file_path = f"{result_path}/{model_name}_score.json"
    output_file_path = f"{result_path}/{model_name}_score_group_averages.json"

    # 从JSON文件中读取数据
    with open(score_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 遍历数据，计算每个大标题的总分和数量
    i = 0
    sum_val = 0
    for _, value in data.items():
        i += 1
        sum_val += value

    # 构建结果字典，包含各组平均值和各组的分类平均值
    result = {
        "all": sum_val / i
    }

    # 将结果保存到JSON文件
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=4, ensure_ascii=False)

    print(f"Group averages saved to {output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate group averages from evaluation scores.")
    parser.add_argument("--model_name", type=str, required=True, help="Name of the model (e.g., qwen2.5_7b).")
    parser.add_argument("--result_path", type=str, required=True, help="Path to store the result files.")
    args = parser.parse_args()

    calculate_and_save_averages(args)