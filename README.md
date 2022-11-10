# django-github-actions-aws
Demonstrates how to set up a CI/CD Pipeline with GitHub Actions and AWS in a Django project

[Tutorial Here :)](https://www.freecodecamp.org/news/how-to-setup-a-ci-cd-pipeline-with-github-actions-and-aws/)

## Como configurar um pipeline de CI/CD com GitHub Actions e AWS Elastic Beanstalk

Integração Contínua – Como executar compilações e testes automaticamente
Nesta seção, veremos como podemos configurar o GitHub Actions para executar automaticamente compilações e testes em solicitações push ou pull para a ramificação principal de um repositório.

### Pré-requisitos
Um projeto Django configurado localmente com pelo menos uma visualização que retorna alguma resposta definida.
Um caso de teste escrito para as visualizações que você definiu.
Eu criei um projeto de demonstração do Django que você pode pegar neste repositório :

git clone https://github.com/Nyior/django-github-actions-aws

Após baixar o código, crie um virtualenv e instale os requisitos via pip:

pip install -r requirements.txt

Nota: O projeto já possui todos os arquivos que iremos adicionando de forma incremental à medida que avançamos. Talvez você ainda possa fazer o download e tentar entender o conteúdo dos arquivos à medida que avançamos. O projeto certamente não é interessante. Ele é criado apenas para fins de demonstração.

### configurar uma conta da AWS

[Tutorial Here Create Account AWS :)](https://aws.amazon.com/pt/getting-started/guides/setup-environment/module-one/)

### Agora que você tem um projeto Django configurado localmente, vamos configurar o GitHub Actions.

Como configurar ações do GitHub
Ok, então temos nossa configuração do projeto. Também temos um caso de teste escrito para a visão que definimos, mas o mais importante é que enviamos nossa mudança brilhante para o GitHub.

O objetivo é fazer com que o GitHub acione uma compilação e execute nossos testes toda vez que enviarmos ou abrirmos uma solicitação pull em main/master. Acabamos de enviar nossa alteração para main, mas o GitHub Actions não acionou a compilação nem executou nossos testes.

Por que não? Porque ainda não definimos um fluxo de trabalho. Lembre-se, um fluxo de trabalho é onde especificamos os trabalhos que queremos que o GitHub Actions execute.

Na verdade, Nyior, como você sabia que nenhuma compilação foi acionada e, por extensão, nenhum fluxo de trabalho definido? Todo repositório do GitHub tem uma Actionguia. Se você navegar até essa guia, saberá se um repositório tem um fluxo de trabalho definido ou não.

O primeiro repositório na primeira imagem tem um fluxo de trabalho definido chamado 'Lint and Test'. O segundo repositório na segunda imagem não tem fluxo de trabalho - é por isso que você não vê uma lista com o título 'Todos os fluxos de trabalho', como é o caso do primeiro repositório.

Ah ok, agora entendi. Então, como defino um fluxo de trabalho no meu repositório?

Crie uma pasta nomeada .githubna raiz do diretório do seu projeto.
Crie uma pasta nomeada workflowsno .githubdiretório: é aqui que você criará todos os seus arquivos YAML.
Vamos criar nosso primeiro fluxo de trabalho que conterá nossos trabalhos de compilação e teste. Fazemos isso criando um arquivo com uma .ymlextensão. Vamos nomear este arquivo build_and_test.yml
Adicione o conteúdo abaixo no yaml arquivo que você acabou de criar:

```
name: Build and Test

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2
    - name: Set up Python Environment
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run Tests
      run: |
        python manage.py test
```

Vamos entender cada linha no arquivo acima.

name: Build and TestEste é o nome do nosso fluxo de trabalho. Ao navegar para a guia de ações, cada fluxo de trabalho que você definir será identificado pelo nome que você der aqui nessa lista.
**on:É aqui que você especifica os eventos que devem acionar a execução do nosso fluxo de trabalho. Em nosso arquivo de configuração passamos dois eventos. Especificamos a ramificação principal como a ramificação de destino.

**jobs**:Lembre-se, um fluxo de trabalho é apenas uma coleção de trabalhos.

**test**:Este é o nome do trabalho que definimos neste fluxo de trabalho. Você poderia nomeá-lo qualquer coisa realmente. Observe que é o único trabalho e o trabalho de construção não está lá? Bem, é código Python, portanto, nenhuma etapa de compilação é necessária. É por isso que não definimos o trabalho de construção.

**runs-on** O GitHub fornece executores Ubuntu Linux, Microsoft Windows e macOS para executar seus fluxos de trabalho. Aqui você especifica o tipo de corredor que deseja usar. No nosso caso, estamos usando o runner Ubuntu Linux.

Uma tarefa é composta por uma série de tarefas   steps  que geralmente são executadas sequencialmente no mesmo executor. Em nosso arquivo acima, cada etapa é marcada por um hífen. **-name** representa o nome da etapa. Cada etapa pode ser um script de shell que está sendo executado ou um arquivo action. Você define uma etapa com usesse estiver executando um action ou define uma etapa com runse estiver executando um script de shell.
Agora que você definiu um workflow adicionando o arquivo de configuração na pasta designada, você pode confirmar e enviar sua alteração para seu repositório remoto.

Se você navegar até a Actionsguia do seu repositório remoto, deverá ver um fluxo de trabalho com o nome Build and Test (o nome que demos a ele) listado lá.

Parte 3: Entrega contínua – Como implantar automaticamente nosso código na AWS
Nesta seção, veremos como podemos fazer com que o GitHub Actions implante automaticamente nosso código na AWS em uma solicitação push ou pull para o branch principal. A AWS oferece uma ampla gama de serviços. Para este tutorial, usaremos um serviço de computação chamado Elastic Beanstalk.

### configurar seu ambiente Elastic Beanstalk
Depois de fazer login em sua conta da AWS, siga as etapas a seguir para configurar seu ambiente Elastic Beanstalk.

Primeiro, procure por "Elastic Beanstalk" no campo de pesquisa, conforme mostrado na imagem abaixo. Em seguida, clique no serviço Elastic Beanstalk.

Depois de clicar no serviço Elastic Beanstalk na etapa anterior, você será direcionado para a página mostrada na imagem abaixo. Nessa página, clique no prompt "Criar um novo ambiente". Certifique-se de selecionar "ambiente de servidor Web" na próxima etapa.

Após selecionar o "ambiente do servidor Web" na página anterior, você será levado para a página mostrada nas imagens abaixo.

Nessa página, envie um nome de aplicativo, um nome de ambiente e também selecione uma plataforma. Para este tutorial, vamos com a plataforma Python.

Depois de enviar o formulário preenchido na etapa anterior, depois de um tempo seu aplicativo e seu ambiente associado serão criados. Você deve ver os nomes enviados exibidos na barra lateral esquerda.

Pegue o nome do aplicativo e o nome do ambiente. Vamos precisar deles nas etapas subsequentes.

Agora que temos nosso ambiente Elastic Beanstalk totalmente configurado, é hora de configurar o GitHub Actions para acionar a implantação automática na AWS na solicitação push ou pull para main.

### configurar seu projeto para o Elastic Beanstalk
Por padrão, o Elastic Beanstalk procura um arquivo chamado application.pyem nosso projeto. Ele usa esse arquivo para executar nosso aplicativo, mas não temos esse arquivo em nosso projeto. Nós? Precisamos dizer ao Elastic Beanstalk para usar o wsgi.py arquivo em nosso projeto para executar nosso aplicativo. Para isso, siga o seguinte passo:

Crie uma pasta nomeada .ebextensionsno diretório do seu projeto. Nessa pasta crie um arquivo de configuração. Você pode nomeá-lo como quiser. Eu nomeei o meu eb.config. Adicione o conteúdo abaixo ao seu arquivo de configuração:

option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: django_github_actions_aws.wsgi:application

substitua django_github_actions_aws pelo nome do seu projeto caso necessário.

Uma última coisa que você precisa fazer nesta seção é ir ao seu settings.pyarquivo e atualizar a ALLOWED_HOSTS configuração para all:

ALLOWED_HOSTS = ['*']

Observe que usar o curinga tem grandes desvantagens de segurança. Estamos usando-o aqui apenas para fins de demonstração.

Agora que terminamos de configurar nosso projeto para o Elastic Beanstalk, é hora de atualizar nosso arquivo de fluxo de trabalho.

### atualize seu arquivo de fluxo de trabalho
Existem cinco informações importantes que precisamos para concluir esta etapa: nome do aplicativo, nome do ambiente, ID da chave de acesso, chave de acesso secreta e a região do servidor (após o login, você pode pegar a região da seção mais à direita da barra de navegação ).

Como o ID da chave de acesso e a chave de acesso secreta são dados confidenciais, vamos escondê-los em algum lugar em nosso repositório e acessá-los em nosso arquivo de fluxo de trabalho.

Para fazer isso, vá para a guia de configurações do seu repositório e clique em segredos, conforme mostrado na imagem abaixo. Lá, você pode criar seus segredos como pares de valores-chave, crie ambas abaixo e insira os dados coletados na sua conta IAM na AWS

AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY

Em seguida, adicione o trabalho de implantação ao final do arquivo de fluxo de trabalho existente:

```
deploy:
    needs: [test]
    runs-on: ubuntu-latest

    steps:
    - name: Checkout source code
      uses: actions/checkout@v2

    - name: Generate deployment package
      run: zip -r deploy.zip . -x '*.git*'

    - name: Deploy to EB
      uses: einaregilsson/beanstalk-deploy@v20
      with:

      	// Remember the secrets we embedded? this is how we access them
        aws_access_key: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws_secret_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}

        // Replace the values here with your names you submitted in one of
        // The previous sections
        application_name: django-github-actions-aws
        environment_name: django-github-actions-aws

        // The version number could be anything. You can find a dynamic way
        // Of doing this.
        version_label: 12348
        region: "us-east-2"
        deployment_package: deploy.zip
```

**needs** simplesmente diz ao GitHub Actions para começar a executar o deploymenttrabalho apenas após o testtrabalho ter sido concluído com um status de aprovação.

A etapa **Deploy to EB** usa uma ação existente, **einaregilsson/beanstalk-deploy@v20**. Lembra como dissemos que actionssão alguns aplicativos reutilizáveis ​​que cuidam de algumas tarefas repetidas com frequência para nós? **einaregilsson/beanstalk-deploy@v20** é uma dessas ações.

Para reforçar o que foi dito acima, lembre-se que nossa implantação deveria seguir as seguintes etapas: **GitHub -> Amazon S3 -> Elastic Beanstalk**.

No entanto, ao longo deste tutorial, não fizemos nenhuma configuração do Amazon s3. Além disso, em nosso arquivo de fluxo de trabalho, não fizemos upload para um bucket s3 nem extraímos de um bucket s3 para nosso ambiente Elastic Beanstalk.

Normalmente, devemos fazer tudo isso, mas não fizemos aqui – porque sob o capô, a **einaregilsson/beanstalk-deploy@v20** ação faz todo o trabalho pesado para nós. Você também pode criar o seu próprio **action** que cuida de algumas tarefas repetitivas e disponibilizá-lo para outros desenvolvedores por meio do GitHub Marketplace.

Agora que você atualizou seu arquivo de fluxo de trabalho localmente, você pode confirmar e enviar essa alteração para seu controle remoto. Seus trabalhos serão executados e seu código será implantado na instância do Elastic Beanstalk que você criou. E é isso. Terminamos >>>