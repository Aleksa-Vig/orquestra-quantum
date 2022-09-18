
from cirq import measure
from orquestra.quantum.circuits._gates import GateOperation
from orquestra.quantum.circuits import CNOT, H, Circuit, X, Z, Y
from icecream import ic
from orquestra.quantum.symbolic_simulator import SymbolicSimulator
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.integrations.cirq.conversions._circuit_conversions import export_to_cirq

from orquestra.integrations.qiskit.conversions import (
    export_to_qiskit,
    import_from_qiskit,
)
import qiskit.providers.aer.noise as noise
from orquestra.integrations.qiskit.simulator import QiskitSimulator
from orquestra.quantum.circuits import CNOT, Circuit, X


from PauliSandwichBackend import PauliSandwichBackend

bell_circuit = Circuit([CNOT(0, 1), X(0), X(1), CNOT(1, 2)])

noise_model = noise.NoiseModel()
error = noise.depolarizing_error(0.1, 2)
noise_model.add_all_qubit_quantum_error(error, ["cx"])

qiskit_sim = QiskitSimulator(device_name="aer_simulator", noise_model=noise_model)
noisey_measurements = qiskit_sim.run_circuit_and_measure(bell_circuit, 1000)

Array_circuit = [Z(0),X(0),Z(0)]
for i in range(2):
    tester=PauliSandwichBackend(GateOperation(bell_circuit.operations[0].gate, i),Array_circuit, qiskit_sim)
measurements = tester.run_circuit_and_measure(bell_circuit,1000)

ic(noisey_measurements.get_counts())
ic(measurements.get_counts())
