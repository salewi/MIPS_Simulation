# Unit Test for the TestCombinationalCircuits class

import unittest              # import unittesting

from MIPSPhase1    import BoolArray
from MIPSphase2 import CombinationalCircuits   # import your stage two class
from stage3outline  import RegisterFile,Memory


class TestUnitClass3(unittest.TestCase):

   def setUp(self):
      self.regs = RegisterFile()
      self.mem  = Memory()
    
   def testRFinit(self):
      for i in range(32):
         r = self.regs.getReg(i)
         self.assertEqual(type(r),type(BoolArray("0")))
         self.assertEqual(len(r),32)
         if i != 29:
            self.assertEqual(int(r),0)
         else:
            self.assertEqual(int(r),int("3e0",16))
            
   def testRFreadCyc(self):
      rs,rt,rd = 5,29,8
      a,b = self.regs.readCycle(rs,rt,rd)
      self.assertEqual(int(a),0)
      self.assertEqual(int(b),int("3e0",16))
      
   def testRFwriteCycTrue(self):
      rs,rt,rd = 5,29,8
      a,b = self.regs.readCycle(rs,rt,rd)
      self.regs.writeCycle(True,BoolArray("BADDAD",32))
      x = self.regs.getReg(8)
      self.assertEqual(int(x),int("BADDAD",16))

   def testRFwriteCycFalse(self):
      rs,rt,rd = 5,29,8
      a,b = self.regs.readCycle(rs,rt,rd)
      self.regs.writeCycle(False,BoolArray("BADDAD",32))
      x = self.regs.getReg(8)
      print("reg8",int(x))
      self.assertEqual(int(x),0)

   def testMMinitlimit1(self):
      self.assertEqual(int(self.mem.instrCycle(BoolArray("3FC",32))),0)

   def testMMinitlimit2(self):
      with self.assertRaises(KeyError):
         self.mem.instrCycle(BoolArray("400",32))

   def testLoad(self):
      self.mem.loadProgram("addtwo.txt")
      self.assertEqual(int(self.mem.instrCycle(BoolArray("0",32))),
                       int("200607a5",16))
      self.assertEqual(int(self.mem.instrCycle(BoolArray("4",32))),
                       int("2007FFFF",16))
      self.assertEqual(int(self.mem.instrCycle(BoolArray("8",32))),
                       int("00C74020",16))
      self.assertEqual(int(self.mem.instrCycle(BoolArray("C",32))),
                       int("FC000000",16))
      self.assertEqual(int(self.mem.instrCycle(BoolArray("10",32))),
                       int("0",16))

   def testDataCycle(self):
      addr  = BoolArray("000000C4",32)  #196
      data  = BoolArray("00ADDFAD",32)
      other = BoolArray("000000DD",32)
      readval = self.mem.dataCycle(addr,data,True,False)
      self.assertEqual(int(readval),int("0",32))
      readval = self.mem.dataCycle(addr,data,False,True)
      readval = self.mem.dataCycle(addr,other,True,False)
      self.assertEqual(int(readval),int("ADDFAD",16))
      
   

if __name__ == "__main__":
    unittest.main()
