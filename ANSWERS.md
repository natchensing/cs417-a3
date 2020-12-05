## Observed behaviour

Describe in general words the observed behaviour of each of these servers and
how it affects the video playback experience. Then explain what you believe is
happening and what is causing the described behaviour.

* FUNKY A: NOTHING NOTICEABLE

* FUNKY B: NOTICEABLE LAG

* FUNKY C: VIDEO JUMPS BACK AND FORTH

* FUNKY D: NOTICEABLE LAG AND VIDEO JUMPS BACK AND FORTH

* FUNKY E: VIDEO PLAYED AT TWICE THE SPEED

* FUNKY F: VIDEO PLAYED AT HALF SPEED

* FUNKY G: UNEVEN CHOPPINESS AND LAG, SLOWER THAN NORMAL

* FUNKY H: VIDEO FREEZES MOMENTARILY INTERMITTENTLY


## Statistics

You may add additional columns with more relevant data.

REGULAR STATS:
 - FRAME RATE: 25.108695652173914
 - PACKET LOSS RATE: 0.0       
 - OUT OF ORDER: 0
 - PACKETS RECEIVED: 231

| FUNKY SERVER | FRAME RATE (pkts/sec) | PACKET LOSS RATE (/sec) | OUT OF ORDER | packets received
|:------------:|-----------------------|-------------------------|--------------|
|      A       |          22.4         |           2.7           |      21      | 206
|      B       |          14.9         |           9.0           |      55      | 147
|      C       |          25.1         |           0.0           |      89      | 231
|      D       |          13.5         |           11.6          |      98      | 123
|      E       |          25.1         |           0.0           |      1       | 231
|      F       |          25.1         |           0.0           |      1       | 231
|      G       |          19.3         |           5.8           |      42      | 178
|      H       |          25.1         |           0.0           |      1       | 231


## Result of analysis

Explain in a few words what you believe is actually happening based on the statistics above.

* FUNKY A: EVEN WITH THE LOSS RATE AND OUT OF ORDER PACKETS, BUFFER IS STILL LARGE ENOUGH TO COMPENSATE

* FUNKY B: FEWER RTP PACKETS RECEIVED WHICH CAUSES LAGGING IN THE LATER HALF

* FUNKY C: NO LOST PACKETS, JUST A LOT OF OUT OF ORDER PACKETS THAT ARRIVED AT WRONG TIME

* FUNKY D: NUMBER OF PACKETS RECEIVED IS HALVED, BOTH DUE TO LOSING PACKETS AND OUT OF ORDER PACKETS

* FUNKY E: SERVER SENDS RTP PACKET FASTER THAN NORMAL

* FUNKY F: SERVER SENDS RTP PACKET SLOWER THAN NORMAL

* FUNKY G: SERVER SENDS RTP PACKET SLOWER AND WITH SOME OUT OF ORDER

* FUNKY H: CLIENT CAN'T KEEP UP WITH IDEAL PLAYBACK SPEED AT TIMES WHEN BUFFER GETS DEPLETED BECAUSE SERVER IS NOT SENDING THEM FAST ENOUGH
