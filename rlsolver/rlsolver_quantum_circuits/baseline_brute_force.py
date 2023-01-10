import pickle as pkl
import torch as th
from copy import deepcopy
device = th.device("cuda:0")
reward = 0
N = 4

with open(f"test_data_tensor_train_N={N}.pkl", 'rb') as f:
    a = pkl.load(f).detach().cpu()
num_env = a.shape[0]
start_ =  th.as_tensor([i for i in range(N)]).repeat(1, num_env).reshape(num_env, -1).to(device)
end_ =  th.as_tensor([i for i in range(N)]).repeat(1, num_env).reshape(num_env, -1).to(device)
reward = th.zeros(num_env, 6)
permute_list = th.as_tensor([[0, 1, 2], [0, 2, 1], [1, 0, 2], [1, 2, 0], [2, 0, 1], [2, 1, 0]])


for k in range(num_env):
    for permute_i in range(6):
        permute = permute_list[permute_i]
        r = 0
        state = a[k]
        start = deepcopy(start_[k]) + 1
        end = deepcopy(end_[k]) + 1
        for i in permute:
            tmp = 1
            for j in range(start[i], end[i] + 1):
                tmp *= (state[j, j] * state[j, start[i] - 1] * state[end[i] + 1, j])
            for j in range(start[i + 1], end[i + 1] + 1):
                tmp *= (state[j, j] * state[j, start[i + 1] - 1] * state[end[i + 1] + 1, j])
            tmp = tmp / state[start[i + 1], start[i + 1] - 1]
            start_new = min(start[i], start[i + 1])
            end_new = max(end[i], end[i + 1])
            for __ in range(start_new, end_new + 1):
                start[__-1] = start_new
                end[__-1] = end_new

            r += tmp
        reward[k, permute_i] = r
    print(reward[k], permute_list[reward[k].min(dim=-1)[1]])
print(reward.min(dim=-1)[0].mean())
with open("record_r.pkl", "wb") as f:
    import pickle as pkl
    pkl.dump(reward, f)

