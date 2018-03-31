"""
Example used in the README. In this example a Bell state is made.

Note: if you have only cloned the QISKit repository but not
used `pip install`, the examples only work from the root directory.
"""

# Import the QISKit
import qiskit

# Authenticate for access to remote backends
try:
    import Qconfig
    qiskit.api.register(token=Qconfig.APItoken)
except:
    print("""WARNING: There's no connection with the API for remote backends.
             Have you initialized a Qconfig.py file with your personal token?
             For now, there's only access to local simulator backends...""")

local_backends = qiskit.backends.local_backends()
remote_backends = qiskit.backends.remote_backends()

try:
    # Create a Quantum Register with 2 qubits.
    q = qiskit.QuantumRegister(2)
    # Create a Classical Register with 2 bits.
    c = qiskit.ClassicalRegister(2)
    # Create a Quantum Circuit
    qc = qiskit.QuantumCircuit(q, c)

    # Add a H gate on qubit 0, putting this qubit in superposition.
    qc.h(q[0])
    # Add a CX (CNOT) gate on control qubit 0 and target qubit 1, putting
    # the qubits in a Bell state.
    qc.cx(q[0], q[1])
    # Add a Measure gate to see the state.
    qc.measure(q, c)

    # See a list of available local simulators
    print("Local backends: ", qiskit.backends.local_backends())

    # Compile and run the Quantum circuit on a simulator backend
    sim_result = qiskit.execute(qc)

    # Show the results
    print("simulation: ", sim_result)
    print(sim_result.get_counts(qc))

    # Compile and run the Quantum Program on a real device backend
    if remote_backends:
        # see a list of available remote backends
        print("Remote backends: ", qiskit.backends.remote_backends())

        try:
            # select least busy available device and execute
            # this we should make a method to get the best backend
            device_status = [qiskit.backends.status(backend)
                             for backend in remote_backends if "simulator" not in backend]
            best_device = min([x for x in device_status if x['available'] is True],
                              key=lambda x: x['pending_jobs'])
            print("Running on current least busy device: ", best_device['backend'])

            my_backend = qiskit.backends.get_backend_instance(best_device['backend'])

            #runing the job
            compile_config = {
                'backend': best_device['backend'],
                'shots': 1024,
                'max_credits': 10
                }
            exp_result = qiskit.execute(qc, compile_config, wait=5, timeout=300)

            # Show the results
            print("experiment: ", exp_result)
            print(exp_result.get_counts(qc))
        except:
            print("All devices are currently unavailable.")

except qiskit.QISKitError as ex:
    print('There was an error in the circuit!. Error = {}'.format(ex))
