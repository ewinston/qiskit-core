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
Rotation around the z-axis.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate


class RZGate(Gate):
    r"""rotation around the z-axis.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{RZ}}(\theta)
            = \exp\left(-i \frac{\theta}{2} \sigma_Z \right)
            = \begin{bmatrix}
                e^{-i \theta/2} & 0 \\
                0 & e^{i \theta/2}
            \end{bmatrix}
    """

    def __init__(self, phi, phase=0, label=None):
        """Create new rz single qubit gate."""
        super().__init__("rz", 1, [phi],
                         phase=phase, label=label)

    def _define(self):
        """
        gate rz(phi) a { u1(phi) a; }
        """
        q = QuantumRegister(1, "q")
        self.definition = [
            (U1Gate(self.params[0], phase=self.phase), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate.

        rz(phi)^dagger = rz(-phi)
        """
        return RZGate(-self.params[0], phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the RZ gate."""
        return numpy.array([[numpy.exp(-1j * self.params[0] / 2), 0],
                            [0, numpy.exp(1j * self.params[0] / 2)]],
                           dtype=complex)


def rz(self, phi, q):  # pylint: disable=invalid-name
    """Apply Rz to q."""
    return self.append(RZGate(phi), [q], [])


QuantumCircuit.rz = rz
