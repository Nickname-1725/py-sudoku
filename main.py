
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
  seen_ls = tuple (set() for _ in range(9)) 
  # 1. 利用集合的哈希特性，快速检查是否重复
  # 2. 生成9个集合
  # 3. seen_ls元组本身不可改变，但集合可更新

  while len(results) < times:
    new_tuple_ls = gen_3x3_tuple_ls()

    # 将嵌套列表展平并转换为不可变的元组
    flattened = tuple (itertools.chain.from_iterable(new_tuple_ls))

    if any(tuple_ in seen for tuple_, seen in zip(flattened, seen_ls)):
      continue

    # 只有不重复的才能加入结果
    for seen, tuple_in_block in zip (seen_ls, flattened):
      seen.add (tuple_in_block)
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

  return table

def pretty_print_sudoku (sudoku_table):
  def group_ls (lst, group_size):
    # 把列表按照每组的长度分组
    # lst可能是列表或者向量, 只需允许索引访问即可
    groups = [lst[i:i+group_size] for i in range(0, len(lst), group_size)]
    return groups

  print("-------------------")
  for vector_group in group_ls (sudoku_table, 3):
    for vector in vector_group:
      groups = group_ls (vector, 3)
      formatted_list = "|".join(" ".join(map(str, group)) for group in groups)

      print("|{}|".format(formatted_list))
    print("-------------------")

def main () -> None:
  """
  生成并打印数独(答案)
  """
  pretty_print_sudoku (gen_sudoku (gen_3x3_tuple_ls_times (9)))

if  __name__ == "__main__":
  main ()
