import SwiftUI
import OCCULUSCore

@main
struct OCCULUSApp: App {
    var body: some Scene {
        WindowGroup {
            TabView {
                DashboardView().tabItem { Label("Simulation", systemImage: "scope") }
                LiveCameraView().tabItem { Label("Live Camera", systemImage: "camera.viewfinder") }
            }
        }
    }
}
