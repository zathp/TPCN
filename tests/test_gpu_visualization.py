import pytest
import torch

from tpcn.signal_copy_distance.gpu_visualization import TorchSnapshotExporter
from tpcn.signal_copy_distance.model import DistanceSignalCopyNet
from tpcn.signal_copy_distance.space import make_contiguous_layout
from tpcn.visualization import ReferenceVisualizer, parse_snapshot


def _model(device: torch.device) -> DistanceSignalCopyNet:
    layout = make_contiguous_layout(n_neurons=3, input_width=1, output_width=1, virtual_distance=1, local_radius=1)
    return DistanceSignalCopyNet.from_layout(1, 0.5, layout, device=device)


def _run(device: torch.device, capture: bool) -> tuple[torch.Tensor, bytes | None]:
    torch.manual_seed(7)
    model = _model(device)
    hidden = torch.tensor([[0.25, -0.5, 0.75]], device=device)
    with torch.no_grad():
        result, _ = model.step(torch.tensor([[0.4]], device=device), hidden)
    record = TorchSnapshotExporter(enabled=capture).capture(
        model, result, timestamp=2.0, epoch=4, processed_events=(3, 4, 5)
    )
    return result, record


@pytest.mark.parametrize("device", [torch.device("cpu")])
def test_torch_records_round_trip_through_cpu_reference_parser(device: torch.device) -> None:
    _, record = _run(device, True)

    assert record is not None
    snapshot = parse_snapshot(record)
    assert tuple(item.neuron_id for item in snapshot.neurons) == ("n-0", "n-1", "n-2")
    assert snapshot.connections
    assert ReferenceVisualizer.load((record,)).frames()[0]["epoch"] == 4


@pytest.mark.skipif(not torch.cuda.is_available(), reason="CUDA is unavailable")
def test_cuda_records_have_cpu_semantics() -> None:
    cpu_result, cpu_record = _run(torch.device("cpu"), True)
    gpu_result, gpu_record = _run(torch.device("cuda"), True)

    assert cpu_record is not None and gpu_record is not None
    cpu_snapshot = parse_snapshot(cpu_record)
    gpu_snapshot = parse_snapshot(gpu_record)
    assert tuple(item.neuron_id for item in cpu_snapshot.neurons) == tuple(item.neuron_id for item in gpu_snapshot.neurons)
    assert cpu_snapshot.connections == gpu_snapshot.connections
    for cpu_neuron, gpu_neuron in zip(cpu_snapshot.neurons, gpu_snapshot.neurons):
        assert gpu_neuron.state == pytest.approx(cpu_neuron.state, rel=1e-5, abs=1e-6)
        assert gpu_neuron.activation == pytest.approx(cpu_neuron.activation, rel=1e-5, abs=1e-6)
    torch.testing.assert_close(gpu_result.cpu(), cpu_result, rtol=1e-5, atol=1e-6)


def test_capture_on_and_off_do_not_change_gpu_workload() -> None:
    without_capture, no_record = _run(torch.device("cpu"), False)
    with_capture, record = _run(torch.device("cpu"), True)

    assert no_record is None
    assert record is not None
    torch.testing.assert_close(with_capture, without_capture)


def test_periodic_capture_is_optional_and_ordered() -> None:
    model = _model(torch.device("cpu"))
    hidden = torch.ones(1, 3)
    exporter = TorchSnapshotExporter(interval=2)

    assert exporter.capture(model, hidden, timestamp=0.0, epoch=1) is None
    second = exporter.capture(model, hidden, timestamp=2.0, epoch=2)
    assert second is not None
    assert parse_snapshot(second).epoch == 2