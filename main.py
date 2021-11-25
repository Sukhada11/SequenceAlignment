import datetime
class Solution:
    def __init__(self,fileName):
        self.file=fileName
        self.delta =30
        self.alpha={
            "{}_{}".format("A", "A"): 0,
            "{}_{}".format("A","C"):110,
            "{}_{}".format("A", "G"): 48,
            "{}_{}".format("A", "T"): 94,
            "{}_{}".format("C", "C"): 0,
             "{}_{}".format("C","A"):110,
            "{}_{}".format("C", "G"): 118,
            "{}_{}".format("C", "T"): 48,
            "{}_{}".format("G", "G"): 0,
            "{}_{}".format("G", "A"): 48,
            "{}_{}".format("G", "C"): 118,
            "{}_{}".format("G", "T"): 110,
            "{}_{}".format("T", "T"): 0,
            "{}_{}".format("T", "A"): 94,
            "{}_{}".format("T", "C"): 48,
            "{}_{}".format("T", "G"): 110}



    def readFile(self):
        f = open(self.file)
        lines = f.read().splitlines()
        str_idxs=[]
        for i,line in enumerate(lines):
            if line.isalpha():
                str_idxs.append(i)

        return [[lines[str_idxs[0]],lines[str_idxs[0]+1:str_idxs[1]]],[lines[str_idxs[1]],lines[str_idxs[1]+1:]]]

    def inputStringGenerator(self,obj):
        baseString = obj[0]
        operations = obj[1]
        debug=[]
        if not operations:
            return baseString,""
        for idx in operations:
            idx = int(idx)
            curr = baseString[:idx+1]+ baseString+ baseString[idx+1:]
            baseString = curr
            debug.append(baseString)
        return baseString,debug

    def matrixGenertaor(self,x,y):
        dp = []
        m=len(x)
        n=len(y)
        for i in range(m + 1):
            dp.append([0] * (n + 1))
        for i in range(m + 1):
            dp[i][0] = self.delta * i
        for i in range(n + 1):
            dp[0][i] = self.delta * i
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                    dp[i][j] = min(
                    dp[i][j - 1] + self.delta,
                    dp[i - 1][j] + self.delta,
                    dp[i - 1][j - 1] +self.alpha["{}_{}".format(x[i-1],y[j-1])])
        return dp

    def getLastCol(self,x,y):
        dp = self.matrixGenertaor(x, y)
        res = [row[-1] for row in dp]
        return res
    def advancedSolver(self,x,y):
         Z = ""
         W = ""

         if len(x) == 0:
             for i in range(1,len(y)):
                 Z = Z + '_'
                 W = W + y[i]
         elif len(y) == 0:
            for i in range(1,len(x)):
                 Z = Z + x[i]
                 W = W + '_'

         elif len(x) == 1 or len(y) == 1:
            Z, W = self.basicSolver(x,y)
         else:
            xmid = len(x) // 2
            scoreL = self.getLastCol(x[:xmid-1],y)
            scoreR = self.getLastCol(x[xmid:][::-1],y[::-1])
            scoreR = scoreR[::-1]
            #print(len(scoreR),len(scoreL))
            temp=[]
            for i in range(len(scoreL)):
                temp.append(scoreR[i]+scoreL[i])
            max_val = max(temp)
            index_max = temp.index(max_val)
            ymid = index_max

            Z1,W1  = self.advancedSolver(x[:xmid-1],y[:ymid-1])
            Z2,W2 = self.advancedSolver(x[xmid:],y[ymid:])
            Z=Z1+Z2
            W=W1+W2
         return Z,W


    def basicSolver(self,x,y):
        dp = self.matrixGenertaor(x,y)
        m = len(x)
        n = len(y)
        l= m + n
        i = m
        j = n
        xptr = l
        yptr = l
        xalligned=[""]*(l+1)
        yalligned =[""]*(l+1)
        while (i > 0 and j > 0):
            if (x[i - 1] == y[j - 1]):
                xalligned[xptr] = x[i - 1]
                yalligned[yptr] = y[j - 1]
                xptr -= 1
                yptr -= 1
                i -= 1
                j -= 1
            elif (dp[i - 1][j - 1] + self.alpha["{}_{}".format(x[i-1],y[j-1])]) == dp[i][j]:
                xalligned[xptr] = x[i - 1]
                yalligned[yptr] = y[j - 1]
                xptr -= 1
                yptr -= 1
                i -= 1
                j -= 1
            elif (dp[i - 1][j] + self.delta == dp[i][j]):
                xalligned[xptr] = x[i - 1]
                yalligned[yptr] = '_'
                xptr -= 1
                yptr -= 1
                i-=1

            elif (dp[i][j - 1] + self.delta == dp[i][j]):
                xalligned[xptr] = '_'
                yalligned[yptr] = y[j-1]
                xptr -= 1
                yptr -= 1
                j -= 1
        print(i,j)
        while (xptr > 0):
            if (i > 0):
                i-=1
                xalligned[xptr] = x[i]
            else :
                xalligned[xptr] = '_'
            if (j > 0):
                j -= 1
                yalligned[xptr] = y[j]
            else:
                yalligned[xptr] = '_'
            xptr -= 1

        id = 1
        for i in range(1,l,1):
             if (yalligned[i]=='_' and xalligned[i]!='_')or(yalligned[i]!='_' and xalligned[i]=='_')or (yalligned[i]!='_' and xalligned[i]!='_') :
                 id=i
                 break
        a=("".join(xalligned[id:]))
        b=("".join(yalligned[id:]))
        print(dp[-1][-1])
        return a,b

begin_time = datetime.datetime.now()
obj = Solution("ip.txt")
x=(obj.readFile())
str1,d1 = obj.inputStringGenerator(x[0])
str2,d2 = obj.inputStringGenerator(x[1])
print(str1,str2)
a,b = obj.basicSolver(str1,str2)
c,d = obj.advancedSolver(str1,str2)
print(a,b)
print(c,d)
print(datetime.datetime.now() - begin_time)