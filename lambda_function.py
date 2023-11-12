import sys
import subprocess
import io

def exec_python_code(code):
    #execute python code and capture the output
    original_stdout = sys.stdout
    sys.stdout = output_capture =io.StringIO() #redirect standard output to buffer

    try:
        exec(code) #use exec to capture the output
        print('not starting')
        output=output_capture.getvalue()
        print('out of the code',output)
        return output
    except Exception as e:
        return str(e)
    finally:
        sys.stdout = original_stdout

def exec_java_code(code):
    #execute java code and capture the output
    try:
        print('this is the code to be executed',code)
        #create a temporary file to store the code
        with open('/tmp/Main.java', 'w') as java_file:
            java_file.write(code)
        #compile the code
        compile_result=subprocess.run(['javac', '/tmp/Main.java'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print('compile result',compile_result.returncode)
        #if the code has compilation error, return the error message
        if compile_result.returncode != 0:
            return compile_result.stderr.decode()
        run_result=subprocess.run(['java', '-classpath', '/tmp', 'Main'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print
        return run_result.stdout.decode()
    except Exception as e:
        return str(e)

def exec_cpp_code(code):
    try:
        print('this is the code to be executed',code)
        #crate a temporary file to store the code
        with open('/tmp/Main.cpp', 'w') as cpp_file:
            cpp_file.write(code)

        #compile the code
        compile_result=subprocess.run(['g++', '/tmp/Main.cpp', '-o', '/tmp/temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print('compile result',compile_result.returncode)

        #if the code has compilation error, return the error message
        if compile_result.returncode != 0:
            return compile_result.stderr.decode()
        
        #run the code
        run_result=subprocess.run(['/tmp/temp'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        print('run result',run_result.returncode)
        return run_result.stdout.decode()
    except Exception as e:
        return str(e)

def handler(event, context):
    language=event.get('language', 'python')
    code=event.get('code', '')
    if language == 'python':
        result=exec_python_code(code)
    elif language == 'java':
        result=exec_java_code(code)
    elif language == 'cpp':
        result=exec_cpp_code(code)
    else :
        result="Invalid language"+language
    return {
        'statusCode': 200,
        'body': result  
    }