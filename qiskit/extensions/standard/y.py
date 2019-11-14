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
Pauli Y (bit-phase-flip) gate.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumRegister
from qiskit.circuit import QuantumCircuit
from qiskit.qasm import pi
from qiskit.extensions.standard.u3 import U3Gate


class YGate(Gate):
    r"""Pauli Y (bit-phase-flip) gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{Z}} =
            \begin{bmatrix}
                0 & -i \\
                i & 0
            \end{bmatrix}
    """

    def __init__(self, phase_angle=0, label=None):
        """Create new Y gate."""
        super().__init__("y", 1, [], phase_angle=phase_angle, label=label)

    def _define(self):
        q = QuantumRegister(1, "q")
        self.definition = [
            (U3Gate(pi, pi/2, pi/2, phase_angle=self.phase_angle), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return YGate(phase_angle=-self.phase_angle)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Z gate."""
        return numpy.array([[0, -1j],
                            [1j, 0]], dtype=complex)


def y(self, q):
    """Apply Y to q."""
    return self.append(YGate(), [q], [])


QuantumCircuit.y = y
