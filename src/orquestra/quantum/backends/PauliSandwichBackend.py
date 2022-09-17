from orquestra.quantum.circuits._gates import GateOperation
from orquestra.quantum.circuits import CNOT, H, Circuit
from icecream import ic
from orquestra.integrations.qiskit.backend import QiskitBackend
from orquestra.quantum.api.backend import QuantumBackend
from orquestra.quantum.measurements import Measurements

class PauliSandwichBackend(QuantumBackend):   
    def __init__(self, U, bread_gates, inner_backend):
        # define attributes for U, bread_gates, and inner_backend
        self.U = U
        self.bread_gates = bread_gates
        self.inner_backend = inner_backend
        
    def run_circuit_and_measure(self, circuit, n_samples):
        data_qubit_indices = tuple(range(circuit.n_qubits))
        new_circuit = Circuit([])
        n_sandwiches = 0
        # create and run sandwiched circuit
        for operation in circuit.operations:
            # print("U: ",type(self.U))
            # print("Op: ",type(operation))
            if operation.gate is self.U.gate:
                # print("Sandwich U")
                for P in self.bread_gates:
                    # print("dagger: ",type(self.U.gate.dagger(*op_indices)))
                    n_sandwiches += 1
                    op_indices = operation.qubit_indices
                    control_qubit_index = circuit.n_qubits + n_sandwiches -1
                    controlled_P_qubits = (control_qubit_index,) + data_qubit_indices
                    # sandwich U between controlled operations
                    # breakpoint()
                    # Pprime = self.U.gate(*op_indices).lifted_matrix(control_qubit_index) * P.lifted_matrix(control_qubit_index) * self.U.gate.dagger(*op_indices).lifted_matrix(control_qubit_index)
                    new_circuit +=  self.U.gate.dagger(*op_indices)
                    new_circuit += P
                    new_circuit +=  self.U.gate(*op_indices)
                    new_circuit.to_unitary()
                    new_circuit += operation
            else:
                new_circuit += operation
            raw_meas = self.inner_backend.run_circuit_and_measure(new_circuit, n_samples)
            # eliminate runs in which an error was caught
            raw_counts = raw_meas.get_counts() # get dictionary of outputs
            sandwiched_counts = {}
            for key in raw_counts.keys():
                if "1" not in key[circuit.n_qubits:]:
                    sandwiched_counts[key[:circuit.n_qubits]] = raw_counts[key]
        return Measurements.from_counts(sandwiched_counts)