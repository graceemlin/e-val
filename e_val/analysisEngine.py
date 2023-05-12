from subprocess import Popen, PIPE, STDOUT
from json import loads

class AnalysisEngine:
    def __init__(self, katagoPath, configPath, modelPath):
        self.queries = {}
        print("Starting Katago Analysis Engine")
        self.analysisProc = Popen([katagoPath, "analysis", "-config", configPath, "-model", modelPath], stdin=PIPE, stdout=PIPE, stderr=STDOUT, universal_newlines=True)
        while True:
            line = self.analysisProc.stdout.readline()
            print(line.rstrip())
            if "ready to begin handling requests" in line:
                break
        print("KataGo Analysis Engine online")

    def submitQuery(self, query):
        self.queries[query.id] = query
        data = query.toJson()
        #print(data)
        self.analysisProc.stdin.write(data)
        self.analysisProc.stdin.write("\n")
        self.analysisProc.stdin.flush()

    def pollResult(self):
        result = loads(self.analysisProc.stdout.readline())
        if result["id"] in self.queries:
            self.queries[result["id"]].setResult(result)
        return result