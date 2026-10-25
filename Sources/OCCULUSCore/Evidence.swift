import Foundation
#if canImport(CryptoKit)
import CryptoKit
#endif

public struct EvidenceEnvelope: Codable, Sendable {
    public let schemaVersion: String
    public let modelVersion: String
    public let createdAt: String
    public let source: String
    public let seed: UInt64
    public let frameCount: Int
    public let payloadSHA256: String
    public let algorithm: String
    public let publicKeyBase64: String
    public let signatureBase64: String
}

public enum EvidenceError: Error { case unavailable, invalidSignature, invalidDigest }

public enum Evidence {
    public static func encodeFrames(_ frames: [Frame]) throws -> Data {
        let encoder = JSONEncoder()
        encoder.outputFormatting = [.sortedKeys]
        return try encoder.encode(frames)
    }
    #if canImport(CryptoKit)
    public static func digest(_ data: Data) -> String { SHA256.hash(data: data).map { String(format: "%02x", $0) }.joined() }
    public static func sign(_ data: Data, seed: UInt64, frameCount: Int, key: Curve25519.Signing.PrivateKey) throws -> EvidenceEnvelope {
        let signature = try key.signature(for: data)
        return EvidenceEnvelope(schemaVersion: "1.0", modelVersion: "2.0.1", createdAt: ISO8601DateFormatter().string(from: Date()), source: "SYNTHETIC_SIMULATION", seed: seed, frameCount: frameCount, payloadSHA256: digest(data), algorithm: "Ed25519", publicKeyBase64: key.publicKey.rawRepresentation.base64EncodedString(), signatureBase64: signature.base64EncodedString())
    }
    public static func verify(_ data: Data, envelope: EvidenceEnvelope) throws -> Bool {
        guard digest(data) == envelope.payloadSHA256 else { throw EvidenceError.invalidDigest }
        guard envelope.algorithm == "Ed25519", let pub = Data(base64Encoded: envelope.publicKeyBase64), let sig = Data(base64Encoded: envelope.signatureBase64) else { throw EvidenceError.invalidSignature }
        let key = try Curve25519.Signing.PublicKey(rawRepresentation: pub)
        guard key.isValidSignature(sig, for: data) else { throw EvidenceError.invalidSignature }
        return true
    }
    #endif
}
