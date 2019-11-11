;This file was created using Turing-Machine-Simulator by @tareqdandachi

 li a0, 11184810; value to return
 li a5, 51966; address of starting position of tape in memory
 mv a1, a5; current address in memory

 

      halt:
        lw a0, 0(a2)
        lw a1, 4(a2)
        ret
      