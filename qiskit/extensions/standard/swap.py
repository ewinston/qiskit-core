# -*- coding: utf-8 -*-

# This code is part of Qiskit.
#
# (C) Copyright IBM 2017.
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""
SWAP gate.
"""
import numpy

from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.u1 import U1Gate


class SwapGate(Gate):
    r"""SWAP gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{SWAP}}
            = \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & 0 & 1 & 0 \\
                0 & 1 & 0 & 0 \\
                0 & 0 & 0 & 1
            \end{bmatrix}
    """

    def __init__(self, phase_angle=0, label=None):
        """Create new SWAP gate."""
        super().__init__("swap", 2, [],
                         phase_angle=phase_angle, label=label)

    def _define(self):
        """
        gate swap a,b { cx a,b; cx b,a; cx a,b; }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (CnotGate(), [q[0], q[1]], []),
            (CnotGate(), [q[1], q[0]], []),
            (CnotGate(), [q[0], q[1]], [])
        ]
        # Temporary fix to add phase angle until we have added
        # them to controlled gates like CNOT.
        if self.phase_angle:
            self.definition.append(
                (U1Gate(0, phase_angle=self.phase_angle), [q[0]], []))

    def inverse(self):
        """Invert this gate."""
        return SwapGate(phase_angle=-self.phase_angle)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Swap gate."""
        return numpy.array([[1, 0, 0, 0],
                            [0, 0, 1, 0],
                            [0, 1, 0, 0],
                            [0, 0, 0, 1]], dtype=complex)


def swap(self, qubit1, qubit2):
    """Apply SWAP from qubit1 to qubit2."""
    return self.append(SwapGate(), [qubit1, qubit2], [])


QuantumCircuit.swap = swap
