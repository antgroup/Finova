import argparse
import os
import time
import pandas as pd
from tqdm import tqdm
from evaluator.api_evaluator import APIEvaluator
from utils.dataloader import load_dataset
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_evaluator(model_name, model_path, api_key):
    """
    加载评估模型
    """
    try:
        evaluator = APIEvaluator(
            api_key=api_key,
            api_base=model_path,
            model_name=model_name
        )
        return evaluator
    except Exception as e:
        print(f"模型加载失败: {e}")
        raise

def get_answer(data, evaluator, model_name, args):
    """
    获取模型答案
    """
    prompt_query = data['prompt']
    max_retries = args.max_retries
    retry_delay = args.retry_delay
    
    for attempt in range(max_retries):
        try:
            model_answer = evaluator.answer(prompt_query)
            data[f'{model_name}_answer'] = model_answer
            break
        except Exception as e:
            if attempt < max_retries - 1:
                print(
                    f"获取 {model_name} 答案失败，第 {attempt + 1} 次重试。错误: {str(e)}"
                )
                time.sleep(retry_delay)
            else:
                print(
                    f"获取 {model_name} 答案失败，已达最大重试次数。错误: {str(e)}"
                )
                data[f'{model_name}_answer'] = "获取答案失败"
    
    return data

def fineva_main(args):
    """
    主处理函数
    """
    
    try:
        # 导入模型
        evaluator = load_evaluator(args.model_name, args.model_path, args.api_key)
        print(f'模型 {args.model_name} 加载成功')

        # 导入数据
        dataset = load_dataset("../data", args.dataset_name)

        # 多线程处理
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []
            for data in dataset:
                future = executor.submit(
                    get_answer, 
                    data, 
                    evaluator, 
                    args.model_name,
                    args,
                )
                futures.append(future)
            
            for future in tqdm(as_completed(futures), total=len(futures), desc="处理中"):
                future.result()  

        # 保存结果
        df = pd.DataFrame(dataset)
        os.makedirs(args.save_path, exist_ok=True)

        save_file = os.path.join(args.save_path, f'{args.model_name}_ga.csv')
        df.to_csv(save_file, index=False)
        print(f'结果已保存到 {save_file}')

    except Exception as e:
        print(f"处理过程发生错误: {e}")
        raise

def parse_arguments():
    """
    解析命令行参数
    """
    parser = argparse.ArgumentParser(description="FinEva 大模型评估工具")
    parser.add_argument('--model_name', required=True, type=str, help="模型名称")
    parser.add_argument('--model_path', required=False, type=str, help="模型路径/API Base")
    parser.add_argument('--api_key', required=False, type=str, help="API密钥")
    parser.add_argument('--save_path', required=True, type=str, help="结果保存路径")
    parser.add_argument('--dataset_name', required=True, type=str, help="数据集名称")
    parser.add_argument('--threads', type=int, default=20, help="并行处理的线程数")
    
    # 重试相关参数
    parser.add_argument('--max_retries', type=int, default=5, help="最大重试次数")
    parser.add_argument('--retry_delay', type=int, default=2, help="重试延迟时间(秒)")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    fineva_main(args)
