import sys
import os
import json
import re
from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QProcess, QTimer

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class RenderManager(QMainWindow):
    def __init__(self):
        super().__init__()
        
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))
            
        self.config_file = os.path.join(self.base_dir, "render_config.json")
        
        loader = QUiLoader()
        ui_path = resource_path("main_window.ui")
        ui_file = QFile(ui_path)
        if not ui_file.open(QFile.ReadOnly): return
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        self.setCentralWidget(self.ui)
        self.setWindowTitle("Render Champ v1.3")
        self.resize(self.ui.size())

        self.render_process = QProcess()
        self.render_process.finished.connect(self.on_render_finished)
        self.current_total_frames = 0 

        self.ui.btnAdd.clicked.connect(self.add_file)
        self.ui.btnRemove.clicked.connect(self.remove_file)
        self.ui.btnStart.clicked.connect(self.start_render)
        self.ui.btnStop.clicked.connect(self.stop_render)
        
        self.load_state()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(5000)

    def get_blend_frame_count(self, blender_exe, blend_path):
        """Native Qt Probe: No black windows, no shell errors."""
        probe = QProcess()
        # Clean paths of extra quotes if they exist
        exe = blender_exe.strip().replace('"', '')
        file = blend_path.strip().replace('"', '')
        
        script = "import bpy; print('FRAME_COUNT:' + str(bpy.context.scene.frame_end))"
        args = ["-b", file, "--python-expr", script]
        
        probe.start(exe, args)
        
        # Give it up to 15 seconds to open Blender and read the file
        if not probe.waitForFinished(15000):
            probe.kill()
            return None
            
        output = str(probe.readAllStandardOutput())
        match = re.search(r'FRAME_COUNT:(\d+)', output)
        return int(match.group(1)) if match else None

    def load_state(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r") as f:
                    data = json.load(f)
                    self.ui.listQueue.addItems(data.get("queue", []))
                    self.ui.lineBlenderPath.setText(data.get("blender_path", ""))
            except: pass

    def save_state(self):
        queue = [self.ui.listQueue.item(i).text() for i in range(self.ui.listQueue.count())]
        data = {"queue": queue, "blender_path": self.ui.lineBlenderPath.text()}
        with open(self.config_file, "w") as f:
            json.dump(data, f, indent=4)

    def add_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select .blend", "", "Blender (*.blend)")
        if path:
            self.ui.listQueue.addItem(path)
            self.save_state()

    def remove_file(self):
        for item in self.ui.listQueue.selectedItems():
            self.ui.listQueue.takeItem(self.ui.listQueue.row(item))
        self.save_state()

    def start_render(self):
        if self.ui.listQueue.count() == 0: return
        
        blender_exe = self.ui.lineBlenderPath.text().strip().replace('"', '')
        blend_path = self.ui.listQueue.item(0).text()
        
        if not os.path.exists(blender_exe):
            QMessageBox.critical(self, "Error", f"Blender not found at: {blender_exe}")
            return

        self.save_state()
        self.ui.lblStatus.setText("🔍 Syncing with .blend metadata...")
        QApplication.processEvents() 

        # Using the new native probe
        frames = self.get_blend_frame_count(blender_exe, blend_path)
        
        if frames is None:
            QMessageBox.warning(self, "Audit Failed", "Metadata probe failed. Check if the .blend is corrupted or paths are locked.")
            self.ui.lblStatus.setText("Ready.")
            return
            
        self.current_total_frames = frames
        base_name = os.path.splitext(os.path.basename(blend_path))[0]
        out_dir = os.path.join(os.path.dirname(blend_path), f"{base_name}_output")
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        existing = [f for f in os.listdir(out_dir) if f.endswith('.png')]
        start_frame = 1
        if existing:
            nums = [int(re.findall(r'\d+', f)[-1]) for f in existing if re.findall(r'\d+', f)]
            if nums: start_frame = max(nums) + 1

        args = ["-b", blend_path, "-o", f"{out_dir}/frame_####", "-s", str(start_frame), "-a", "-t", "2"]
        self.render_process.start(blender_exe, args)
        self.ui.lblStatus.setText(f"🚀 {base_name} | Total Frames: {self.current_total_frames}")

    def update_ui(self):
        if self.render_process.state() == QProcess.Running:
            if self.ui.listQueue.count() > 0:
                blend_path = self.ui.listQueue.item(0).text()
                base_name = os.path.splitext(os.path.basename(blend_path))[0]
                out_dir = os.path.join(os.path.dirname(blend_path), f"{base_name}_output")
                if os.path.exists(out_dir):
                    count = len([f for f in os.listdir(out_dir) if f.endswith('.png')])
                    total = self.current_total_frames if self.current_total_frames > 0 else 1
                    prog = min(int((count / total) * 100), 100)
                    self.ui.progressBar.setValue(prog)

    def on_render_finished(self):
        if self.ui.listQueue.count() > 0:
            self.ui.listQueue.takeItem(0)
            self.save_state()
            if self.ui.listQueue.count() > 0:
                self.start_render()
            else:
                self.ui.lblStatus.setText("✅ All Done!")
                self.ui.progressBar.setValue(100)

    def stop_render(self):
        if self.render_process.state() == QProcess.Running:
            self.render_process.terminate()
            self.ui.lblStatus.setText("🛑 Stopped.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenderManager()
    window.show()
    sys.exit(app.exec())