#!/usr/bin/env python3
"""Deterministic architecture-source and DOT syntax gate; no external Python packages."""
from pathlib import Path
import subprocess
root=Path(__file__).resolve().parents[1]
files=['Sources/OCCULUSCore/Simulation.swift','Sources/OCCULUSCore/DataPlane.swift','Sources/OCCULUSCore/Evidence.swift','iOS/OCCULUSApp/OCCULUSApp.swift','iOS/OCCULUSApp/DashboardView.swift','iOS/OCCULUSApp/LiveCameraView.swift','research-python/src/bop5ii/model.py','research-python/src/bop5ii/validation.py']
for rel in files:
    assert (root/rel).is_file(), rel
checks={'Simulation.swift':['struct Observation','struct Frame','struct Configuration','struct SeededRNG','enum Simulator'], 'DataPlane.swift':['enum FeedSource','enum EventKind','struct OC2Event','enum DataPlane'], 'Evidence.swift':['struct EvidenceEnvelope','enum Evidence'], 'DashboardView.swift':['struct DashboardView','struct PupilView'], 'LiveCameraView.swift':['struct LiveCameraView','class CameraPreviewController']}
for filename, symbols in checks.items():
    path=next(p for p in (root/'Sources').rglob(filename)) if filename in ('Simulation.swift','DataPlane.swift','Evidence.swift') else root/'iOS/OCCULUSApp'/filename
    body=path.read_text()
    for symbol in symbols: assert symbol in body, f'{path}: {symbol}'
for rel in ['01-domain-object-model.puml','02-software-architecture.dot','02-software-architecture.svg','02-software-architecture.png','03-runtime-sequence.puml','04-component-map.mmd','SOURCE-TRACEABILITY.md']:
    assert (root/'docs/uml'/rel).stat().st_size>100, rel
subprocess.run(['dot','-Tsvg',str(root/'docs/uml/02-software-architecture.dot'),'-o','/dev/null'],check=True)
print('PASS: source traceability, UML artifacts and DOT syntax')
