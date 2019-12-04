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
Toffoli gate. Controlled-Controlled-X.
"""

import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.x import XGate
from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.t import TGate
from qiskit.extensions.standard.t import TdgGate


class ToffoliGate(ControlledGate):
    r"""Toffoli (Controlled-CNOT) gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CX}} =&
            I \otimes |0, 0 \rangle\!\langle 0, 0| +
            I \otimes |0, 1 \rangle\!\langle 0, 1| +
            I \otimes |1, 0 \rangle\!\langle 1, 0| +
            U_{\text{X}} \otimes |1, 1 \rangle\!\langle 1, 1| \\
            =&
            \begin{bmatrix}
                1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
                0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
                0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
                0 & 0 & 0 & 0 & 0 & 0 & 0 & 1 \\
                0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
                0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
                0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
                0 & 0 & 0 & 1 & 0 & 0 & 0 & 0
            \end{bmatrix}
    """
    def __init__(self,  phase=0, label=None):
        """Create new Toffoli gate."""
        super().__init__("ccx", 3, [],  phase=0, label=None,
                         num_ctrl_qubits=2)
        self.base_gate = XGate
        self.base_gate_name = "x"

    def _define(self):
        """
        gate ccx a,b,c
        {
        h c; cx b,c; tdg c; cx a,c;
        t c; cx b,c; tdg c; cx a,c;
        t b; t c; h c; cx a,b;
        t a; tdg b; cx a,b;}
        """
        q = QuantumRegister(3, "q")
        self.definition = [
            (HGate(phase=self.phase), [q[2]], []),
            (CnotGate(), [q[1], q[2]], []),
            (TdgGate(), [q[2]], []),
            (CnotGate(), [q[0], q[2]], []),
            (TGate(), [q[2]], []),
            (CnotGate(), [q[1], q[2]], []),
            (TdgGate(), [q[2]], []),
            (CnotGate(), [q[0], q[2]], []),
            (TGate(), [q[1]], []),
            (TGate(), [q[2]], []),
            (HGate(), [q[2]], []),
            (CnotGate(), [q[0], q[1]], []),
            (TGate(), [q[0]], []),
            (TdgGate(), [q[1]], []),
            (CnotGate(), [q[0], q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return ToffoliGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Toffoli gate."""
        return numpy.array([[1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1],
                            [0, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0]], dtype=complex)


def ccx(self, ctl1, ctl2, tgt):
    """Apply Toffoli to ctl1 and ctl2 to tgt."""
    return self.append(ToffoliGate(), [ctl1, ctl2, tgt], [])


QuantumCircuit.ccx = ccx
QuantumCircuit.toffoli = ccx
