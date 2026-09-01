from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
MARK='WarRoomRosterV25'
if MARK in s:
    print('V25 current ClassicArmory roster API already installed')
    raise SystemExit(0)
if 'HandleGuildRoster' not in s or 'WarRoomRosterV24' not in s:
    raise RuntimeError('V21-V24 live roster launcher patches must run before V25')

# ClassicArmory's current site loads guild data from this JSON POST API.  The
# old V21 path scraped EpicForge HTML, whose guild snapshot can be months old.
# Keep the old sources only as degraded fallbacks; try the current roster API
# first and pass its JSON through unchanged for the V25 frontend normalizer.
strip_anchor='    private static string StripHtml(string html)'
post_method=r'''    private static string PostJsonText(string url,string json)
    {
        byte[] body=Encoding.UTF8.GetBytes(json??"{}");
        var req=(HttpWebRequest)WebRequest.Create(url);
        req.Method="POST";req.Proxy=null;req.AllowAutoRedirect=true;
        req.Timeout=10000;req.ReadWriteTimeout=10000;
        req.UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) WarRoom/1.7.28";
        req.Accept="application/json,*/*";req.ContentType="application/json; charset=utf-8";
        req.Headers[HttpRequestHeader.AcceptLanguage]="en-US,en;q=0.9";
        req.AutomaticDecompression=DecompressionMethods.GZip|DecompressionMethods.Deflate;
        req.ContentLength=body.Length;
        using(var rs=req.GetRequestStream())rs.Write(body,0,body.Length);
        using(var resp=(HttpWebResponse)req.GetResponse())using(var stream=resp.GetResponseStream())using(var sr=new StreamReader(stream,Encoding.UTF8,true))return sr.ReadToEnd();
    }

'''
if strip_anchor not in s:
    raise RuntimeError('V25 StripHtml anchor missing')
s=s.replace(strip_anchor,post_method+strip_anchor,1)

urls_anchor='''        string[] urls={\n'''
if urls_anchor not in s:
    raise RuntimeError('V25 guild source anchor missing')
classic_block=r'''        string classicError="";
        try
        {
            const string WarRoomRosterV25="classic-armory-current-post-api";
            string classicBody=PostJsonText("https://classic-armory.org/api/v1/guild","{\"region\":\"us\",\"realm\":\"dreamscythe\",\"name\":\"Me Not That Kind Of Orc\",\"flavor\":\"tbc-anniversary\"}");
            if(!string.IsNullOrWhiteSpace(classicBody)&&classicBody.IndexOf("\"roster\"",StringComparison.OrdinalIgnoreCase)>=0&&classicBody.IndexOf("\"guild\"",StringComparison.OrdinalIgnoreCase)>=0)
            {
                lock(GuildRosterLock){GuildRosterCacheJson=classicBody;GuildRosterCacheAtUtc=DateTime.UtcNow;}
                ctx.Response.Headers["X-WarRoom-Roster"]="live";
                ctx.Response.Headers["X-WarRoom-Roster-Source"]="ClassicArmory.org";
                Write(ctx,200,"application/json; charset=utf-8",classicBody);return;
            }
            classicError="ClassicArmory.org returned an unexpected guild payload";
        }
        catch(Exception ex){classicError="ClassicArmory.org: "+ex.Message;}

'''
s=s.replace(urls_anchor,classic_block+urls_anchor,1)
# If all degraded fallbacks fail, retain the current-source failure in detail.
s=s.replace('string[] sources={"EpicForge.au","ClassicArmory.gg","ClassicArmory.gg"};string lastError="";',
            'string[] sources={"EpicForge.au","ClassicArmory.gg","ClassicArmory.gg"};string lastError=classicError;',1)

for marker in [MARK,'classic-armory.org/api/v1/guild','classic-armory-current-post-api','PostJsonText','X-WarRoom-Roster-Source"]:
    if marker not in s:
        raise RuntimeError('V25 current roster marker missing: '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 V25 current ClassicArmory roster API installed')
