1. sbflSubmission.py file is inside Submission folder.

2. Open command promt or terminal inside ChironCore folder and write following command ,

 command - python  ./chiron.py --SBFL ./example/sbfl5.tl --buggy ./example/Sbfl5_buggy.tl -vars '[\":x\", \":y\", \":z\",\":a\"]' --timeout 10 --ntests 20 --popsize 20 --cxpb 1.0 --mutpb 1.0 --ngen 20 --verbose True --popsize 100 --cxpb 1.0 --mutpb 1.0 --ngen 100 --verbose True

3. 5 test cases are given inside tests folder (or example folder) inside ChironCore folder, their outputs are present under Outputs folder
which is present under tests folder inside ChironCore folder

4. 5 testcases ( examples ) are given 
    1. sbfl1.tl 
      sbfl1_buggy.tl
    this test case takes :x,:y and :z as input.

    2. sbfl2.tl 
      sbfl2_buggy.tl
    this test case takes :x,:y and :z as input.

    3. sbfl3.tl 
     sbfl3_buggy.tl
    this test case takes :x,:y, and :z as input.

    4. sbfl4.tl 
     sbfl4_buggy.tl
    this test case takes :x,:y, and :z as input.


    5. sbfl5.tl 
     sbfl5_buggy.tl    
    this test case takes :x,:y, and :z as input.