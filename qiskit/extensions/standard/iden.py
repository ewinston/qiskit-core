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
Identity gate.
"""
import numpy
from qiskit.circuit import Gate
from qiskit.circuit import QuantumCircuit


class IdGate(Gate):
    r"""Identity gate.

    Identity gate corresponds to a single-qubit gate wait cycle,
    and should not be optimized or unrolled (it is an opaque gate).

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{I}} =
            \begin{bmatrix}
                1 & 0 \\
                0 & 1
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new Identity gate."""
        super().__init__("id", 1, [], phase=phase, label=label)

    def inverse(self):
        """Invert this gate."""
        return IdGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Id gate."""
        return numpy.array([[1, 0],
                            [0, 1]], dtype=complex)


def iden(self, q):
    """Apply Identity to q.

    Identity gate corresponds to a single-qubit gate wait cycle,
    and should not be optimized or unrolled (it is an opaque gate).
    """
    return self.append(IdGate(), [q], [])


QuantumCircuit.iden = iden
