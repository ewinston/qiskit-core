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
Diagonal single qubit gate.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u3 import U3Gate


class U1Gate(Gate):
    r"""Diagonal single-qubit gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_1(\lambda) = \begin{bmatrix}
            1 & 0 \\
            0 &  e^{i \lambda}
            \end{bmatrix}
    """

    def __init__(self, theta, phase_angle=0, label=None):
        """Create new diagonal single-qubit gate."""
        super().__init__("u1", 1, [theta],
                         phase_angle=phase_angle, label=label)

    def _define(self):
        q = QuantumRegister(1, "q")
        self.definition = [
            (U3Gate(0, 0, self.params[0], phase_angle=self.phase_angle),
             [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return U1Gate(-self.params[0], phase_angle=-self.phase_angle)

    def _matrix_definition(self):
        """Return a Numpy.array for the U3 gate."""
        lam = self.params[0]
        lam = float(lam)
        return numpy.array([[1, 0], [0, numpy.exp(1j * lam)]], dtype=complex)


def u1(self, theta, q):  # pylint: disable=invalid-name
    """Apply u1 with angle theta to q."""
    return self.append(U1Gate(theta), [q], [])


QuantumCircuit.u1 = u1
