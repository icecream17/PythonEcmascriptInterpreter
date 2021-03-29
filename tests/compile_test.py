# Add parent folder to path so that js_interpreter can be imported
import sys
sys.path.append('../')


try:
   import js_interpreter

   import js_interpreter.Algorithm
   import js_interpreter.Grammar
   import js_interpreter.Terms
   import js_interpreter.TypesAndValues

   import js_interpreter.errors
except Exception as error:
   assert False, error
else:
   assert True, "Everything compiled!"
