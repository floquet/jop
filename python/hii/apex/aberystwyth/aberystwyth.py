import datetime  # timestamps
import subprocess
import os
import platform  # uname
import pwd
import sys


def run_apex(input_file=None, output_file=None):
    """
    Run the APEX executable with optional input/output files

    Parameters:
    -----------
    input_file : str, optional
        Path to input file
    output_file : str, optional
        Path to output file

    Returns:
    --------
    int
        Return code from executable
    str
        Output from executable
    """
    # Construct command
    cmd = ["./apex"]  # Basic command

    # Add input/output redirection if specified
    if input_file:
        cmd.extend(["<", input_file])
    if output_file:
        cmd.extend([">", output_file])

    try:
        # Run the executable
        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        return result.returncode, result.stdout

    except subprocess.CalledProcessError as e:
        print(f"Error running apex: {e}")
        print(f"Error output: {e.stderr}")
        return e.returncode, e.stderr

    except FileNotFoundError:
        print("Error: apex executable not found")
        return 1, "Executable not found"


def pr_provenance():
    print("\n", datetime.datetime.now())
    print("source:  %s/%s" % (os.getcwd(), os.path.basename(__file__)))
    print("user id:", pwd.getpwuid(os.getuid()).pw_name)
    print("platform info:")
    print("    platform: ", platform.platform())
    print("    uname:    ", platform.uname())
    # print( "    node:     ", platform.node( ) )
    # print( os.environ )
    print("version info:")
    print("    python:   %s" % sys.version)
    print("    platform:", platform.__version__)
    return


# Example usage
if __name__ == "__main__":
    # Check if executable exists
    if not os.path.exists("./apex"):
        print("Error: apex executable not found in current directory")
        sys.exit(1)

    # Run without input/output files
    print(f"Running Fortran executable apex")
    returncode, output = run_apex()
    print(f"Return code: {returncode}")
    print(f"Output:\n{output}")

    # Run with input/output files
    returncode, output = run_apex(input_file="input.dat", output_file="output.dat")

    print(f"Python execution complete")
    pr_provenance()
