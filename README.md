<a href="https://developer.atlassian.com/cloud/jira/platform/rest/v3/api-group-issue-worklogs/#api-rest-api-3-worklog-list-post">Documentação Completa</a>

<p>
    Esses scripts irão, realizar a busca e transformação de dados em virtude de um modelo predefinido de dados a serem analizados. Esses scripts possuem diversos métodos, funções e modelos de ingestão e envio de dados via zip para um serviço terceiro, em tempo de execução.
</p>
<p>
    Além disso há um método paralelo para controle de reabertura de items e de log de erros em virtude de cada consulta, os erros, nesta implementação, não incrementam novos items e loga o momento da última execução do script.
</p>

<table>
    <tr>
        <td>Indice</td>
        <td>Int</td>
    </tr>
    <tr>
        <td>ID</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Chave</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Status</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Relator</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Resumo</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Categoria</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Classificação</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Tipo de Item</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Sintoma</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Resolução</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Versão do App</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Recorrente</td>
        <td>Bool</td>
    </tr>    
    <tr>
        <td>Criticidade</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>Prioridade</td>
        <td>Str</td>
    </tr>
    <tr>
        <td>SLA Cumprido(1ª Resposta)</td>
        <td>Bool</td>
    </tr>
    <tr>
        <td>SLA Cumprido(Resolução)</td>
        <td>Bool</td>
    </tr>
    <tr>
        <td>Reaberto</td>
        <td>Bool</td>
    </tr>
    <tr>
        <td>Satisfaction</td>
        <td>Bool</td>
    </tr>
    <tr>
        <td>Data Criação</td>
        <td>Datetime</td>
    </tr>
        <tr>
            <td>Data Resolução</td>
            <td>Datetime</td>
        </tr>
        <tr>
            <td>Data Alteração</td>
            <td>Datetime</td>
        </tr>
        <tr>
            <td>Tempo Gasto</td>
            <td>HH:mm:ss</td>
        </tr>
        <tr>
            <td>Tempo de Resolução</td>
            <td>HH:mm:ss</td>
        </tr>
        <tr>
            <td>Tempo 1ª Resposta</td>
            <td>HH:mm:ss</td>
        </tr>
        <tr>
            <td>Nome cliente</td>
            <td>Str</td>
        </tr>
        <tr>
            <td>Responsável</td>
            <td>Str</td>
        </tr>
        <tr>
            <td>Semana</td>
            <td>Str</td>
        </tr>
        <tr>
            <td>Dia</td>
            <td>Str</td>
        </tr>
        <tr>        
            <td>Quinzena</td>
            <td>Str</td>
        </tr>
        <tr>
            <td>Mês</td>
            <td>Str</td>
        </tr>
        <tr>
            <td>Trimestre</td>
            <td>Str</td>
        </tr>
</table>
