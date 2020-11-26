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
   INTEGER, PARAMETER::DDP = SELECTED_REAL_KIND(8,10)
   INTEGER(KIND=DDP), ALLOCATABLE, DIMENSION(:,:,:):: V
   INTEGER(KIND=DDP):: cn, ie, ij, nt, i, j, n_rep, ih, ig, irr, nta, imenor, jmenor, ijmenor, il, ic, ind
   INTEGER(KIND=DDP):: icod, iprof, nclass, ierro, ndclass
   REAL(KIND=DDP), ALLOCATABLE, DIMENSION(:,:,:):: a
   REAL(KIND=SSP), ALLOCATABLE, DIMENSION(:,:):: tr, tclass, RG, XX, G
   REAL(KIND=SSP), ALLOCATABLE, DIMENSION(:):: cl, cld, res1, res2
   REAL(KIND=SSP):: menor, k1, k2, c1min, c1max, c2min, c2max, c3min, c3max, prof
   REAL(KIND=DDP):: c4min, c4max, a1,a2, a3, a4, a5, a6, b1, b2, b3, b4, d, inicio, fim
   REAL(KIND=SSP):: somacon, soma, xxclasse
   CHARACTER(LEN=80):: cab, litologia, tic, L

   CALL CPU_TIME(inicio)

   ALLOCATE(V(20,20,8), a(20,20,10), xx(810,3), G(1000,20), res1(8), res2(8))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!$$$$$$$$$$$$ ALOCANDO OS ARQUIVOS DE ENTRADA E DE SAÍDA DA REDE $$$$$$$$$$$$$$!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!Entradas
   OPEN(1,FILE='../inputs/well/sint01/1/dados_sint_T1.txt')! Cria o arquivo dados-treinamento e armazena na unidade 1
   OPEN(2,FILE='../inputs/well/sint01/1/dados_sint_c1.txt')! Cria o arquivo entrada e armazena na unidade de memória 2
!Saidas
   OPEN(3,FILE='../outputs/saida1.txt')! Cria o arquivo saida1 e armazena na unidade 3. SOM1
   OPEN(4,FILE='../outputs/saida2.txt')! Cria o arquivo saida2 e armazena na unidade 4. SOM2
   OPEN(5,FILE='../outputs/saida3.txt')! Cria o arquivo saida3 e armazena na unidade 5. SOM3
   OPEN(7,FILE='../outputs/conv.txt')! Cria o arquivo de saída com os dados de convergência do modelo.
   OPEN(8,FILE='../outputs/classificacao.txt')! arquivo de classificacao final



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!$$$$$$$$$$$$$$$$$$$$$ LEITURA DOS ARQUIVOS DE ENTRADA $$$$$$$$$$$$$$$$$$$$$$!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

!!!! LEITURA DO ARQUIVO DE TREINAMENTO UNIDADE 1 !!!!


   READ(1,15) cab    ! cabeçalho
   !WRITE(6,15) cab
   READ(1,15) cab    ! linha em branco abaixo do cabeçalho
   !WRITE(6,15) cab

   ij=1 ! Atribui o valor 1 a variável ij
   DO WHILE (.true.) ! Inicia o laço condicinal. Faça enquanto verdade a leitura de
      READ(1,*,end=10) litologia, a1,a2,a3,a4,a5,a6  ! dados de treinamento, no formato livre, terminando na unidade de memória 10.! Armazena cl e tr a leitura das colunas 1,2,3,4
      ij=ij+1 ! Adiciona um valor a variável ij.
   END DO ! Finaliza o laço

10 CONTINUE !Continua o programa na unidade de memória 10
   CLOSE(1) !Fecha a unidade de memória 1

   nt=ij-1! A variável nt vai armazenar a contagem de linhas em ij. Fazendo a operação ij-1 obtem-se o número de dados de treinamento
   WRITE(6,*) "n de dados de treinamento=",nt ! Escreve na unidade de memória 6 (na tela), no formato livre, a variável nt



