#!/bin/bash

model_name="" #模型名称
model="" #模型地址

api_key="none"
dataset_name="all" 
date_part="" #测评时间
result_dir="${dataset_name}_${model_name}"
result_path="../result_${date_part}/${result_dir}"  # 组合成完整路径
port=8003  # 服务端口
cuda_devices="0,1,2,3,4,5,6,7"
tensor_parallel_size=$(echo $cuda_devices | tr -cd ',' | wc -c)  
tensor_parallel_size=$((tensor_parallel_size + 1)) 

# 打印调试信息
echo "Running script with model_name=$model_name, model=$model, result_path=$result_path"
echo "Using CUDA_VISIBLE_DEVICES=$cuda_devices, tensor_parallel_size=$tensor_parallel_size, port=$port"

# 设置 CUDA_VISIBLE_DEVICES
export CUDA_VISIBLE_DEVICES=$cuda_devices

# 创建日志目录
log_dir="./log"
mkdir -p $log_dir

# 生成带时间戳的日志文件名
timestamp=$(date +"%Y%m%d_%H%M%S")
logfile="$log_dir/logfile_$timestamp.log"

# 定义清理函数
cleanup() {
    echo "Cleaning up..."
    if [ -n "$vllm_pid" ]; then
        echo "Stopping vllm service and all child processes..."
        pkill -P $vllm_pid  # 终止所有子进程
        kill $vllm_pid       # 终止主进程
    fi
    echo "Cleanup completed."
}

trap cleanup EXIT

echo "Starting vllm service on port $port..."
python -m vllm.entrypoints.openai.api_server \
    --model $model \
    --served-model-name $model_name \
    --trust-remote-code \
    --tensor-parallel-size $tensor_parallel_size \
    --gpu-memory-utilization 0.9 \
    --port $port >> $logfile 2>&1 &

# 获取 vllm 服务的进程 ID
vllm_pid=$!

timeout=8000
start_time=$(date +%s)  # 记录开始时间

echo "Waiting for vllm service to start..."
while ! curl -s "http://localhost:$port/v1" > /dev/null; do
    current_time=$(date +%s)
    elapsed_time=$((current_time - start_time))
    
    if [ $elapsed_time -ge $timeout ]; then
        echo "Service did not become available within $timeout seconds. Stopping vllm service and exiting..."
        exit 1
    fi
    
    echo "Service not yet available, retrying in 5 seconds... (Elapsed time: $elapsed_time seconds)"
    sleep 5
done

echo "vllm service is up and running on port $port."

# 进入 src 目录并执行评测
cd ../src

echo "Running evaluation..."
python exec_eval_main.py \
    --model_name $model_name \
    --model_path "http://localhost:$port/v1" \
    --api_key $api_key \
    --dataset_name $dataset_name \
    --save_path $result_path
    # --think_mode

# 获取评分
echo "Calculating scores..."
python get_score_think.py \
    --model_name $model_name \
    --dataset_name $dataset_name \
    --result_path $result_path

# 计算并保存平均值
echo "Calculating and saving averages..."
python calculate_and_save_averages.py \
    --model_name $model_name \
    --result_path $result_path

echo "Script execution completed."
