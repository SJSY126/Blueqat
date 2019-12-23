import warnings
from .qasm_parser_backend_generator import generate_backend

def _qasm_runner_cirq(qasm, shots=None, returns=None, **kwargs):
    if returns is None:
        returns = "cirq_result"
    elif returns not in ("cirq_result", 'draw'):
        raise ValueError("`returns` shall be None, 'draw', 'cirq_result' or '_exception'")

    import_error = None
    try:
        with warnings.catch_warnings():
            from cirq import Simulator
            from cirq.contrib.qasm_import import circuit_from_qasm
    except Exception as e:
        import_error = e

    if import_error:
        if returns == "_exception":
            return e
        if isinstance(import_error, ImportError):
            raise ImportError("Cannot import Cirq. To use this backend, please install qiskit." +
                              " `pip install Cirq`.")
        else:
            raise ValueError("Unknown error raised when importing Cirq. To get exception, " +
                             'run this backend with arg `returns="_exception"`')
    else:
        if returns == "_exception":
            return None
        cirq_circuit = circuit_from_qasm(qasm)
        if returns == "draw":
            return cirq_circuit
        if shots is None:
            shots = 1024
        simulator = cirq.Simulator()
        result = simulator.run(cirq_circuit, repetitions=shots, **kwargs)
        if returns == "cirq_result":
            return result
        return result

cirq_backend = generate_backend(_qasm_runner_cirq)
