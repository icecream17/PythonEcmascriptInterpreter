import sys
print('Not done yet!')
sys.exit(0)



import js_interpreter
import js_interpreter.test262


# If not finished, exit
if not js_interpreter.finished:
   print("not js_interpreter.finished")
   sys.exit(0)

if not js_interpreter.test262.finished:
   print("not js_interpreter.test262.finished")
   sys.exit(0)

# Otherwise...
# Github

import github

githubAPI = github.Github()
repo262 = githubAPI.get_repo("tc39/test262")
dirs = {
   "harness": repo262.get_content("harness"),
   "test": repo262.get_content("test")
}

# Constants

filesToEvaluateBeforehand = (
   dirs["harness"].get_content("sta.js"),
   dirs["harness"].get_content("assert.js"),
)

useStrictDirective = '"use strict";\n'
yamlTokenDelimiter = {
  "start": '/*---',
  "end": '---*/'
}

asyncPass = 'Test262:AsyncTestComplete'
asyncFailPrefix = 'Test262:AsyncTestFailure:'
asyncWaitTime = 10 # Seconds

hostCode = """
function $DONOTEVALUATE () {
   throw ReferenceError("Some code was evaluated. Expected not to evaluate this code")
}
"""

# Functions

import yaml
import time
import asyncio
import functools

def getTextOfFile (file):
   # Use utf-8 bc it's common and base64 only uses 64 chars anyway
   return file.decoded_content.decode('utf-8')

def isDirectory (file):
   return file.content_type == "dir"

def pathSuccess (path):
   print(f'Success! {path}')

def getIncludeText (path):
   return getTextOfFile(dirs["harness"].get_content(path))

def race (func1, func2):
   done_first, second = asyncio.new_event_loop().run_until_complete(
      asyncio.wait({func1(), func2()})
   )
   second.cancel()
   return done_first;

async def tooslow (seconds):
   await asyncio.sleep(seconds)
   raise TimeoutError("Code took way too long to finish")

async def asyncEval (realm, text):
   realm.evalulate(text)

def _innerRun (realm, text, isAsync, negative):
   # TODO: negative specificity
   # TODO: Replace Exception with something else
   starttime = time.time()

   try:
      if isAsync:
         race(
            functools.partial(asyncEval, realm, text),
            functools.partial(tooslow, asyncWaitTime)
         )
      else:
         realm.evaluate(text)
   except Exception as error:
      if isinstance(error, TimeoutError):
         return ("FAIL", error)
      if negative is not None:
         return "PASS"
      return ("FAIL", error)
   else:
      if negative is not None:
         return ("FAIL", Exception("Expected code to throw error but instead nothing happened"))
      return "PASS"
      

def runTest (text, path):
   yamlStartIndex = text.index(yamlTokenDelimiter["start"])
   yamlEndIndex = text.index(yamlTokenDelimiter["end"])
   yamlMetadataText = text[yamlStartIndex:yamlEndIndex]
   yamlMetadata = yaml.load(yamlMetadataText)
   
   flags = yamlMetadata.get("flags", [])
   realmMods = {
      "module": False,
      "async": False
   }
   withAddStrict = True
   withNoStrict = True
   raw = False
   negative = realmMods.get("negative")

   if "onlyStrict" in flags:
      withAddStrict = False
   elif "noStrict" in flags:
      withNoStrict = False

   if "module" in flags:
      withAddStrict = False
      realmMods["module"] = True

   if "raw" in flags:
      withAddStrict = False
      raw = True
   
   if "async" in flags:
      realmMods["async"] = True
  
   fileIncludes = yamlMetadata.get("includes", []) # List of paths

   realm = js_interpreter.test262.createRealm(realmMods)
   if negative is not None:
      if negative.get("phase") == "parse" and negative.get("type") == "ReferenceError":
         realm.evaluate(hostCode["Do not evaluate"])

   for file in filesToEvaluateBeforehand:
      realm.evaluate(getTextOfFile(file))

   if not raw:
      for file in fileIncludes:
         realm.evaluate(getIncludeText(file))
   
   assert _innerRun(realm, text, realmMods["async"], realmMods.get("negative")) == "PASS"

   if withAddStrict:
      realm = js_interpreter.test262.createRealm(realmMods)
      if negative is not None:
         if negative.get("phase") == "parse" and negative.get("type") == "ReferenceError":
            realm.evaluate(hostCode["Do not evaluate"])

      for file in filesToEvaluateBeforehand:
         realm.evaluate(getTextOfFile(file))
      
      if not raw:
         for file in fileIncludes:
            realm.evaluate(getIncludeText(file))

      assert _innerRun(realm, useStrictDirective + text, realmMods["async"], realmMods.get("negative")) == "PASS"


def runTestFile (file):
   runTest(getTextOfFile(file), file.path)

def searchTestDir (testDir):
   for content in testDir:
      if isDirectory(content):
         searchTestDir(content)
      elif file.path.endsWith("_FIXTURE.js"):
         continue
      else:
         runTestFile(content)

   pathSuccess(testDir.path)

for testDir in dirs["test"].get_content(""):
   searchTestDir(testDir, "test")



