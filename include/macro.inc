.ifndef .L_MACRO_INC
.L_MACRO_INC:

.macro jlabel label
    glabel \label
.endm

.macro glabel label
    .global \label
    \label:
.endm

.macro dlabel label
    .global \label
    \label:
.endm

.endif
