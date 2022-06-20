all: run.zx player.zx

run.zx: run.bas
	zmakebas -a 10 -n run -o run.zx run.bas

player.zx: player.asm
	pasmo --tap player.asm player.zx
