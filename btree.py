import copy

class Node:
    def __init__(self, m):
        self.k = [None] * (m - 1)  # 키 값 리스트
        self.p = [None] * m   # 자식 노드로 가는 포인터를 모아둔 리스트. 분기의 수에 따라 self.key와 self.pointer의 크기가 정해짐
        self.n = 0          # (m / 2)-1 ≤ n ≤ m-1   m/2는의 나머지는 무조건 버림

    def __str__(self):
        return f"{self.k}"


class BTree:
    def __init__(self, m):
        self.root = None
        self.m = m

    def searchPath(self,node, m, key, stack = []):
        x = node
        i = 0
        
        while True:
            stack.append(x)
            while (i < x.n and key > x.k[i]):
                i += 1

            if (i < x.n and key == x.k[i]):
                return True, stack
            
            if x.p[i] is None:
                break

            x = x.p[i]
        return False, stack


    def insertKey(self, m, x, y, newKey):
        i = x.n - 1
        while (i >= 0 and newKey < x.k[i]):
            x.k[i + 1] = x.k[i]
            x.p[i + 2] = x.p[i + 1]
            i -= 1
        x.k[i + 1] = newKey
        x.p[i + 2] = y
        x.n += 1


    def splitNode(self, m, x, y, newKey):
        tempNode = Node(m + 1)
        
        temp2 = copy.deepcopy(x)

        for i in range(len(temp2.k)):
            tempNode.k[i] = temp2.k[i]
        for i in range(len(temp2.p)):
            temp2.p[i] = temp2.p
        tempNode.n = temp2.n

        self.insertKey(m, tempNode, y, newKey)
        # print(f"tempNode : {tempNode}")
        
        centerKey = tempNode.k[int(tempNode.n / 2)]
        # print(f"centerKey : {centerKey}")

        x.n = 0
        i = 0
        # x.k.clear()
        # x.p.clear()
        x.k = [None] * (m - 1)
        x.p = [None] * (m)
        while (tempNode.k[i] < centerKey):
            x.k[i] = tempNode.k[i]
            x.p[i] = tempNode.p[i]
            i += 1
            x.n += 1

        x.p[i] = tempNode.p[i]
        newNode = Node(m)
        i += 1
        # print(f"split_node_x : {x}")
        while (i < tempNode.n):
            newNode.k[newNode.n] = tempNode.k[i]
            newNode.p[newNode.n] = tempNode.p[i]
            i += 1
            newNode.n += 1
        newNode.p[newNode.n] = tempNode.p[i]

        return centerKey, newNode



    def deleteKey(self, m, x, oldKey):
        i = 0
        while oldKey > x.k[i]:
            i += 1

        while i < x.n:
            x.k[i] = x.k[i + 1]
            x.p[i + 1] = x.p[i + 2]
            i += 1
        x.n -= 1


    def bestSibling(self, m, x, y):
        i = 0
        while y.p[i] != x:
            i += 1

        if i == 0:
            return i + 1
        elif i == y.n:
            return i - 1
        elif y.p[i].n >= y.p[i + 1].n:
            return i - 1
        return i + 1


    def redistributeKeys(self, m, x, y, bestSib):
        i = 0
        while y.p[i] != x:
            i += 1

        bestNode = y.p[bestSib]
        if (bestSib < i):
            lastKey =bestNode.K[bestNode.n - 1]
            self.insertKey(m, x, None, y.K[i - 1])
            x.p[1] = x.p[0]
            x.p[0] <- bestNode.p[bestNode.n]
            bestNode.P[bestNode.n] = None
            self.deleteKey(m, bestNode, lastKey)
            y.K[i - 1] = lastKey
        else:
            firstKey = bestNode.k[0]
            self.insertKey(m, m, x, None, y.k[i])
            x.p[x.n] = bestNode.p[0]
            bestNode.p[0] = bestNode.p[1]
            self.deleteKey(m, bestNode, firstKey)
            y.k[i] = firstKey


    def mergeNode(self, m, x, y, bestSib):
        i = 0
        while y.p[i] != x:
            i += 1
        bestNode = y.p[bestSib]
        if bestSib > i:
            tmp = i
            i = bestSib
            bestSib = tmp
        bestNode.k[bestNode.n] = y.k[i - 1]
        bestNode.n += 1

        j = 0
        while j < x.n:
            bestNode.k[bestNode.n] = x.k[j]
            bestNode.p[bestNode.n] = x.p[j]
            bestNode.n += 1
            j += 1

        bestNode.p[bestNode.n] = x.p[x.n]
        self.deleteKey(m, y, y.k[i - 1])

    
    def insertBT(self, m, newKey):
        
        T = self.root
        if T is None:
            T = Node(m)
            T.k[0] = newKey
            T.n += 1
            self.root = T
            print(self.inorderBT(self.root))
            return

        found, stack = self.searchPath(self.root, m, newKey, [])

        if found:
            print(f"i {newKey} : The key already exists")
            return 

        finished = False

        x = stack.pop()
        # print(f"first pop : {x}, stack : {stack}")
        y = None
        # print(f"x is {x}, x.n : {x.n} , m-1 : {m-1}")
        
        while True:
            if x.n < m - 1:
                self.insertKey(m, x, y, newKey)
                finished = True
            else:
                newKey, newNode = self.splitNode(m, x, y, newKey)
                y = newNode
                # print(f"newKey : {newKey}, newNode : {newNode}")
                # print(f"stack : {stack}")
                if stack:
                    x = stack.pop()
                    # print(f"stack.pop : {x}")
                else:
                    # print(f"newKey : {newKey}, x : {x}, y : {y}")
                    T = Node(m)
                    T.k[0] = newKey
                    T.p[0] = x
                    T.p[1] = y
                    T.n = 1
                    
                    if x == self.root:
                        self.root = T
                    finished = True
            if finished:
                break

        # print(f"Root : {self.root}")
        self.inorderBT(self.root)
        # print()



    def deleteBT(self, m, oldKey):
        found, stack = self.searchPath(self.root, m, oldKey)
        if not found:
            print(f"d {oldKey} : The key does not exist")
            return

        x = stack.pop()
        y = None

        if x.p:
            internalNode = x
            i = x.index(oldKey)

            stack.append(x)
            self.searchPath(x.p[i + 1], m, x.k[i], stack)

            x = stack.pop()
            temp = internalNode.k[i]
            internalNode.k[i] = x.k[0]
            x.k[0] = temp

        finished = False
        self.deleteKey(m, x, oldKey)

        if stack:
            y = stack.pop()

        print(self.inorderBT(self.root))


        while True:
            if (self.root == x or x.n >= (m - 1) / 2):
                finished = True
            else:
                bestSib = self.bestSibling(m, x, y)

                if (y.p[bestSib].n > (m - 1) / 2):
                    self.redistributeKeys(m, x, y, bestSib)
                    finished = True
                else:
                    self.mergeNode(m, x, y, bestSib)
                    x = y
                    if stack:
                        y = stack.pop()
                    else:
                        finished = True
            
            if not finished:
                break
        if (y is not None and y.n == 0):
            self.root = y.p[0]


    def inorderBT(self, node):
        for i in range(node.n):
            print(f"node.p[i] : {node.p[i]}, node.k[i] : {node.k[i]}")
            if node.p[i]:
                self.inorderBT(node.p[i])
                if node.k[i]:
                    print(node.k[i], end = " ")
            else:
                for j in node.k:
                    if j:
                        print(j, end = " ")


m = 3
BT = BTree(m)
input_list = []



