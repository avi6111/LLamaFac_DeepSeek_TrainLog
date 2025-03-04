from multiprocessing import process
import pyarrow.parquet as pq

# 分块读取 Parquet 文件
table = pq.read_table("large_file.parquet", memory_map=True)
batch_size = 1000
for batch in table.to_batches(max_chunksize=batch_size):
    process(batch)  # 逐块处理