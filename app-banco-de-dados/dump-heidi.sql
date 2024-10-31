INSERT INTO joaovictorCarrijo_tbusuario VALUES(
	999,
	"Margarido",
	"Margarido@calabreso.com",
	"P@ssw0rd"
);

SELECT codigo, nome, email, senha FROM Vollo_tbusuario;

DELETE FROM Vollo_tbusuario WHERE nome = "Margarido";


/* MUDANDO A ESTRUTURA - Codigo como primery key e Email Unique*/

DROP TABLE joaovictor_tbusuario; -- Apagando a tabela antigad

CREATE TABLE joaovictor_tbusuario (
	codigo INT PRIMARY KEY, -- Primary key não permite valores nulos e não deve ter valores repetidos
	nome VARCHAR(80),
	email VARCHAR(50) UNIQUE, -- Emails não podem se repetir
	senha VARCHAR(30)
);

INSERT INTO joaovictor_tbusuario VALUES(
	1,
	"joaozinho",
	"joao@fatec.com",
	"P@ssw0rd"
);

SELECT * FROM joaovictor_tbusuario;


/* MUDANDO A ESTRUTURA - Primary Key com auto_increment */

DROP TABLE joaovictor_tbusuario;

CREATE TABLE joaovictor_tbusuario (
	codigo INT PRIMARY KEY AUTO_INCREMENT, -- Auto_increment faz com que o valor da coluna seja inserido automaticamente, dessa forma não precisa especificar 
	username VARCHAR(80),								-- o valor na hora de dar um insert into
	senha VARCHAR(30)
);

INSERT INTO joaovictor_tbusuario ( username, senha) VALUES(
	"joaozinho",
	"123"
	-- Não precisa colocar mais o id do usuário, pois ele auto incrementa
);

SELECT * FROM joaovictor_tbusuario;

SELECT * FROM joaovictor_tbusuario WHERE codigo = 1;

SELECT * FROM joaovictor_tbusuario WHERE nome='joaozinho';

-- Selecionando multiplus regitros com o operador lIKE e operador coringa
SELECT * FROM joaovictor_tbusuario WHERE nome LIKE "joao%"; -- Basicamente, você está falando: selecione tudo na tabela onde o nome é mais ou menos "joao", seguido de várias letras
SELECT * FROM joaovictor_tbusuario WHERE nome LIKE "joao_";-- Agora, aqui você está faldno: selecione tudo na onde o nome é mais ou menos "joao", seguido de UMA LETRA

-- OPERADORES CORINGA:
-- % => Qualquer sequencia de caracter. Exemplo: joao paulo
-- _ => Qualquer caracter (só um). Exemplo: joaop




/*		AULA 10.10		*/

-- DELETAR registros
DELETE FROM joaovictor_tbusuario
WHERE Codigo = 4; -- Nunca se esqueça do where, ou todos os registros vão embora!


-- ATUALIZAR registros
UPDATE joaovictor_tbusuario SET nome = "João victor"
WHERE nome = "jaozin"; -- Não se esqueça do Where, se não todo mundo vai se chamar João Victor.


/* AULA 22.10 - Atividade com tabela mais complexa*/
CREATE TABLE joaovictor_tbcliente (
	codigo INT PRIMARY KEY AUTO_INCREMENT, 
	nome VARCHAR(80),								
	cpf VARCHAR(11),
	rg VARCHAR(12),
	endereco VARCHAR(100),
	bairro VARCHAR(70),
	cidade VARCHAR (50),
	cep VARCHAR(9)
);