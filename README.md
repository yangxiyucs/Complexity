# RestServicePython
Python Worker-Manager distributed system for calculating code complexity -- Gregory Penrose ID: 14316190

This python code requires a few dependecies in order to run, most notably Flask and Radon. 
If you do not currently have these installed on python you can add both of them via pip as so:
    
    pip install radon       # API for calculating code complexity
    
    pip install flask       # API for creating RESTful web application
    
    pip install requests    # handle GET, POST requests over http
    
    pip install pygit2      # API for pulling git repos and walking through commits

To run application, start the Manager. This will start the flask app and create the server on a locahost network with port 5000. Once the server is running spawn in Worker nodes, which will request work from the Manager. The Manager and Workers can be spawned in by running the code on an IDE such as PyCharm, or by executing in the terminal (ALWAYS start a Manager before starting any Workers).

To execute from command line run these commands:

    python ./Manager.py
    
    python ./Worker.py      # Multiple workers can be spawned, but each needs its own terminal to run in

Since my computer contains only a QuadCore Processor, I was only able to get to 4 Worker nodes (more could be added, but with a quad core only 4 processes were able to be computed concurrently so the decrease in runtime begins to level off after 4 workers) before overloading the processor. With the addition of each worker node, the runtime for calculating the complexity of each commit in a repo is considerably cut. The image belows helps in indicating the reduction of computation time with the addition of each worker.

![Results](https://github.com/Roughosing/RestServicePython/blob/master/CC_Results.png "Results")

Once the work has been distributed the Manager needs to be restarted in order to give any new workers additional work, as such each time the worker(s) complete their processes, the time taken for each n workers to complete the task was logged by the code, then graphed manually using Google sheets, rather than using pyplot. 

The results i.e. a list of the cyclomatic complexities for each .py file in the commit are sent back to the Manager using the POST request, these are then added to a list of all the other results computed by the workers.

N.B. The above graph indicating computation time for the n amount of workers was made prior to finalizing the and fixing the POST request of sending the results back to the Manager. Although as the POST request would take an equal amount of time for each worker, it would only scale the results and not alter their ratios, as such the graph is fine as is.

Post Script:

    - Costraints
        - For some reason around the 360-370th commit for the given repo, the code breaks on a SyntaxError caused by an unknown file which cannot be located, and subsequently cannot be fixed. As such I have implemented a constraint on the workers that they only ask for work up to the ~350th commit, after which they will terminate with the output "Process Terminated". 
        For the purpose of this assignment this seemed like a reasonable constraint, given more time, I could have explored a solution to solve this problem, but for what is requiredof my solution, 350 commits will suffice as enough for a meaningful analysis.
