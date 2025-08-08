L='port'
K=ValueError
C=open
A=print
import socket as E,ssl,json as F,concurrent.futures,re
G='speed.cloudflare.com'
H='/meta'
I='all.txt'
B='live.txt'
D=[]
def J(host,path,proxy):
	G=proxy;D=host;M=f"""GET {path} HTTP/1.1\r
Host: {D}\r
User-Agent: Mozilla/5.0\r
Connection: close\r
\r
""";H=G.get('ip',D);I=int(G.get(L,443));B=None
	try:
		N=ssl.create_default_context();B=E.create_connection((H,I),timeout=5);B=N.wrap_socket(B,server_hostname=D);B.sendall(M.encode());C=b''
		while True:
			J=B.recv(4096)
			if not J:break
			C+=J
		C=C.decode('utf-8',errors='ignore');Q,O=C.split('\r\n\r\n',1);return F.loads(O)
	except(F.JSONDecodeError,K):A(f"Error parsing JSON dari {H}:{I}")
	except(E.error,ssl.SSLError)as P:A(f"Error koneksi: {P}")
	finally:
		if B:B.close()
	return{}
def O(org_name):A=org_name;return re.sub('[^a-zA-Z0-9\\s]','',A)if A else A
def M(proxy_line):
	N='clientIp';B=proxy_line;B=B.strip()
	if not B:return
	try:
		E,F,T,U=B.split(',');P={'ip':E,L:F};I,C=[J(G,H,{}),J(G,H,P)]
		if I and C and I.get(N)!=C.get(N):Q=O(C.get('asOrganization'));R=C.get('country');M=f"{E},{F},{R},{Q}";A(f"CF PROXY LIVE!: {M}");D.append(M)
		else:A(f"CF PROXY DEAD!: {E}:{F}")
	except K:A(f"Format baris proxy tidak valid: {B}. Pastikan formatnya ip,port,country,org")
	except Exception as S:A(f"Error saat memproses proxy {B}: {S}")
C(B,'w').close()
A(f"File {B} telah dikosongkan sebelum proses scan dimulai.")
try:
	with C(I,'r')as N:P=N.readlines()
except FileNotFoundError:A(f"File tidak ditemukan: {I}");exit()
Q=50
with concurrent.futures.ThreadPoolExecutor(max_workers=Q)as R:S=[R.submit(M,A)for A in P];concurrent.futures.wait(S)
if D:
	with C(B,'w')as T:T.write('\n'.join(D)+'\n')
	A(f"Semua proxy aktif disimpan ke {B}")
A('Pengecekan proxy selesai.')