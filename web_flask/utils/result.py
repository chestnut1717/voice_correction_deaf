import numpy as np
import dtw
import librosa
import matplotlib.pyplot as plt

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

# LCS 알고리즘을 사용하여 두 string 중에서 겹치는 음소 subsequence 출력 용도
def lcs_algo(S1, S2, m, n):
    L = [[0 for x in range(n+1)] for x in range(m+1)]

    # bottom-up 방식으로 matrix 쌇아감
    for i in range(m+1):
        for j in range(n+1):
            if i == 0 or j == 0:
                L[i][j] = 0
            elif S1[i-1] == S2[j-1]:
                L[i][j] = L[i-1][j-1] + 1
            else:
                L[i][j] = max(L[i-1][j], L[i][j-1])

    index = L[m][n]

    lcs_algo = [""] * (index+1)
    lcs_algo[index] = ""

    i = m
    j = n
    while i > 0 and j > 0:

        if S1[i-1] == S2[j-1]:
            lcs_algo[index-1] = S1[i-1]
            i -= 1
            j -= 1
            index -= 1

        elif L[i-1][j] > L[i][j-1]:
            i -= 1
        else:
            j -= 1
            
    #  subsequences 출력
    print("S1 : " + S1 + "\nS2 : " + S2)

    lcs = "".join(lcs_algo)
    print("LCS: " + lcs)

    return lcs

# 정확도 및 score 반환
def calculate_acc(ans, lcs):
    accuracy = int(len(lcs) / len(ans) * 100)
    score = ""

    if accuracy == 100:
        score = "Perfect"
    elif accuracy >= 80:
        score = "Great"
    elif accuracy >= 60:
        score = "Good"
    else:
        score = "Try Again"

    return accuracy, score

# 정답 음소와 발화자의 음소 중, 일치하는 음소 구분해서 출력해주는 함수
def highlight(ans, lcs):
  # answer phonemes중에 틀린것은 0, 일치하는 것은 1로 두어, 0인것은 나중에 틀린것 표시하기 위함
  correct = [[i, 0] for i in ans]
  idx=0

  # lcs에서 하니씩 음소를 가져와서 answer과 비교함
  ## 일치하면 correct의 해당 음소의 값을 0에서 1로
  for char in lcs:
      while idx < len(ans):
          tmp = ans[idx]

          if tmp == char:
              correct[idx][1] = 1
              idx += 1
              break
          idx += 1
    
  return correct

def to_graph(ans_wav, deaf_wav):

    rms1, rms2 = librosa.feature.rms(ans_wav), librosa.feature.rms(deaf_wav)
    compare, sample = downsample(rms1, rms2)
    plt.plot(compare, sample)
    # new_alignment = dtw.dtw(compare.flatten(), sample.flatten())
    # new_alignment.plot(type='twoway').savefig('rms.png')
    plt.savefig('dtw.png')
    return None
