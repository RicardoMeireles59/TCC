/* FLASHCARDS */

const flashcards = [

    {
        pergunta: 'Como se diz "olá" em inglês?',
        resposta: 'Hello'
    },

    {
        pergunta: 'Como se diz "bom dia" em inglês?',
        resposta: 'Good Morning'
    },

    {
        pergunta: 'Como se diz "obrigado" em inglês?',
        resposta: 'Thank You'
    },

    {
        pergunta: 'Como se diz "cachorro" em inglês?',
        resposta: 'Dog'
    }

];

/* ÍNDICE */

let indiceAtual = 0;

/* CONTADORES */

let acertos = 0;

let revisoes = 0;

let erros = 0;

/* ELEMENTOS */

const perguntaCard =
    document.getElementById('pergunta-card');

const respostaCard =
    document.getElementById('resposta-card');

const flashcard =
    document.getElementById('flashcard');

/* CARREGAR CARD */

function carregarCard() {

    perguntaCard.innerText =
        flashcards[indiceAtual].pergunta;

    respostaCard.innerText =
        flashcards[indiceAtual].resposta;

    document.getElementById(
        'card-atual'
    ).innerText = indiceAtual + 1;

    document.getElementById(
        'total-cards'
    ).innerText = flashcards.length;

    flashcard.classList.remove('flip');
}

/* PRÓXIMO */

function proximoCard() {

    indiceAtual++;

    if (indiceAtual >= flashcards.length) {

        indiceAtual = 0;
    }

    carregarCard();
}

/* ANTERIOR */

function cardAnterior() {

    indiceAtual--;

    if (indiceAtual < 0) {

        indiceAtual = flashcards.length - 1;
    }

    carregarCard();
}

/* VIRAR */

function virarCard() {

    flashcard.classList.toggle('flip');
}

/* ACERTO */

function marcarAcerto() {

    acertos++;

    atualizarBarra();
}

/* REVISÃO */

function marcarRevisao() {

    revisoes++;

    atualizarBarra();
}

/* ERRO */

function marcarErro() {

    erros++;

    atualizarBarra();
}

/* ATUALIZAR */

function atualizarBarra() {

    document.getElementById(
        'total-acertos'
    ).innerText = acertos;

    document.getElementById(
        'total-revisao'
    ).innerText = revisoes;

    document.getElementById(
        'total-erros'
    ).innerText = erros;
}

/* TESTES */

function testarSistema() {

    console.log(
        'Teste de carregamento:',
        flashcards.length > 0
    );

    console.log(
        'Teste próximo card:',
        typeof proximoCard === 'function'
    );

    console.log(
        'Teste virar:',
        typeof virarCard === 'function'
    );

    console.log(
        'Teste revisão:',
        typeof marcarRevisao === 'function'
    );
}

/* INICIAR */

carregarCard();

testarSistema();