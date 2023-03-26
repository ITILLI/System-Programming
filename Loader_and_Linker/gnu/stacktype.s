	.file	"stacktype.c"
	.text
	.globl	stack
	.bss
	.align 32
	.type	stack, @object
	.size	stack, 512
stack:
	.zero	512
	.globl	top
	.align 4
	.type	top, @object
	.size	top, 4
top:
	.zero	4
	.ident	"GCC: (Ubuntu 11.3.0-1ubuntu1~22.04) 11.3.0"
	.section	.note.GNU-stack,"",@progbits
	.section	.note.gnu.property,"a"
	.align 8
	.long	1f - 0f
	.long	4f - 1f
	.long	5
0:
	.string	"GNU"
1:
	.align 8
	.long	0xc0000002
	.long	3f - 2f
2:
	.long	0x3
3:
	.align 8
4:
