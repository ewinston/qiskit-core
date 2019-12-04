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
S=diag(1,i) Clifford phase gate or its inverse.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.qasm import pi
from qiskit.extensions.standard.u1 import U1Gate


class SGate(Gate):
    r"""S Clifford phase gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{S}}(\theta, \phi) =
            \begin{bmatrix}
                1 & 0 \\
                0 & i
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new S gate."""
        super().__init__("s", 1, [], phase=phase, label=label)

    def _define(self):
        """
        gate s a { u1(pi/2) a; }
        """
        q = QuantumRegister(1, "q")
        self.definition = [
            (U1Gate(pi / 2, phase=self.phase), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return SdgGate(phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the S gate."""
        return numpy.array([[1, 0],
                            [0, 1j]], dtype=complex)


class SdgGate(Gate):
    r"""Sdg Clifford adjoint phase gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{S}^\dagger} =
            \begin{bmatrix}
                1 & 0 \\
                0 & -i
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new Sdg gate."""
        super().__init__("sdg", 1, [], phase=phase, label=label)

    def _define(self):
        """
        gate sdg a { u1(-pi/2) a; }
        """
        q = QuantumRegister(1, "q")
        self.definition = [
            (U1Gate(-pi / 2, phase=self.phase), [q[0]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return SGate(phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the Sdg gate."""
        return numpy.array([[1, 0],
                            [0, -1j]], dtype=complex)


def s(self, q):  # pylint: disable=invalid-name
    """Apply S to q."""
    return self.append(SGate(), [q], [])


def sdg(self, q):
    """Apply Sdg to q."""
    return self.append(SdgGate(), [q], [])


QuantumCircuit.s = s
QuantumCircuit.sdg = sdg
