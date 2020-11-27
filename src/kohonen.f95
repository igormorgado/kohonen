! C     PROGRAMA - rede neural para identifica��o de litologia
! C     VARIAVEIS UTILIZADAS

! C	DEFINICAO DO TIPO DAS VARIAVEIS

 implicit real*8(a-h,o-z)
   real*8,allocatable::cl(:),tr(:,:),tclass(:,:),cld(:)
   real*8 menor,g(1000,120),a(120,120,10),xx(810,3),k1,k2,res1(4),res2(4)
   real*8 init
   REAL*8, DIMENSION(4):: xmin, xmax
   integer*4 v(120,120,12),cn
   character*11 L(4),tic
   character*80 cab, branco

! cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
! c	ARQUIVOS 
! cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc

!Entradas
open(1,FILE='../inputs/well/sint01/1/dados_sint_T1.txt')!dados-treinamento
open(2,FILE='../inputs/well/sint01/1/dados_sint_c1.txt')! dados de classific


!Saidas: mapas
open(3,file='../outputs/saida1.txt')
open(4,file='../outputs/saida2.txt') ! mapas: neur�nios visitados, props., e litos.
open(5,file='../outputs/saida3.txt')
!Saidas: converg�ncia e modelo classificado
open(7,file='../outputs/conv.txt')! converg�ncia
open(8,file='../outputs/classificacao.txt')  ! classificacao

!************************* INICIO *************************************************
CALL CPU_TIME(init)

! c       Leitura do arquivo de treinamento
read(1,15) cab    ! cabe�alho
!read(1,15) cab    ! linha em branco abaixo do cabe�alho. Retira-se essa linha do dado convolvido. 

ij=1
 do while (.true.)
  read(1,*,end=6) branco,a1,a2,a3,a4,a5,a6
  ij=ij+1
 end do
6 continue
 close(1)
nt=ij-1
write(6,*) "n de dados de treinamento",nt

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

! ccc	leitura do arquivo de entrada
! ccc	litologias a serem determinadas
read(2,15) cab    ! cabe�alho
!read(2,15) cab    ! linha em branco abaixo do cabe�alho
ij=1
 do while (.true.)
  read(2,*,end=7) branco,a1,a2,a3,a4,a5,a6
  ij=ij+1
 end do
7 continue
 close(2)

nclass=ij-1
write(6,*) "n de dados a serem classificados",nclass

! ALOCACAO DINAMICA;
allocate (tr(1:nt,4),cl(1:nt),tclass(1:nclass,4),cld(1:nclass))

open(1,file='../inputs/well/sint01/1/dados_sint_T1.txt')

read(1,15) cab    ! cabe�alho
!read(1,15) cab    ! linha em branco abaixo do cabe�alho

do i=1,nt
 read(1,*)branco,cl(i),prof,tr(i,1),tr(i,2),tr(i,3),tr(i,4)
end do
 close(1)

!!!!! LEITURA DOS DADOS DE CLASSIFICACAO PARA POSTERIOR NORMALIZACAO :
open(2,file='../inputs/well/sint01/1/dados_sint_c1.txt')
 read(2,15) cab    ! cabe�alho
! read(2,15) cab    ! linha em branco abaixo do cabe�alho
 
  do i=1,nclass
   read(2,*) branco,cld(i),prof,tclass(i,1),tclass(i,2),tclass(i,3),tclass(i,4)
  end do
  close(2)

! CRITERIO DA NORMALIZACAO:
 xmin = MINVAL(tclass,1) ! min dos dados de classificacao
 xmax = MAXVAL(tclass,1) ! max dos dados de classificacao
 
 CALL minmax(tr,nt,4, xmin, xmax) ! normalizacao dos dados de treinamento (em funcao dos ranges do dado de classificacao)
 CALL minmax(tclass, nclass, 4, xmin, xmax)  ! normalizacao dos dados de classificacao
 
