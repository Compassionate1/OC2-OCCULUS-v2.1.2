// swift-tools-version: 6.0
import PackageDescription
let package = Package(name: "OCCULUSCore", platforms: [.iOS(.v17), .macOS(.v13)], products: [.library(name: "OCCULUSCore", targets: ["OCCULUSCore"])], targets: [.target(name: "OCCULUSCore"), .testTarget(name: "OCCULUSCoreTests", dependencies: ["OCCULUSCore"])])
