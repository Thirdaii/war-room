using System;
using System.Diagnostics;
using System.IO;
using System.Windows.Forms;

internal static class WarRoomLauncher
{
    [STAThread]
    private static void Main()
    {
        try
        {
            string root = AppDomain.CurrentDomain.BaseDirectory;
            string updater = Path.Combine(root, "WarRoomUpdater.ps1");
            string index = Path.Combine(root, "index.html");

            if (!File.Exists(updater))
            {
                if (File.Exists(index))
                {
                    Process.Start(new ProcessStartInfo(index) { UseShellExecute = true });
                    return;
                }
                throw new FileNotFoundException("War Room updater was not found.", updater);
            }

            var psi = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                WorkingDirectory = root,
                UseShellExecute = false,
                CreateNoWindow = true,
                WindowStyle = ProcessWindowStyle.Hidden,
                Arguments = "-NoProfile -ExecutionPolicy Bypass -File \"" + updater + "\""
            };

            Process.Start(psi);
        }
        catch (Exception ex)
        {
            MessageBox.Show(
                "War Room could not start.\n\n" + ex.Message +
                "\n\nYou can still use Launch War Room.bat as an emergency fallback.",
                "Me Not That Kind Of Orc - War Room",
                MessageBoxButtons.OK,
                MessageBoxIcon.Error);
        }
    }
}