! constru��o do tabuteiro - configura��o inicial rand�mica
 res1=minval(tr,dim=1)
 res2=maxval(tr,dim=1)

 c1min=res1(1)   !2.05d0
 c1max=res2(1)   !3.66d0

 c2min=res1(2)   !5.11d-1
 c2max=res2(2)   !8.38d0

 c3min=res1(3)   !4.12d2
 c3max=res2(3)   !5.72d8

 c4min=res1(4)   !4.61d0
 c4max=res2(4)   !5.88d0

 nta=20   !20 ! n�mero de neur�nios em cada lado do tabuleiro

! Adicionando rotina que calcula o n �timo de neuronios (Jian,2014)
! M = 5 [N]**(1/2)
!M, n neuronios
!N, n observa��es

!nta = (5*((nt)**(1/2)))  ! Adaptado de Jian(2014). Torna a rede adaptativa. 


 print*, 'numero de neuronios da rede=',nta**2
 a = 0d0 ! limpando a variavel
 do i=1,nta
   do j=1,nta
     a(i,j,1)=rand()*(c1max-c1min)+c1min
     a(i,j,2)=rand()*(c2max-c2min)+c2min
     a(i,j,3)=rand()*(c3max-c3min)+c3min
     a(i,j,4)=rand()*(c4max-c4min)+c4min
   end do
 end do

! determina��o das vizinhan�as do tabuleiro/toro
 
! vizinhan�a da aresta horizontal superior
 do i=1,nta
   v(1,i,1)=nta ! acima 
   v(1,i,2)=i 
   v(1,i,3)=1 !direito
   v(1,i,4)=i+1
   if(i+1 == nta+1) then
     v(1,i,4)=1
   end if
   v(1,i,5)=2 ! abaixo
   v(1,i,6)=i
   v(1,i,7)=1  !esquerda
   v(1,i,8)=i-1
   if(i-1 == -1) then
     v(1,i,8)=nta
   end if

! vizinhan�a da aresta horizontal inferior

   v(nta,i,1)=nta-1 ! acima 
   v(nta,i,2)=i 
   v(nta,i,3)=nta   !direito
   v(nta,i,4)=i+1
   if(i+1 == nta+1) then
     v(nta,i,4)=1
   end if	
   v(nta,i,5)=1   ! abaixo
   v(nta,i,6)=i	
   v(nta,i,7)=nta   ! esquerda
   v(nta,i,8)=i-1	
   if(i-1 == -1) then
     v(nta,i,8)=nta
   end if	

! vizinhan�a da aresta lateral esquerda

   v(i,1,1)=i-1  ! acima
   if(i-1 == 0)then
     v(i,1,1)=nta
   end if
   v(i,1,2)=1 
   v(i,1,3)=i    ! a direita
   v(i,1,4)=2
   v(i,1,5)=i+1  ! abaixo
   if(i+1 == nta+1) then
     v(i,1,5)=1
   end if
   v(i,1,6)=1	
   v(i,1,7)=i    ! a esquerda	
   v(i,1,8)=nta	

! vizinhan�a da aresta lateral direita


   v(i,nta,1)=i-1  ! acima
   if(i-1 == 0)then
     v(i,nta,1)=nta
   end if
   v(i,nta,2)=nta 
   v(i,nta,3)=i    ! a direita
   v(i,nta,4)=1
   v(i,nta,5)=i+1  ! abaixo
   if(i+1 == nta+1) then
     v(i,nta,5)=1
   end if
   v(i,nta,6)=nta	
   v(i,nta,7)=i    ! a esquerda	
   v(i,nta,8)=nta-1	
 end do ! fim do loop do numero de neuronios