!!!!! LEITURA DO ARQUIVO DE ENTRADA UNIDADE 2 CLASSIFICAÇÂO!!!!

   READ(2,15) cab   !lê linha referente ao cabeçalho
   READ(2,15) cab   !Lê linha em branco abaixo do cabeçalho

   ie=1
   DO WHILE (.TRUE.)
      READ(2,*,END=8) litologia, a1,a2,a3,a4,a5,a6 !lê o miolo do dado e armazena nas variáveis
      ie=ie+1
   ENDDO
8  CONTINUE
   CLOSE(2)

   ndclass=ij-1
   WRITE(6,*)"N dados a serem classificados",ndclass

   ALLOCATE(tr(1:nt,4),cl(1:nt),tclass(1:nclass,4),cld(1:nclass))

   OPEN(1,FILE='../inputs/well/sint01/1/dados_sint_T1.txt')

   READ(1,15)
   READ(1,15)

   DO i=1,nt
      READ(1,*) litologia,cl(i),tr(i,1),tr(i,2),tr(i,3),tr(1,4)
   END DO
   CLOSE(1)



!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!$$$$$$$$$$$$$$$$$$$$$$$ CONSTRUÇÃO DO HIPERPLANO $$$$$$$$$$$$$$$$$$$$$$$!!!!
!!!!$$$$$$$$$$$$$$$$$$$$$ CONFIGURAÇÃO INICIAL RANDÔMICA $$$$$$$$$$$$$$$$$$$!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

   res1=MINVAL(tr,DIM=1)
   res2=MAXVAL(tr,DIM=1)


!Construção da geometria da rede (tabuleiro de vizinhos e competição)

   c1min=res1(1)! 2.05d0 ! Notação científica o número após o "d"indica o fator exponencial. Valor mínimo da propriedade 1
   c1max=res2(1)!3.66d0 ! Valor máximo da propriedade 1

   c2min=res1(2)!5.11d-1 ! Valor mínimo da propriedade 2
   c2max=res2(2)!8.38d0 ! Valor máximo da propriedade 2

   c3min=res1(3)!4.12d2 ! Valor mínimo da propriedade 3
   c3max=res2(3)!5.72d8 ! Valor máximo da propriedade 3

   c4min=res1(4)!4.61d0 ! Valor mínimo da propriedade 4
   c4max=res2(4)!5.88d0 ! Valor máximo da propriedade 4

   nta=20    ! número de neorônios em cada lado do tabuleiro

   !nta é a variável que representa a quantidade de neurônios

   PRINT*, 'numero de neoronios da rede=',nta**2

   ! Inicia o laço
   DO i=1,nta ! A geometria do tabuleiro. Faz o índice i variar de 1 até nta
      DO j=1,nta ! Faz o índice j variar de 1 até nta
         a(i,j,1)=rand()*(c1max-c1min)+c1min! Pega uma variável randômica que varia de 0 até 1 multiplica por uma janela de variação (delta) e soma com o valor mínimo e finalmente armazena na matriz A. A soma com o valor mínimo serve para quando o rand() for 0 se obter exatamente o valor mínimo.
         a(i,j,2)=rand()*(c2max-c2min)+c2min ! Repete a operação para a propriedade 2
         a(i,j,3)=rand()*(c3max-c3min)+c3min ! Repete a operação para a propriedade 3
         a(i,j,4)=rand()*(c4max-c4min)+c4min ! Repete a operação para a propriedade 4
         a(i,j,10)=0d0 ! Dimensão 10 indica se o neurônio é vencedor ou não. 1 vencedor 0 não-vencedor.
      END DO ! Final do primeiro laço
   END DO ! Final do segundo laço


! Determinação das vizinhanças do tabuleiro
! Criação do Hiperplano: v -> MATRIZ DE VIZINHANÇAS!!!!!!!! Define os índices i, j,
! Ele é composto por quatro vizinhos. E utiliza LÓGICA DE PONTEIROS!!!
!!! VIZINHANÇA DA ARESTA HORIZONTAL SUPERIOR
! Este bloco determina o vizinho que se localiza na aresta horizontal superior

   DO i=1,nta ! Inicia o laço que varia de 1 até nta (número de neurônios)
      v(1,i,1)=nta ! acima
      v(1,i,2)=i
      v(1,i,3)=1 !direita
      v(1,i,4)=i+1
      IF(i+1 == nta+1) THEN
         v(1,i,4)=1
      END IF
      v(1,i,5)=2 ! abaixo
      v(1,i,6)=i
      v(1,i,7)=1  !esquerda
      v(1,i,8)=i-1
      IF(i-1 == -1) THEN
         v(1,i,8)=nta
      END IF

