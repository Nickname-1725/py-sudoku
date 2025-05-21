
import random
import itertools
import array
import copy # 引入深拷贝
import argparse # 引入命令行参数解析
import warnings # 引入警告

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

def solve_sudoku(board : list[list[int]]):
  """
  求解数独，判断是否可解（会修改board，使其变为已解状态）
  """
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

def solve_sudoku_guess_from_big(board : list[list[int]]):
  """
  求解数独，（会修改board，使其变为已解状态）
  与solve_sudoku不同的是，它会从较大数开始猜测
  """
  # 遍历
  for row in range(9):
    for col in range(9):
      if board[row][col] == 0: # 找到空格
        
        for num in reversed (range(1, 10)): # 尝试 9-1
          if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku(board): # 进一步求解数独
              return True
          board[row][col] = 0  # 尝试失败, 回溯
        return False # 1-9 均无法完成
  return True # 没有空格，成功

def sudoku_unique_p (board : list[list[int]]) -> bool:
  """
  判断解的唯一性（此函数不会改变输入board的值）
  注意：前提首先是数独可解，如果数独不可解，同样会返回False
  """
  board_1 = copy.deepcopy (board)
  board_2 = copy.deepcopy (board)

  solve_sudoku (board_1)
  solve_sudoku_guess_from_big (board_2)
  return board_1 == board_2

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
      formatted_list = "|".join(" ".join(map(lambda x: str (x) if x != 0 else " "
                                             , group)) for group in groups)

      print("|{}|".format(formatted_list))
    print("-------------------")

def generate_random_tuples (limit:int =20) -> list[tuple[int]]:
  """
  给定长度，随机生成一组代表数独坐标的元组
  """
  all_tuples = list(itertools.product(range(0, 9), repeat=2)) # 从0下标开始0~8共有9个位置
  random.shuffle(all_tuples)
  return all_tuples[:limit]

def generate_unique_puzzle (board:list[list[int]], retain_num):
  """
  生成移除给定个数数字的数独谜题，解唯一
  限定输入retain_num范围为25~80，范围外会被强制修改
  """
  if retain_num < 25:
    warnings.warn ("保留数字个数调整为25：理论下限为17，但过少时生成数独极其困难。")
    retain_num = 25
  if retain_num > 80:
    warnings.warn ("保留数字个数调整为80：至少移除1个数字，它才算谜题吧。")
    retain_num = 80

  while True:
    # 9*9 - 保留数字个数 = 去除的数字个数
    remove_ls = generate_random_tuples (81 - retain_num)
    puzzle = copy.deepcopy(board)
    for tuple_ in remove_ls:
      puzzle [tuple_[0]][tuple_[1]] = 0
    if sudoku_unique_p (puzzle):
      return puzzle

def main (output : str, retain : int) -> None:
  """
  生成并打印数独(答案)
  """
  if retain <= 0: raise ValueError ("这不可能，怎么会不超过0个(ﾟOﾟ)")
  if retain >81 : raise ValueError ("这不可能，怎么会超过9×9个(ﾟOﾟ)")

  tuple_ls_x9 = gen_3x3_tuple_ls_times (9)
  sudoku = gen_sudoku (tuple_ls_x9)
  if output != "puzzle-only": # 是需要答案的情形
    print ("答案")
    pretty_print_sudoku (sudoku)

  if output != "answer-only": # 是需要谜题的情形
    puzzle = generate_unique_puzzle (sudoku, retain)
    print ("谜题")
    pretty_print_sudoku (puzzle)

if  __name__ == "__main__":
  # 创建解析器
  parser = argparse.ArgumentParser(description="数独随机生成器")
  parser.add_argument(
    "--output",
    type=str,
    choices=["answer-only", "puzzle-only", "both"],
    default="answer-only",
    help="输出的形式，是否需要答案或谜题"
  )
  parser.add_argument(
    "--retain",
    type=int,
    default=None,
    help="数独中保留的数字个数，仅在输出谜题时需要"
  )

  # 解析命令行参数
  args = parser.parse_args()

  # 验证参数
  if args.output in ["puzzle-only", "both"] and args.retain is None:
    parser.error("当 output 为 'puzzle-only' 或 'both' 时，必须指定 --retain 参数")
  if args.output == "answer-only" and args.retain is not None:
    warnings.warn("当 output 为 'answer-only' 时，不需要指定 --retain 参数")

  # 调用主函数
  main(output=args.output, retain=args.retain)
