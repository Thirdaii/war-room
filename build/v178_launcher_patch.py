from pathlib import Path
import re

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
version=Path('build/version.txt').read_text(encoding='utf-8').strip()

# Preserve v1.7.26 item-appearance capability and add the same-origin Classic model proxy.
s=s.replace('private static readonly Dictionary<string,string> EnchantmentCache = new Dictionary<string,string>();', 'private static readonly Dictionary<string,string> EnchantmentCache = new Dictionary<string,string>();\n    private static readonly Dictionary<string,string> ItemAppearanceCache = new Dictionary<string,string>();')
s=s.replace('private static readonly object EnchantmentLock = new object();', 'private static readonly object EnchantmentLock = new object();\n    private static readonly object ItemAppearanceLock = new object();')
s=s.replace('if(path.Equals("/enchantment",StringComparison.OrdinalIgnoreCase)){HandleEnchantment(ctx);return;}', 'if(path.Equals("/enchantment",StringComparison.OrdinalIgnoreCase)){HandleEnchantment(ctx);return;}\n            if(path.Equals("/item-appearance",StringComparison.OrdinalIgnoreCase)){HandleItemAppearance(ctx);return;}\n            if(path.StartsWith("/modelviewer/classic/",StringComparison.OrdinalIgnoreCase)){HandleModelViewerProxy(ctx);return;}')
s=re.sub(r'\{\\"ok\\":true,\\"version\\":\\"[^\"]+\\",\\"tls\\":\\"1\.2\\",\\"itemIcons\\":true,\\"gems\\":true,\\"enchantments\\":true\}', '{\\"ok\\":true,\\"version\\":\\"'+version+'\\",\\"tls\\":\\"1.2\\",\\"itemIcons\\":true,\\"gems\\":true,\\"enchantments\\":true,\\"itemAppearances\\":true,\\"modelViewerProxy\\":true}', s)
s=re.sub(r'WarRoom/\d+\.\d+\.\d+', 'WarRoom/'+version, s)

# Restore v1.7.26 clean shutdown semantics. The stale v1.7.25 source starts a
# message loop but never exits it when the dedicated Edge app process closes.
old_host='private sealed class HostContext:ApplicationContext{private readonly HttpListener listener;private readonly Process launched;public HostContext(HttpListener listener,Process launched){this.listener=listener;this.launched=launched;}protected override void ExitThreadCore(){try{if(listener!=null){listener.Stop();listener.Close();}}catch{}try{if(launched!=null)launched.Dispose();}catch{}base.ExitThreadCore();}}'
new_host='private sealed class HostContext:ApplicationContext{private readonly HttpListener listener;private readonly Process launched;private readonly System.Windows.Forms.Timer exitTimer;public HostContext(HttpListener listener,Process launched){this.listener=listener;this.launched=launched;exitTimer=new System.Windows.Forms.Timer();exitTimer.Interval=400;exitTimer.Tick+=(s,e)=>{try{if(this.launched!=null&&this.launched.HasExited){exitTimer.Stop();ExitThread();}}catch{}};exitTimer.Start();}protected override void ExitThreadCore(){try{if(exitTimer!=null){exitTimer.Stop();exitTimer.Dispose();}}catch{}try{if(listener!=null){listener.Stop();listener.Close();}}catch{}try{if(launched!=null)launched.Dispose();}catch{}base.ExitThreadCore();}}'
if old_host not in s: raise RuntimeError('HostContext anchor missing; clean-shutdown patch not applied')
s=s.replace(old_host,new_host,1)

anchor='    private static void ServeStatic(HttpListenerContext ctx,string requestPath)'
if anchor not in s: raise RuntimeError('ServeStatic anchor missing')
methods=r'''    private static string ExtractDisplayId(string xml)
    {
        if(string.IsNullOrWhiteSpace(xml))return "";
        string[] patterns={"\\\"displayid\\\"\\s*:\\s*(\\d+)","\\\"displayId\\\"\\s*:\\s*(\\d+)","<displayid[^>]*>(\\d+)</displayid>","<displayId[^>]*>(\\d+)</displayId>"};
        foreach(string pattern in patterns){var m=Regex.Match(xml,pattern,RegexOptions.IgnoreCase);if(m.Success)return m.Groups[1].Value;}
        return "";
    }

    private static void HandleItemAppearance(HttpListenerContext ctx)
    {
        string id=(ctx.Request.QueryString["id"]??"").Trim();
        if(!ValidId(id)){Write(ctx,400,"application/json","{\"error\":\"Invalid item id\"}");return;}
        string displayId=null;lock(ItemAppearanceLock){ItemAppearanceCache.TryGetValue(id,out displayId);}
        if(string.IsNullOrWhiteSpace(displayId)){
            try{using(var wc=WowClient("application/xml,text/xml,*/*")){string xml=wc.DownloadString("https://www.wowhead.com/tbc/item="+id+"&xml");displayId=ExtractDisplayId(xml);}}
            catch{}
            if(!string.IsNullOrWhiteSpace(displayId))lock(ItemAppearanceLock){ItemAppearanceCache[id]=displayId;}
        }
        if(string.IsNullOrWhiteSpace(displayId)){Write(ctx,404,"application/json","{\"error\":\"Appearance not found\",\"id\":\""+JsonEscape(id)+"\"}");return;}
        Write(ctx,200,"application/json","{\"id\":\""+JsonEscape(id)+"\",\"displayId\":"+displayId+"}");
    }

    private static void HandleModelViewerProxy(HttpListenerContext ctx)
    {
        string localPath=ctx.Request.Url.AbsolutePath;
        if(!localPath.StartsWith("/modelviewer/classic/",StringComparison.OrdinalIgnoreCase)){Write(ctx,404,"text/plain","Not found");return;}
        string upstream="https://wow.zamimg.com"+localPath+(string.IsNullOrEmpty(ctx.Request.Url.Query)?"":ctx.Request.Url.Query);
        try{
            var req=(HttpWebRequest)WebRequest.Create(upstream);req.Method="GET";req.Proxy=null;req.AllowAutoRedirect=true;req.UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) WarRoom/'''+version+r'''";req.Accept="*/*";req.Referer="https://www.wowhead.com/";req.AutomaticDecompression=DecompressionMethods.GZip|DecompressionMethods.Deflate;
            using(var resp=(HttpWebResponse)req.GetResponse())using(var input=resp.GetResponseStream()){
                ctx.Response.StatusCode=(int)resp.StatusCode;
                ctx.Response.ContentType=string.IsNullOrWhiteSpace(resp.ContentType)?"application/octet-stream":resp.ContentType;
                ctx.Response.Headers["Access-Control-Allow-Origin"]="*";
                ctx.Response.Headers["Cache-Control"]="public, max-age=3600";
                if(resp.ContentLength>=0)ctx.Response.ContentLength64=resp.ContentLength;
                input.CopyTo(ctx.Response.OutputStream);ctx.Response.OutputStream.Close();
            }
        }catch(WebException ex){var r=ex.Response as HttpWebResponse;int status=r==null?502:(int)r.StatusCode;Write(ctx,status,"application/json","{\"error\":\""+JsonEscape(ex.Message)+"\",\"stage\":\"modelviewer-proxy\"}");}
    }

'''
s=s.replace(anchor,methods+anchor,1)

required=['/item-appearance','/modelviewer/classic/','HandleItemAppearance','HandleModelViewerProxy','modelViewerProxy','itemAppearances','exitTimer','HasExited']
for marker in required:
    if marker not in s: raise RuntimeError('launcher patch missing '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v'+version+' native launcher proxy + clean-shutdown patch complete')
