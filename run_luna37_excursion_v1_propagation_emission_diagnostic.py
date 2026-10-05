"""Run the bounded Luna-37 EXCURSION_V1 propagation-to-emission mechanism diagnostic.

Luna-37 reuses the Luna-34 fixture, streams, bounds and per-character record
unchanged (read-only import). The only differences are the explicit finite
``eligibility_capacity=1024`` supplied through the reviewed Luna-36 runtime
API, bounded runner-local eligibility occupancy instrumentation, and the
Luna-37 terminal classifications.
"""

from __future__ import annotations

from contextlib import ExitStack
from pathlib import Path
import platform
import sys
from typing import Any, Callable
from unittest import mock

import run_luna34_excursion_v1_multi_emitter_bridge as base
from tpcn.eligibility import EligibilityCapacityError, EligibilityLedger
from tpcn.experiment_excursion_runtime import ExcursionCharacterRuntime
from tpcn.stroke_dataset import StrokePoint


EXECUTION_BASELINE = "905ee21343ef5a69770f49e40966a40bcc40b0f5"
CONDITIONS = base.CONDITIONS
ELIGIBILITY_CAPACITY = 1024
NAMESPACE = "luna37"
ARTIFACT_DIRECTORY = Path("artifacts/acp0007-luna37-propagation-emission-diagnostic")
SEEDS = (0, 1, 2, 3, 4)
_canonical_json = base._canonical_json
_digest = base._digest


class StopCondition(RuntimeError):
    """A predeclared Luna-37 stop condition; never retried."""

    def __init__(self, reason: str, detail: dict[str, Any]) -> None:
        super().__init__(reason)
        self.reason = reason
        self.detail = detail


def experiment_config() -> dict[str, Any]:
    config = base.experiment_config()
    config["schema"] = "TPCN-LUNA37-EXCURSION-V1-1"
    config.pop("api_baseline", None)
    config["execution_baseline"] = EXECUTION_BASELINE
    config["inherited_from"] = "run_luna34_excursion_v1_multi_emitter_bridge.py (unchanged fixture)"
    config["network"]["eligibility_capacity"] = {
        "value": ELIGIBILITY_CAPACITY,
        "scope": "per ledger, passed through ExcursionCharacterRuntime(eligibility_capacity=...)",
        "derivation": (
            "equals the declared per-character runtime_event_budget; one eligibility trace is "
            "created per canonical emission and each emission consumes at least one event"
        ),
        "tuned": False,
        "searched": False,
        "condition_or_seed_specific": False,
    }
    config["namespace"] = NAMESPACE
    config["stop_conditions"] = [
        "EligibilityCapacityError",
        "peak ledger occupancy equal to capacity",
        "any other production exception",
        "occupancy does not reconcile",
        "effective capacity differs from 1024",
        "nondeterministic replay",
    ]
    config["no_edge_contamination_is_classified_not_raised"] = True
    config["excluded_endpoints"] = list(config["excluded_endpoints"]) + [
        "structural growth, candidate formation as an endpoint, pruning, N3",
    ]
    return config


class _OccupancyAudit:
    def __init__(self) -> None:
        self.ledgers: list[EligibilityLedger] = []
        self.stats: dict[str, dict[str, Any]] = {}
        self.capacity_errors: list[dict[str, Any]] = []

    def register(self, ledger: EligibilityLedger) -> None:
        self.ledgers.append(ledger)
        self.stats[ledger.ledger_id] = {
            "ledger_id": ledger.ledger_id,
            "configured_capacity": ledger.max_traces,
            "initial_occupancy": len(ledger.traces),
            "created": 0,
            "removed": 0,
            "peak_occupancy": len(ledger.traces),
            "creation_trace_ids": [],
        }

    def observe(self, ledger: EligibilityLedger, call: Callable[[], Any], timestamp: float, trace_id: str | None) -> Any:
        before = {trace.trace_id for trace in ledger.traces}
        stats = self.stats[ledger.ledger_id]
        try:
            result = call()
        except EligibilityCapacityError:
            self.capacity_errors.append(
                {
                    "ledger_id": ledger.ledger_id,
                    "trace_id": trace_id,
                    "emission_index": stats["created"] + 1,
                    "timestamp": timestamp,
                    "occupancy": len(before),
                    "capacity": ledger.max_traces,
                }
            )
            raise
        after = {trace.trace_id for trace in ledger.traces}
        stats["created"] += len(after - before)
        stats["removed"] += len(before - after)
        stats["creation_trace_ids"].extend(sorted(after - before))
        stats["peak_occupancy"] = max(stats["peak_occupancy"], len(after))
        return result

    def finalize(self) -> list[dict[str, Any]]:
        records = []
        for ledger in self.ledgers:
            stats = dict(self.stats[ledger.ledger_id])
            stats["final_occupancy"] = len(ledger.traces)
            stats["reconciles"] = (
                stats["initial_occupancy"] + stats["created"] - stats["removed"]
                == stats["final_occupancy"]
            )
            records.append(stats)
        return sorted(records, key=lambda item: item["ledger_id"])


