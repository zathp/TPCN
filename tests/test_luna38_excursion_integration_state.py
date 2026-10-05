from __future__ import annotations

import math

import pytest

from tpcn.excursion_neuron import (
    E1Config,
    E1EventBudgetExceeded,
    IntegrationConfig,
    MultiExcursionNeuron,
    SingleExcursionNeuron,
)
from tpcn.ir2 import neuron_from_ir2, neuron_to_ir2, neuron_to_ir2_e2
from tpcn.visualization import ExcursionNeuronRecord

CLASSES = (SingleExcursionNeuron, MultiExcursionNeuron)
B = tuple((float(t), 0.4) for t in (0, 2, 4, 6))


def stream(times, value):
    return tuple((float(t), value) for t in times)


def drive(cls, config, events, *, settle=True):
    neuron = cls("n", config=config)
    emissions = []
    for timestamp, value in events:
        emitted = neuron.process_pending(through=timestamp)
        while emitted is not None or neuron.pending_internal_event is not None and neuron.pending_internal_event.timestamp <= timestamp:
            if emitted is not None:
                emissions.append(emitted)
            emitted = neuron.process_pending(through=timestamp)
            if emitted is None:
                break
        neuron.receive_contribution(timestamp, value)
    if settle:
        for _ in range(500):
            if neuron.pending_internal_event is None:
                break
            emitted = neuron.process_pending()
            if emitted is not None:
                emissions.append(emitted)
        assert neuron.pending_internal_event is None
    return neuron, tuple(emissions)


def enabled(**kwargs):
    return E1Config(integration=IntegrationConfig(), **kwargs)


def zs(neuron):
    return [entry.z_post_discharge for entry in neuron.integration_trace]


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_a_isolated_weak_input(cls):
    neuron, emissions = drive(cls, enabled(), [(0.0, 0.4)], settle=False)
    assert emissions == ()
    assert neuron.integration_trace[0].z_after_input == 0.4
    neuron.receive_contribution(100.0, 0.0)
    assert abs(neuron.integration_state) < 1e-4
    assert abs(neuron.state) < 1e-4
    assert neuron.emissions == type(neuron.emissions)(maxlen=neuron.emissions.maxlen)


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_b_repeated_related_inputs_integrate_and_discharge(cls):
    neuron, emissions = drive(cls, enabled(), B)
    trace = neuron.integration_trace
    assert [e.z_after_input for e in trace[:3]] == pytest.approx([0.4, 0.727490, 0.995620], abs=1e-5)
    assert [e.discharge_amount for e in trace] == [0.0, 0.0, 0.0, 1.0]
    last = trace[3]
    assert last.timestamp == 6.0 and last.integrated
    assert last.x_post_discharge == pytest.approx(1.4625, abs=1e-4)
    assert last.z_post_discharge == pytest.approx(0.21514, abs=1e-5)
    assert last.classification == "integrated_discharge"
    assert len(emissions) == 1
    assert emissions[0].timestamp == 6.5 and emissions[0].payload > 0
    assert emissions[0].timestamp - last.timestamp > 0
    assert last.emission_id == emissions[0].event_id
    assert last.emission_timestamp == 6.5
    assert last.theta_e == 1.0 and last.theta_z == 1.0
    assert all(not e.crossed_theta_e for e in trace[:3]) and last.crossed_theta_e


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_b3_three_inputs_do_not_emit(cls):
    neuron, emissions = drive(cls, enabled(), B[:3])
    assert emissions == ()
    assert neuron.integration_trace[-1].z_after_input == pytest.approx(0.99562, abs=1e-5)
    disabled, _ = drive(cls, E1Config(), B[:3], settle=False)
    live, _ = drive(cls, enabled(), B[:3], settle=False)
    assert live.state == disabled.state


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_c10_and_c40_far_spacing_do_not_emit(cls):
    neuron, emissions = drive(cls, enabled(), stream((0, 10, 20, 30), 0.4))
    assert emissions == ()
    assert zs(neuron) == pytest.approx([0.4, 0.54715, 0.60129, 0.6212], abs=1e-4)
    neuron, emissions = drive(cls, enabled(), stream((0, 40, 80, 120), 0.4))
    assert emissions == ()
    assert max(zs(neuron)) <= 0.4075