!!! VIZINHAÇA DA ARESTA HORIZONTAL INFERIOR

      v(nta,i,1)=nta-1 ! acima
      v(nta,i,2)=i
      v(nta,i,3)=nta   !direito
      v(nta,i,4)=i+1
      IF(i+1 == nta+1) THEN
         v(nta,i,4)=1
      END IF
      v(nta,i,5)=1   ! abaixo
      v(nta,i,6)=i
      v(nta,i,7)=nta   ! esquerda
      v(nta,i,8)=i-1
      IF(i-1 == -1) THEN
         v(nta,i,8)=nta
      END IF

! vizinhança da aresta lateral esquerda

      v(i,1,1)=i-1  ! acima
      IF(i-1 == 0) THEN
         v(i,1,1)=nta
      END IF
      v(i,1,2)=1
      v(i,1,3)=i    ! a direita
      v(i,1,4)=2
      v(i,1,5)=i+1  ! abaixo
      IF(i+1 == nta+1) THEN
         v(i,1,5)=1
      END IF
      v(i,1,6)=1
      v(i,1,7)=i    ! a esquerda
      v(i,1,8)=nta

! vizinhanca da aresta lateral direita

      v(i,nta,1)=i-1  ! acima
      IF(i-1 == 0) THEN
         v(i,nta,1)=nta
      END IF
      v(i,nta,2)=nta
      v(i,nta,3)=i    ! a direita
      v(i,nta,4)=1
      v(i,nta,5)=i+1  ! abaixo
      IF(i+1 == nta+1) THEN
         v(i,nta,5)=1
      END IF
      v(i,nta,6)=nta
      v(i,nta,7)=i    ! a esquerda
      v(i,nta,8)=nta-1
   END DO

! vizinhancas no miolo

   DO i=2,nta-1
      DO j=2,nta-1
         v(i,j,1)=i-1 !acima
         v(i,j,2)=j
         v(i,j,3)=i ! a direita
         v(i,j,4)=j+1
         v(i,j,5)=i+1 ! abaixo
         v(i,j,6)=j
         v(i,j,7)=i ! a esquerda
         v(i,j,8)=j-1
      END DO
   END DO

!! fim da detrminacao das vizinhancas

!  Inicio do treinamento
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
   k1=0.9d0
   k2=0.1d0

   n_rep=1000 !1040
   d = 0.0d0

   DO ih=1,n_rep       !tempo !Laço do ih
      k1=1d0*(1d0-dfloat(ih)/dfloat(n_rep+1))
      k2=k1/1.2d0
!print*, 'k1=',k1
      DO ig=1,nt  !144  ! dados de treinamento   !!  Loop1
! busca pelo neoronio vitorioso
         menor=1.0d10  !deve ser um n�mero grande
         ij=1
         DO i=1,nta
            DO j=1,nta
               a1=a(i,j,1)
               a2=a(i,j,2)
               a3=a(i,j,3)
               a4=a(i,j,4)

               b1=tr(ig,1)
               b2=tr(ig,2)
               b3=tr(ig,3)
               b4=tr(ig,4)

               CALL euclideana(a1,a2,a3,a4,b1,b2,b3,b4,d)
               !print*, 'dist',i,j,ij,d
               IF(d.lt.menor) THEN
                  menor=d
                  imenor=i
                  jmenor=j
                  ijmenor=ij
               END IF
            END DO
            ij=ij+1
         END DO
      END DO ! ig
!print*, 'menor',menor
!print*, 'indices do menor',imenor,jmenor,ijmenor

! atualização do neuronio vitorioso
      a(imenor,jmenor,1)=a(imenor,jmenor,1)+k1*(tr(ig,1)-a(imenor,jmenor,1))
      a(imenor,jmenor,2)=a(imenor,jmenor,2)+k1*(tr(ig,2)-a(imenor,jmenor,2))
      a(imenor,jmenor,3)=a(imenor,jmenor,3)+k1*(tr(ig,3)-a(imenor,jmenor,3))
      a(imenor,jmenor,4)=a(imenor,jmenor,4)+k1*(tr(ig,4)-a(imenor,jmenor,4))
      a(imenor,jmenor,9)=cl(ig)
      a(imenor,jmenor,10)=1d0
