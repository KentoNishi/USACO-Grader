import os
import subprocess
import time
import sys
if(len(sys.argv) == 2):
    testInput = sys.argv[1]
else:
    print("Give the absolute path to your solution program (C++).")
    testInput = input("Solution path: ") or ""
if(testInput == ""):
    sys.exit()
solutionPath = os.path.abspath(testInput)
solutionPath = solutionPath.replace("\\", "/")
solutionPathWSL = (os.popen("wsl eval wslpath " +
                            solutionPath).read()).split()[0]
solutionPathParent = os.path.dirname(solutionPath)
solutionPathParentWSL = (
    os.popen("wsl eval wslpath "+solutionPathParent).read()).split()[0]
try:
    solutionFile = open(solutionPath, encoding="utf8").read()
except FileNotFoundError:
    sys.exit()
delim = "// Test case path: ["
try:
    if(solutionFile.index(delim) == 0):
        testInput = solutionFile[len(delim):solutionFile.index("]")]
except Exception:
    print("Test case folders can be downloaded from USACO's website.")
    print("After unzipping, get the path to the specific problem's test cases.")
    print("The given path should contain files with extensions \"in\" and \"out\".")
    testInput = input("Test case folder: ") or ""
if(testInput == ""):
    sys.exit()
testCasePath = os.path.abspath(testInput)


def test(testPath, answerPath):
    testPathWSL = (os.popen("wsl eval wslpath " +
                            testPath.replace("\\", "/")).read()).split()[0]
    executableLocation = solutionPathParentWSL+"/result"
    with open(os.path.join(solutionPathParent, os.path.basename(solutionPathParent)+".in"), "w") as inputFile:
        inputFile.write(open(testPath, "r").read())
        inputFile.close()
        os.popen("wsl eval \"cd "+solutionPathParentWSL +
                 ";" + executableLocation+"\"").read()
        answer = open(os.path.join(solutionPathParent, os.path.basename(
            solutionPathParent)+".out"), "r").read()
        file = open(answerPath, encoding="utf8").read()
        return (file == answer)


compiler = subprocess.Popen(
    "wsl eval g++ "+solutionPathWSL+" -g -o "+solutionPathParentWSL+"/result;")
compiler.wait()
correct = 0
incorrect = 0
try:
    for filename in os.listdir(testCasePath):
        testName = os.path.splitext(filename)[0]
        if(os.path.splitext(filename)[-1] == ".in"):
            testPath = os.path.join(testCasePath, testName+".in")
            answerPath = os.path.join(testCasePath, testName+".out")
            start = time.time()
            result = test(testPath, answerPath)
            execTime = time.time()-start
            if result:
                correct += 1
            else:
                incorrect += 1
            print(testName+" ("+format(execTime, '.3f') + "s"+")" +
                  ": "+("✅" if result else "❌"))
    print("Correct: "+str(correct)+", Incorrect: "+str(incorrect))
except Exception:
    pass
