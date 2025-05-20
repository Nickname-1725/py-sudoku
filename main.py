
import random
import itertools
import array

def solve_sudoku(board : list[list[int]]):
  """
  求解数独，判断是否可解（会修改board，使其变为已解状态）
  """
  def is_valid(board, row, col, num):
    """
    检验行、列、九宫格
    """
    # 行检查
    for i in range(9):
        if board[row][i] == num:
            return False
    # 列检查
    for i in range(9):
        if board[i][col] == num:
            return False
    # 九宫格检查
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False
    return True
  
  # 遍历
  for row in range(9):
    for col in range(9):
      if board[row][col] == 0: # 找到空格
        
        for num in range(1, 10): # 尝试 1-9
          if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board): # 进一步求解数独
              return True
          board[row][col] = 0  # 尝试失败, 回溯
        return False # 1-9 均无法完成
  return True # 没有空格，成功

def rand_series_gen (length:int =9) -> list[int]:
  # random.sample 一次性生成不重复随机数列表
  return random.sample(range(1, length + 1), length)

def gen_3x3_tuple_ls () -> tuple[int]:
  """
  生成一组（9个）九宫格内的坐标
  返回值类型为tuple(int)
  """
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

def gen_3x3_tuple_ls_times (times:int =9) -> list[tuple[int]]:
  """
  为每个数字生成各自九宫格内的坐标，确保相互不重叠
  返回值类型为list(tuple(int))
  """
  results = []
  seen_ls = tuple (set() for _ in range(9)) 
  # 1. 利用集合的哈希特性，快速检查是否重复
  # 2. 生成9个集合
  # 3. seen_ls元组本身不可改变，但集合可更新

  while len(results) < times:
    new_tuple_ls = gen_3x3_tuple_ls()

    # 将嵌套列表展平并转换为不可变的元组
    flattened = tuple (itertools.chain.from_iterable(new_tuple_ls))

    # 检查是否重复，只有不重复的才能加入结果
    if any(tuple_ in seen for tuple_, seen in zip(flattened, seen_ls)):
      continue

    # 检查是否有解，只有有解才能更新结果
    try_results = list.copy (results)
    try_results.append (new_tuple_ls)
    if not solve_sudoku (gen_sudoku (try_results)):
      continue
    
    # 更新结果
    for seen, tuple_in_block in zip (seen_ls, flattened):
      seen.add (tuple_in_block)
    results = try_results

  return results

def gen_sudoku (tuple_3x3_x9 : list[tuple[int]]) -> list[array.array[int]]:
  """
  生成代表数独的嵌套数组(列表)
  返回类型为list(array(int))
  """
  rows, cols = 9, 9
  table = [array.array('i', [0] * cols) for _ in range(rows)]

  for nested_ls, num in zip (tuple_3x3_x9, range(1,10)):
    for ls, h_chunks_indx in zip (nested_ls, range(3)):
      for (x_,y_), v_chunks_indx in zip (ls, range(3)):
        y = y_ -1 + h_chunks_indx*3
        x = x_ -1 + v_chunks_indx*3
        table [y][x] = num

  return table

def pretty_print_sudoku (sudoku_table : list[array.array[int]]) -> None:
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
  tuple_ls_x9 = gen_3x3_tuple_ls_times (9)
  pretty_print_sudoku (gen_sudoku (tuple_ls_x9))

if  __name__ == "__main__":
  main ()
