#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>

typedef struct {
    long long inicio;
    long long fim;
    double resultado;
} ThreadArgs;
void *calcularParcial(void *args) {
    
    ThreadArgs *threadArgs = (ThreadArgs *)args;
    long long inicio = threadArgs->inicio;
    long long fim = threadArgs->fim;
    double soma = 0.0;

    for (long long i = inicio; i < fim; i++) {
        double sinal = (i % 2 == 0) ? 1.0 : -1.0;
        soma += sinal / (double)(2 * i + 1);
    }

    threadArgs->resultado = soma;
    return NULL;
}

int main(int argc, char *argv[]){
    if (argc != 3){
        fprintf(stderr, "Uso: %s <numeroDeThreads> <numeroDeTermos>\n", argv[0]);
        fprintf(stderr, "Exemplo: %s 4 1000000000\n", argv[0]);
        return EXIT_FAILURE;
    }

    int N = atoi(argv[1]);
    long long numTermos = atoll(argv[2]);

    if(N <= 0 || numTermos <= 0){
        fprintf(stderr, "Erro: numeroDeThreads e numeroDeTermos devem ser positivos.\n");
        return EXIT_FAILURE;
    }

    pthread_t *threads = malloc(N * sizeof(pthread_t));
    ThreadArgs *args = malloc(N * sizeof(ThreadArgs));

    long long termosPorThread = numTermos / N;
    long long resto = numTermos % N;

    long long proximoInicio = 0;
    for(int i = 0; i < N; i++){
        args[i].inicio = proximoInicio;
        long long qtd = termosPorThread + (i < resto ? 1 : 0);
        args[i].fim = proximoInicio + qtd;
        proximoInicio = args[i].fim;

        if (pthread_create(&threads[i], NULL, calcularParcial, &args[i]) != 0) {
            fprintf(stderr, "Erro ao criar thread %d\n", i);
            return EXIT_FAILURE;
        }
    }

    for(int i = 0; i < N; i++){
        if(pthread_join(threads[i], NULL) != 0) {
            fprintf(stderr, "Erro ao esperar thread %d\n", i);
            return EXIT_FAILURE;
        }
    }

    double somaTotal = 0.0;
    for(int i = 0; i < N; i++){
        somaTotal += args[i].resultado;
    }

    double pi = somaTotal * 4.0;
    printf("Valor aproximado de pi: %.15f\n", pi);

    free(threads);
    free(args);
    return EXIT_SUCCESS;
}