!print*, 'a(imenor,jmenor,9)',a(imenor,jmenor,9)
!atualização das vizinhancas

! vizinhança acima
      il=v(imenor,jmenor,1)
      ic=v(imenor,jmenor,2)
!print*, 'il=',il
!print*, 'ic=',ic
!if(il-1 == 0)then
!il=9
!end if

      a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
      a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
      a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
      a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))

      !a(il,ic,9)=cl(ig)

!!!!!!!!!!!!!!!!!!!!!!!!!!!

! vizinhança a direita
      il=v(imenor,jmenor,3)
      ic=v(imenor,jmenor,4)
      !print*, 'il=',il
      !print*, 'ic=',ic
      !if(ic == 10)then
      !ic=1
      !end if
      a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
      a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
      a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
      a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))
      !a(il,ic,9)=cl(ig)  ! ????
      !!!!!!!!!!!!!!!!!!!!!!!!!!!

! vizinhança abaixo
      il=v(imenor,jmenor,5)
      ic=v(imenor,jmenor,6)
!print*, 'il=',il
!print*, 'ic=',ic
!if(il-1 == 9)then
!il=1
!end if
      a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
      a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
      a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
      a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))
      !a(il,ic,9)=cl(ig)  ! ????
      ! vizinhança a esquerda
      il=v(imenor,jmenor,7)
      ic=v(imenor,jmenor,8)
      !print*, 'il=',il
      !print*, 'ic=',ic
      !if(ic == -1)then
      !ic=9
      ! end if
      a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
      a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
      a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
      a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))
      !a(il,ic,9)=cl(ig)  ! ????

      somacon=0d0
      DO irr=1,nt
         ind=irr
         menor=1.d20  !deve ser um número grande
         ij=1
         DO i=1,nta
            DO j=1,nta
               a1=a(i,j,1)
               a2=a(i,j,2)
               a3=a(i,j,3)
               a4=a(i,j,4)

               b1=tr(ind,1)
               b2=tr(ind,2)
               b3=tr(ind,3)
               b4=tr(ind,4)

               CALL euclideana(a1,a2,a3,a4,b1,b2,b3,b4,d)

               IF(d.LT.menor) THEN
                  menor=d
                  imenor=i
                  jmenor=j
                  ijmenor=i
               END IF
               ij=ij+1
            END DO
         END DO

         IF(a(imenor,jmenor,9).ne.cl(ind)) THEN
            somacon=somacon+1d0
         END IF


         WRITE(7,*)ih,somacon

      END DO   !loop do irr  (repetições do treinamento)
   END DO   ! loop do ih (dados de treinamento)

!UUUUUUUUUUUUUUUUUUUUUUUUUU
! Usando a rede para construir o arquivo com a covergência
! do treinamento da rede


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! final do loop de treinamento
! contagem dos neorônios vitoriosos
   soma=0d0

   DO i=1,nta
      DO j=1,nta
         soma=soma+a(i,j,10)
      END DO
   END DO
   PRINT*, 'neorônios vitoriosos=', soma

! contagem dos neorônios sem uso

   soma=0d0
   DO i=1,nta
      DO j=1,nta
         IF(a(i,j,1).eq. 0d0) THEN
            soma=soma+1
         END IF
      END DO
   END DO
   PRINT*, 'neorônios sem uso =', soma

!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2

!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

