import os
import subprocess
import streamlit as st
from streamlit.components.v1 import html

# Default jobs directory
jobs_directory = "jobs"

def list_jobs(path):
    """List all C files in the jobs directory."""
    try:
        return [f for f in os.listdir(path) if f.endswith('.c')]
    except FileNotFoundError:
        return []

def compile_program(program_path):
    """Compile the given C program."""
    compile_command = f"gcc {program_path} -o {program_path[:-2]}"
    result = subprocess.run(compile_command, shell=True, text=True, capture_output=True)
    return result

def run_program(program_path):
    """Run the compiled program."""
    executable = program_path[:-2]
    if os.path.exists(executable):
        result = subprocess.run([f"./{executable}"], text=True, capture_output=True)
        return result
    else:
        return None

def compile_and_run_all(path):
    """Compile and run all C programs in the directory."""
    results = []
    jobs = list_jobs(path)
    for job in jobs:
        job_path = os.path.join(path, job)
        compile_result = compile_program(job_path)
        if compile_result.returncode == 0:
            run_result = run_program(job_path)
            results.append((job, "Success", run_result.stdout if run_result else "Execution error"))
        else:
            results.append((job, "Compilation failed", compile_result.stderr))
    return results

# Streamlit App
# Custom CSS styling
st.markdown(
    """
    <style>
    body {
        background-color: white;
        color: green;
    }
    .stButton > button {
        background-color: green;
        color: white;
        border: 2px solid green;
        border-radius: 5px;
    }
    .stButton > button:hover {
        background-color: red;
        color: white;
        border: 2px solid red;
    }
    .stTextInput > div > input {
        border: 2px solid green;
        border-radius: 5px;
        color: black;
        background-color: white;
    }
    .stTextInput > div > input:focus {
        border: 2px solid red;
    }
    .stSelectbox > div > div {
        border: 2px solid green;
        border-radius: 5px;
        background-color: white;
        color: green;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("C-Batch OS Simulator")

# Directory Selector
st.sidebar.header("Configuration")
custom_directory = st.sidebar.text_input("Set Jobs Directory", jobs_directory)
if os.path.isdir(custom_directory):
    jobs_directory = custom_directory
else:
    st.sidebar.error("Invalid directory path. Falling back to default.")

# Main Options
option = st.sidebar.selectbox(
    "Choose an Option:",
    ["List Jobs", "Compile and Run Specific Job", "Compile and Run All Jobs", "Help"]
)

# List Jobs
if option == "List Jobs":
    st.header("Available Jobs")
    jobs = list_jobs(jobs_directory)
    if jobs:
        st.write("Jobs in directory:")
        st.write("\n".join(jobs))
    else:
        st.warning("No jobs found in the specified directory.")

# Compile and Run Specific Job
elif option == "Compile and Run Specific Job":
    st.header("Compile and Run Specific Job")
    jobs = list_jobs(jobs_directory)
    if jobs:
        selected_job = st.selectbox("Select a Job", jobs)
        if st.button("Compile and Run"):
            job_path = os.path.join(jobs_directory, selected_job)
            compile_result = compile_program(job_path)
            if compile_result.returncode == 0:
                st.success("Compilation Successful")
                run_result = run_program(job_path)
                if run_result and run_result.returncode == 0:
                    st.text_area("Program Output:", run_result.stdout)
                else:
                    st.error("Error during execution.")
            else:
                st.error(f"Compilation Failed:\n{compile_result.stderr}")
    else:
        st.warning("No jobs available to compile and run.")

# Compile and Run All Jobs
elif option == "Compile and Run All Jobs":
    st.header("Compile and Run All Jobs")
    results = compile_and_run_all(jobs_directory)
    if results:
        for job, status, output in results:
            st.subheader(f"{job}: {status}")
            if status == "Success":
                st.text_area(f"Output for {job}", output)
            else:
                st.error(output)
    else:
        st.warning("No jobs available to compile and run.")

# Help
elif option == "Help":
    st.header("Help")
    st.write("""
    **C-Batch OS Simulator Help**
    - **List Jobs:** Displays all C programs available in the jobs directory.
    - **Compile and Run Specific Job:** Select and run a specific C program.
    - **Compile and Run All Jobs:** Compile and execute all C programs in the jobs directory.
    - **Set Jobs Directory:** Change the directory containing your C programs.
    """)
