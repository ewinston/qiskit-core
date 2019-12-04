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
controlled-NOT gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.extensions.standard.x import XGate


class CnotGate(ControlledGate):
    r"""Controlled-CNOT gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CX}} =
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{X}} \otimes |1 \rangle\!\langle 1|
            =
            \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & 0 & 0 & 1 \\
                0 & 0 & 1 & 0 \\
                0 & 1 & 0 & 0
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new CNOT gate."""
        super().__init__("cx", 2, [], phase=phase, label=label,
                         num_ctrl_qubits=1)
        self.base_gate = XGate
        self.base_gate_name = "x"

    def inverse(self):
        """Invert this gate."""
        return CnotGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Cx gate."""
        return numpy.array([[1, 0, 0, 0],
                            [0, 0, 0, 1],
                            [0, 0, 1, 0],
                            [0, 1, 0, 0]], dtype=complex)


def cx(self, ctl, tgt):  # pylint: disable=invalid-name
    """Apply CX from ctl to tgt."""
    return self.append(CnotGate(), [ctl, tgt], [])


QuantumCircuit.cx = cx
QuantumCircuit.cnot = cx
