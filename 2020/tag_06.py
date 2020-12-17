import time
def make_char_set(str_list):
    return  [set(item) for item in str_list]

def get_puzzle(file_name):
    with open(file_name) as f:
        puzzle = [make_char_set(s.split()) for s in f.read().split("\n\n")]
    return puzzle

def solve_1_2(puzzle):
    s_u = s_is = 0
    for l_item in puzzle:
        s_result_u = s_result_is =  l_item[0]
        for s_item in l_item:
            s_result_u = s_result_u.union(s_item)
            s_result_is = s_result_is.intersection(s_item)
        s_u += len(s_result_u)
        s_is += len(s_result_is)
    return s_u, s_is

p = get_puzzle("tag_06.txt")
start = time.perf_counter()
results = solve_1_2(p)
dt_ms =  (time.perf_counter() - start) * 1000
print("Task 1", results[0], "Task 2", results[1], "time needed [ms]: {0:.1f}".format(dt_ms))