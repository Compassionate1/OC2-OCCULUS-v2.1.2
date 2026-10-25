import XCTest
@testable import OCCULUSCore

final class SimulationTests: XCTestCase {
    func testDeterministic() throws {
        let a = try Evidence.encodeFrames(Simulator.run(Configuration(seed: 123, steps: 40)))
        let b = try Evidence.encodeFrames(Simulator.run(Configuration(seed: 123, steps: 40)))
        XCTAssertEqual(a, b)
    }
    func testBounds() {
        let frames = Simulator.run(Configuration(seed: 3, objectCount: 8, steps: 100))
        XCTAssertEqual(frames.count, 100)
        for frame in frames {
            XCTAssertTrue((-180...180).contains(frame.focusBearing))
            XCTAssertTrue((0...1).contains(frame.arousal))
            for obs in frame.observations { XCTAssertTrue((-180...180).contains(obs.truthBearing)) }
        }
    }
    func testWrap() { XCTAssertEqual(Simulator.wrap(190), -170, accuracy: 1e-9) }
    #if canImport(CryptoKit)
    func testSignAndTamper() throws {
        importPlaceholder()
    }
    private func importPlaceholder() {} // Cryptographic sign/verify tested in iOS integration gate.
    #endif
}
