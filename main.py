
import random
import itertools
import array

def rand_series_gen (length:int =9):
  # random.sample 一次性生成不重复随机数列表
  return random.sample(range(1, length + 1), length)

def gen_3x3_tuple_ls ():
  x_variants = [rand_series_gen(3) for _ in range(3)]
  y_variants = [rand_series_gen(3) for _ in range(3)]

  nested_ls = [
    [
      (x_ls [x_indx], y_ls [y_indx]) # 这里的 x_indx 和 y_indx 是索引
      for x_ls, y_indx in zip(x_variants, range(3))
    ]
    for y_ls, x_indx in zip(y_variants, range(3))
  ]

  return nested_ls

def gen_3x3_tuple_ls_times (times:int =9):
  results = []
  seen = set()  # 利用集合的哈希特性，快速检查是否重复

  while len(results) < times:
    new_tuple_ls = gen_3x3_tuple_ls()

    # 将嵌套列表展平并转换为不可变的元组
    flattened = tuple (zip (list(itertools.chain.from_iterable(new_tuple_ls)), range(9)))
    #print (flattened)

    if seen.intersection(flattened):
      continue
      
    # 只有不重复的才能加入结果
    seen.update(flattened)
    results.append(new_tuple_ls)

  return results

def gen_sudoku (tuple_3x3_x9):
  rows, cols = 9, 9
  table = [array.array('i', [0] * cols) for _ in range(rows)]

  for nested_ls, num in zip (tuple_3x3_x9, range(1,10)):
    for ls, h_chunks_indx in zip (nested_ls, range(3)):
      for (x_,y_), v_chunks_indx in zip (ls, range(3)):
        y = y_ -1 + h_chunks_indx*3
        x = x_ -1 + v_chunks_indx*3
        table [y][x] = num

  #print(nested_array[1][2])  # 输出: 6
  #print(table)
  return table

def main ():
  print (rand_series_gen ())
  print (gen_3x3_tuple_ls ())
  #print (gen_3x3_tuple_ls_times (9))
  print (gen_sudoku (gen_3x3_tuple_ls_times (9)))

if  __name__ == "__main__":
  main ()
