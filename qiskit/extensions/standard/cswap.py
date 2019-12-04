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
Fredkin gate. Controlled-SWAP.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.cx import CnotGate
from qiskit.extensions.standard.ccx import ToffoliGate
from qiskit.extensions.standard.swap import SwapGate


class FredkinGate(ControlledGate):
    r"""Fredkin (Controlled-Swap) gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CSwap}} =&
            I \otimes |0 \rangle\!\langle 0| +
            U_{\text{Swap}} \otimes |1 \rangle\!\langle 1| \\
            =&
            \begin{bmatrix}
                1 & 0 & 0 & 0 & 0 & 0 & 0 & 0 \\
                0 & 1 & 0 & 0 & 0 & 0 & 0 & 0 \\
                0 & 0 & 1 & 0 & 0 & 0 & 0 & 0 \\
                0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 \\
                0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
                0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
                0 & 0 & 0 & 0 & 0 & 0 & 1 & 0 \\
                0 & 0 & 0 & 0 & 0 & 0 & 0 & 1
            \end{bmatrix}
    """

    def __init__(self, phase=0, label=None):
        """Create new Fredkin gate."""
        super().__init__("cswap", 3, [], phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = SwapGate
        self.base_gate_name = "swap"

    def _define(self):
        """
        gate cswap a,b,c
        { cx c,b;
          ccx a,b,c;
          cx c,b;
        }
        """
        q = QuantumRegister(3, "q")
        self.definition = [
            (CnotGate(phase=self.phase), [q[2], q[1]], []),
            (ToffoliGate(), [q[0], q[1], q[2]], []),
            (CnotGate(), [q[2], q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return FredkinGate(phase=-self.phase)  # self-inverse

    def _matrix_definition(self):
        """Return a Numpy.array for the Fredkin gate."""
        return numpy.array([[1, 0, 0, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 1]], dtype=complex)


def cswap(self, ctl, tgt1, tgt2):
    """Apply Fredkin to circuit."""
    return self.append(FredkinGate(), [ctl, tgt1, tgt2], [])


QuantumCircuit.cswap = cswap
QuantumCircuit.fredkin = cswap
