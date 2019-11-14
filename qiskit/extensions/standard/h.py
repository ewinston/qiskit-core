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
Hadamard gate.
"""
import numpy

from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u2 import U2Gate


class HGate(Gate):
    r"""Hadamard gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{H}} = \frac{1}{\sqrt{2}}
            \begin{bmatrix}
                1 & 1 \\
                1 & -1
            \end{bmatrix}
    """

    def __init__(self, phase_angle=0, label=None):
        """Create new Hadamard gate."""
        super().__init__("h", 1, [], phase_angle=phase_angle, label=label)

    def _define(self):
        """
        gate h a { u2(0,pi) a; }
        """
        q = QuantumRegister(1, "q")
        self.definition = [
            (U2Gate(0, pi, phase_angle=self.phase_angle), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return HGate(phase_angle=-self.phase_angle)  # self-inverse

    def to_matrix(self):
        """Return a Numpy.array for the H gate."""
        return numpy.array([[1, 1],
                            [1, -1]], dtype=complex) / numpy.sqrt(2)


def h(self, q):  # pylint: disable=invalid-name
    """Apply H to q."""
    return self.append(HGate(), [q], [])


QuantumCircuit.h = h
