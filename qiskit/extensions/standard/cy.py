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
controlled-Y gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.y import YGate
from qiskit.extensions.standard.s import SGate
from qiskit.extensions.standard.s import SdgGate
from qiskit.extensions.standard.cx import CnotGate


class CyGate(ControlledGate):
    r"""Controlled-Y gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CT}} =
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{Y}} \otimes |1 \rangle\!\langle 1|
            =
            \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & 0 & 0 & -i \\
                0 & 0 & 1 & 0 \\
                0 & i & 0 & 0
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new CY gate."""
        super().__init__("cy", 2, [],  phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = YGate
        self.base_gate_name = "y"

    def _define(self):
        """
        gate cy a,b { sdg b; cx a,b; s b; }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (SdgGate(phase=self.phase), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (SGate(), [q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return CyGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Cy gate."""
        return numpy.array([[1, 0, 0, 0],
                            [0, 0, 0, -1j],
                            [0, 0, 1, 0],
                            [0, 1j, 0, 0]], dtype=complex)


def cy(self, ctl, tgt):  # pylint: disable=invalid-name
    """Apply CY to circuit."""
    return self.append(CyGate(), [ctl, tgt], [])


QuantumCircuit.cy = cy
