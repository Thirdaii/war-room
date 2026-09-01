from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')
MARK='HandleGuildRoster'
if MARK in s:
    print('Live guild roster launcher patch already installed')
    raise SystemExit(0)

# cache fields
field_anchor='    private static readonly object ItemAppearanceLock = new object();'
fields='''    private static readonly object ItemAppearanceLock = new object();\n    private static readonly object GuildRosterLock = new object();\n    private static string GuildRosterCacheJson = null;\n    private static DateTime GuildRosterCacheAtUtc = DateTime.MinValue;'''
if field_anchor not in s: raise RuntimeError('ItemAppearanceLock anchor missing')
s=s.replace(field_anchor,fields,1)

# route
route_anchor='if(path.Equals("/armory",StringComparison.OrdinalIgnoreCase)){HandleArmory(ctx);return;}'
route=route_anchor+'\n            if(path.Equals("/guild-roster",StringComparison.OrdinalIgnoreCase)){HandleGuildRoster(ctx);return;}'
if route_anchor not in s: raise RuntimeError('armory route anchor missing')
s=s.replace(route_anchor,route,1)

# health marker after earlier v1.7.28 patches
s=s.replace('\\"modelViewerProxy\\":true}', '\\"modelViewerProxy\\":true,\\"guildRoster\\":true}', 1)