! vizinhan�as no miolo
 do i=2,nta-1
  do j=2,nta-1
    v(i,j,1)=i-1 !acima 
    v(i,j,2)=j 
    v(i,j,3)=i ! a direita
    v(i,j,4)=j+1
    v(i,j,5)=i+1 ! abaixo
    v(i,j,6)=j	
    v(i,j,7)=i ! a esquerda
    v(i,j,8)=j-1
   end do
 end do
 	
!! fim da detrmina�ao das vizinhan�as
 
!  In�cio do treinamento
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1
! Cozinha do Kohonen:
k1=0.5d0 ! escolhidas ao acaso
k2=0.5d0

n_rep= 10 !10000  !!!!!!!!!!!!!!!!!!!!!!!!!%%%%%%%%%%%%%%%%$$$$$$$$$$$$$$$$$$$ 

 do ih=1,n_rep       !tempo    !!   Loopp 2

   ! taxa de aprendizado variando com o numero de iteracoes:
   k1=1d0*(1d0-dfloat(ih)/dfloat(n_rep+1))
   k2=k1/1.1d0

   !print*, 'k1=',k1

   do ig=1,nt  !144  ! dados de treinamento   !!  Loop1
    ! busca pelo neuronio vitorioso
     menor=1.d20  !deve ser um n�mero grande
     ij=1
     do i=1,nta ! numero de neuronios em x
       do j=1,nta ! e em y

        ! neuronios:
  	a1=a(i,j,1)
  	a2=a(i,j,2)
  	a3=a(i,j,3)
  	a4=a(i,j,4)
	! dados de treinamento:
  	b1=tr(ig,1)
  	b2=tr(ig,2)
  	b3=tr(ig,3)
  	b4=tr(ig,4)

  	call dist(a1,a2,a3,a4,b1,b2,b3,b4,d)

	! localiza��o da menor distancia entre os neuronios e o dado de treinamento:      
  	if(d.LT.menor) then
    	  menor=d
    	  imenor=i
    	  jmenor=j
    	  ijmenor=ij
  	end if
        ij=ij+1
       end do
    end do

!print*, 'menor',menor
!print*, 'indices do menor',imenor,jmenor,ijmenor

    ! atualiza��o do neuronio vitorioso
    a(imenor,jmenor,1)=a(imenor,jmenor,1)+k1*(tr(ig,1)-a(imenor,jmenor,1))
    a(imenor,jmenor,2)=a(imenor,jmenor,2)+k1*(tr(ig,2)-a(imenor,jmenor,2))
    a(imenor,jmenor,3)=a(imenor,jmenor,3)+k1*(tr(ig,3)-a(imenor,jmenor,3))
    a(imenor,jmenor,4)=a(imenor,jmenor,4)+k1*(tr(ig,4)-a(imenor,jmenor,4))

    a(imenor,jmenor,9)=cl(ig)  ! classe do neuronio vencedor
    a(imenor,jmenor,10)=1d0    ! neuronio visitado

    !atualiza��o das vizinhancas

    ! vizinhan�a acima
    il=v(imenor,jmenor,1)
    ic=v(imenor,jmenor,2)
    !print*, 'il=',il
    !print*, 'ic=',ic
    
    !if(il-1 == 0)then
    !  il=9
    !end if

    a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
    a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
    a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
    a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))

    a(il,ic,9)=cl(ig)  ! ????

    ! vizinhan�a a direita
    il=v(imenor,jmenor,3)
    ic=v(imenor,jmenor,4)
    !print*, 'il=',il
    !print*, 'ic=',ic

    !if(ic == 10)then
    !  ic=1
    !end if

    a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
    a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
    a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
    a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))

    a(il,ic,9)=cl(ig)  ! eh o codigo da rocha aqui!
