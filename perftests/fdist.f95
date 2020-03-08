PROGRAM kohonen
   !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
   !Programa inspirado em Artero(2012), Haykin(2001), Hertz(1990)               !
   !Autor: Victor Ribeiro Carreira                                              !
   !Este programa visa cumprir os requisitos para obtenção do título de Doutor  !
   !Identificação de Padrões Litológicos                                        !
   !                                                                            !
   !                          MAPAS DE KOHONEN                                  !
   !+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !$$$$$$$$$$$$$$$$$$$$$ DECLARAÇÃO DAS VARIÁVEIS GLOBAIS $$$$$$$$$$$$$$$$$$$$$!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   IMPLICIT NONE
   INTEGER, PARAMETER::SSP = SELECTED_INT_KIND(r=8)
   INTEGER, PARAMETER::DDP = SELECTED_REAL_KIND(8, 10)
   INTEGER(KIND=DDP):: ie, ij, nt, i, j, n_rep, ih, ig, nta, imenor, jmenor, ijmenor
   INTEGER(KIND=DDP):: nclass, ndclass
   REAL(KIND=DDP), ALLOCATABLE, DIMENSION(:, :, :):: a
   REAL(KIND=SSP), ALLOCATABLE, DIMENSION(:, :):: tr, tclass
   REAL(KIND=SSP), ALLOCATABLE, DIMENSION(:):: cl, cld, res1, res2
   REAL(KIND=SSP):: menor, c1min, c1max, c2min, c2max, c3min, c3max
   REAL(KIND=DDP):: c4min, c4max, a1, a2, a3, a4, a5, a6, b1, b2, b3, b4, d, inicio, fim
   CHARACTER(LEN=80):: cab, litologia

   ALLOCATE (a(20, 20, 10), res1(8), res2(8))

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !
   ! PARAMETROS DA SIMULACAO
   !
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

   ! Dimensoes do Tabuleiro
   nta = 40

   ! Numero de epocas
   n_rep = 1000 !10

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !
   ! Encontra parametros minimos e maximos da entrada
   !
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

   ! Arquivo 1
   OPEN (1, FILE='inputs/dados_sint_T1.txt')
   READ (1, 15) cab
   READ (1, 15) cab
   ij = 1
   DO WHILE (.true.)
      READ (1, *, end=10) litologia, a1, a2, a3, a4, a5, a6
      ij = ij + 1
   END DO
10 CONTINUE
   CLOSE (1)
   nt = ij - 1


   ! Arquivo 2
   OPEN (2, FILE='inputs/dados_sint_c1.txt')
   READ (2, 15) cab   !lê linha referente ao cabeçalho
   READ (2, 15) cab   !Lê linha em branco abaixo do cabeçalho

   ie = 1
   DO WHILE (.TRUE.)
      READ (2, *, END=8) litologia, a1, a2, a3, a4, a5, a6
      ie = ie + 1
   ENDDO
8  CONTINUE
   CLOSE (2)
   ndclass = ij - 1

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !
   ! Carrega a matriz de mostras do arquivo de entrada
   !
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   ALLOCATE (tr(1:nt, 4), cl(1:nt), tclass(1:nclass, 4), cld(1:nclass))

   OPEN (1, FILE='../inputs/dados_sint_T1.txt')

   READ (1, 15)
   READ (1, 15)

   DO i = 1, nt
      READ (1, *) litologia, cl(i), tr(i, 1), tr(i, 2), tr(i, 3), tr(1, 4)
   END DO
   CLOSE (1)

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !
   ! Inicia o Tabuleiro
   !
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   res1 = MINVAL(tr, DIM=1)
   res2 = MAXVAL(tr, DIM=1)

   c1min = res1(1)
   c1max = res2(1)

   c2min = res1(2)
   c2max = res2(2)

   c3min = res1(3)
   c3max = res2(3)

   c4min = res1(4)
   c4max = res2(4)

   DO i = 1, nta
      DO j = 1, nta
         a(i, j, 1) = rand()*(c1max - c1min) + c1min
         a(i, j, 2) = rand()*(c2max - c2min) + c2min 
         a(i, j, 3) = rand()*(c3max - c3min) + c3min 
         a(i, j, 4) = rand()*(c4max - c4min) + c4min 
         a(i, j, 10) = 0d0 
      END DO
   END DO

   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !
   ! Calcula distancias `n_rep` vezes
   !
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   CALL CPU_TIME(inicio)

   ! Faz `n_rep` medicoes
   DO ih = 1, n_rep
      ! Para cada amostra de entrada
      DO ig = 1, nt
         menor = 1.d20
         ij = 1
         ! Para cada linha
         DO i = 1, nta
            ! Para cada coluna
            DO j = 1, nta
               a1 = a(i, j, 1)
               a2 = a(i, j, 2)
               a3 = a(i, j, 3)
               a4 = a(i, j, 4)

               b1 = tr(ig, 1)
               b2 = tr(ig, 2)
               b3 = tr(ig, 3)
               b4 = tr(ig, 4)

               CALL euclideana(a1, a2, a3, a4, b1, b2, b3, b4, d)
               IF (d .LT. menor) THEN
                  menor = d
                  imenor = i
                  jmenor = j
                  ijmenor = ij
               END IF
            END DO
            ij = ij + 1
         END DO
      END DO
   END DO
   CALL CPU_TIME(fim)
   PRINT *, 'Por loop', (fim - inicio)/(n_rep), 's'
   PRINT *, 'Total   ', (fim-inicio), 's'



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
! Subrotinas e formatos
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

15 FORMAT(A71)

CONTAINS

   SUBROUTINE Euclideana(a1, a2, a3, a4, b1, b2, b3, b4, d)
      IMPLICIT NONE
      REAL(KIND=DDP), INTENT(IN)::a1, a2, a3, a4, b1, b2, b3, b4
      REAL(KIND=DDP), INTENT(OUT):: d

      d = SQRT((a1 - b1)**2 + (a2 - b2)**2 + (a3 - b3)**2 + (a4 - b4)**2)

   END SUBROUTINE Euclideana

END PROGRAM kohonen