@pytest.mark.parametrize("cls", CLASSES)
def test_temporal_selectivity_comparison(cls):
    counts = {
        spacing: len(drive(cls, enabled(), stream([i * spacing for i in range(4)], 0.4))[1])
        for spacing in (2, 10, 40)
    }
    assert counts == {2: 1, 10: 0, 40: 0}


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_d_strong_event_identical_to_disabled(cls):
    live, live_em = drive(cls, enabled(), [(0.0, 1.2)])
    base, base_em = drive(cls, E1Config(), [(0.0, 1.2)])
    assert len(live_em) == 1 and live_em == base_em
    assert live.integration_state == 0.0
    assert live.integration_trace[0].classification == "direct"
    assert not live.integration_trace[0].integrated
    assert base.integration_state is None and base.integration_trace == ()


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_f_negative_mirror(cls):
    pos, pos_em = drive(cls, enabled(), B)
    neg, neg_em = drive(cls, enabled(), stream((0, 2, 4, 6), -0.4))
    assert len(neg_em) == 1 and neg_em[0].timestamp == 6.5 and neg_em[0].payload < 0
    assert neg_em[0].payload == -pos_em[0].payload
    assert zs(neg) == pytest.approx([-z for z in zs(pos)])


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_g_bounds_and_conservation(cls):
    config = enabled()
    neuron, emissions = drive(cls, config, stream([3 * i for i in range(40)], 0.4))
    trace = neuron.integration_trace
    integration = config.integration
    assert len(trace) == 40
    assert all(abs(e.z_post_discharge) <= integration.z_max for e in trace)
    discharges = sum(1 for e in trace if e.discharge_amount != 0.0)
    assert discharges == len(emissions) >= 1
    assert discharges <= math.floor(40 * 0.4 * integration.kappa / integration.theta_Z)
    integrated_total = sum(e.input_value for e in trace if e.integrated)
    decayed = sum(
        trace[i - 1].z_post_discharge - trace[i].z_after_decay if i else 0.0
        for i in range(len(trace))
    )
    remaining = trace[-1].z_post_discharge
    assert integration.theta_Z * discharges == pytest.approx(integrated_total - decayed - remaining)
    input_times = {e.timestamp for e in trace}
    assert all(any(0.0 < em.timestamp - t <= 0.5 for t in input_times) for em in emissions)


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_h_disabled_control(cls):
    neuron, emissions = drive(cls, E1Config(), B)
    assert emissions == ()
    assert neuron.integration_state is None


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_i_opposite_sign_blocks_discharge(cls):
    neuron = cls("n", config=enabled(), initial_state=-0.6)
    neuron._z = 0.8
    neuron.receive_contribution(0.0, 0.3)
    entry = neuron.integration_trace[0]
    assert entry.z_after_input == pytest.approx(1.1)
    assert entry.discharge_amount == 0.0
    assert neuron.integration_state == pytest.approx(1.1)
    assert neuron.pending_internal_event is None


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_j_default_threshold_is_legacy(cls):
    assert E1Config().theta_e == 1.0 and E1Config().theta_E == 1.0
    assert E1Config().integration is None
    neuron, emissions = drive(cls, E1Config(), [(0.0, 1.2)])
    assert len(emissions) == 1 and emissions[0].timestamp == 0.5


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_k_raised_threshold_creates_no_new_emission(cls):
    raised = E1Config(theta_e=1.5, theta_hold=1.5, integration=IntegrationConfig(discharge_quantum=1.5))
    for events in (B, [(0.0, 1.2)]):
        neuron, emissions = drive(cls, raised, events)
        _, default = drive(cls, enabled(), events)
        assert emissions == ()
        assert {e.timestamp for e in emissions} <= {e.timestamp for e in default}
        assert neuron.integration_trace[-1].theta_e == 1.5
    neuron, _ = drive(cls, raised, B)
    assert zs(neuron)[:3] == pytest.approx([0.4, 0.727490, 0.995620], abs=1e-5)


@pytest.mark.parametrize("cls", CLASSES)
def test_fixture_l_lowered_threshold_separates_direct_from_integrated(cls):
    lowered = E1Config(theta_e=0.5, integration=IntegrationConfig())
    neuron, emissions = drive(cls, lowered, [(0.0, 0.6)])
    entry = neuron.integration_trace[0]
    assert len(emissions) == 1 and emissions[0].timestamp == 0.5
    assert entry.classification == "direct" and not entry.integrated
    assert entry.z_post_discharge == 0.0 and entry.discharge_amount == 0.0
    assert entry.theta_e == 0.5 and entry.crossed_theta_e
    assert neuron.integration_state == 0.0
    _, default = drive(cls, enabled(), [(0.0, 0.6)])
    assert default == ()
    neuron, emissions = drive(cls, lowered, B)
    trace = neuron.integration_trace
    assert len(emissions) == 1 and emissions[0].timestamp == 6.5
    assert [e.integrated for e in trace] == [True] * 4
    assert [e.classification for e in trace] == ["none", "none", "none", "integrated_discharge"]
    assert zs(neuron)[:3] == pytest.approx([0.4, 0.727490, 0.995620], abs=1e-5)
    assert trace[3].discharge_amount == 1.0 and trace[3].emission_id == emissions[0].event_id


