TestCases (.tl) files is present under "tests" folder which is under "KachuaCore" folder. 

eqtest1.tl, eqtest2.tl represent 1st testcase.
eqtest3.tl, eqtest4.tl represent 2nd testcase.
eqtest5.tl, eqtest6.tl represent 3rd testcase.
eqtest7.tl, eqtest8.tl represent 4th testcase.
eqtest9.tl, eqtest10.tl represent 5th testcase.

to run a test case, create JSON file of first (.tl) file and paste its content in testData1.json, similarly create JSON 
file of second (.tl) file and paste its content under testData2.json. 

Then Run on cmd terminal using " python ..\Submission\symbSubmission.py -b optimized.kw -e['x','y','z'] " to see the outputs.

Json file is created using this command
" python ./kachua.py -t 100 -se tests/eqtest8.tl -d '{\":x\": 5, \":y\": 10, \":z\":10}' -c '{\":c1\": 1, \":c2\": 1, \":c4\": 1, \":c3\": 1}' "

screenshot of output of testcases are present under "outputs" folder which can be found under "tests" folder
