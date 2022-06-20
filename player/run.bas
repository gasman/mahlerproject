10 clear 24999
20 %\{0x6c}oad "player.zx"code
25 let m$=str$(usr 25000)
30 let f$=m$+".bip"
40 let a=26000
50 %aload\{0x20}f$ code a
52 randomize usr 25003
55 let t=0
57 print "machine ";m$;" ready!"
60 let l=peek a:if l=0 then let t=65535: goto 80
70 let p=peek (a+1):let a=a+2
80 let now=usr 25009:if now<t then goto 80
90 if now=65535 then randomize usr 25006:%cd "/":%\{0x6c}oad "boot.zx"
95 let fixlen=l+t-now
100 if p and fixlen>0 then beep fixlen*0.02,p-128
110 let t=t+l:goto 60