@pytest.mark.parametrize("cls", CLASSES)
def test_neutral_attractor_without_input(cls):
    neuron, emissions = drive(cls, enabled(), B)
    count = len(emissions)
    neuron.process_pending(through=1000.0)
    neuron.receive_contribution(1000.0, 0.0)
    assert abs(neuron.state) < 1e-12 and abs(neuron.integration_state) < 1e-12
    assert len(neuron.emissions) == count
    neuron.receive_contribution(2000.0, 0.0)
    assert len(neuron.emissions) == count


@pytest.mark.parametrize("cls", CLASSES)
def test_deterministic_replay(cls):
    first, first_em = drive(cls, enabled(), stream([3 * i for i in range(20)], 0.4))
    second, second_em = drive(cls, enabled(), stream([3 * i for i in range(20)], 0.4))
    assert first_em == second_em
    assert first.integration_trace == second.integration_trace
    assert [e.event_id for e in first_em] == [e.event_id for e in second_em]


@pytest.mark.parametrize("cls", CLASSES)
def test_bounded_trace_and_budget(cls):
    config = E1Config(event_budget=3, integration=IntegrationConfig())
    neuron = cls("n", config=config)
    for t in range(3):
        neuron.receive_contribution(float(t * 40), 0.1)
    with pytest.raises(E1EventBudgetExceeded):
        neuron.receive_contribution(200.0, 0.1)
    assert len(neuron.integration_trace) <= config.event_budget


@pytest.mark.parametrize("cls", CLASSES)
def test_reset_clears_integration_state(cls):
    neuron, _ = drive(cls, enabled(), B)
    neuron.reset()
    assert neuron.integration_state == 0.0 and neuron.integration_trace == ()


def test_m_regime_with_zero_z_equals_disabled():
    live, live_em = drive(MultiExcursionNeuron, enabled(), [(0.0, 5.0)])
    base, base_em = drive(MultiExcursionNeuron, E1Config(), [(0.0, 5.0)])
    assert len(live_em) >= 1
    assert live_em == base_em
    assert live.state == base.state
    assert live.integration_state == 0.0


def test_integration_config_validation():
    IntegrationConfig()
    for kwargs in ({"decay_rate_z": 0.0}, {"input_gain": -1.0}, {"discharge_quantum": float("nan")},
                   {"z_max": float("inf")}, {"discharge_quantum": 5.0, "z_max": 4.0}):
        with pytest.raises((ValueError, TypeError)):
            IntegrationConfig(**kwargs)
    with pytest.raises(ValueError):
        E1Config(integration=IntegrationConfig(decay_rate_z=1.0))
    with pytest.raises(ValueError):
        E1Config(integration=IntegrationConfig(discharge_quantum=0.9, z_max=4.0))
    with pytest.raises(ValueError):
        E1Config(integration=IntegrationConfig(discharge_quantum=3.0))
    with pytest.raises(TypeError):
        E1Config(integration=object())
    with pytest.raises(ValueError):
        E1Config(theta_e=2.0, theta_hold=1.5)


def test_theta_e_is_not_auto_coupled_to_theta_z():
    config = E1Config(theta_e=0.5, integration=IntegrationConfig())
    assert config.theta_E == 0.5 and config.integration.theta_Z == 1.0


def test_ir2_and_tpcv_reject_integration_neurons_and_preserve_theta_e():
    config = enabled()
    with pytest.raises(ValueError):
        neuron_to_ir2(SingleExcursionNeuron("n", config=config))
    with pytest.raises(ValueError):
        neuron_to_ir2_e2(MultiExcursionNeuron("n", config=config))
    with pytest.raises(ValueError):
        ExcursionNeuronRecord.from_neuron(MultiExcursionNeuron("n", config=config))
    plain = SingleExcursionNeuron("n", config=E1Config(theta_e=0.75))
    restored = neuron_from_ir2(neuron_to_ir2(plain))
    assert restored.config.theta_e == 0.75 and restored.config.integration is None
