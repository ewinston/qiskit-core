# This code is part of Qiskit.
#
# (C) Copyright IBM 2017, 2019
#
# This code is licensed under the Apache License, Version 2.0. You may
# obtain a copy of this license in the LICENSE.txt file in the root directory
# of this source tree or at http://www.apache.org/licenses/LICENSE-2.0.
#
# Any modifications or derivative works of this code must retain this
# copyright notice, and modified files need to carry a notice indicating
# that they have been altered from the originals.

"""Rotation around an axis in x-y plane."""

import math
import numpy
from scipy.spatial.transform import Rotation
from qiskit.qasm import pi
from qiskit.circuit.gate import Gate
from qiskit.circuit.parameterexpression import ParameterExpression
from qiskit.circuit.quantumregister import QuantumRegister


class RVGate(Gate):
    r"""Rotation around arbitrary rotation axis v where |v| is
    angle of rotation in radians.

    **Circuit symbol:**

    .. parsed-literal::

             ┌──────┐
        q_0: ┤ R(v) ├
             └──────┘

    **Matrix Representation:**

    .. math::

    \newcommand{\th}{|\vec{v}|}
    \newcommand{\sinc}{\text{sinc}}
        R(\vec{v}) = e^{-i \vec{v}\cdot\vec{\sigma}} =
            \begin{pmatrix}
                \cos{\th} -i v_z \sinc(\th) & -(i v_x + v_y) \sinc(\th) \\
                -(i v_x - v_y) \sinc(\th) & \cos(\th) + i v_z \sinc(\th)
            \end{pmatrix}
    """

    def __init__(self, v_x, v_y, v_z, seq='zxz'):
        """Create new rv single-qubit gate."""
        super().__init__('rv', 1, [v_x, v_y, v_z])
        if any([isinstance(param, ParameterExpression) for param in self.params]):
            pass  # TODO ignore
        else:
            self._rot = Rotation.from_rotvec(self.params)
        self.seq = seq.lower()

    def _define(self):
        """
        gate r(v).
        """
        # pylint: disable=cyclic-import
        from qiskit.circuit import QuantumCircuit, ParameterExpression
        qr = QuantumRegister(1, 'q')
        qc = QuantumCircuit(qr, name=self.name)
        
        if any([isinstance(param, ParameterExpression) for param in self.params]):
            if self.seq != 'zxz':
                raise NotImplementedError('the decomposition of parameter '
                                          'expressions only implmented for '
                                          'zxz decomposition')
            import sympy
            import numpy as np
            v0, v1, v2 = self.params
            norm = np.sqrt(v0**2 + v1**2 + v2**2)
            q0 = v0 / norm * np.sin(norm / 2)
            q1 = v1 / norm * np.sin(norm / 2)
            q2 = v2 / norm * np.sin(norm / 2)
            q3 = np.cos(norm / 2)
            θ = np.arctan2(2 * (q0*q1 + q2*q3), 1 - 2 * (q1**2 + q2**2))
            φ = np.arcsin(2 * (q0*q2 - q3*q1))
            ψ = np.arctan2(2 * (q0*q3 + q1*q2), 1 - 2 * (q2**2 + q3*2))
            qc.rz(θ, 0)
            qc.rx(φ, 0)
            qc.rz(ψ, 0)
        else:
            self._rot = Rotation.from_rotvec(self.params)
            euler = self._rot.as_euler(self.seq)
            for iaxis in range(3):
                if euler[iaxis]:
                    getattr(qc, 'r' + self.seq[iaxis])(euler[iaxis], qr[0])
        self.definition = qc

    def inverse(self):
        """Invert this gate."""
        v0, v1, v2 = self.params
        return RVGate(-v0, -v1, -v2, seq=self.seq)

    def to_matrix(self):
        """Return a numpy.array for the R(v) gate."""
        v = numpy.asarray(self.params, dtype=float)
        θ = numpy.sqrt(v.dot(v))
        nx, ny, nz = v / θ
        sin = numpy.sin(θ/2)
        cos = numpy.cos(θ/2)
        return numpy.array([[-1j * nz * sin + cos, (-ny - 1j*nx) * sin],
                            [(ny - 1j*nx) * sin, 1j * nz * sin + cos]])