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
controlled-H gate.
"""
import numpy as np

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.h import HGate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.t import TGate, TdgGate
from qiskit.extensions.standard.s import SGate, SdgGate


class CHGate(ControlledGate):
    r"""Controlled-Hadamard gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CH}} =
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{H}} \otimes |1 \rangle\!\langle 1|
            = \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & \frac{1}{\sqrt{2}} & 0 & \frac{1}{\sqrt{2}} \\
                0 & 0 & 1 & 0 \\
                0 & \frac{1}{\sqrt{2}} & 0 & -\frac{1}{\sqrt{2}}
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new CH gate."""
        super().__init__("ch", 2, [], phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = HGate
        self.base_gate_name = "h"

    def _define(self):
        """
        gate ch a,b {
            s b;
            h b;
            t b;
            cx a, b;
            tdg b;
            h b;
            sdg b;
        }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (SGate(phase=self.phase), [q[1]], []),
            (HGate(), [q[1]], []),
            (TGate(), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (TdgGate(), [q[1]], []),
            (HGate(), [q[1]], []),
            (SdgGate(), [q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return CHGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Ch gate."""
        return np.array([[1, 0, 0, 0],
                         [0, 1/np.sqrt(2), 0, 1/np.sqrt(2)],
                         [0, 0, 1, 0],
                         [0, 1/np.sqrt(2), 0, -1/np.sqrt(2)]], dtype=complex)


def ch(self, ctl, tgt):  # pylint: disable=invalid-name
    """Apply CH from ctl to tgt."""
    return self.append(CHGate(), [ctl, tgt], [])


QuantumCircuit.ch = ch
