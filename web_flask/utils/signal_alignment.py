import numpy as np

# 두 개의 다른 signal 길이 맞춰주는 함수 고안
def downsample(a, b):
    a, b = a.flatten(), b.flatten()
    if len(a) > len(b):
        target, compare = a, b
    else:
        target, compare = b, a

  # 정규화
    norm = np.linalg.norm(target)
    target = target/norm

    norm = np.linalg.norm(compare)
    compare = compare/norm

    sampled_list = []
    padding_size = int(len(target) / len(compare))
    print(padding_size)
    if padding_size > 1:
        for i in range(0, len(target), padding_size):
            tmp = np.mean( target[i:i+padding_size] )
            sampled_list.append(tmp)
    else:
        per = np.percentile(target, 100 - len(compare)/len(target)*100)
        print('percentile')
        print(len(compare)/len(target))
        print(per)
        sampled_list = target[(target > per)]

    return compare, np.array(sampled_list)