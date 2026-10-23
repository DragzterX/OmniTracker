using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

namespace OmniTrackerLauncher
{
    static class Program
    {
        [STAThread]
        static void Main()
        {
            string appDir = AppDomain.CurrentDomain.BaseDirectory;
            string pythonwPath = Path.Combine(appDir, "backend", ".venv", "Scripts", "pythonw.exe");
            string desktopScript = Path.Combine(appDir, "desktop_app.py");

            if (!File.Exists(pythonwPath))
            {
                MessageBox.Show(
                    "Could not find backend virtual environment at:\n" + pythonwPath + 
                    "\n\nPlease ensure backend dependencies are installed.",
                    "OmniTracker",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            if (!File.Exists(desktopScript))
            {
                MessageBox.Show(
                    "Could not find desktop application script at:\n" + desktopScript,
                    "OmniTracker",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
                return;
            }

            ProcessStartInfo psi = new ProcessStartInfo();
            psi.FileName = pythonwPath;
            psi.Arguments = "\"" + desktopScript + "\"";
            psi.WorkingDirectory = appDir;
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            psi.WindowStyle = ProcessWindowStyle.Hidden;

            try
            {
                using (Process proc = Process.Start(psi))
                {
                    if (proc != null)
                    {
                        proc.WaitForExit();
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(
                    "Error launching OmniTracker:\n" + ex.Message,
                    "OmniTracker Error",
                    MessageBoxButtons.OK,
                    MessageBoxIcon.Error
                );
            }
        }
    }
}
