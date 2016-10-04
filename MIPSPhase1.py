#Stage One Outline
#Dennis John, Olaniyi Ominiwale & Nobert Kimario

from math import ceil
class BoolArray:
# a BoolArray object has as its main instance variable a
# variable length array of boolean constants


    def __init__(self,hexstr,n=32):
        """
        # convert the hextstring to a length n list of booleans
        # be careful of the order of indexing.
        # e.g., BoolArray("5C",8) should produce:
        # should accept either upper or lower case digits
        # [False, False, True,True,True,False,True,False]
        # i: 0      1      2    3   4     5    6     7
        """
        binary=bin(int(hexstr,16))[2:]
        binary=list(reversed(binary))
        self.boolVals=[]
        self.n=n

        for i in range(len(binary)):
            if binary[i]=="1":
                self.boolVals.append(True)
            else:
                self.boolVals.append(False)
        while len(self.boolVals)<n:
            self.boolVals.append(False)

    def __str__(self):
        """
        # __str__ is called when you 'print' a BoolArray object
        # it should return a string of 0's and 1's or T's and F's
        # in reverse order.  the example in the init returns:
        # either  01011000  or FTFTTFFF
       """
        
        t=self.boolVals[:]
        t.reverse()
        bitstring=""
        for i in range(len(t)):
            if t[i]:
                bitstring +="1"
            else:
                bitstring +="0"
                
        return bitstring

    def __len__(self):
        """
        # __len__ is called when you use the the built in len()
        # it should return the numbr of bits from the __init__
        """
        return len(self.boolVals)

    def toHex(self):
        """
        # return a string representing the current value in base 16
        # eg a string whose current barray is [True,False,False,True,False]
        #    should return "09"
        #    the number of hex digits should be len//4 rounded up
        """
        
        t=self.boolVals[:]
        t.reverse()
        
        string=str(self)
        
    
        string=hex(int(string,2))
        string=string[2:]

        d=ceil(self.n/4)-len(string)
        string=d*"0"+string
        return string 

    def __int__(self):
        """
        # converts the array to an integer
        # the example "5C" should return 92
        """
        return int(str(self),2)

    def subArray(self,left,rightplus):
        """
        # extracts a subarray of bits from indices left through rightplus
        # including left and upto but not including rightplus
        #  e.g.  getBits(7,10)  a BoolArray object with bits equal to
        #  bits 7 through 9 inclusive
        """
        lst=self.boolVals[:]
        
        sm=""
        for i in range(len(lst)):
            if lst[i]:
                sm+="1"
            else:
                sm+="0"
        newlst=sm[left:rightplus]
        newlst=newlst[::-1]
        final=hex(int(newlst,2))
        final=final[2:]

        return BoolArray(final,rightplus-left)

    def setBit(self,i,boolval):
        """
        # sets the ith bit of the array to the value boolval
        """
        self.boolVals[i]=boolval      

    def getBit(self,i):
        """
        # returns the ith bit of the array
        """
        return self.boolVals[i]
        
    def catHigh(self,barrayobj):
        """
        # returns a new BoolArray Object whose bits are those
        # of self with bits of barray concatenated on the high end.
        #partly courtsey of Wu & Nick
        """
        n=len(barrayobj)+len(self)
        ans=BoolArray("0",n)

        for i in range(len(self)):
            ans.setBit(i,self.getBit(i))
        for i in range(len(barrayobj)):
            k=len(self)+i
            ans.setBit(k,barrayobj.getBit(i))
        return ans

    

if __name__=="__main__":
    # students MAY NOT alter the code below without permission
    # until after stage one has been approved.
    # exception: you MAY add print statements for debugging purposes
    h1 = BoolArray("5C",8)
    h2 = BoolArray("3456ABCD",32)
    h3 = BoolArray("1F",5)
    # test __str__ 
    assert str(h1) in ["01011100","FTFTTTFF"]
    assert str(h2) in ["00110100010101101010101111001101",
                             "FFTTFTFFFTFTFTTFTFTFTFTTTTFFTTFT"]
    assert str(h3) in ["11111","TTTTT"]

    # test __len__
    assert len(h1)==8
    assert len(h2)==32
    assert len(h3)==5

    # test toHex
    assert h1.toHex() in ["5C","5c"]
    assert h2.toHex() in ["3456ABCD","3456abcd"]
    assert h3.toHex() in ["1F","1f"]

    # test __int__
    assert int(h1) == int("5C",16)
    assert int(h2) == int("3456ABCD",16)
    assert int(h3) == int("1F",16)

    # test setBit()
    h1.setBit(1,True)
    assert h1.toHex() in ["5E","5e"]

    # test subArray
    h4 =  h2.subArray(8,16)
    assert h4.toHex() in ["AB","ab"]

    # test getBit
    assert h3.getBit(1)
    assert not h1.getBit(7)

    # test catHigh()
    h5 = h3.catHigh(h1)
    assert len(h5) == 13
    assert h5.toHex() in ["0BDF","0bdf"]
    
    print("These tests passed!")
