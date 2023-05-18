from subprocess import Popen, PIPE, STDOUT
from json import loads
import glob

class AnalysisEngine:
    def __init__(self, katagoPath, configPath, modelPath):
        self.queries = {}
        if not modelPath:
            print("No model specified, trying to find valid model")
            katago_bin_candidates = glob.glob("./katago_bin/kata1-*.bin.gz")
            if len(katago_bin_candidates) > 0:
                modelPath = katago_bin_candidates[0]
            else:
                local_candidates = glob.glob("./kata1-*.bin.gz")
                if len(local_candidates)>0:
                    modelPath = local_candidates[0]
            if modelPath:
                print("Using", modelPath)
            else:
                raise Exception("No valid model specified or found")
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