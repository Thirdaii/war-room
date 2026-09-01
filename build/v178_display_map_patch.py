from pathlib import Path

p=Path('build/WarRoomLauncher.cs')
s=p.read_text(encoding='utf-8')

route_anchor='if(path.StartsWith("/modelviewer/",StringComparison.OrdinalIgnoreCase)){HandleModelViewerProxy(ctx);return;}'
route='if(path.StartsWith("/display-id-map/",StringComparison.OrdinalIgnoreCase)){HandleDisplayIdMap(ctx);return;}\n            '+route_anchor
if 'HandleDisplayIdMap(ctx)' not in s:
    if route_anchor not in s: raise RuntimeError('Model proxy route anchor missing')
    s=s.replace(route_anchor,route,1)

method_anchor='    private static void HandleModelViewerProxy(HttpListenerContext ctx)'
method=r'''    private static void HandleDisplayIdMap(HttpListenerContext ctx)
    {
        string path=ctx.Request.Url.AbsolutePath.Trim('/');
        string[] parts=path.Split('/');
        if(parts.Length!=3||!string.Equals(parts[0],"display-id-map",StringComparison.OrdinalIgnoreCase)||!ValidId(parts[1])||!ValidId(parts[2])){Write(ctx,400,"application/json","{\"error\":\"Invalid display-id map request\"}");return;}
        string upstream="https://wotlk.murlocvillage.com/api/items/"+Uri.EscapeDataString(parts[1])+"/"+Uri.EscapeDataString(parts[2]);
        try{
            using(var wc=WowClient("application/json, text/plain, */*")){
                string body=wc.DownloadString(upstream);
                if(string.IsNullOrWhiteSpace(body)){Write(ctx,502,"application/json","{\"error\":\"Empty display-id mapping response\"}");return;}
                ctx.Response.Headers["Access-Control-Allow-Origin"]="*";
                Write(ctx,200,"application/json; charset=utf-8",body);
            }
        }catch(WebException ex){var r=ex.Response as HttpWebResponse;int status=r==null?502:(int)r.StatusCode;Write(ctx,status,"application/json","{\"error\":\""+JsonEscape(ex.Message)+"\",\"stage\":\"display-id-map\"}");}
    }

'''
if 'private static void HandleDisplayIdMap' not in s:
    if method_anchor not in s: raise RuntimeError('Model proxy method anchor missing')
    s=s.replace(method_anchor,method+method_anchor,1)

for marker in ['/display-id-map/','HandleDisplayIdMap','wotlk.murlocvillage.com/api/items/']:
    if marker not in s: raise RuntimeError('Display-id proxy marker missing: '+marker)
p.write_text(s,encoding='utf-8')
print('War Room v1.7.28 same-origin WotLK display-id conversion proxy complete')
