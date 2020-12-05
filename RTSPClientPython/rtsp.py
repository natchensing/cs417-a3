import io, socket
import random
import re
from threading import Thread
from time import sleep
import _thread

class RTSPException(Exception):
    def __init__(self, response):
        super().__init__(f'Server error: {response.message} (error code: {response.response_code})')

class Response:
    def __init__(self, reader):
        '''Reads and parses the data associated to an RTSP response'''
        first_line = reader.readline().split(' ', 2)
        if len(first_line) != 3:
            raise Exception('Invalid response format. Expected first line with version, code and message')
        self.version, _, self.message = first_line
        if self.version != 'RTSP/1.0':
            raise Exception('Invalid response version. Expected RTSP/1.0')
        self.response_code = int(first_line[1])

        while True:
            line = reader.readline().strip()
            if not line or ':' not in line: break
            hdr_name, hdr_value = line.split(':', 1)
            self.headers[hdr_name.lower()] = hdr_value
            if hdr_name.lower() == 'cseq':
                self.cseq = int(hdr_value)
            elif hdr_name.lower() == 'session':
                self.session_id = int(hdr_value)

        if self.response_code != 200:
            raise RTSPException(self)

class Connection:
    BUFFER_LENGTH = 0x10000
    # STATES
    INIT = 0
    READY = 1
    PLAYING = 2
    # COMMANDS
    SETUP = 0
    PLAY = 1
    PAUSE = 2
    TEARDOWN = 3
    SESSION_PATTERN = r".*Session: (\d+)"
    RTSP_PATTERN = r"RTSP/1.0 (\d+) ([a-zA-Z]+)"
    RTP_SOFT_TIMEOUT = 5

    def __init__(self, session, address):
        '''Establishes a new connection with an RTSP server. No message is
	sent at this point, and no stream is set up.
        '''
        self.session = session
        # TODO
        self.state = self.INIT
        self.fileName = None
        self.seqNum = 0
        self.sessionNum = 0
        self.address = address[0]
        self.portNum = int(address[1])
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_sock = None
        self.timeStamps = {}
        self.dataBuffer = {}
        self.t = None
        # CONNECT TO SERVER
        try:
            self.socket.connect((self.address, self.portNum))
        except:
            print('Connection to port \'%s\' failed.' %self.portNum)
            return

        print("[SUCCESS] Connection established.")

    def send_request(self, command, include_session=True, extra_headers=None):
        '''Helper function that generates an RTSP request and sends it to the
        RTSP connection.
        '''
        # TODO
        self.seqNum += 1
        if command == self.SETUP and self.state == self.INIT:
            request = "SETUP " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + str(self.seqNum) + "\r\n" + "Transport: RTP/UDP; client_port= " + str(self.data_port) + "\r\n\r\n"
            pass
        elif command == self.PLAY and self.state == self.READY:
            request = "PLAY " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + str(self.seqNum) + "\r\n" + "Session: " + str(self.sessionNum) + "\r\n\r\n"
            pass
        elif command == self.PAUSE and self.state == self.PLAYING:
            request = "PAUSE " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + str(self.seqNum) + "\r\n" + "Session: " + str(self.sessionNum) + "\r\n\r\n"
            pass
        elif command == self.TEARDOWN and self.state != self.INIT:
            request = "TEARDOWN " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + str(self.seqNum) + "\r\n" + "Session: " + str(self.sessionNum) + "\r\n\r\n"
            pass
        else:
            print('Invalid command %s' %command)
            return
        req = bytes(request, 'utf-8')
        self.socket.send(req)
        print("Request sent: %s" %request)

    def start_rtp_timer(self):
        '''Starts a thread that reads RTP packets repeatedly and process the
	corresponding frame (method ). The data received from the
	datagram socket is assumed to be no larger than BUFFER_LENGTH
	bytes. This data is then parsed into its useful components,
	and the method `self.session.process_frame()` is called with
	the resulting data. In case of timeout no exception should be
	thrown.
        '''

        # TODO
        self.t = Thread(target = self.process_data)
        self.t.start()

    def stop_rtp_timer(self):
        '''Stops the thread that reads RTP packets'''

        # TODO
        self.t.join()

    def setup(self, filename):
        '''Sends a SETUP request to the server. This method is responsible for
	sending the SETUP request, receiving the response and
	retrieving the session identification to be used in future
	messages. It is also responsible for establishing an RTP
	datagram socket to be used for data transmission by the
	server. The datagram socket should be created with a random
	UDP port number, and the port number used in that connection
	has to be sent to the RTSP server for setup. This datagram
	socket should also be defined to timeout after 1 second if no
	packet is received.
        '''

        # TODO
        # print("setup triggered")
        if self.state != self.INIT:
            print("incorrect state")
            return
        self.fileName = filename
        # Create RTP datagram socket
        if self.data_sock is None:
            self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.data_port = random.randint(0, 65353)
            self.data_sock.bind((self.address, self.data_port))
            # self.data_sock.connect(self.address, self.data_port)
        # print("before send")
        self.send_request(self.SETUP)
        # Get and process reply
        buf = self.socket.recv(self.BUFFER_LENGTH)
        if not buf:
            print("nothing received")
            return
        reply = buf.decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.search(self.SESSION_PATTERN, reply)
        if session_match:
            self.sessionNum = session_match.group(1)
        self.state = self.READY

    def play(self):
        '''Sends a PLAY request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, starting the RTP timer responsible for
	receiving RTP packets with frames.
        '''

        # TODO
        if self.state != self.READY:
            print("incorrect state")
            return
        self.send_request(self.PLAY)
        # Get and process reply
        buf = self.socket.recv(self.BUFFER_LENGTH)
        if not buf:
            print("nothing received")
            return
        reply = buf.decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.search(self.SESSION_PATTERN, reply)
        if session_match:
            sessionNum = session_match.group(1)
            if sessionNum == self.sessionNum:
                self.start_rtp_timer()
        self.state = self.PLAYING

    def pause(self):
        '''Sends a PAUSE request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, cancelling the RTP thread responsible for
	receiving RTP packets with frames.
        '''

        # TODO
        if self.state != self.PLAYING:
            print("incorrect state")
            return
        self.send_request(self.PAUSE)
        # Get and process reply
        buf = self.socket.recv(self.BUFFER_LENGTH)
        if not buf:
            print("nothing received")
            return
        reply = buf.decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.search(self.SESSION_PATTERN, reply)
        if session_match:
            sessionNum = session_match.group(1)
            if sessionNum == self.sessionNum:
                self.stop_rtp_timer()
        self.state = self.READY

    def teardown(self):
        '''Sends a TEARDOWN request to the server. This method is responsible
	for sending the request, receiving the response and, in case
	of a successful response, closing the RTP socket. This method
	does not close the RTSP connection, and a further SETUP in the
	same connection should be accepted. Also this method can be
	called both for a paused and for a playing stream, so the
	timer responsible for receiving RTP packets will also be
	cancelled.
        '''

        # TODO
        if self.state == self.INIT:
            print("incorrect state")
            return
        self.send_request(self.TEARDOWN)

        buf = self.socket.recv(self.BUFFER_LENGTH)

        if not buf:
            print("nothing received")
            return
        reply = buf.decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.search(self.SESSION_PATTERN, reply)
        if session_match:
            sessionNum = session_match.group(1)
            if sessionNum == self.sessionNum:
                self.stop_rtp_timer()
        self.state = self.INIT

    def close(self):
        '''Closes the connection with the RTSP server. This method should also
	close any open resource associated to this connection, such as
	the RTP connection, if it is still open.
        '''

        # TODO
        self.socket.shutdown(socket.SHUT_RDWR)
        self.close()

    def check_rtsp_head(self, reply):
        '''Helper function to check if the rtsp header indicates successful transmisson'''
        resp_match = re.match(self.RTSP_PATTERN, reply)
        if not resp_match:
            return False
        if resp_match.group(1) and resp_match.group(2):
            return resp_match.group(1) == "200" and resp_match.group(2) == "OK"
        return False

    def process_data(self):
        self.data_sock.settimeout(self.RTP_SOFT_TIMEOUT / 1000.)
        while True:
            if self.state != self.PLAYING:
                sleep(self.RTP_SOFT_TIMEOUT/1000.)  # diminish cpu hogging
                continue
            packet = self.recv_rtp_packet()
            #print(len(packet))
            marker = packet[1] >> 7
            #print(marker)
            payloadType = (packet[1] << 1) >> 1
            #print(payloadType)
            seqNum = packet[2] * 256 + packet[3]
            timeStamp = packet[4] * 16777216 + packet[5] * 65536 + packet[6] *256 + packet[7]
            #print(seqNum)
            #print(timeStamp)
            self.timeStamps[seqNum] = timeStamp
            self.dataBuffer[seqNum] = packet[12:]
            self.session.process_frame(payloadType, marker, seqNum, timeStamp, packet[12:])

    def recv_rtp_packet(self):
        packet = bytes()
        while True:
            try:
                packet += self.data_sock.recv(self.BUFFER_LENGTH)
                if packet.endswith(b'\xff\xd9'):
                    break
            except socket.timeout:
                continue
        return packet
