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
controlled-u3 gate.
"""
import numpy

from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.u3 import U3Gate
from qiskit.extensions.standard.cx import CnotGate


class Cu3Gate(ControlledGate):
    r"""Controlled-u3 gate.

    **Matrix Definition**

    The matrix for this gate is given by:

    .. math::

        U_{\text{CZ}} =
            I \otimes |0 \rangle\!\langle 0| +
            U_3(\theta, \phi, \lambda) \otimes |1 \rangle\!\langle 1|
            =
            \begin{bmatrix}
                1 & 0 & 0 & 0 \\
                0 & \cos(\theta / 2) & 0 & -e^{i\lambda}\sin(\theta / 2) \\
                0 & 0 & 1 & 0 \\
                0 & e^{i\phi}\sin(\theta / 2) & 0 & e^{i(\phi+\lambda)}\cos(\theta / 2)
            \end{bmatrix}
    """

    def __init__(self, theta, phi, lam, phase=0, label=None):
        """Create new cu3 gate."""
        super().__init__("cu3", 2, [theta, phi, lam], phase=0, label=None,
                         num_ctrl_qubits=1)
        self.base_gate = U3Gate
        self.base_gate_name = "u3"

    def _define(self):
        """
        gate cu3(theta,phi,lambda) c, t
        { u1((lambda+phi)/2) c;
          u1((lambda-phi)/2) t;
          cx c,t;
          u3(-theta/2,0,-(phi+lambda)/2) t;
          cx c,t;
          u3(theta/2,phi,0) t;
        }
        """
        q = QuantumRegister(2, "q")
        self.definition = [
            (U1Gate((self.params[2] + self.params[1]) / 2, phase=self.phase), [q[0]], []),
            (U1Gate((self.params[2] - self.params[1]) / 2), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (U3Gate(-self.params[0] / 2, 0, -(self.params[1] + self.params[2]) / 2), [q[1]], []),
            (CnotGate(), [q[0], q[1]], []),
            (U3Gate(self.params[0] / 2, self.params[1], 0), [q[1]], [])
        ]

    def inverse(self):
        """Invert this gate."""
        return Cu3Gate(-self.params[0], -self.params[2], -self.params[1],
                       phase=-self.phase)

    def _matrix_definition(self):
        """Return a Numpy.array for the Cu3 gate."""
        theta, phi, lam = self.params
        theta, phi, lam = float(theta), float(phi), float(lam)
        return numpy.array([[1, 0, 0, 0],
                            [0, numpy.cos(theta / 2),
                             0, -numpy.exp(1j * lam) * numpy.sin(theta / 2)],
                            [0, 0, 1, 0],
                            [0, numpy.exp(1j * phi) * numpy.sin(theta / 2),
                             0, numpy.exp(1j * (phi + lam)) * numpy.cos(theta / 2)]
                            ], dtype=complex)


def cu3(self, theta, phi, lam, ctl, tgt):
    """Apply cu3 from ctl to tgt with angle theta, phi, lam."""
    return self.append(Cu3Gate(theta, phi, lam), [ctl, tgt], [])


QuantumCircuit.cu3 = cu3
