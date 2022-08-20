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