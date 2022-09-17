
from orquestra.quantum.circuits._gates import GateOperation
from orquestra.quantum.circuits import CNOT, H, Circuit, X, Z
from icecream import ic
from orquestra.quantum.symbolic_simulator import SymbolicSimulator
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)


from PauliSandwichBackend import PauliSandwichBackend

bell_circuit = Circuit()
bell_circuit += H(0)
bell_circuit += CNOT(0, 1)

Array_circuit = Circuit()

Array_circuit += Z(1)
Array_circuit += Y(1)
Array_circuit += Z(1)
Array_circuit += Z(1)
Array_circuit += X(1)



sym_simulator = SymbolicSimulator()
num_samples = 1000
measurements2 = sym_simulator.run_circuit_and_measure(bell_circuit, num_samples)
ic(measurements2.get_counts())

qiskit_circuit = export_to_qiskit(bell_circuit)
qiskit_circuit.x(1)
from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

bell_circuit_X = import_from_qiskit(qiskit_circuit)

cirq_circuit = export_to_cirq(bell_circuit_X)
print(cirq_circuit)

sv_simulator = QiskitSimulator("aer_simulator_statevector")
wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
ic(wavefunction.amplitudes)

print('\n\n\n')

sym_simulator = SymbolicSimulator()

Circuit([])
tester=PauliSandwichBackend(GateOperation(bell_circuit.operations[0].gate, 0),bell_circuit.operations,sym_simulator)
measurements = tester.run_circuit_and_measure(bell_circuit,num_samples)
ic(measurements.get_counts())


qiskit_circuit = export_to_qiskit(bell_circuit)
qiskit_circuit.x(1)
from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

bell_circuit_X = import_from_qiskit(qiskit_circuit)
cirq_circuit = export_to_cirq(bell_circuit_X)
print(cirq_circuit)
sv_simulator = QiskitSimulator("aer_simulator_statevector")
wavefunction = sv_simulator.get_wavefunction(bell_circuit_X)
ic(wavefunction.amplitudes)




