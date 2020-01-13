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
Controlled-u1 gate.
"""
from qiskit.circuit import ControlledGate
from qiskit.circuit import QuantumCircuit
from qiskit.circuit import QuantumRegister
from qiskit.extensions.standard.u1 import U1Gate
from qiskit.extensions.standard.cx import CXGate


class CU1Meta(type):
    """
    Metaclass to ensure that Cu1 and CU1 are of the same type.
    Can be removed when Cu1Gate gets removed.
    """
    @classmethod
    def __instancecheck__(mcs, inst):
        return type(inst) in {CU1Gate, Cu1Gate}  # pylint: disable=unidiomatic-typecheck


class CU1Gate(ControlledGate, metaclass=CU1Meta):
    """The controlled-u1 gate."""

    def __init__(self, theta):
        """Create new cu1 gate."""
        super().__init__('cu1', 2, [theta], num_ctrl_qubits=1)
        self.base_gate = U1Gate
        self.base_gate_name = 'u1'

    def _define(self):
        """
        gate cu1(lambda) a,b
        { u1(lambda/2) a; cx a,b;
          u1(-lambda/2) b; cx a,b;
          u1(lambda/2) b;
        }
        """
        definition = []
        q = QuantumRegister(2, 'q')
        rule = [
            (U1Gate(self.params[0] / 2), [q[0]], []),
            (CXGate(), [q[0], q[1]], []),
            (U1Gate(-self.params[0] / 2), [q[1]], []),
            (CXGate(), [q[0], q[1]], []),
            (U1Gate(self.params[0] / 2), [q[1]], [])
        ]
        for inst in rule:
            definition.append(inst)
        self.definition = definition

    def inverse(self):
        """Invert this gate."""
        return CU1Gate(-self.params[0])


class Cu1Gate(CU1Gate, metaclass=CU1Meta):
    """
    Deprecated CU1Gate class.
    """
    def __init__(self, theta):
        import warnings
        warnings.warn('Cu1Gate is deprecated, use CU1Gate (uppercase) instead!', DeprecationWarning,
                      2)
        super().__init__(theta)


def cu1(self, theta, ctl, tgt):
    """Apply cu1 from ctl to tgt with angle theta."""
    return self.append(CU1Gate(theta), [ctl, tgt], [])


QuantumCircuit.cu1 = cu1
