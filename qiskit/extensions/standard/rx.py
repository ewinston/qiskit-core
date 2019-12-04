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
Rotation around the x-axis.
"""
import math
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.r import RGate


class RXGate(Gate):
    r"""rotation around the x-axis.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{RX}}(\theta)
            = \exp\left(-i \frac{\theta}{2} \sigma_X \right)
            = \begin{bmatrix}
                \cos(\theta / 2) & -i \sin(\theta / 2) \\
                -i \sin(\theta / 2) &  \cos(\theta / 2)
            \end{bmatrix}
    """

    def __init__(self, theta, phase=0, label=None):
        """Create new rx single qubit gate."""
        super().__init__("rx", 1, [theta],
                         phase=phase, label=label)

    def _define(self):
        """
        gate rx(theta) a {r(theta, 0) a;}
        """
        q = QuantumRegister(1, "q")
        self.definition = [
            (RGate(self.params[0], 0, phase=self.phase),
             [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate.

        rx(theta)^dagger = rx(-theta)
        """
        return RXGate(-self.params[0], phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the RX gate."""
        cos = math.cos(self.params[0] / 2)
        sin = math.sin(self.params[0] / 2)
        return numpy.array([[cos, -1j * sin],
                            [-1j * sin, cos]], dtype=complex)


def rx(self, theta, q):  # pylint: disable=invalid-name
    """Apply Rx to q."""
    return self.append(RXGate(theta), [q], [])


QuantumCircuit.rx = rx