!!!!!!!!!!!!!!!!!!!!!!!!!!!

    ! vizinhan�a abaixo
    il=v(imenor,jmenor,5)
    ic=v(imenor,jmenor,6)
    !print*, 'il=',il
    !print*, 'ic=',ic

     !if(il-1 == 9)then
     !  il=1
     !end if

     a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
     a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
     a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
     a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))

     a(il,ic,9)=cl(ig)  ! ????

     ! vizinhan�a a esquerda
     il=v(imenor,jmenor,7)
     ic=v(imenor,jmenor,8)
     !print*, 'il=',il
     !print*, 'ic=',ic

     !if(ic == -1)then
     !  ic=9
     !end if

     a(il,ic,1)=a(il,ic,1)+k2*(tr(ig,1)-a(il,ic,1))
     a(il,ic,2)=a(il,ic,2)+k2*(tr(ig,2)-a(il,ic,2))
     a(il,ic,3)=a(il,ic,3)+k2*(tr(ig,3)-a(il,ic,3))
     a(il,ic,4)=a(il,ic,4)+k2*(tr(ig,4)-a(il,ic,4))

     a(il,ic,9)=cl(ig)  ! ????
     
  end do   ! loop do ig (dados de treinamento)
  
! Usando a rede para construir o arquivo com a coverg�ncia
! do treinamento da rede 

 somacon=0d0
 do irr=1,nt
   ind=irr
   menor=1.d20  !deve ser um n�mero grande
   ij=1
   do i=1,nta
     do j=1,nta
       ! neuronios treinados
       a1=a(i,j,1)
       a2=a(i,j,2)
       a3=a(i,j,3)
       a4=a(i,j,4)
       ! 
       b1=tr(ind,1)
       b2=tr(ind,2)
       b3=tr(ind,3)
       b4=tr(ind,4)

       call dist(a1,a2,a3,a4,b1,b2,b3,b4,d)

       if(d.LT.menor) then
         menor=d
         imenor=i
         jmenor=j
         ijmenor=ij
       end if
       ij=ij+1
     end do
   end do
   ! verificando o numero de erros associados ao codigo da rocha:
   if(a(imenor,jmenor,9).ne.cl(ind)) then
     somacon=somacon+1d0
   end if
 end do

 write(7,*)ih,somacon
 write(6,*)'iteracao=', ih
 
 end do   !loop do ih  (repeti��es do treinamento)

 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! final do loop de treinamento

! contagem dos neur�nios vitoriosos
 soma=0d0
 do i=1,nta
   do j=1,nta
     soma=soma+a(i,j,10)
   end do
 end do
 print*, 'neur�nios vitoriosos=', soma

! contagem dos neur�nios sem uso
 soma=0d0
 do i=1,nta
   do j=1,nta
     if(a(i,j,10).eq. 0d0)then
       soma=soma+1
     end if
   end do
 end do
 print*, 'neur�nios sem uso =', soma

!!@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2

