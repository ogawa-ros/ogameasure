
class adios(object):

    def __init__(self, com):
        self.com = com
        pass

    def _set_att(self, no, value):
        self.com.open()
        self.com.send(att["att{0}_{1}dB".format(no, value).encode()])
        self.com.close()
        return

    def get_att1(self):
        self.com.open()
        self.com.send(off['level_off'.encode()])
        while True:
            try:
                temp = self.com.recv()
                if temp.find(':')==-1: continue
                else: pass
                #print temp
                break
            except communicator.CommunicatorTimeout:
                print('(error) att1')
                continue
            continue
        self.com.close()
        time.sleep(0.1)

        do1 = int(temp[-16])*1
        do2 = int(temp[-15])*2
        do3 = int(temp[-14])*4
        do4 = int(temp[-13])*8
        do5 = int(temp[-11])*16
        att1 = do1+do2+do3+do4+do5
        return att1

    def get_att2(self):
        self.com.open()
        self.com.send(off['level_off'.encode()])
        while True:
            try:
                temp = self.com.recv()
                if temp.find(':')==-1: continue
                else: pass
                break
            except communicator.CommunicatorTimeout:
                print('(error) att2')
                continue
            continue
        self.com.close()
        time.sleep(0.1)

        do6 = int(temp[-10])*1
        do7 = int(temp[-9])*2
        do8 = int(temp[-8])*4
        do9 = int(temp[-6])*8
        do10 = int(temp[-5])*16
        att2 = do6+do7+do8+do9+do10
        return att2
