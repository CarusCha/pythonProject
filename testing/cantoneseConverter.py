import pandas as pd

def contains(list, filter):
    for x in list:
        if filter(x):
            return True
    return False


class Cantonese:
    tone = 6 # 성조
    vowelList = ['a', 'e', 'i', 'o', 'u']

    def yaleConverter(word):
        preWordList = []
        finalWord = ''

        for i, character in enumerate(word):
            try:
                intChar = int(character)
                try:
                    firstVowelIndex = preWordList.index(
                        next(x for x in preWordList if (contains(Cantonese.vowelList, lambda y: y == x))))
                    lastVowelIndex = len(preWordList) - (preWordList[::-1].index(
                        next(x for x in preWordList[::-1] if (contains(Cantonese.vowelList, lambda y: y == x))))) - 1
                    # print(firstVowelIndex)
                    # print(lastVowelIndex)

                    markedChar = Cantonese.addMark(preWordList[firstVowelIndex:lastVowelIndex + 1], intChar)
                    del preWordList[firstVowelIndex:lastVowelIndex + 1]
                    preWordList.insert(firstVowelIndex, markedChar)

                    finalWord += ''.join(preWordList)
                    preWordList = []
                except:
                    finalWord = ''.join(preWordList) + '`'
                    preWordList = []


            except:
                preWordList.append(character)
                if (len(word) - 1) == i:
                    finalWord += ''.join(preWordList)



        return finalWord




    def addMark(vowelList, num):
        markedVowel = ''
        try:
            if num == 1:
                if vowelList[0] == 'a':
                    markedVowel = 'ā'
                elif vowelList[0] == 'e':
                    markedVowel = 'ē'
                elif vowelList[0] == 'i':
                    markedVowel = 'ī'
                elif vowelList[0] == 'o':
                    markedVowel = 'ō'
                elif vowelList[0] == 'u':
                    markedVowel = 'ū'
            elif (num == 2) | (num == 5):
                if vowelList[0] == 'a':
                    markedVowel = 'á'
                elif vowelList[0] == 'e':
                    markedVowel = 'é'
                elif vowelList[0] == 'i':
                    markedVowel = 'í'
                elif vowelList[0] == 'o':
                    markedVowel = 'ó'
                elif vowelList[0] == 'u':
                    markedVowel = 'ú'
            elif (num == 3) | (num == 6):
                markedVowel = vowelList[0]

            elif num == 4:
                if vowelList[0] == 'a':
                    markedVowel = 'à'
                elif vowelList[0] == 'e':
                    markedVowel = 'è'
                elif vowelList[0] == 'i':
                    markedVowel = 'ì'
                elif vowelList[0] == 'o':
                    markedVowel = 'ò'
                elif vowelList[0] == 'u':
                    markedVowel = 'ù'
        except:
            pass


        otherVowels = ''.join(vowelList[1:len(vowelList)]) if len(vowelList) > 1 else ''
        return markedVowel + otherVowels + ('h' if (num == 5 or num == 6 or num == 4) else '')




print(Cantonese.yaleConverter('daat3, go3'))

dfs = pd.read_excel('/Users/carus/Downloads/cantonese.xlsx', sheet_name = 1)
dataList = dfs['Cantonese(Tone Numbers)'].values.tolist()

newList = []
for i, v in enumerate(dataList):
    newList.append(Cantonese.yaleConverter(v))

newDict = {'Cantonese(Tone Marks)':newList}
a = pd.DataFrame(newList)
writer = pd.ExcelWriter('/Users/carus/Downloads/cantonese_.xlsx', engine='xlsxwriter')
a.to_excel(writer, sheet_name='Sheet1')
writer.save()