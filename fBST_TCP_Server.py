import socket


class Node:
    def __init__(self, data):
        self.CharAlphbet = data
        self.c_right = None
        self.c_left = None


def dataInsertion():
    root = Node('p')

    root.c_left = Node('h')
    root.c_left.c_left = Node('d')
    root.c_left.c_right = Node('l')
    root.c_left.c_left.c_left = Node('b')
    root.c_left.c_left.c_right = Node('f')
    root.c_left.c_right.c_left = Node('j')
    root.c_left.c_right.c_right = Node('n')
    root.c_left.c_left.c_left.c_left = Node('a')
    root.c_left.c_left.c_left.c_right = Node('c')
    root.c_left.c_left.c_right.c_left = Node('e')
    root.c_left.c_left.c_right.c_right = Node('g')

    root.c_left.c_right.c_left.c_left = Node('i')
    root.c_left.c_right.c_left.c_right = Node('k')
    root.c_left.c_right.c_right.c_left = Node('m')
    root.c_left.c_right.c_right.c_right = Node('o')

    root.c_right = Node('t')
    root.c_right.c_left = Node('r')

    root.c_right.c_right = Node('x')

    root.c_right.c_left.c_left = Node('q')
    root.c_right.c_left.c_right = Node('s')

    root.c_right.c_right.c_left = Node('v')
    root.c_right.c_right.c_right = Node('y')

    root.c_right.c_right.c_left.c_left = Node('u')
    root.c_right.c_right.c_left.c_right = Node('w')

    root.c_right.c_right.c_right.c_right = Node('z')
    return root


class LenghtBST:
    def __init__(self, data):
        self.data = data
        self.info = []
        self.infoPw = []
        #kzt
        self.infoAmount = []
        self.left = None
        self.right = None


def RootLengthTree():
    root = None
    list_length = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 29, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23,
                   25, 27, 30]
    length = len(list_length)
    print(length)

    for i in range(0, length):
        print("data", list_length[i])
        root = insert(root, list_length[i])
    return root


def insert(node, key):
    # Return a new node if the tree is empty
    if node is None:
        return LenghtBST(key)
    # Traverse to the right place and insert the node
    if key < node.data:
        node.left = insert(node.left, key)
    else:
        node.right = insert(node.right, key)

    return node


