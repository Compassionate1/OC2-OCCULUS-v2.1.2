import SwiftUI
import OCCULUSCore
import CryptoKit

struct DashboardView: View {
    @State private var frames = Simulator.run(Configuration())
    @State private var tick = 0
    @State private var seed: UInt64 = 52
    @State private var aperture = 35.0
    @State private var exported: URL?
    @State private var status = "Synthetic observations only"
    private var frame: Frame { frames[min(tick, frames.count - 1)] }

    var body: some View {
        NavigationStack {
            ScrollView {
                VStack(spacing: 18) {
                    Text("OC2 v2.0.1 • RESTRICTED • SYNTHETIC")
                        .font(.caption.monospaced()).foregroundStyle(.orange)
                    PupilView(frame: frame).frame(height: 300)
                    HStack {
                        Label("Focus \(Int(frame.focusBearing))°", systemImage: "scope")
                        Spacer()
                        Text("Arousal \(frame.arousal, specifier: "%.2f")")
                    }.font(.caption.monospaced())
                    Slider(value: Binding(get: { Double(tick) }, set: { tick = Int($0) }), in: 0...Double(max(1, frames.count - 1)), step: 1)
                    Text("Frame \(tick + 1) / \(frames.count) · Observations \(frame.observations.count)")
                        .font(.caption)
                    HStack {
                        Text("Aperture ±\(Int(aperture))°")
                        Slider(value: $aperture, in: 5...90, step: 5)
                    }
                    Button("Run New Simulation") {
                        seed &+= 1
                        frames = Simulator.run(Configuration(seed: seed, apertureHalfWidth: aperture))
                        tick = 0; exported = nil
                    }.buttonStyle(.borderedProminent)
                    Button("Export Signed Evidence") { exportEvidence() }
                        .buttonStyle(.bordered)
                    if let exported { ShareLink(item: exported) { Label("Share evidence files", systemImage: "square.and.arrow.up") } }
                    Text(status).font(.caption).foregroundStyle(.secondary)
                    Text("Simulation tab uses synthetic data only. Live Camera is a separate opt-in local preview.")
                        .font(.footnote).foregroundStyle(.secondary)
                }.padding()
            }
            .navigationTitle("OC2 • OCCULUS")
        }
    }

    private func exportEvidence() {
        do {
            let payload = try Evidence.encodeFrames(frames)
            // An ephemeral key provides integrity but is NOT a trusted device identity.
            let key = Curve25519.Signing.PrivateKey()
            let envelope = try Evidence.sign(payload, seed: seed, frameCount: frames.count, key: key)
            let directory = FileManager.default.temporaryDirectory.appendingPathComponent("OCCULUS-\(UUID().uuidString)", isDirectory: true)
            try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
            try payload.write(to: directory.appendingPathComponent("frames.json"), options: .atomic)
            let encoder = JSONEncoder(); encoder.outputFormatting = [.prettyPrinted, .sortedKeys]
            try encoder.encode(envelope).write(to: directory.appendingPathComponent("manifest.json"), options: .atomic)
            // Share the folder so manifest and payload remain together.
            exported = directory
            status = "Ed25519 signed. Share both manifest.json and frames.json. Ephemeral self-signed key."
        } catch { status = "Evidence export failed: \(error.localizedDescription)" }
    }
}

struct PupilView: View {
    let frame: Frame
    var body: some View {
        GeometryReader { geo in
            let center = CGPoint(x: geo.size.width / 2, y: geo.size.height / 2)
            let radius = min(geo.size.width, geo.size.height) * 0.42
            ZStack {
                Circle().stroke(.teal.opacity(0.5), lineWidth: 2).frame(width: radius * 2, height: radius * 2)
                Circle().fill(.teal.opacity(0.18)).frame(width: radius * 1.45, height: radius * 1.45)
                Ellipse().fill(.black).frame(width: 22, height: radius * 1.25)
                Path { path in
                    path.move(to: center)
                    for offset in stride(from: -frame.apertureHalfWidth, through: frame.apertureHalfWidth, by: 2) {
                        let angle = (frame.focusBearing + offset - 90) * .pi / 180
                        path.addLine(to: CGPoint(x: center.x + radius * cos(angle), y: center.y + radius * sin(angle)))
                    }
                    path.closeSubpath()
                }.fill(.cyan.opacity(0.14))
                ForEach(frame.observations, id: \.objectID) { obs in
                    if let bearing = obs.measuredBearing {
                        let angle = (bearing - 90) * .pi / 180
                        Circle().fill(obs.modality == "visual" ? .green : .orange)
                            .frame(width: 10, height: 10)
                            .position(x: center.x + radius * cos(angle), y: center.y + radius * sin(angle))
                    }
                }
                Text("N").font(.caption).position(x: center.x, y: center.y - radius - 9)
            }.frame(maxWidth: .infinity, maxHeight: .infinity)
        }
        .accessibilityLabel("Synthetic 360-degree sensory plot with visual and auditory observations")
    }
}
