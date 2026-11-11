"""Create explicitly synthetic, deterministic teaching evidence (no network access)."""
from pathlib import Path
import json,datetime,hashlib,struct,socket,zipfile
ROOT=Path(__file__).resolve().parent.parent
DEST=ROOT/'work'/'case-fixture';DEST.mkdir(exist_ok=True)
base=datetime.datetime(2026,9,1,10,0,tzinfo=datetime.timezone.utc)
def stamp(seconds):return (base+datetime.timedelta(seconds=seconds)).isoformat().replace('+00:00','Z')
events=[]
def event(i,seconds,dataset,action,outcome,src='10.77.0.12',**fields):
    e={'@timestamp':stamp(seconds),'event':{'id':f'CASE-M01-{i:02d}','dataset':dataset,'action':action,'outcome':outcome},'labels':{'case_id':'CASE-M01','synthetic':'true'},'host':{'name':'ubu01'},'source':{'ip':src},'destination':{'ip':'10.77.0.11'}}
    e.update(fields);events.append(e)
for i in range(1,7):event(i,i*5,'linux.auth','ssh_login','failure',user={'name':'trainee01'})
event(7,40,'linux.auth','ssh_login','success',user={'name':'trainee01'})
event(8,45,'linux.auth','ssh_login','success',src='10.77.0.99',user={'name':'maintainer'})
for i,secs,path,status in [(9,50,'/',200),(10,55,'/private.txt',404),(11,60,'/does-not-exist',404),(12,65,'/status',200)]:
    event(i,secs,'web.access','http_request','success' if status==200 else 'failure',url={'path':path},http={'response':{'status_code':status}})
