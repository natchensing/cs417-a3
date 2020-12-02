import io, socket
import random
import re
from threading import Thread
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
    SESSION_PATTERN = r"Session: (\d+)"
    RTSP_PATTERN = r"RTSP/1.0 (\d+) ([a-zA-Z]+)"

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

        if command == self.SETUP:
            request = "SETUP " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + self.seqNum + "\r\n" + "Transport: RTP/UDP; client_port= " + self.data_port + "\r\n"
            pass
        elif command == self.PLAY:
            request = "PLAY " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + self.seqNum + "\r\n" + "Session: " + self.sessionNum + "\r\n"
            pass
        elif command == self.PAUSE:
            request = "PAUSE " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + self.seqNum + "\r\n" + "Session: " + self.sessionNum + "\r\n"
            pass
        elif command == self.TEARDOWN:
            request = "TEARDOWN " + self.fileName + " RTSP/1.0\r\n" + "CSeq: " + self.seqNum + "\r\n" + "Session: " + self.sessionNum + "\r\n"
            pass
        else:
            print('Invalid command %s' %command)
            return

        self.socket.send(request)
        print("Request sent: %s" %request)
        self.seqNum += 1

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

    def stop_rtp_timer(self):
        '''Stops the thread that reads RTP packets'''

        # TODO

    def setup(self):
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

        # Create RTP datagram socket
        if self.data_sock is None:
            self.data_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.data_port = random.randint(0, 65353)
            self.data_sock.bind(self.address, self.data_port)
            # self.data_sock.connect(self.address, self.data_port)

        self.send_request(self.SETUP)
        # Get and process reply
        reply = self.socket.recv(self.BUFFER_LENGTH).decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.match(self.SESSION_PATTERN, reply)
        if session_match:
            self.sessionNum = session_match.group(1) 

    def play(self):
        '''Sends a PLAY request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, starting the RTP timer responsible for
	receiving RTP packets with frames.
        '''

        # TODO
        self.send_request(self.PLAY)
        # Get and process reply
        reply = self.socket.recv(self.BUFFER_LENGTH).decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.match(self.SESSION_PATTERN, reply)
        if session_match:
            sessionNum = session_match(1)
            if sessionNum == self.sessionNum:
                self.start_rtp_timer()

    def pause(self):
        '''Sends a PAUSE request to the server. This method is responsible for
	sending the request, receiving the response and, in case of a
	successful response, cancelling the RTP thread responsible for
	receiving RTP packets with frames.
        '''

        # TODO
        self.send_request(self.PAUSE)
        # Get and process reply
        reply = self.socket.recv(self.BUFFER_LENGTH).decode("utf-8")
        if not self.check_rtsp_head(reply):
            print("transmission failed")
            print(reply)
            return
        session_match = re.match(self.SESSION_PATTERN, reply)
        if session_match:
            sessionNum = session_match(1)
            if sessionNum == self.sessionNum:
                self.stop_rtp_timer()

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

    def close(self):
        '''Closes the connection with the RTSP server. This method should also
	close any open resource associated to this connection, such as
	the RTP connection, if it is still open.
        '''

        # TODO

    def check_rtsp_head(self, reply):
        '''Helper function to check if the rtsp header indicates successful transmisson'''
        resp_match = re.match(self.RTSP_PATTERN, reply)
        if not resp_match:
            return False
        if resp_match.group(1) and resp_match.group(2):
            return resp_match.group(1) == "200" and resp_match.group(2) == "OK"
        return False

