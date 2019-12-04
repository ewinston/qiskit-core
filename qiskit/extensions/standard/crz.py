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
controlled-rz gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.rz import RZGate


class CrzGate(ControlledGate):
    r"""Controlled rotation around the z axis.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CRZ}}(\theta) =
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{RZ}}(\theta) \otimes |1 \rangle\!\langle 1|
            = \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & e^{-i \theta/2} & 0 & 0 \\
                0 & 0 & 1 & 0 \\
                0 & 0 & 0 & e^{i \theta/2}
            \end{bmatrix}
    """
    def __init__(self, theta, phase=0, label=None):
        """Create new crz gate."""
        super().__init__("crz", 2, [theta], phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = RZGate
        self.base_gate_name = "rz"

    def _define(self):
        """
        gate crz(lambda) a,b
        { u1(lambda/2) b; cx a,b;
          u1(-lambda/2) b; cx a,b;
        }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (U1Gate(self.params[0] / 2, phase=self.phase), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (U1Gate(-self.params[0] / 2), [q[1]], []),
            (CnotGate(), [q[0], q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return CrzGate(-self.params[0], phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the Controlled-Rz gate."""
        theta = float(self.params[0])
        return numpy.array([[1, 0, 0, 0],
                            [0, numpy.exp(-1j * theta / 2), 0, 0],
                            [0, 0, 1, 0],
                            [0, 0, 0, numpy.exp(1j * theta / 2)]], dtype=complex)


def crz(self, theta, ctl, tgt):
    """Apply crz from ctl to tgt with angle theta."""
    return self.append(CrzGate(theta), [ctl, tgt], [])


QuantumCircuit.crz = crz