def _character_record(
    *,
    seed: int,
    sequence_index: int,
    condition: str,
    points: tuple[StrokePoint, ...],
) -> dict[str, Any]:
    audit = _OccupancyAudit()
    original_init = EligibilityLedger.__init__
    original_record = EligibilityLedger.record_activity
    original_signal = EligibilityLedger.apply_signal

    def init(ledger: EligibilityLedger, *args: Any, **kwargs: Any) -> None:
        original_init(ledger, *args, **kwargs)
        audit.register(ledger)

    def record_activity(ledger: EligibilityLedger, event: Any) -> Any:
        return audit.observe(
            ledger,
            lambda: original_record(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    def apply_signal(ledger: EligibilityLedger, event: Any) -> Any:
        return audit.observe(
            ledger,
            lambda: original_signal(ledger, event),
            event.timestamp,
            getattr(event.payload, "trace_id", None),
        )

    def runtime_factory(*args: Any, **kwargs: Any) -> ExcursionCharacterRuntime:
        kwargs["namespace"] = NAMESPACE
        return ExcursionCharacterRuntime(*args, eligibility_capacity=ELIGIBILITY_CAPACITY, **kwargs)

    with ExitStack() as stack:
        stack.enter_context(mock.patch.object(base, "ExcursionCharacterRuntime", runtime_factory))
        stack.enter_context(mock.patch.object(EligibilityLedger, "__init__", init))
        stack.enter_context(mock.patch.object(EligibilityLedger, "record_activity", record_activity))
        stack.enter_context(mock.patch.object(EligibilityLedger, "apply_signal", apply_signal))
        try:
            record = _base_record(seed, sequence_index, condition, points)
        except EligibilityCapacityError as error:
            raise StopCondition(
                "EligibilityCapacityError",
                {
                    "seed": seed,
                    "condition": condition,
                    "character_id": f"c{seed:02d}-{sequence_index:03d}",
                    "errors": audit.capacity_errors,
                    "message": str(error),
                },
            ) from error

    ledgers = audit.finalize()
    if len(ledgers) != len(base.NODES) or any(
        item["configured_capacity"] != ELIGIBILITY_CAPACITY for item in ledgers
    ):
        raise StopCondition("effective capacity is not 1024 per ledger", {"ledgers": ledgers})
    if not all(item["reconciles"] for item in ledgers):
        raise StopCondition("occupancy does not reconcile", {"ledgers": ledgers})
    if any(item["peak_occupancy"] >= ELIGIBILITY_CAPACITY for item in ledgers):
        raise StopCondition("peak occupancy reached capacity", {"ledgers": ledgers})

    emissions = record["canonical_emissions"]
    source_count = sum(item["emitter_id"] == "source" for item in emissions)
    routed = record["routed_contributions"]
    state_records = record["destination_state_replay"]["records"]
    destination_count = sum(item["emitter_id"] == "destination" for item in emissions)
    record["eligibility"] = {
        "runtime_property_capacity": ELIGIBILITY_CAPACITY,
        "ledgers": ledgers,
        "capacity_errors": audit.capacity_errors,
    }
    record["mechanism_counts"] = {
        "source_canonical_emissions": source_count,
        "routed_transfers": len(routed),
        "destination_receptions": len(routed),
        "destination_state_changes": sum(
            item["state_after"] != item["state_before"] for item in state_records
        ),
        "destination_canonical_emissions": destination_count,
    }
    record["no_edge_contaminated"] = bool(
        condition == "NO_EDGE_CONTROL" and (routed or destination_count)
    )
    record.pop("replay_digest", None)
    record["replay_digest"] = _digest(record)
    return record


def _base_record(
    seed: int, sequence_index: int, condition: str, points: tuple[StrokePoint, ...]
) -> dict[str, Any]:
    try:
        return base._character_record(
            seed=seed, sequence_index=sequence_index, condition=condition, points=points
        )
    except RuntimeError as error:
        if str(error) == "no-edge control produced routed work or a destination emission":
            raise StopCondition(
                "NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL",
                {
                    "seed": seed,
                    "condition": condition,
                    "character_id": f"c{seed:02d}-{sequence_index:03d}",
                    "message": str(error),
                },
            ) from error
        raise


def _condition_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    summary = base._condition_summary(records)
    ledgers = [ledger for record in records for ledger in record["eligibility"]["ledgers"]]
    counts = [record["mechanism_counts"] for record in records]
    summary.update(
        {
            "downstream_receiving_characters": sum(item["destination_receptions"] > 0 for item in counts),
            "destination_state_change_characters": sum(item["destination_state_changes"] > 0 for item in counts),
            "destination_state_changes": sum(item["destination_state_changes"] for item in counts),
            "peak_eligibility_occupancy": max((item["peak_occupancy"] for item in ledgers), default=0),
            "final_eligibility_occupancy_max": max((item["final_occupancy"] for item in ledgers), default=0),
            "eligibility_creations": sum(item["created"] for item in ledgers),
            "eligibility_removals": sum(item["removed"] for item in ledgers),
            "configured_capacities": sorted({item["configured_capacity"] for item in ledgers}),
            "all_ledgers_reconcile": all(item["reconciles"] for item in ledgers),
            "no_edge_contaminated_characters": sum(record["no_edge_contaminated"] for record in records),
        }
    )
    return summary


def _summarize(results: dict[str, Any], stop: dict[str, Any] | None, replay: dict[str, Any] | None) -> dict[str, Any]:
    runs = results["runs"]
    per_seed = {
        seed: {
            condition: _condition_summary(records)
            for condition, records in conditions.items()
            if records
        }
        for seed, conditions in runs.items()
    }
    per_condition = {
        condition: _condition_summary(
            [r for conditions in runs.values() for r in conditions.get(condition, [])]
        )
        for condition in CONDITIONS
    }
    sensitivity_streams = []
    for seed, conditions in runs.items():
        default = {r["character_id"]: r for r in conditions.get("DEFAULT_STATIC_EDGE", [])}
        n2 = {r["character_id"]: r for r in conditions.get("STATIC_N2_BOUND_SENSITIVITY", [])}
        for character_id in sorted(set(default) & set(n2)):
            d = default[character_id]["mechanism_counts"]["destination_canonical_emissions"]
            s = n2[character_id]["mechanism_counts"]["destination_canonical_emissions"]
            if s > 0 and d == 0:
                sensitivity_streams.append(
                    {"seed": int(seed), "character_id": character_id, "default": d, "n2": s}
                )
    default_emits = per_condition["DEFAULT_STATIC_EDGE"]["destination_emissions"] > 0
    n2_emits = per_condition["STATIC_N2_BOUND_SENSITIVITY"]["destination_emissions"] > 0
    no_edge_emits = per_condition["NO_EDGE_CONTROL"]["destination_emissions"] > 0
    no_edge_clean = (
        per_condition["NO_EDGE_CONTROL"]["routed_contributions"] == 0 and not no_edge_emits
    )
    complete = stop is None
    classifications: list[str] = []
    if stop is not None:
        if stop["reason"] == "NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL":
            classifications.append("NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL")
        classifications.append("BLOCKED — FIXTURE OR PUBLIC API INSUFFICIENT")
    else:
        if not (default_emits or n2_emits or no_edge_emits):
            classifications.append("DESTINATION EMISSION ABSENT IN ALL CONDITIONS")
        if default_emits:
            classifications.append("DESTINATION EMISSION PRESENT UNDER DEFAULT STATIC EDGE")
            classifications.append("INCONSISTENT WITH POST-LUNA-33 INTERPRETATION")
        if n2_emits and not default_emits:
            classifications.append("DESTINATION EMISSION PRESENT ONLY UNDER STATIC N2 SENSITIVITY")
        if sensitivity_streams:
            classifications.append("STATIC N2 CHANGES RESULT RELATIVE TO DEFAULT")
        if not no_edge_clean:
            classifications.append("NO-EDGE CONTROL NOT A VALID NEGATIVE CONTROL")
        if replay is not None and not replay["equal"]:
            classifications.append("BLOCKED — FIXTURE OR PUBLIC API INSUFFICIENT")
    return {
        "schema": "TPCN-LUNA37-EXCURSION-V1-SUMMARY-1",
        "execution_baseline": EXECUTION_BASELINE,
        "eligibility_capacity": ELIGIBILITY_CAPACITY,
        "capacity_tuned": False,
        "complete": complete,
        "stop_condition": stop,
        "design_counts": {
            "seeds": len(runs),
            "character_condition_executions": sum(
                len(records) for conditions in runs.values() for records in conditions.values()
            ),
        },
        "per_seed": per_seed,
        "per_condition": per_condition,
        "no_edge_control_is_genuine_negative": no_edge_clean and complete,
        "static_n2_sensitivity_streams": sensitivity_streams,
        "deterministic_replay": replay,
        "terminal_classifications": classifications,
        "interpretation_boundary": (
            "Bounded single-fixture mechanism observation only; not ACP-0007 efficacy, "
            "candidate formation in the four-class task, beneficial growth, generality, "
            "accuracy, prediction/resource benefit, or an architecture conclusion."
        ),
    }


def _run_once(seeds: tuple[int, ...]) -> tuple[dict[str, Any], dict[str, Any] | None]:
    runs: dict[str, Any] = {}
    stop: dict[str, Any] | None = None
    for seed in seeds:
        sequences = base._training_point_sequences(seed)
        seed_runs: dict[str, list[dict[str, Any]]] = {condition: [] for condition in CONDITIONS}
        runs[str(seed)] = seed_runs
        try:
            for condition in CONDITIONS:
                for sequence_index, points in enumerate(sequences):
                    seed_runs[condition].append(
                        _character_record(
                            seed=seed,
                            sequence_index=sequence_index,
                            condition=condition,
                            points=points,
                        )
                    )
        except StopCondition as error:
            stop = {"reason": error.reason, "detail": error.detail}
        except Exception as error:  # any other production exception is a stop condition
            stop = {"reason": "production exception", "detail": {"type": type(error).__name__, "message": str(error)}}
        if stop is not None:
            break
    results = {
        "schema": "TPCN-LUNA37-EXCURSION-V1-RESULTS-1",
        "execution_baseline": EXECUTION_BASELINE,
        "eligibility_capacity": ELIGIBILITY_CAPACITY,
        "conditions": list(CONDITIONS),
        "environment": {"python": sys.version, "platform": platform.platform()},
        "runs": runs,
    }
    return results, stop


def _all_digest(results: dict[str, Any]) -> str:
    return _digest(
        [
            record["replay_digest"]
            for seed in sorted(results["runs"])
            for condition in CONDITIONS
            for record in results["runs"][seed][condition]
        ]
    )


def run_experiment(
    output_directory: Path = ARTIFACT_DIRECTORY,
    seeds: tuple[int, ...] = SEEDS,
) -> tuple[dict[str, Any], dict[str, Any]]:
    results, stop = _run_once(seeds)
    replay_results, replay_stop = _run_once(seeds)
    first, second = _all_digest(results), _all_digest(replay_results)
    replay = {
        "initial_digest": first,
        "replay_digest": second,
        "equal": first == second and stop == replay_stop,
    }
    summary = _summarize(results, stop, replay)
    output_directory.mkdir(parents=True, exist_ok=True)
    for filename, value in (
        ("config.json", experiment_config()),
        ("results.json", results),
        ("summary.json", summary),
    ):
        (output_directory / filename).write_text(_canonical_json(value) + "\n", encoding="utf-8")
    return results, summary


def main() -> None:
    _, summary = run_experiment()
    print(_canonical_json(summary))


if __name__ == "__main__":
    main()
