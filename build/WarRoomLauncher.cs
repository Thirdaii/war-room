using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Forms;

internal static class WarRoomLauncher
{
    private static readonly string Root = AppDomain.CurrentDomain.BaseDirectory;
    private static readonly Dictionary<string,string> ItemIconCache = new Dictionary<string,string>();
    private static readonly object ItemIconLock = new object();

    [STAThread]
    private static void Main(string[] args)
    {
        try
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
            if (args != null && Array.Exists(args, a => string.Equals(a, "--app", StringComparison.OrdinalIgnoreCase))) { RunAppHost(); return; }
            string updater = Path.Combine(Root, "WarRoomUpdater.ps1");
            string index = Path.Combine(Root, "index.html");
            if (!File.Exists(updater)) { if (File.Exists(index)) { StartAppMode(); return; } throw new FileNotFoundException("War Room updater was not found.", updater); }
            var psi = new ProcessStartInfo { FileName = "powershell.exe", WorkingDirectory = Root, UseShellExecute = false, CreateNoWindow = true, WindowStyle = ProcessWindowStyle.Hidden, Arguments = "-NoProfile -ExecutionPolicy Bypass -File \"" + updater + "\"" };
            Process.Start(psi);
        }
        catch (Exception ex) { ShowError(ex); }
    }

    private static void StartAppMode() { Process.Start(new ProcessStartInfo { FileName = Process.GetCurrentProcess().MainModule.FileName, WorkingDirectory = Root, UseShellExecute = false, Arguments = "--app" }); }

    private static void RunAppHost()
    {
        string index = Path.Combine(Root, "index.html");
        if (!File.Exists(index)) throw new FileNotFoundException("index.html not found", index);
        int port = FindPort(); string baseUrl = "http://127.0.0.1:" + port + "/";
        var listener = new HttpListener(); listener.Prefixes.Add(baseUrl); listener.Start();
        var serverThread = new Thread(() => { while (listener.IsListening) { try { var ctx = listener.GetContext(); ThreadPool.QueueUserWorkItem(_ => Handle(ctx)); } catch { if (!listener.IsListening) break; } } });
        serverThread.IsBackground = true; serverThread.Start();
        WaitForHealth(baseUrl);
        Process app = LaunchEdgeApp(baseUrl);
        // Edge may hand --app off to an existing browser process and let the spawned process exit immediately.
        // Do not tie the local HTTP server lifetime to that transient Process object.
        Application.Run(new HostContext(listener, app));
    }

    private static void WaitForHealth(string baseUrl)
    {
        Exception last = null;
        for (int i = 0; i < 40; i++)
        {
            try
            {
                var req = (HttpWebRequest)WebRequest.Create(baseUrl + "health"); req.Timeout = 250; req.ReadWriteTimeout = 250; req.Proxy = null;
                using (var resp = (HttpWebResponse)req.GetResponse()) if (resp.StatusCode == HttpStatusCode.OK) return;
            }
            catch (Exception ex) { last = ex; Thread.Sleep(50); }
        }
        try { listenerFailureCleanup(); } catch { }
        throw new InvalidOperationException("War Room local server did not become healthy before launch.", last);
    }

    private static void listenerFailureCleanup() { }

    private static Process LaunchEdgeApp(string url)
    {
        string[] candidates = { Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFilesX86), "Microsoft", "Edge", "Application", "msedge.exe"), Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ProgramFiles), "Microsoft", "Edge", "Application", "msedge.exe") };
        string profile = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "WarRoom", "EdgeProfile"); Directory.CreateDirectory(profile);
        foreach (string edge in candidates) { if (!File.Exists(edge)) continue; return Process.Start(new ProcessStartInfo { FileName = edge, WorkingDirectory = Root, UseShellExecute = false, Arguments = "--user-data-dir=\"" + profile + "\" --app=\"" + url + "\" --start-maximized --no-first-run --disable-features=msEdgeFirstRunExperience" }); }
        Process.Start(new ProcessStartInfo(url) { UseShellExecute = true }); return null;
    }

    private static int FindPort()
    {
        for (int port = 43871; port < 43920; port++) { try { var l = new System.Net.Sockets.TcpListener(IPAddress.Loopback, port); l.Start(); l.Stop(); return port; } catch { } }
        throw new InvalidOperationException("Could not find a local port for War Room.");
    }

    private static void Handle(HttpListenerContext ctx)
    {
        try
        {
            string path = ctx.Request.Url.AbsolutePath;
            if (path.Equals("/armory", StringComparison.OrdinalIgnoreCase)) { HandleArmory(ctx); return; }
            if (path.Equals("/item-icon", StringComparison.OrdinalIgnoreCase)) { HandleItemIcon(ctx); return; }
            if (path.Equals("/health", StringComparison.OrdinalIgnoreCase)) { Write(ctx, 200, "application/json", "{\"ok\":true,\"version\":\"1.7.23\",\"tls\":\"1.2\",\"itemIcons\":true}"); return; }
            ServeStatic(ctx, path);
        }
        catch (Exception ex) { Write(ctx, 500, "application/json", "{\"error\":\"" + JsonEscape(ex.Message) + "\",\"stage\":\"local-host\"}"); }
    }

    private static void HandleArmory(HttpListenerContext ctx)
    {
        string name = ctx.Request.QueryString["name"] ?? "";
        if (string.IsNullOrWhiteSpace(name)) { Write(ctx, 400, "application/json", "{\"error\":\"Missing character name\",\"stage\":\"request\"}"); return; }
        string url = "https://classicarmory.gg/api/character/us/dreamscythe/" + Uri.EscapeDataString(name.Trim()) + "?ns=classicann";
        try
        {
            ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
            using (var wc = new WebClient())
            {
                wc.Encoding = Encoding.UTF8; wc.Headers[HttpRequestHeader.UserAgent] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) WarRoom/1.7.23"; wc.Headers[HttpRequestHeader.Accept] = "application/json, text/plain, */*"; wc.Headers[HttpRequestHeader.AcceptLanguage] = "en-US,en;q=0.9";
                string body = wc.DownloadString(url);
                if (string.IsNullOrWhiteSpace(body) || (!body.TrimStart().StartsWith("{") && !body.TrimStart().StartsWith("["))) { Write(ctx, 502, "application/json", "{\"error\":\"Armory returned a non-JSON payload\",\"stage\":\"upstream-parse\",\"upstream\":\"classicarmory.gg\"}"); return; }
                ctx.Response.Headers["X-WarRoom-Armory"] = "ok"; Write(ctx, 200, "application/json; charset=utf-8", body);
            }
        }
        catch (WebException ex)
        {
            var response = ex.Response as HttpWebResponse; int status = response != null ? (int)response.StatusCode : 502; string upstreamBody = "";
            try { if (response != null && response.GetResponseStream() != null) using (var sr = new StreamReader(response.GetResponseStream())) upstreamBody = sr.ReadToEnd(); } catch { }
            string message = response != null ? ("Armory request failed (HTTP " + status + ")") : ex.Message; string detail = string.IsNullOrWhiteSpace(upstreamBody) ? "" : upstreamBody; if (detail.Length > 240) detail = detail.Substring(0, 240);
            Write(ctx, status >= 400 && status < 600 ? status : 502, "application/json", "{\"error\":\"" + JsonEscape(message) + "\",\"stage\":\"upstream-request\",\"upstream\":\"classicarmory.gg\",\"detail\":\"" + JsonEscape(detail) + "\"}");
        }
        catch (Exception ex) { Write(ctx, 502, "application/json", "{\"error\":\"" + JsonEscape(ex.Message) + "\",\"stage\":\"proxy\",\"upstream\":\"classicarmory.gg\"}"); }
    }

    private static void HandleItemIcon(HttpListenerContext ctx)
    {
        string id = (ctx.Request.QueryString["id"] ?? "").Trim();
        if (!Regex.IsMatch(id, "^[0-9]{1,10}$")) { Write(ctx, 400, "application/json", "{\"error\":\"Invalid item id\"}"); return; }
        string icon = null; lock (ItemIconLock) { ItemIconCache.TryGetValue(id, out icon); }
        if (string.IsNullOrWhiteSpace(icon))
        {
            try
            {
                ServicePointManager.SecurityProtocol = SecurityProtocolType.Tls12;
                using (var wc = new WebClient())
                {
                    wc.Encoding = Encoding.UTF8; wc.Headers[HttpRequestHeader.UserAgent] = "Mozilla/5.0 WarRoom/1.7.23"; wc.Headers[HttpRequestHeader.Accept] = "application/xml,text/xml,*/*";
                    string xml = wc.DownloadString("https://www.wowhead.com/tbc/item=" + id + "&xml");
                    var m = Regex.Match(xml ?? "", "<icon[^>]*>([^<]+)</icon>", RegexOptions.IgnoreCase);
                    if (m.Success) icon = WebUtility.HtmlDecode(m.Groups[1].Value).Trim();
                }
                if (!string.IsNullOrWhiteSpace(icon)) lock (ItemIconLock) { ItemIconCache[id] = icon; }
            }
            catch { }
        }
        if (string.IsNullOrWhiteSpace(icon)) { Write(ctx, 404, "application/json", "{\"error\":\"Icon not found\",\"id\":\"" + JsonEscape(id) + "\"}"); return; }
        string image = "https://wow.zamimg.com/images/wow/icons/large/" + Uri.EscapeDataString(icon.ToLowerInvariant().Replace(".blp", "")) + ".jpg";
        Write(ctx, 200, "application/json", "{\"id\":\"" + JsonEscape(id) + "\",\"icon\":\"" + JsonEscape(icon) + "\",\"url\":\"" + JsonEscape(image) + "\"}");
    }

    private static void ServeStatic(HttpListenerContext ctx, string requestPath)
    {
        string relative = Uri.UnescapeDataString(requestPath.TrimStart('/').Replace('/', Path.DirectorySeparatorChar)); if (string.IsNullOrWhiteSpace(relative)) relative = "index.html";
        string full = Path.GetFullPath(Path.Combine(Root, relative)); if (!full.StartsWith(Path.GetFullPath(Root), StringComparison.OrdinalIgnoreCase) || !File.Exists(full)) { Write(ctx, 404, "text/plain", "Not found"); return; }
        byte[] bytes = File.ReadAllBytes(full); ctx.Response.StatusCode = 200; ctx.Response.ContentType = Mime(full); ctx.Response.ContentLength64 = bytes.Length; ctx.Response.OutputStream.Write(bytes, 0, bytes.Length); ctx.Response.OutputStream.Close();
    }

    private static string Mime(string path)
    {
        switch (Path.GetExtension(path).ToLowerInvariant()) { case ".html": return "text/html; charset=utf-8"; case ".js": return "application/javascript; charset=utf-8"; case ".css": return "text/css; charset=utf-8"; case ".json": return "application/json; charset=utf-8"; case ".png": return "image/png"; case ".jpg": case ".jpeg": return "image/jpeg"; case ".webp": return "image/webp"; case ".svg": return "image/svg+xml"; case ".ico": return "image/x-icon"; default: return "application/octet-stream"; }
    }

    private static void Write(HttpListenerContext ctx, int status, string type, string body)
    {
        byte[] bytes = Encoding.UTF8.GetBytes(body ?? ""); ctx.Response.StatusCode = status; ctx.Response.ContentType = type; ctx.Response.Headers["Cache-Control"] = "no-store"; ctx.Response.ContentLength64 = bytes.Length; ctx.Response.OutputStream.Write(bytes, 0, bytes.Length); ctx.Response.OutputStream.Close();
    }

    private static string JsonEscape(string s) { return (s ?? "").Replace("\\", "\\\\").Replace("\"", "\\\"").Replace("\r", " ").Replace("\n", " "); }
    private sealed class HostContext : ApplicationContext
    {
        private readonly HttpListener listener; private readonly Process launched;
        public HostContext(HttpListener listener, Process launched) { this.listener=listener; this.launched=launched; }
        protected override void ExitThreadCore() { try { if(listener!=null){listener.Stop();listener.Close();} } catch {} try { if(launched!=null) launched.Dispose(); } catch {} base.ExitThreadCore(); }
    }
    private static void ShowError(Exception ex) { MessageBox.Show("War Room could not start.\n\n" + ex.Message + "\n\nYou can still use Launch War Room.bat as an emergency fallback.", "Me Not That Kind Of Orc - War Room", MessageBoxButtons.OK, MessageBoxIcon.Error); }
}
