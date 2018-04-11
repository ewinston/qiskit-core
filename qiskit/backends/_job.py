from concurrent import futures
from futures import Futures
import logging
from qiskit._result import Result
from qiskit._qiskiterror import QISKitError
from qiskit._compiler import compile_circuit


logger = logging.getLogger(__name__)

class Job(Futures):
    def __init__(self):
        super().__init__(self)

    def cancel():
        
