# Gerador de Fragmentos Timbrais

## Descrição

O Gerador de Fragmentos Timbrais é um programa que gera fragmentos musicais com o auxílio de Grafos Timbrais. O principal objetivo deste programa é possibilitar experimentos associados à aplicação de grafos em composição musical. Os parâmetros admitidos pelo programa, entretanto, permitem ao usuário|compositor controlar diversos aspectos musicais, para além da modelagem por grafos. 

## Instalação

Para instalar as dependências do projeto, execute:

```bash
pip install -r requirements.txt
```

## Uso

Para executar o sistema, utilize o comando:

```bash
python cli.py
```

### Parâmetros Admitidos (em breve)

## Estrutura do Projeto

- `app/`: Contém os módulos principais do sistema.
  - `main.py`: Módulo principal que gerencia a geração e exportação de composições.
  - `interface/`: Contém as interfaces gráficas.
    - `tkinterface.py`: Interface gráfica utilizando Tkinter.
    - `parsGUIinterface.py`: Interface gráfica abstrata.
  - `composition.py`: Módulo que define a classe `Composition` para manipulação de composições musicais.
  - `encoder.py`: Módulo que define o encoder JSON para a classe `Composition`.
  - `utils.py`: Módulo com funções utilitárias.
- `cli.py`: Script para execução do sistema via linha de comando.
- `requirements.txt`: Arquivo com as dependências do projeto.
- `setup.py`: Script de configuração para instalação do pacote.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

## Licença

Este projeto está licenciado sob a licença GNU GPLv3. Veja o arquivo `LICENSE` para mais detalhes.

## Autor

Luan Simões - [luansimoes@cos.ufrj.br](mailto:luansimoes@cos.ufrj.br)

## Nota

Esse programa foi desenvolvido como apoio para a proposta de aplicação de grafos em música apresentada em minha dissertação "Grafos Timbrais: propriedades estruturais e aplicação musical", para obtenção do grau de Mestre em Ciências em Engenharia de Sistemas e Computação, pelo PESC-COPPE (UFRJ).
