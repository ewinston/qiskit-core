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
controlled-u1 gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.cx import CnotGate


class Cu1Gate(ControlledGate):
    r"""Controlled-Z gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{Cu1}}(\lambda) =
            I \otimes |0 \rangle\!\langle 0| +
            U_{1}(\lambda) \otimes |1 \rangle\!\langle 1|
            =
            \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & 1 & 0 & 0 \\
                0 & 0 & 1 & 0 \\
                0 & 0 & 0 & e^{i \lambda}
            \end{bmatrix}
    """

    def __init__(self, theta, phase=0, label=None):
        """Create new cu1 gate."""
        super().__init__("cu1", 2, [theta], phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = U1Gate
        self.base_gate_name = "u1"

    def _define(self):
        """
        gate cu1(lambda) a,b
        { u1(lambda/2) a; cx a,b;
          u1(-lambda/2) b; cx a,b;
          u1(lambda/2) b;
        }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (U1Gate(self.params[0] / 2, phase=self.phase), [q[0]], []),
            (CnotGate(), [q[0], q[1]], []),
            (U1Gate(-self.params[0] / 2), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (U1Gate(self.params[0] / 2), [q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return Cu1Gate(-self.params[0], phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the Cu1 gate."""
        lam = float(self.params[0])
        return numpy.array([[1, 0, 0, 0],
                            [0, 1, 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, numpy.exp(1j * lam)]], dtype=complex)


def cu1(self, theta, ctl, tgt):
    """Apply cu1 from ctl to tgt with angle theta."""
    return self.append(Cu1Gate(theta), [ctl, tgt], [])


QuantumCircuit.cu1 = cu1