class TCPserver:
    def __init__(self):
        self.server_ip = 'localhost'
        self.server_port = 9998
        self.sock = None
        self.AlphaRoot = dataInsertion()
        self.RLTroot = RootLengthTree()
        if self.AlphaRoot:
            print('AlphaDatabase created!')
            self.inorderForAlpha(self.AlphaRoot)
            print('\n')
        if self.RLTroot:
            print('[+][+] Root lenght tree created')
            self.inorderForRLT(self.RLTroot)
            print('\n')

    def inorderForRLT(self, RLTroot):
        if RLTroot is not None:
            self.inorderForRLT(RLTroot.left)
            print(RLTroot.data, ' >', end=' ')
            self.inorderForRLT(RLTroot.right)

    def inorderForAlpha(self, AlphaRoot):
        if AlphaRoot is not None:
            self.inorderForAlpha(AlphaRoot.c_left)
            print(AlphaRoot.CharAlphbet, ' >', end=' ')
            self.inorderForAlpha(AlphaRoot.c_right)

    def main(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((self.server_ip, self.server_port))
        server.listen(1)
        print(f'[*] Listening on {self.server_ip}:{self.server_port} >:')
        while True:
            client, address = server.accept()
            print(f'[*] Accepted connection from {address[0]}:{address[1]}')
            self.handle_client(client)
    
    def handle_client(self, client):

        with client as self.sock:
            request = self.sock.recv(4096)
            client_sms = request.decode("utf-8")
            print(f'[*] Received:', client_sms)
            option, c_uname, c_pw,c_amount = client_sms.split(' ')
            if option == '1':
                print("This is for registration")
                print("Checking amount: ",c_amount)
                success = self.forRegistration(c_uname, c_pw,c_amount)
                print('Testing for ', success)
                if success == 'success':
                    data = '201' + ' ' + 'SuccessRegistration'+' '+'0'
                    data = bytes(data, 'utf-8')
                    self.sock.send(data)
                elif success == 'AlreadyExit':
                    data = '400' + ' ' + 'UsernameDuplicated'+' '+'0'
                    data = bytes(data, 'utf-8')
                    self.sock.send(data)

            elif option == '2':
                self.loginAlpha(c_uname, c_pw)

            elif option == '3':
                print('Transfer proceed!')
                # getAmount fun ko call ya mal
                receiverName = c_pw
                transferamount = int(c_amount)
                print("Checking transferamount: " ,transferamount ,type(transferamount))
                print("Checking senderName: ",c_uname,type(c_uname))
                uLength = len(c_uname)
                rLength = len(receiverName)
                senderAmount =  self.login_serachinRLTforAmount(self.RLTroot,uLength,c_uname)
                receiverAmount = self.login_serachinRLTforAmount(self.RLTroot ,rLength ,receiverName)
                #
                fsenderAmount = int(senderAmount) - transferamount
                freceiverAmount = int(receiverAmount) + transferamount
                print("Checking returning Amount: ",senderAmount,type(senderAmount))
                print("Checking returning receiver Amount: " ,receiverAmount ,type(receiverAmount))

                print("Checking final Sender Amount: " ,fsenderAmount ,type(fsenderAmount))
                print("Checking final receiver Amount: " ,freceiverAmount ,type(freceiverAmount))
                
                #for updating amount sender
                flag1,Amount = self.login_serachinRLTforUpdatingAmount(self.RLTroot ,uLength ,c_uname,fsenderAmount)
                if flag1:
                    print("Updating sender's amount from {} to {} : Successful!!!".format(senderAmount,Amount))

                # for updating amount receiver
                flag2,Amount = self.login_serachinRLTforUpdatingAmount(self.RLTroot ,rLength ,receiverName ,freceiverAmount)
                if flag2:
                    print("Updating receiver's amount from {} to {} : Successful!!!".format(receiverAmount,Amount))
                # client ko pyan post tr
                data = '301' + ' ' + 'Transfer_Transition_Successful!'+' '+'amount'
                data = bytes(data, "utf-8")
                self.sock.send(data)

            elif option == '4':
                print('Deposit proceed!')
                uLength = len(c_uname)
                depositAmount = int(c_amount)
                senderAmount = self.login_serachinRLTforAmount(self.RLTroot ,uLength ,c_uname)
                fsenderAmount = int(senderAmount) + depositAmount
                # for updating deposit amount sender
                flag1 ,Amount = self.login_serachinRLTforUpdatingAmount(self.RLTroot ,uLength ,c_uname ,fsenderAmount)
                if flag1 :
                    print("[***Deposit] Updating sender's amount from {} to {} : Successful!!!".format(senderAmount ,Amount))
                data = '302' + ' ' + 'Deposit_Transition_Successful!' + ' ' + 'amount'
                data = bytes(data ,"utf-8")
                self.sock.send(data)
            
            elif option == '5':
                print('Withdraw proceed!')
                uLength = len(c_uname)
                withdrawAmount = int(c_amount)
                senderAmount = self.login_serachinRLTforAmount(self.RLTroot ,uLength ,c_uname)
                fsenderAmount = int(senderAmount) - withdrawAmount
                # for updating deposit amount sender
                flag1 ,Amount = self.login_serachinRLTforUpdatingAmount(self.RLTroot ,uLength ,c_uname ,fsenderAmount)
                if flag1 :
                    print("[***Withdraw] Updating sender's amount from {} to {} : Successful!!!".format(senderAmount ,Amount))
                data = '303' + ' ' + 'Withdraw_Transition_Successful!' + ' ' + 'amount'
                data = bytes(data ,"utf-8")
                self.sock.send(data)
            
            elif option == '6':
                print('UpdateName proceed!')
                uLength = len(c_uname)
                newName = c_pw
                # for updating name
                flag = self.login_serachinRLTforUpdatingName(self.RLTroot,uLength,c_uname,newName)
                if flag :
                    print("[***UpdatingName] Updating sender's name from {} to {} : Successful!!!".format(c_uname ,newName))
                data = '304' + ' ' + 'Updating_Name_Successful!' + ' ' + 'amount'
                data = bytes(data ,"utf-8")
                self.sock.send(data)
                

# ______________________________________Transition process testing____________________________________________
#     def loginAlphaforAmount(self ,uname) :
#         uname = uname.lower( )
#         firstData = uname [0]
#         Length = len(uname)
#         self.login_SearchInAlphaforAmount(self.AlphaRoot ,uname ,firstData ,Length)
#
#     def login_SearchInAlphaforAmount(self, AlphaRoot, uname, firstData, Lenght):
#             alphaNo = ord(AlphaRoot.CharAlphbet)
#             firstNo = ord(firstData)
#             if AlphaRoot is None:
#                 print('Alpha root is empty cannot be proceed!in Login!')
#             if AlphaRoot.CharAlphbet == firstData:
#                 print("Alpha was found : ", AlphaRoot.CharAlphbet)
#                 self.login_serachinRLTforAmount(self.RLTroot, Lenght, uname)
#
#             elif alphaNo < firstNo:
#                 return self.login_SearchInAlphaforAmount(AlphaRoot.c_right, uname, firstData, Lenght)
#             elif alphaNo > firstNo:
#                 return self.login_SearchInAlphaforAmount(AlphaRoot.c_left, uname, firstData, Lenght)

    def login_serachinRLTforAmount(self, RLTroot, Length, uname):
            if RLTroot is None:
                print('RLT root is empty cannot be proceed! in Login!')
            if RLTroot.data == Length:
                print('from Login_searchinRLT:', RLTroot.data)
                InfoNameLength = len(RLTroot.info)
                Amount = None
                for i in range(0, InfoNameLength):
                    if RLTroot.info[i] == uname:
                        print("Amount Success for User:", RLTroot.infoAmount[i])
                        Amount = RLTroot.infoAmount[i]
                return Amount
                # return "1000"
                #         data = '200' + ' ' + RLTroot.info[i]
                #         data = bytes(data, 'utf-8')
                #
                #         self.sock.send(data)
                # data = '400' + ' ' + uname
                # data = bytes(data, 'utf-8')
                # self.sock.send(data)


            elif RLTroot.data < Length:
                return self.login_serachinRLTforAmount(RLTroot.right, Length, uname)
            elif RLTroot.data > Length:
                return self.login_serachinRLTforAmount(RLTroot.left, Length, uname)
        
    
    def login_serachinRLTforUpdatingAmount(self, RLTroot, Length, uname,amount):
            if RLTroot is None:
                print('RLT root is empty cannot be proceed! in Login!')
            if RLTroot.data == Length:
                print('from Login_searchinRLT:', RLTroot.data)
                InfoNameLength = len(RLTroot.info)
                Amount = None
                flag = None
                for i in range(0, InfoNameLength):
                    if RLTroot.info[i] == uname:
                        print("Amount Updating Success for User:", RLTroot.info[i])
                        RLTroot.infoAmount[i] = amount
                        Amount = RLTroot.infoAmount[i]
                        flag = True
                return flag,Amount
                # return "1000"
                #         data = '200' + ' ' + RLTroot.info[i]
                #         data = bytes(data, 'utf-8')
                #
                #         self.sock.send(data)
                # data = '400' + ' ' + uname
                # data = bytes(data, 'utf-8')
                # self.sock.send(data)


            elif RLTroot.data < Length:
                return self.login_serachinRLTforUpdatingAmount(RLTroot.right, Length, uname,amount)
            elif RLTroot.data > Length:
                return self.login_serachinRLTforUpdatingAmount(RLTroot.left, Length, uname,amount)


    
    def login_serachinRLTforUpdatingName(self, RLTroot, Length, uname,newName):
            if RLTroot is None:
                print('RLT root is empty cannot be proceed! in Login!')
            if RLTroot.data == Length:
                print('from Login_searchinRLT:', RLTroot.data)
                InfoNameLength = len(RLTroot.info)
                flag = None
                for i in range(0, InfoNameLength):
                    if RLTroot.info[i] == uname:
                        print("Amount Success for User:", RLTroot.infoAmount[i])
                        RLTroot.info[i] = newName
                        flag = True
                return flag
                # return "1000"
                #         data = '200' + ' ' + RLTroot.info[i]
                #         data = bytes(data, 'utf-8')
                #
                #         self.sock.send(data)
                # data = '400' + ' ' + uname
                # data = bytes(data, 'utf-8')
                # self.sock.send(data)


            elif RLTroot.data < Length:
                return self.login_serachinRLTforUpdatingName(RLTroot.right, Length, uname,newName)
            elif RLTroot.data > Length:
                return self.login_serachinRLTforUpdatingName(RLTroot.left, Length, uname,newName)
# ______________________________________Transition process testing ending____________________________________________

    def forRegistration(self ,uname ,pw ,amount) :
        uname = uname.lower( )
        firstData = uname [0]
    
        Length = len(uname)
        success = self.searchInAlpha(self.AlphaRoot ,uname ,firstData ,Length ,pw ,amount)
        print('for registartion function' ,success)
        return success

    def searchInAlpha(self ,AlphaRoot ,uname ,firstData ,Lenght ,pw ,amount) :
        success = None
        alphaNo = ord(AlphaRoot.CharAlphbet)
        firstNo = ord(firstData)
        if AlphaRoot is None :
            print('Alpha root is empty cannot be proceed!')
        if AlphaRoot.CharAlphbet == firstData :
            print("Alpha was found : " ,AlphaRoot.CharAlphbet)
            success = self.insertInRLT(self.RLTroot ,Lenght ,uname ,pw ,amount)
            print('Return from insertInRLT:' ,success)
            success = success
            return success
        elif alphaNo < firstNo :
            return self.searchInAlpha(AlphaRoot.c_right ,uname ,firstData ,Lenght ,pw ,amount)
        elif alphaNo > firstNo :
            return self.searchInAlpha(AlphaRoot.c_left ,uname ,firstData ,Lenght ,pw ,amount)

    def insertInRLT(self ,RLTroot ,Lenght ,uname ,pw ,amount) :
        flag = None
        if RLTroot is None :
            print('RLT root is empty cannot be proceed!')
        if RLTroot.data == Lenght :
            infoLength = len(RLTroot.info)
            if infoLength == 0 :
                print('for insertInRLT ' ,RLTroot.data)
                RLTroot.info.append(uname)
                RLTroot.infoPw.append(pw)
                RLTroot.infoAmount.append(amount)
                flag = 'success'
                print(flag)
                return flag
            else :
                for i in RLTroot.info :
                    if i == uname :
                        print("Already Exit!")
                        flag = 'AlreadyExit'
                        print(flag)
                        return flag
                RLTroot.info [infoLength].append(uname)
                RLTroot.infoPw [infoLength].append(pw)
                RLTroot.infoAmount [infoLength].append(amount)
                flag = 'success'
                print(flag)
                return flag
    
    
        elif RLTroot.data < Lenght :
            return self.insertInRLT(RLTroot.right ,Lenght ,uname ,pw ,amount)
        elif RLTroot.data > Lenght :
            return self.insertInRLT(RLTroot.left ,Lenght ,uname ,pw ,amount)

    def loginAlpha(self ,uname ,pw) :
        uname = uname.lower( )
        firstData = uname [0]
        Length = len(uname)
        self.login_SearchInAlpha(self.AlphaRoot ,uname ,firstData ,Length ,pw)

    def login_SearchInAlpha(self ,AlphaRoot ,uname ,firstData ,Lenght ,pw) :
        alphaNo = ord(AlphaRoot.CharAlphbet)
        firstNo = ord(firstData)
        if AlphaRoot is None :
            print('Alpha root is empty cannot be proceed!in Login!')
        if AlphaRoot.CharAlphbet == firstData :
            print("Alpha was found : " ,AlphaRoot.CharAlphbet)
            self.login_serachinRLT(self.RLTroot ,Lenght ,uname ,pw)
    
        elif alphaNo < firstNo :
            return self.login_SearchInAlpha(AlphaRoot.c_right ,uname ,firstData ,Lenght ,pw)
        elif alphaNo > firstNo :
            return self.login_SearchInAlpha(AlphaRoot.c_left ,uname ,firstData ,Lenght ,pw)

    def login_serachinRLT(self ,RLTroot ,Length ,uname ,pw) :
        if RLTroot is None :
            print('RLT root is empty cannot be proceed! in Login!')
        if RLTroot.data == Length :
            print('from Login_searchinRLT:' ,RLTroot.data)
            InfoNameLength = len(RLTroot.info)
            for i in range(0 ,InfoNameLength) :
                if RLTroot.info [i] == uname and RLTroot.infoPw [i] == pw :
                    print("Login Success for User:" ,RLTroot.info[i] + RLTroot.infoAmount[i])
                    data = '200' + ' ' + RLTroot.info [i] + ' ' + RLTroot.infoAmount [i]
                    data = bytes(data ,'utf-8')
                
                    self.sock.send(data)
            data = '400' + ' ' + uname
            data = bytes(data ,'utf-8')
            self.sock.send(data)
    
    
        elif RLTroot.data < Length :
            return self.login_serachinRLT(RLTroot.right ,Length ,uname ,pw)
        elif RLTroot.data > Length :
            return self.login_serachinRLT(RLTroot.left ,Length ,uname ,pw)

if __name__ == "__main__":
    tcpServer: TCPserver = TCPserver()
    tcpServer.main()