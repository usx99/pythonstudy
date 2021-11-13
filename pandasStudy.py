
import bookmarks as bm
import pandas as pd
import time
csv_file = bm.FileBookmark("my_csv_file")
#print (csv_file.path)

#csv_file = 'C://Users//yhkim//documents//raw_data_big.csv'
#df = pd.read_csv(csv_file)
df = pd.read_csv(csv_file.path)

# 처음 다섯줄
#print (df.head())

# 컬럼명 확인하기
#print (df.columns)
# ROW기준 0부터 3
#print (dt[0:3])
#첫줄 확인하기
print (df.loc[0])
#마지막줄 확인하기
print (df.iloc[-1])
#행 개수 세기
dfRowCount = len(df)
print ('totalCount', dfRowCount)
# 유저별 unique count
userCount = len(df.groupby('user_identifier'))
print ('userCount ', userCount)
#print (dt['seq_num'])
#print (df.groupby('user_identifier'))
df['state'] = df['subfeature'].fillna('') + '_' + df['subfeature_value'].fillna('') + '_' + df['subfeature_meta'].fillna('')
# 유저별 인덱스 추가 - 기존열은 남겨놓고 업데이트
df.set_index('user_identifier', drop=False, inplace=True)
# 유저 array
userAr = df['user_identifier'].unique()
print (userAr)
treeDf = pd.DataFrame(data=[[1, 0, 'start_start_game_게임 시작']], columns = ['nodeCode', 'parentNodeCode', 'state'])
treeDf.set_index(['parentNodeCode', 'state'], drop=False, inplace=True)
print (treeDf)
i = 0
nodeCode = 1
parentNodeCode = 0
currentNodeCode = 1
prevNodeCode = 0
state = ''
startTime = time.time()
for u in userAr:
    # 유저별 df
    uDf = df.loc[u].sort_values(by = 'seq_num', ascending=True)

    # 유저별 df 인덱스 초기화
    uDf.reset_index(drop=True, inplace=True)
    if i%1000 == 0 :
        print(i, ' ', state, time.time() - startTime)
    i = i+1
    #if i == 30 :break

    #print(uDf)
    prevNodeCode = 0
    currentNodeCode = 1

    #print(u)
    #print(prevNodeCode, currentNodeCode)
    #print (u, 'start ')
    arState = uDf['state']
    #print(arState[0])

    for j in range (0, len(uDf)):
        #print ('uj:' , u, j, prevNodeCode, currentNodeCode)
        #if uDf.loc[j]['feature_name'] != 'funnel_dummy':

        state = arState[j]

        # print (j, state)
        # state 들어간 것을 찾는다.
        #pnc = treeDf.loc[(treeDf['parentNodeCode'] == prevNodeCode) & (treeDf['state'] == state)]
        try:
            pnc = treeDf.loc[(prevNodeCode, state)]
            currentNodeCode = (int(pnc['nodeCode']))
            #print('찾음', prevNodeCode, state)

        except KeyError: #없으면
            #print ('못찾음', prevNodeCode, state)
            #print (treeDf)
            nodeCode = nodeCode + 1
            #print (u, nodeCode, currentNodeCode, prevNodeCode, state)

            iDf = pd.DataFrame([(nodeCode, prevNodeCode, state)], columns=treeDf.columns, index=[(prevNodeCode, state)])
            treeDf = treeDf.append(iDf)
            currentNodeCode = nodeCode

        prevNodeCode = currentNodeCode
        #print(' ')
    # end of for j


# end of for u
print(treeDf)
