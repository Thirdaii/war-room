from pathlib import Path
import re,sys
p=Path(sys.argv[1]) if len(sys.argv)>1 else Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')

def once(old,new,label):
    global s
    if old not in s: raise RuntimeError('v1.7.26 launcher patch missing '+label)
    s=s.replace(old,new,1)

once('private static readonly Dictionary<string,string> EnchantmentCache = new Dictionary<string,string>();','private static readonly Dictionary<string,string> EnchantmentCache = new Dictionary<string,string>();\n    private static readonly Dictionary<string,string> ItemAppearanceCache = new Dictionary<string,string>();','appearance cache')
once('private static readonly object EnchantmentLock = new object();','private static readonly object EnchantmentLock = new object();\n    private static readonly object ItemAppearanceLock = new object();','appearance lock')
once('if(path.Equals("/enchantment",StringComparison.OrdinalIgnoreCase)){HandleEnchantment(ctx);return;}','if(path.Equals("/enchantment",StringComparison.OrdinalIgnoreCase)){HandleEnchantment(ctx);return;}\n            if(path.Equals("/item-appearance",StringComparison.OrdinalIgnoreCase)){HandleItemAppearance(ctx);return;}','appearance route')
s=s.replace('"version\\\":\\\"1.7.25','"version\\\":\\\"1.7.26').replace('WarRoom/1.7.25','WarRoom/1.7.26')
once('\\\"enchantments\\\":true}', '\\\"enchantments\\\":true,\\\"itemAppearances\\\":true}', 'health capability')
needle='    private static void ServeStatic(HttpListenerContext ctx,string requestPath)'
method=r'''    private static void HandleItemAppearance(HttpListenerContext ctx)
    {
        string id=(ctx.Request.QueryString["id"]??"").Trim();
        if(!ValidId(id)){Write(ctx,400,"application/json","{\"error\":\"Invalid item id\"}");return;}
        string json=null; lock(ItemAppearanceLock){ItemAppearanceCache.TryGetValue(id,out json);}
        if(string.IsNullOrWhiteSpace(json))
        {
            try
            {
                using(var wc=WowClient("text/html,application/xhtml+xml,*/*"))
                {
                    string html=wc.DownloadString("https://www.wowhead.com/tbc/item="+id);
                    string displayId="";
                    string[] patterns={
                        @"displayid\s*[:=]\s*[\""']?(\d+)",
                        @"displayId\s*[:=]\s*[\""']?(\d+)",
                        @"display_id\s*[:=]\s*[\""']?(\d+)",
                        @"itemDisplayInfoId\s*[:=]\s*[\""']?(\d+)"
                    };
                    foreach(string pattern in patterns){var m=Regex.Match(html??"",pattern,RegexOptions.IgnoreCase);if(m.Success&&ValidId(m.Groups[1].Value)){displayId=m.Groups[1].Value;break;}}
                    if(!string.IsNullOrWhiteSpace(displayId)) json="{\"id\":\""+JsonEscape(id)+"\",\"displayId\":"+displayId+",\"source\":\"wowhead-tbc\"}";
                }
                if(!string.IsNullOrWhiteSpace(json))lock(ItemAppearanceLock){ItemAppearanceCache[id]=json;}
            }
            catch{}
        }
        if(string.IsNullOrWhiteSpace(json)){Write(ctx,404,"application/json","{\"error\":\"Appearance not found\",\"id\":\""+JsonEscape(id)+"\"}");return;}
        Write(ctx,200,"application/json",json);
    }

'''
once(needle,method+needle,'appearance handler insertion')
p.write_text(s,encoding='utf-8')
print('War Room v1.7.26 item appearance resolver patched into '+str(p))
