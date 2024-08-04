<h1>Fullstack Service Networking Season.2 <br />PySimpleGUI Chatting (N:M) Client & Server Program</h1>	

Server : Python (aioquic)<br />
> quic_chat 서버를 사용함 (alpn 서비스 식별자만 수정함)

Client : GUI Desktop Application (Python + aioquic & PySimpleGUI)<br />
> Simple Loopback Procotol Client 기반으로 개발됨

Networking : QUIC

Packaging : Poetry (추가 패키지: aioquic, PySimpleGUI)

<br />
<br />

<h2>실행 방법</h2>	

프로젝트를 다운로드 함

폴더안에서 poetry shell를 실행함<br />
> poetry shell

폴더안에서 필요한 패키지를 설치함<br />
> poetry install

src/server.py를 실행함<br />
> python server.py --certificate ../cert/server.crt --private-key ../cert/server.key --port 8053

복수의 src/client.py를 동시에 실행함<br />
> python client.py --ca-certs ../cert/server.crt --port 8053

Poetry 실행을 중지함<br />
> exit

<br />
<br />

<h2>수정 방법</h2>	

Server
> step.1: 개발할 프로토콜을 lib/server_lib_chattingprotocol.py 처럼 개발함<br />
> step.2: server.py 코드의 [SHOULD BE MODIFIED] 부분을 step.1에 맞춰서 수정함<br />
> step.3: 코드를 실행함

Client 
> step.1: 개발할 프로토콜을 lib/client_lib_chattingprotocol.py 처럼 개발함<br />
> step.2: client.py 코드의 [SHOULD BE MODIFIED] 부분을 step.1에 맞춰서 수정함<br />
> step.3: 코드를 실행함

<br />
<br />

<h2>실행 화면</h2>	

<img src="/screen/client-1.png" width="1000"/>

<img src="/screen/client-2.png" width="1000"/>

<img src="/screen/client-3.png" width="1000"/>

<img src="/screen/server.png" width="1000"/>

<img src="/screen/client-4.png" width="1000"/>
