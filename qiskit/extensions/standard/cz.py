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
controlled-Phase gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.z import ZGate


class CzGate(ControlledGate):
    r"""Controlled-Z gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CZ}} =
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{Z}} \otimes |1 \rangle\!\langle 1|
            =
            \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & 1 & 0 & 0 \\
                0 & 0 & 1 & 0 \\
                0 & 0 & 0 & -1
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new CZ gate."""
        super().__init__("cz", 2, [], phase=phase, label=label,
                         num_ctrl_qubits=1)
        self.base_gate = ZGate
        self.base_gate_name = "z"

    def _define(self):
        """
        gate cz a,b { h b; cx a,b; h b; }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (HGate(phase=self.phase), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (HGate(), [q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return CzGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Cz gate."""
        return numpy.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, -1]], dtype=complex)


def cz(self, ctl, tgt):  # pylint: disable=invalid-name
    """Apply CZ to circuit."""
    return self.append(CzGate(), [ctl, tgt], [])


QuantumCircuit.cz = cz
