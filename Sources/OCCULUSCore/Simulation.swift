import Foundation

public struct Observation: Codable, Sendable {
    public let tick: Int
    public let objectID: Int
    public let truthBearing: Double
    public let measuredBearing: Double?
    public let modality: String
    public let occluded: Bool
    public let snrDB: Double
    public let ambiguity: Bool
    public let confidence: Double
}

public struct Frame: Codable, Sendable {
    public let tick: Int
    public let focusBearing: Double
    public let apertureHalfWidth: Double
    public let arousal: Double
    public let observations: [Observation]
}

public struct Configuration: Sendable {
    public var seed: UInt64
    public var objectCount: Int
    public var steps: Int
    public var apertureHalfWidth: Double
    public init(seed: UInt64 = 52, objectCount: Int = 7, steps: Int = 120, apertureHalfWidth: Double = 35) {
        self.seed = seed; self.objectCount = max(1, min(50, objectCount)); self.steps = max(1, min(10000, steps)); self.apertureHalfWidth = max(5, min(90, apertureHalfWidth))
    }
}

public struct SeededRNG: Sendable {
    private var state: UInt64
    public init(seed: UInt64) { state = seed }
    public mutating func uniform() -> Double {
        state &+= 0x9E3779B97F4A7C15
        var z = state
        z = (z ^ (z >> 30)) &* 0xBF58476D1CE4E5B9
        z = (z ^ (z >> 27)) &* 0x94D049BB133111EB
        return Double((z ^ (z >> 31)) >> 11) / Double(1 << 53)
    }
    public mutating func gaussian() -> Double {
        let u = max(uniform(), 1e-12)
        return sqrt(-2 * log(u)) * cos(2 * .pi * uniform())
    }
}

public enum Simulator {
    public static func wrap(_ angle: Double) -> Double {
        let a = (angle + 180).truncatingRemainder(dividingBy: 360)
        return (a < 0 ? a + 360 : a) - 180
    }
    public static func run(_ config: Configuration) -> [Frame] {
        var rng = SeededRNG(seed: config.seed)
        let initial = (0..<config.objectCount).map { _ in rng.uniform() * 360 - 180 }
        let velocity = (0..<config.objectCount).map { _ in (rng.uniform() - 0.5) * 2.4 }
        var focus = 0.0
        var arousal = 0.15
        var frames: [Frame] = []
        for tick in 0..<config.steps {
            var observations: [Observation] = []
            for id in 0..<config.objectCount {
                let truth = wrap(initial[id] + Double(tick) * velocity[id] + 8 * sin(Double(tick) * 0.035 + Double(id)))
                let inFOV = abs(wrap(truth - focus)) <= config.apertureHalfWidth
                let occluded = inFOV && rng.uniform() < (0.12 + 0.16 * (1 + sin(Double(tick) * 0.08 + Double(id))) / 2)
                let snr = -3 + 25 * rng.uniform()
                let audible = snr > 0 && rng.uniform() < min(0.98, 0.40 + snr / 32)
                let visual = inFOV && !occluded
                if visual {
                    let sigma = 0.8 + max(0, 12 - snr) / 6
                    observations.append(Observation(tick: tick, objectID: id, truthBearing: truth, measuredBearing: wrap(truth + sigma * rng.gaussian()), modality: "visual", occluded: false, snrDB: snr, ambiguity: false, confidence: min(0.98, 0.75 + snr / 100)))
                } else if audible {
                    // A single symmetric two-ear timing cue can be front/back ambiguous.
                    let ambiguous = rng.uniform() < 0.30
                    let bearing = ambiguous ? wrap(180 - truth) : truth
                    observations.append(Observation(tick: tick, objectID: id, truthBearing: truth, measuredBearing: wrap(bearing + (3 + 35 / (snr + 5)) * rng.gaussian()), modality: "auditory", occluded: occluded, snrDB: snr, ambiguity: ambiguous, confidence: ambiguous ? 0.35 : min(0.8, snr / 30)))
                }
            }
            // Attention shifts toward the strongest nonambiguous observation.
            if let selected = observations.filter({ !$0.ambiguity }).max(by: { $0.confidence < $1.confidence }), let bearing = selected.measuredBearing {
                focus = wrap(focus + 0.28 * wrap(bearing - focus))
                arousal = min(1, 0.88 * arousal + 0.12 * selected.confidence)
            } else { arousal *= 0.92 }
            frames.append(Frame(tick: tick, focusBearing: focus, apertureHalfWidth: config.apertureHalfWidth, arousal: arousal, observations: observations))
        }
        return frames
    }
}
