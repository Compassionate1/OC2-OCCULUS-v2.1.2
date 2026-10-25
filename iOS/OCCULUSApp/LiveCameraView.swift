import SwiftUI
import AVFoundation
import OCCULUSCore

/// Opt-in local camera preview. No recording, face identification, target tracking,
/// audio capture, remote upload, or image analysis is performed.
@MainActor final class CameraPreviewController: NSObject, ObservableObject {
    @Published var status = "Camera off"
    @Published var running = false
    let session = AVCaptureSession()
    private var input: AVCaptureDeviceInput?
    func start() async {
        guard !running else { return }
        let authorized: Bool
        switch AVCaptureDevice.authorizationStatus(for: .video) {
        case .authorized: authorized = true
        case .notDetermined: authorized = await AVCaptureDevice.requestAccess(for: .video)
        default: authorized = false
        }
        guard authorized else { status = "Camera permission denied"; return }
        guard let device = AVCaptureDevice.default(for: .video) else { status = "No camera available"; return }
        do {
            let newInput = try AVCaptureDeviceInput(device: device)
            session.beginConfiguration()
            session.sessionPreset = .medium
            if let input { session.removeInput(input) }
            guard session.canAddInput(newInput) else { session.commitConfiguration(); status = "Camera input unsupported"; return }
            session.addInput(newInput)
            input = newInput
            session.commitConfiguration()
            // Session start can block; dispatch outside the main actor.
            let captureSession = session
            DispatchQueue.global(qos: .userInitiated).async { captureSession.startRunning() }
            running = true
            status = "Live camera preview (local only)"
        } catch { status = "Camera error: \(error.localizedDescription)" }
    }
    func stop() {
        let captureSession = session
        DispatchQueue.global(qos: .userInitiated).async { captureSession.stopRunning() }
        running = false
        status = "Camera off"
    }
}

struct CameraLayer: UIViewRepresentable {
    let session: AVCaptureSession
    func makeUIView(context: Context) -> PreviewUIView { let view = PreviewUIView(); view.previewLayer.session = session; return view }
    func updateUIView(_ uiView: PreviewUIView, context: Context) { uiView.previewLayer.session = session }
}
final class PreviewUIView: UIView {
    override class var layerClass: AnyClass { AVCaptureVideoPreviewLayer.self }
    var previewLayer: AVCaptureVideoPreviewLayer { layer as! AVCaptureVideoPreviewLayer }
    override init(frame: CGRect) { super.init(frame: frame); previewLayer.videoGravity = .resizeAspectFill }
    required init?(coder: NSCoder) { fatalError("init(coder:) unsupported") }
}

struct LiveCameraView: View {
    @StateObject private var controller = CameraPreviewController()
    var body: some View {
        VStack(spacing: 14) {
            Text("OC2 • LIVE CAMERA • LOCAL PREVIEW").font(.caption.monospaced()).foregroundStyle(.orange)
            ZStack {
                CameraLayer(session: controller.session)
                Image(systemName: "viewfinder").font(.system(size: 120, weight: .ultraLight)).foregroundStyle(.green.opacity(0.8))
            }.frame(height: 340).clipped().background(.black)
            Text(controller.status).font(.caption)
            HStack {
                Button("Start Camera") { Task { await controller.start() } }.buttonStyle(.borderedProminent).disabled(controller.running)
                Button("Stop") { controller.stop() }.buttonStyle(.bordered).disabled(!controller.running)
            }
            Text("Live camera is opt-in and stays on device. No object recognition, audio acquisition, tracking, or streaming is performed on live frames. Synthetic tracking data remains separate.")
                .font(.footnote).foregroundStyle(.secondary)
        }.padding().onDisappear { controller.stop() }
    }
}