event(13,70,'windows.process','process_start','success',process={'name':'cmd.exe','command_line':'cmd.exe /c echo CYBERLAB-M01'},host={'name':'win01'})
event(14,75,'windows.process','process_start','success',process={'name':'notepad.exe','command_line':'notepad.exe'},host={'name':'win01'})
event(15,80,'file.integrity','modified','success',file={'path':'/srv/labshare/case.txt'},change={'approved':True})
event(16,85,'file.integrity','baseline','success',file={'path':'/srv/labshare/case.txt'})
def lines(name,rows): (DEST/name).write_text(''.join(json.dumps(x,separators=(',',':'))+'\n' for x in rows),encoding='utf-8')
lines('events.ndjson',events)
bulk=[]
for e in events:bulk.extend([{'index':{'_id':e['event']['id']}},e])
lines('events.bulk.ndjson',bulk)
raw=[]
for e in events[:8]:raw.append({'event_time':e['@timestamp'],'event_id':e['event']['id'],'case_id':'CASE-M01','client_ip':e['source']['ip'],'username':e['user']['name'],'result':e['event']['outcome']})
lines('auth-input.ndjson',raw)
bad=dict(raw[0]);bad['event_time']='not-a-date';bad['event_id']='CASE-M01-BAD'
lines('auth-bad.ndjson',[bad])
(DEST/'http-access.log').write_text(''.join(f'10.77.0.12 - - [{(base+datetime.timedelta(seconds=secs)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET {path} HTTP/1.1" {status} 0 "-" "CyberLab-Synthetic"\n' for secs,path,status in [(50,'/',200),(55,'/private.txt',404),(60,'/does-not-exist',404),(65,'/status',200)]),encoding='utf-8')
def checksum(data):
    if len(data)%2:data+=b'\0'
    s=sum(struct.unpack('!%dH'%(len(data)//2),data));s=(s&65535)+(s>>16);s=(s&65535)+(s>>16)
    return (~s)&65535
packets=[]
def packet(t,src,dst,sport,dport,seq,ack,flags,payload=b''):
    sa,da=socket.inet_aton(src),socket.inet_aton(dst)
    tcp=struct.pack('!HHIIBBHHH',sport,dport,seq,ack,5<<4,flags,65535,0,0)
    pseudo=sa+da+struct.pack('!BBH',0,6,len(tcp)+len(payload))
    cs=checksum(pseudo+tcp+payload);tcp=tcp[:16]+struct.pack('!H',cs)+tcp[18:]
    ip=struct.pack('!BBHHHBBH4s4s',0x45,0,20+len(tcp)+len(payload),len(packets)+1,0x4000,64,6,0,sa,da)
    ip=ip[:10]+struct.pack('!H',checksum(ip))+ip[12:]
    eth=bytes.fromhex('0200000000110200000000120800') if src.endswith('.12') else bytes.fromhex('0200000000120200000000110800')
    packets.append((int(base.timestamp())+int(t),int((t-int(t))*1000000),eth+ip+tcp+payload))
for j,(t,path,status) in enumerate([(50,'/',200),(55,'/private.txt',404),(60,'/does-not-exist',404),(65,'/status',200)]):
    c,s='10.77.0.12','10.77.0.11';cp=45000+j;cs=1000+j*1000;ss=9000+j*1000
    req=f'GET {path} HTTP/1.1\r\nHost: lab.example.test\r\nUser-Agent: CyberLab-Synthetic\r\nConnection: close\r\n\r\n'.encode()
    res=f'HTTP/1.1 {status} {"OK" if status==200 else "Not Found"}\r\nContent-Length: 0\r\nConnection: close\r\n\r\n'.encode()
    packet(t,c,s,cp,80,cs,0,2);packet(t+.01,s,c,80,cp,ss,cs+1,18);packet(t+.02,c,s,cp,80,cs+1,ss+1,16)
    packet(t+.03,c,s,cp,80,cs+1,ss+1,24,req);packet(t+.04,s,c,80,cp,ss+1,cs+1+len(req),24,res)
    packet(t+.05,c,s,cp,80,cs+1+len(req),ss+1+len(res),17)
    packet(t+.06,s,c,80,cp,ss+1+len(res),cs+2+len(req),17)
    packet(t+.07,c,s,cp,80,cs+2+len(req),ss+2+len(res),16)
with (DEST/'web-case.pcap').open('wb') as f:
    f.write(struct.pack('<IHHIIII',0xa1b2c3d4,2,4,0,0,65535,1))
    for sec,usec,data in packets:f.write(struct.pack('<IIII',sec,usec,len(data),len(data))+data)
truth={'case':'CASE-M01','synthetic':True,'event_count':16,'dataset_counts':{'linux.auth':8,'web.access':4,'windows.process':2,'file.integrity':2},'ssh_failures_trainee01':6,'ssh_successes_total':2,'web_404':2,'windows_marker_events':1,'pcap_http_transactions':4,'pcap_packets':len(packets),'earliest':events[0]['@timestamp'],'latest':events[-1]['@timestamp'],'conclusion':'Synthetic failed logins followed by a success warrant review; they do not establish unauthorized access. Both missing-path requests returned 404. No real user, malware, credential theft, or exfiltration is present.'}
(DEST/'mentor-answer-key.json').write_text(json.dumps(truth,indent=2),encoding='utf-8')
(DEST/'README.txt').write_text('CASE-M01: SYNTHETIC TRAINING FIXTURE\nAll records and packets were authored for this course; none were captured from a real person or network. Fixed time: 2026-09-01 10:00:00 UTC. events.ndjson contains normalized teaching records, NOT native Sysmon EVTX, Wazuh output, or full ECS/CIM conformance. web-case.pcap is a synthetic Ethernet/IPv4/TCP capture of four HTTP requests and empty responses; it contains no executable or malware. Do not expect an IDS signature to fire on benign HTTP. The four web rows correspond to these requests; Linux authentication, Windows, and file rows are separate synthetic story elements and are not visible in that HTTP-only PCAP. Hash originals, preserve timestamps, and do not claim this fixture proves live collection. Read mentor-answer-key.json after your first investigation. Files are tiny to stay below trial ingestion limits.\n',encoding='utf-8')
files=sorted(DEST.iterdir())
(DEST/'SHA256SUMS').write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+f.name+'\n' for f in files if f.name!='SHA256SUMS'),encoding='utf-8')
out=ROOT/'outputs/security-foundations';out.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(out/'case-m01.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in sorted(DEST.iterdir()):z.write(f,'case-m01/'+f.name)
print('Built CASE-M01: 16 normalized events; 32 valid synthetic packet records.')
