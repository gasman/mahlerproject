	org 25000

	include "spectranet.inc"
	include "sockdefs.inc"

syncport	equ 1860

	jp get_ip  ; 25000
	jp F_opensocket ; 25003
	jp F_closesocket ; 25006
	jp F_wait ; 25009

get_ip
; get last byte of IP address
	ld de,ip_buffer
	ld hl,GET_IFCONFIG_INET
	call HLCALL
	ld a,(ip_buffer+3)
	ld c,a
	ld b,0
	ret

ip_buffer ds 4

; Open the socket and bind to a port.
F_opensocket:
    call PAGEIN                 ; Spectranet ROM pagein

    ld c, SOCK_DGRAM            ; UDP socket
    call SOCKET
    jp c, J_error
    ld (syncsock), a

    ld de, syncport
    call BIND
    jp c, J_error

    jp PAGEOUT                  ; exit back to BASIC    

F_closesocket:
    call PAGEIN
    ld a, (syncsock)
    call CLOSE
    jp PAGEOUT

; Set the border to red to indicate an error.
J_error:
    ld c,a
    ld b,0
    ld a, 2
    out (254), a
    push bc
    call PAGEOUT
    pop bc
    ret

syncsock:   defb 0x00           ; Storage for socket handle
sockinfo:   defb 0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00
buffer:     defb 0x00,0x00

; Wait for a datagram to come in, and put the first 2 bytes of the 
; received datagram into BC
F_wait:
    call PAGEIN

catchup_lp
    ld a, (syncsock)
    call POLLFD
    bit 7,a ; check for error
    jp nz, J_error
    bit 2,a ; is there data waiting?
    jp z,catchup_done ; if not, we're ready to receive an actual timestamp

    ; if there is data buffered, consume it and throw it away
    call recv_packet
    jp c, J_error
    jp catchup_lp

catchup_done
    call recv_packet ; this is the real packet that reflects the current time
    jp c, J_error
    ld bc, (buffer)             ; BASIC gets this value from usr

    jp PAGEOUT

recv_packet
    ld a, (syncsock)
    ld hl, sockinfo
    ld de, buffer
    ld bc, 2
    jp RECVFROM               ; this will block until we get a datagram
