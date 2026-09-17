GraphQL é uma linguagem de consulta e um ambiente de execução para APIs
Em vez de usar a arquitetura tradicional REST (onde o servidor define exatamente a
estrutura de cada resposta em múltiplos endereços), o GraphQL permite que o cliente 
(como um aplicativo para celular ou um site) peça exatamente os dados de que precisa.

Com base no código do servidor, existe uma chave `secret` que recebe um valor randômico.

```js
const secret = randomInt(0, 10 ** 5); // 1 in a 100k??
```

Além disso é definida uma query, onde a partir de um PIN fornecido, é retornado uma string:

```
schema: `type Query {
    flag(pin: Int): String
}
```

Caso o PIN seja igual ao valor `secret`, é retornada a flag, que era armazenada, originalmente
em uma variável de ambiente:

```js
Query: {
    flag: (_, { pin }) => {
        if (pin != secret) {
            return 'Wrong!';
        }
        return process.env.FLAG || 'corctf{test}';
    }
}
```


Para resolvermos o desafio precisamos testar todos os valores possíveis para a chave `secret`
e verificar para qual PIN a flag é retornada. As tentativas serão automatizadas utilizando
requests com o Python. No `web.js`, observa-se que para cada POST feito são enviados ao usuário
valores corretos se forem enviadas menos de 10 requests em 1 minuto. Com mais requests sendo enviadas
o texto "no u" é recebido pelo usuário:
```js
setInterval(() => requests = 10, 60000);
...
...
app.post('/', async (req, res) => {
    if (requests <= 0) {
        return res.send('no u')
    }
    requests --;
    return res.graphql(req.body);
});
```

Assim devemos realizar 100000 tentativas de pin em no máximo 10 requests.

Isso é possível utilizando aliases. Com eles é possível fazer a query de múltiplos campos idênticos
(nesse caso, o campo flag):

```js
{
    f1:flag(pin: 1234)
    f2:flag(pin: 1235)
    f3:flag(pin: 1236)
}
```

Podemos tentar criar 100000 aliases para procurar a chave, porém como o payload
é grande demais, recebemos o código 413 (Content Too Large).

Dividido igualmente 10000 aliases nas 10 requisições (max), conseguimos encontrar a flag.
Assim basta interpretar a resposta recebida com o JSON e buscar em qual dos campos há a string
"corctf" e conseguimos recuperar a FLAG. No CTF ao vivo a flag era "corctf{STONKS}", 
mas como estamos rodando os arquivos offline, recebemos a flag "corctf{test}".
