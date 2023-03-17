    .text
.globl _asmMain
    .def _asmMain; .scl2; .type32; .endef
_asmMain:
    movl $1, %eax
    addl $4, %eax
    subl $2, %eax
    ret