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
Pauli Z (phase-flip) gate.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u1 import U1Gate


class ZGate(Gate):
    r"""Pauli Z (phase-flip) gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{Z}} =
            \begin{bmatrix}
                1 & 0 \\
                0 & -1
            \end{bmatrix}
    """

    def __init__(self, phase_angle=0, label=None):
        """Create new Z gate."""
        super().__init__("z", 1, [], phase_angle=phase_angle, label=label)

    def _define(self):
        q = QuantumRegister(1, "q")
        self.definition = [
            (U1Gate(pi, phase_angle=self.phase_angle), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return ZGate(phase_angle=-self.phase_angle)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Z gate."""
        return numpy.array([[1, 0],
                            [0, -1]], dtype=complex)


def z(self, q):
    """Apply Z to q."""
    return self.append(ZGate(), [q], [])


QuantumCircuit.z = z