method_anchor='    private static void ServeStatic(HttpListenerContext ctx,string requestPath)'
if method_anchor not in s: raise RuntimeError('ServeStatic method anchor missing')
methods=r'''    private sealed class GuildMemberRow
    {
        public string Name="";
        public int Level=0;
        public string ClassName="";
        public string Race="";
        public string Rank="";
        public int GearScore=0;
    }

    private static string DownloadText(string url,string accept)
    {
        var req=(HttpWebRequest)WebRequest.Create(url);
        req.Method="GET";req.Proxy=null;req.AllowAutoRedirect=true;
        req.Timeout=8000;req.ReadWriteTimeout=8000;
        req.UserAgent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) WarRoom/1.7.28";
        req.Accept=accept;req.Headers[HttpRequestHeader.AcceptLanguage]="en-US,en;q=0.9";
        req.AutomaticDecompression=DecompressionMethods.GZip|DecompressionMethods.Deflate;
        using(var resp=(HttpWebResponse)req.GetResponse())using(var stream=resp.GetResponseStream())using(var sr=new StreamReader(stream,Encoding.UTF8,true))return sr.ReadToEnd();
    }

    private static string StripHtml(string html)
    {
        string x=html??"";
        x=Regex.Replace(x,"<script\\b[^>]*>.*?</script>"," ",RegexOptions.IgnoreCase|RegexOptions.Singleline);
        x=Regex.Replace(x,"<style\\b[^>]*>.*?</style>"," ",RegexOptions.IgnoreCase|RegexOptions.Singleline);
        x=Regex.Replace(x,"<br\\s*/?>"," ",RegexOptions.IgnoreCase);
        x=Regex.Replace(x,"<[^>]+>"," ",RegexOptions.Singleline);
        x=WebUtility.HtmlDecode(x);
        return Regex.Replace(x,"\\s+"," ").Trim();
    }

    private static string UrlPathName(string encoded)
    {
        string x=(encoded??"").Replace("+"," ");
        try{x=Uri.UnescapeDataString(x);}catch{}
        return WebUtility.HtmlDecode(x).Trim();
    }

    private static int ParseFirstInt(string text)
    {
        var m=Regex.Match(text??"","(?<![0-9])([0-9]{1,5})(?![0-9])");
        int n;return m.Success&&int.TryParse(m.Groups[1].Value,out n)?n:0;
    }

    private static string FindKnown(string text,string[] values)
    {
        string t=text??"";
        foreach(string v in values)if(Regex.IsMatch(t,"(?<![A-Za-z])"+Regex.Escape(v)+"(?![A-Za-z])",RegexOptions.IgnoreCase))return v;
        return "";
    }

    private static string ParseRank(string row,string cellText)
    {
        string c=StripHtml(cellText);
        if(!string.IsNullOrWhiteSpace(c)&&c.Length<40&&!Regex.IsMatch(c,"^(GS|BiS|Lv)\\b",RegexOptions.IgnoreCase))return c;
        var m=Regex.Match(StripHtml(row),"(Guild Master|Officer|Veteran|Initiate|Recruit|Member|Rank\\s+[0-9]+)",RegexOptions.IgnoreCase);
        if(!m.Success)return "Member";
        string r=m.Groups[1].Value;
        if(string.Equals(r,"guild master",StringComparison.OrdinalIgnoreCase))return "Guild Master";
        if(string.Equals(r,"officer",StringComparison.OrdinalIgnoreCase))return "Officer";
        if(string.Equals(r,"veteran",StringComparison.OrdinalIgnoreCase))return "Veteran";
        if(string.Equals(r,"initiate",StringComparison.OrdinalIgnoreCase))return "Initiate";
        if(string.Equals(r,"recruit",StringComparison.OrdinalIgnoreCase))return "Recruit";
        if(string.Equals(r,"member",StringComparison.OrdinalIgnoreCase))return "Member";
        return r;
    }

    private static void AddGuildRow(List<GuildMemberRow> rows,HashSet<string> seen,string name,int level,string cls,string race,string rank,int gs)
    {
        name=(name??"").Trim();cls=(cls??"").Trim();race=(race??"").Trim();rank=(rank??"").Trim();
        if(level!=70||string.IsNullOrWhiteSpace(name)||string.IsNullOrWhiteSpace(cls)||seen.Contains(name))return;
        seen.Add(name);rows.Add(new GuildMemberRow{Name=name,Level=70,ClassName=cls,Race=race,Rank=string.IsNullOrWhiteSpace(rank)?"Member":rank,GearScore=gs});
    }

    private static List<GuildMemberRow> ParseGuildRosterHtml(string html)
    {
        var rows=new List<GuildMemberRow>();var seen=new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        string[] classes={"Warrior","Paladin","Hunter","Rogue","Priest","Shaman","Mage","Warlock","Druid"};
        string[] races={"Blood Elf","Tauren","Undead","Troll","Orc","Human","Dwarf","Night Elf","Gnome","Draenei"};
        foreach(Match tr in Regex.Matches(html??"","<tr\\b[^>]*>(.*?)</tr>",RegexOptions.IgnoreCase|RegexOptions.Singleline))
        {
            string row=tr.Groups[1].Value;
            var hm=Regex.Match(row,"href=[\\\"'][^\\\"']*/character/(?:us/)?dreamscythe/([^\\\"'?#/]+)",RegexOptions.IgnoreCase);
            if(!hm.Success)continue;
            string name=UrlPathName(hm.Groups[1].Value),plain=StripHtml(row);
            int level=0;var lm=Regex.Match(plain,"(?:Lv|Level)\\s*([0-9]{1,2})",RegexOptions.IgnoreCase);if(lm.Success)int.TryParse(lm.Groups[1].Value,out level);
            var cells=Regex.Matches(row,"<td\\b[^>]*>(.*?)</td>",RegexOptions.IgnoreCase|RegexOptions.Singleline);
            if(level==0&&cells.Count>1)level=ParseFirstInt(StripHtml(cells[1].Groups[1].Value));
            string cls=FindKnown(plain,classes),race=FindKnown(plain,races),rank=cells.Count>4?ParseRank(row,cells[4].Groups[1].Value):ParseRank(row,"");
            int gs=0;if(cells.Count>5){var gm=Regex.Match(StripHtml(cells[5].Groups[1].Value),"(?:GS\\s*)?([0-9]{2,5})",RegexOptions.IgnoreCase);if(gm.Success)int.TryParse(gm.Groups[1].Value,out gs);}
            AddGuildRow(rows,seen,name,level,cls,race,rank,gs);
        }
        if(rows.Count>=10)return rows;
        // Card-based/server-rendered fallback: inspect a small neighborhood around each character link.
        foreach(Match hm in Regex.Matches(html??"","href=[\\\"'][^\\\"']*/character/(?:us/)?dreamscythe/([^\\\"'?#/]+)",RegexOptions.IgnoreCase))
        {
            string name=UrlPathName(hm.Groups[1].Value);if(seen.Contains(name))continue;
            int start=Math.Max(0,hm.Index-700),len=Math.Min((html??"").Length-start,1500);string frag=(html??"").Substring(start,len),plain=StripHtml(frag);
            int level=0;var lm=Regex.Match(plain,"(?:Lv|Level)\\s*([0-9]{1,2})",RegexOptions.IgnoreCase);if(lm.Success)int.TryParse(lm.Groups[1].Value,out level);
            string cls=FindKnown(plain,classes),race=FindKnown(plain,races),rank=ParseRank(frag,"");int gs=0;var gm=Regex.Match(plain,"GS\\s*([0-9]{2,5})",RegexOptions.IgnoreCase);if(gm.Success)int.TryParse(gm.Groups[1].Value,out gs);
            AddGuildRow(rows,seen,name,level,cls,race,rank,gs);
        }
        return rows;
    }

    private static string GuildRosterJson(List<GuildMemberRow> rows,string source,string upstream)
    {
        var sb=new StringBuilder();sb.Append("{\\\"source\\\":\\\"").Append(JsonEscape(source)).Append("\\\",\\\"upstream\\\":\\\"").Append(JsonEscape(upstream)).Append("\\\",\\\"fetchedAt\\\":\\\"").Append(JsonEscape(DateTime.UtcNow.ToString("o"))).Append("\\\",\\\"members\\\":[");
        for(int i=0;i<rows.Count;i++){
            if(i>0)sb.Append(',');var r=rows[i];sb.Append("{\\\"name\\\":\\\"").Append(JsonEscape(r.Name)).Append("\\\",\\\"rank\\\":\\\"").Append(JsonEscape(r.Rank)).Append("\\\",\\\"level\\\":70,\\\"class\\\":\\\"").Append(JsonEscape(r.ClassName)).Append("\\\",\\\"race\\\":\\\"").Append(JsonEscape(r.Race)).Append("\\\"");if(r.GearScore>0)sb.Append(",\\\"gearscore\\\":").Append(r.GearScore);sb.Append('}');
        }
        sb.Append("]}");return sb.ToString();
    }

    private static void HandleGuildRoster(HttpListenerContext ctx)
    {
        bool force=string.Equals(ctx.Request.QueryString["refresh"],"1",StringComparison.OrdinalIgnoreCase);
        lock(GuildRosterLock){if(!force&&!string.IsNullOrWhiteSpace(GuildRosterCacheJson)&&(DateTime.UtcNow-GuildRosterCacheAtUtc).TotalSeconds<120){ctx.Response.Headers["X-WarRoom-Roster"]="cache";Write(ctx,200,"application/json; charset=utf-8",GuildRosterCacheJson);return;}}
        string[] urls={
            "https://classicarmory.gg/guild/us/dreamscythe/me-not-that-kind-of-orc?ns=classicann",
            "https://classicarmory.gg/guild/us/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?ns=classicann",
            "https://epicforge.au/guild/dreamscythe/Me%20Not%20That%20Kind%20Of%20Orc?mode=anniversary"
        };
        string[] sources={"ClassicArmory.gg","ClassicArmory.gg","EpicForge.au"};string lastError="";
        for(int i=0;i<urls.Length;i++){
            try{
                string html=DownloadText(urls[i],"text/html,application/xhtml+xml,*/*");
                if(string.IsNullOrWhiteSpace(html)){lastError="empty response from "+sources[i];continue;}
                var rows=ParseGuildRosterHtml(html);
                if(rows.Count<10){lastError=sources[i]+" returned only "+rows.Count+" usable level 70 rows";continue;}
                string json=GuildRosterJson(rows,sources[i],urls[i]);lock(GuildRosterLock){GuildRosterCacheJson=json;GuildRosterCacheAtUtc=DateTime.UtcNow;}
                ctx.Response.Headers["X-WarRoom-Roster"]="live";Write(ctx,200,"application/json; charset=utf-8",json);return;
            }catch(Exception ex){lastError=sources[i]+": "+ex.Message;}
        }
        Write(ctx,502,"application/json","{\\\"error\\\":\\\"Live guild roster unavailable\\\",\\\"detail\\\":\\\""+JsonEscape(lastError)+"\\\",\\\"stage\\\":\\\"guild-roster\\\"}");
    }

'''
s=s.replace(method_anchor,methods+method_anchor,1)
for marker in ['/guild-roster','HandleGuildRoster','GuildRosterCacheJson','classicarmory.gg/guild/us/dreamscythe','epicforge.au/guild/dreamscythe','guildRoster']:
    if marker not in s: raise RuntimeError('live roster launcher marker missing: '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 live guild roster native proxy patch complete')
