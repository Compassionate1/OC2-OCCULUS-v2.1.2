import Foundation

public enum FeedSource: String, Codable, Sendable { case simulation, camera, microphone, imported }
public enum EventKind: String, Codable, Sendable { case visualObservation, auditoryObservation, state, cameraStatus, audioStatus, validation }

/// Canonical OC2 v2.0.0 multimodal event envelope. No raw media is transmitted by this type.
public struct OC2Event: Codable, Sendable, Equatable {
    public let schemaVersion: String
    public let eventID: UUID
    public let timestamp: Date
    public let source: FeedSource
    public let kind: EventKind
    public let frameIndex: Int?
    public let bearingDegrees: Double?
    public let confidence: Double?
    public let detail: String
    public let synthetic: Bool
    public init(source: FeedSource, kind: EventKind, frameIndex: Int? = nil, bearingDegrees: Double? = nil, confidence: Double? = nil, detail: String, timestamp: Date = Date()) {
        self.schemaVersion = "oc2.event.v2"
        self.eventID = UUID()
        self.timestamp = timestamp
        self.source = source
        self.kind = kind
        self.frameIndex = frameIndex
        self.bearingDegrees = bearingDegrees
        self.confidence = confidence
        self.detail = detail
        self.synthetic = source == .simulation
    }
}

public enum DataPlane {
    public static func events(from frames: [Frame]) -> [OC2Event] {
        frames.flatMap { frame -> [OC2Event] in
            let state = OC2Event(source: .simulation, kind: .state, frameIndex: frame.tick, bearingDegrees: frame.focusBearing, confidence: frame.arousal, detail: "apertureHalfWidth=\(frame.apertureHalfWidth)")
            return [state] + frame.observations.map { observation in
                OC2Event(source: .simulation, kind: observation.modality == "visual" ? .visualObservation : .auditoryObservation, frameIndex: frame.tick, bearingDegrees: observation.measuredBearing, confidence: observation.confidence, detail: "syntheticObject=\(observation.objectID);occluded=\(observation.occluded);snrDB=\(observation.snrDB);ambiguous=\(observation.ambiguity)")
            }
        }
    }
    public static func encodeJSONL(_ events: [OC2Event]) throws -> Data {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        encoder.dateEncodingStrategy = .iso8601
        var output = Data()
        for event in events {
            output.append(try encoder.encode(event))
            output.append(0x0A)
        }
        return output
    }
}
