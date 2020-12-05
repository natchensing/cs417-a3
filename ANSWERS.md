## Observed behaviour

Describe in general words the observed behaviour of each of these servers and
how it affects the video playback experience. Then explain what you believe is
happening and what is causing the described behaviour.

* FUNKY A: THERE IS LAG, BUT NOT ENOUGH TO RUIN USER EXPERIENCE

* FUNKY B: NOTICEABLE LAG, ENOUGH TO NOTICE

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
|      B       |          16.0         |           9.0           |      55      | 147
|      C       |          25.1         |           0.0           |      89      | 231
|      D       |          13.5         |           11.6          |      98      | 123
|      E       |          25.1         |           0.0           |      1       | 231
|      F       |          25.1         |           0.0           |      1       | 231
|      G       |          19.3         |           5.8           |      42      | 178
|      H       |          25.1         |           0.0           |      1       | 231


## Result of analysis

Explain in a few words what you believe is actually happening based on the statistics above.

* FUNKY A:

* FUNKY B:

* FUNKY C: NO LOST PACKETS, JUST A LOT OF OUT OF ORDER PACKETS THAT ARRIVED AT WRONG TIME

* FUNKY D:

* FUNKY E:

* FUNKY F:

* FUNKY G:

* FUNKY H:
