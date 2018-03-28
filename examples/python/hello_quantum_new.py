"""
Example used in the README. In this example a Bell state is made.

Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

# Import the QISKit SDK
import qiskit
# Import the IBMQ Experience API
from IBMQuantumExperience import IBMQuantumExperience

# Authenticate for access to remote backends
try:
    import Qconfig
    api = IBMQuantumExperience(token=Qconfig.APItoken,
                               config={'url': Qconfig.config['url']})
    remote_backends = qiskit.backends.discover_remote_backends(api)
except:
    print("""WARNING: There's no connection with IBMQuantumExperience servers.
             Have you initialized a Qconfig.py file with your personal token?
             For now, there's only access to local simulator backends...""")
local_backends = qiskit.backends.discover_local_backends()

try:
    # Create a Quantum Register called "qr" with 2 qubits.
    qr = qiskit.QuantumRegister("qr", 2)
    # Create a Classical Register called "cr" with 2 bits.
    cr = qiskit.ClassicalRegister("cr", 2)
    # Create a Quantum Circuit called involving "qr" and "cr"
    qc = qiskit.QuantumCircuit(qr, cr)

    # Add a H gate on qubit 0, putting this qubit in superposition.
    qc.h(qr[0])
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
    # the qubits in a Bell state.
    qc.cx(qr[0], qr[1])
    # Add a Measure gate to see the state.
    qc.measure(qr, cr)
 
    #setting up the backend
    print("(Local Backends)")
    for backend in local_backends:
        print(backend)
    my_backend = qiskit.backends.get_backend_instance('local_qasm_simulator')
    # ideally this should be 
    #my_backend = qiskit.backends.get_backend_instance(filter on local and qasm simulator)
    # backend methods that exsist are .config, .status .calibration and .run and .parameters
    # new method is .valid 

    #compiling the job
    qp = qiskit.QuantumProgram()
    qp.add_circuit("bell", qc)
    qobj = qp.compile("bell", backend='local_qasm_simulator', shots=1024, seed=1)
    q_job = qiskit.QuantumJob(qobj, preformatted=True)
    # I am not convince the q_job is the correct class i would make a qobj class
    # ideally this should be qobj = qiskit.compile([qc],config) or qobj = QuantumObject([qc]) then qobj.compile

    #runing the job
    sim_result = my_backend.run(q_job)
    #ideally this would be
    #job = my_backend.run(qobj)
    #job.status
    #sim_result=job.results
    # the job is a new object that runs when it does and i dont wait for it to finish and can get results later
    # other job methods are job.abort


    # Show the results
    print("simulation: ", sim_result)
    print(sim_result.get_counts("bell"))

    # Compile and run the Quantum Program on a real device backend
    if remote_backends:


        # see a list of available remote backends
        print("\n(Remote Backends)")
        for backend in remote_backends:
            exp_backend = qiskit.backends.get_backend_instance(backend)
            backend_status = exp_backend.status
            print(backend, backend_status)

        # select least busy available device and execute
        device_status = [api.backend_status(backend)
                         for backend in remote_backends if "simulator" not in backend]
        best_device = min([x for x in device_status if x['available']==True],
                          key=lambda x:x['pending_jobs'])
        print("Running on current least busy device: ", best_device['backend'])
        my_backend = qiskit.backends.get_backend_instance(best_device['backend'])
        # this gets replaced by 
        # my_backend = qiskit.backends.get_backend_instance(filter remote, device, smallest queue)

        #compiling the job
        qp = qiskit.QuantumProgram()
        qp.add_circuit("bell", qc)
        qobj = qp.compile("bell", backend=best_device['backend'], shots=1024, seed=1)
        wait = 5
        timeout = 300
        q_job = qiskit.QuantumJob(qobj, preformatted=True, resources={
                    'max_credits': qobj['config']['max_credits'], 'wait': wait,
                    'timeout': timeout})
        # I am not convince the q_job is the correct class i would make a qobj class
        # ideally this should be qobj = qiskit.compile([qc],config) or qobj = QuantumObject([qc]) then qobj.compile

        #runing the job
        exp_result = my_backend.run(q_job)
        #ideally this would be
        #job = my_backend.run(qobj)
        #job.status
        #sim_result=job.results
        # the job is a new object that runs when it does and i dont wait for it to finish and can get results later
        # other job methods are job.abort
        #job = my_backend.run(qobj)
        #job.status()
        #exp_result=job.results()

        # Show the results
        print("experiment: ", exp_result)
        print(exp_result.get_counts("bell"))

except qiskit.QISKitError as ex:
    print('There was an error in the circuit!. Error = {}'.format(ex))