! mapeamento dos neoronios vitoriosos
   cn=10  ! o elemento a(i,j,10) vale 1 se o neoronio for vitorioso
   DO i=1,nta
      WRITE (3,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
   END DO

!!!!!!!!!!!!!!!!!!!!!!!!!

! mapeamento das classes do neoronios vitoriosos
   cn=9 ! classe do vitorioso
   DO i=1,nta
      WRITE(4,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
   END DO

!!!!!!!!!!!!!!!!!!!!!!!!

! mapeamento dos valores das propriedades dos neoronios vitoriosos
   cn=1 ! classe do vitorioso Pode variar de 1 at� 4
   DO i=1,nta
      WRITE(5,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
   END DO


!!!!!!!!!!!!!!!111 final do treinamento


   pause
!!!!!!!!!!!!!!!!    Usando a rede   fluxograma 3

   OPEN(2,FILE='../inputs/well/sint01/1/dados_sint_c1.txt')


   READ(2,15) cab !cabeçalho
   !WRITE(6,15) cab
   READ(2,15) cab ! linha em branco em baixo da caceta do cabeçalho
   !WRITE(6,15) cab

   DO i=1,ndclass
      READ(2,*) litologia, cld(i), prof, tclass(i,1),tclass(i,2),tclass(i,3), tclass(i,4)
   END DO
   CLOSE(2)



   ierro=0
   DO irr=1,nclass
      ind=irr
      menor=1.d20  !deve ser um número grande
      ij=1
      DO i=1,nta
         DO j=1,nta
            a1=a(i,j,1)
            a2=a(i,j,2)
            a3=a(i,j,3)
            a4=a(i,j,4)

            b1=tclass(ind,1)
            b2=tclass(ind,2)
            b3=tclass(ind,3)
            b4=tclass(ind,4)

            CALL euclideana(a1,a2,a3,a4,b1,b2,b3,b4,d)

            IF(d.LT.menor) THEN
               menor=d
               imenor=i
               jmenor=j
               ijmenor=ij
            END IF

            ij=ij+1

         END DO
      END DO

      xxclasse=a(imenor,jmenor,9)

      IF(xxclasse .EQ. cld(ind)) THEN
         tic="joinha"
      ELSE
         ierro=ierro+1
         tic="vacilou. deu mole. perdeu."
      END IF
      WRITE(8,*) ind,'classe=',xxclasse,'=',cld(ind),'--',tic
   END DO

   PRINT*,'numero de erros=',ierro, '   ', 100d0*ierro/ndclass,'%'

   CALL CPU_TIME(fim)
   PRINT*,'Tempo de máquina=', fim-inicio , 'segundos'

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ FORMATOS UTILIZADOS $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

11 FORMAT(10(ES12.4E3,2x))
12 FORMAT(I3,2x,3(f6.2,2x))
13 FORMAT(4(ES12.4E3,2x))
14 FORMAT(4(ES9.2E2,2x))
15 FORMAT(A71)
16 FORMAT(A11,8(ES9.2E3))
17 FORMAT(A30,2x,ES12.4E3)
18 FORMAT(2(f6.2,2x),2x,A11,2x,ES12.4E3)

! cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
! c	LEITURA DOS DADOS REAIS
! cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc



   print*,' ************ FIM *************'
   print*,''

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!$$$$$$$$$$$$$$$$$$$$$ SUBROTINAS $$$$$$$$$$$$$$$$$$$$$$!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

CONTAINS

   SUBROUTINE Euclideana(a1,a2,a3,a4,b1,b2,b3,b4,d)
      IMPLICIT NONE
      REAL(KIND=DDP), INTENT(IN)::a1,a2,a3,a4,b1,b2,b3,b4
      REAL(KIND=DDP), INTENT(OUT):: d


      d=SQRT((a1-b1)**2+(a2-b2)**2+(a3-b3)**2+(a4-b4)**2)


   END SUBROUTINE Euclideana


   SUBROUTINE INVERT(A,i)
      IMPLICIT NONE
      REAL(KIND=DDP):: A(i,j), B(i)
      INTEGER:: i,im,j,k,l

      !real*8 A(i,i),B(i)
      !integer*4 i,im,j,k,l
      IM=I-1
      DO 5 K=1,I
         DO 2 J=1,IM
2        B(J)=A(1,J+1)/A(1,1)
         B(I)=1.d0/A(1,1)
         DO 4 L=1,IM
            DO 3 J=1,IM
3           A(L,J)=A(L+1,J+1)-A(L+1,1)*B(J)
4        A(L,I)=-A(L+1,1)*B(I)
         DO 5 J=1,I
5     A(I,J)=B(J)
      RETURN

   END SUBROUTINE INVERT

END PROGRAM kohonen