! mapeamento dos neuronios vitoriosos
 cn=10  ! o elemento a(i,j,10) vale 1 se o neuronio for vitorioso
 do i=1,nta
   write (3,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
 end do

!!!!!!!!!!!!!!!!!!!!!!!!!

! mapeamento das classes dos neuronios vitoriosos
 cn=9 ! classe do vitorioso 
 do i=1,nta
   write (4,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
 end do

!!!!!!!!!!!!!!!!!!!!!!!!

! mapeamento dos valores das propriedades dos neuronios vitoriosos
 cn=1 !   classe do vitorioso Pode variar de 1 at� 4
 do i=1,nta
   write (5,'(*(ES12.4E3,2x))') (a(i,j,cn),j=1,nta)
 end do


!!!!!!!!!!!!!!!!!! final do treinamento !!!!!!!!!!!!!!!!!!!!!!

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!$$$$$$$$$$$$$$$$ ETAPA DE CLASSIFICA��O $$$$$$$$$$$$$$$$$$$$$$$!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


!!!!!!!!!!!!!!!!    Usando a rede   fluxograma 3

  
 ierro=0
 do irr=1,nclass
   ind=irr
   menor=1.d20  !deve ser um n�mero grande
   ij=1
   do i=1,nta
     do j=1,nta
       ! neuronios treinados:
       a1=a(i,j,1)
       a2=a(i,j,2)
       a3=a(i,j,3)
       a4=a(i,j,4)
       ! dados de classificacao: 
       b1=tclass(ind,1)
       b2=tclass(ind,2)
       b3=tclass(ind,3)
       b4=tclass(ind,4)

       call dist(a1,a2,a3,a4,b1,b2,b3,b4,d)

       if(d.LT.menor) then
         menor=d
         imenor=i
         jmenor=j
         ijmenor=ij
       end if
       ij=ij+1
     end do
   end do
 ! localizando o tipo de rocha:
 xxclasse=a(imenor,jmenor,9)
 print*, ind,'classe=',xxclasse,'=',cld(ind)

 If(xxclasse .eq. cld(ind)) then
   tic="certo"
 else
   ierro=ierro+1
   tic="errado"
 end if

 write(8,*) ind,'classe=',xxclasse,'=',cld(ind),' --',tic

! if(a(imenor,jmenor,9).ne.cl(ind)) then
   !!print*, ind,'erro'
!end if

 end do

print*,'numero de erros=',ierro,'  ',100d0*ierro/nclass,'%'

CALL CPU_TIME(fina)

print*,'tempo de m�quina=',fina-init,'segundos'

11 format(10(ES12.4E3,2x))
12 format(I3,2x,3(f6.2,2x))
13 format(4(ES12.4E3,2x))
14 format(4(ES9.2E2,2x))
15 format(A71)
16 format(A11,8(ES9.2E3))
17 format(A30,2x,ES12.4E3)
18 format(2(f6.2,2x),2x,A11,2x,ES12.4E3)


 print*,' ************ FIM *************'
 print*,''

 stop
 end

! ccccccccccccccccc
! ccccccccccccccccc

! ccccccccccccccccccccccccccccccccccccccccc

subroutine dist(a1,a2,a3,a4,b1,b2,b3,b4,d)
 real*8 a1,a2,a3,a4,b1,b2,b3,b4,d
 d=dsqrt((a1-b1)**2+(a2-b2)**2+(a3-b3)**2+(a4-b4)**2)

 return
end
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
 SUBROUTINE minmax(x, nx, ny, a, b) ! normalizacao dos perfis a partir do metodo min max scaling (igual ao do calculdo do IGR)
 ! inputs:
 INTEGER*4, INTENT(IN):: nx,ny ! dimensoes 
 REAL*8, INTENT(INOUT), DIMENSION(nx,ny) :: x
 REAL*8, DIMENSION( ny ):: a, b ! limites inferior e superior dos dados de classificacao.
 INTEGER*4:: i,j 

  ! loop da normalizacao para cada propriedade:
 DO i=1, nx
   DO j=1, ny
     x(i,j) = ( x(i,j) - a(j) )/ ( b(j) - a(j) )
   END DO
 END DO

 RETURN
 END SUBROUTINE minmax


 SUBROUTINE minmax_standard(x, nx, ny, mean, std) ! normalizacao dos perfis a partir do metodo standardization Z-core
 ! inputs:
 INTEGER*4, INTENT(IN):: nx,ny ! dimensoes 
 REAL*8, INTENT(INOUT), DIMENSION(nx,ny) :: x
 REAL*8, INTENT(IN), DIMENSION( ny ):: mean, std
 INTEGER*4:: i,j 

 ! loop da normalizacao:
 DO i=1,nx
   DO j=1,ny
     x(i,j) = ( x(i,j) - mean(j) )/ ( std(j) )
   END DO
 END DO
 
 RETURN
 END SUBROUTINE minmax_standard


!SUBROUTINE tradutor(palavra)
!INTEGER*4:: i,j
!CHARACTER(LEN=300),INTENT(INOUT):: portuguese, english


!END SUBROUTINE tradutor

