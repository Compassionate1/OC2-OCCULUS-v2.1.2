import XCTest
@testable import OCCULUSCore

final class DataPlaneTests: XCTestCase {
    func testSyntheticEventEnvelope() throws {
        let frames = Simulator.run(Configuration(seed: 52, objectCount: 3, steps: 12))
        let events = DataPlane.events(from: frames)
        XCTAssertEqual(events.filter { $0.kind == .state }.count, 12)
        XCTAssertTrue(events.allSatisfy { $0.synthetic && $0.source == .simulation })
        let jsonl = try DataPlane.encodeJSONL(events)
        XCTAssertEqual(jsonl.filter { $0 == 10 }.count, events.count)
    }
    func testDeterministicSimulation() throws {
        let a = Simulator.run(Configuration(seed: 99, objectCount: 4, steps: 20))
        let b = Simulator.run(Configuration(seed: 99, objectCount: 4, steps: 20))
        XCTAssertEqual(try Evidence.encodeFrames(a), try Evidence.encodeFrames(b))
    }
}
