from Src import DataBaseNeo4J
from datetime import *

class Features(DataBaseNeo4J.Database):
    def __init__(self, address):
        super().__init__()
        self.address = address;

    def getAddressLifeTimeOrActivityDaysOrMaximumNumberDailyTransactions(self, getWhat):
        #Está query irá encontrar transações aonde este endereço foi output, encontrar o bloco desta transação e me retorna o timestamp do bloco
        queryOut =  "MATCH (a:address)<-[:locked]-(:output)<-[:out]-(transaction:tx) WHERE a.address='{}' OPTIONAL MATCH (transaction)-[:inc]->(block:block) return block.time".format(self.address)

        # Está query irá encontrar transações aonde este endereço foi input, encontrar o bloco desta transação e me retorna o timestamp do bloco
        queryIn = "MATCH (a:address)<-[:locked]-(:output)-[:in]->(transaction:tx) WHERE a.address='{}' OPTIONAL MATCH (transaction)-[:inc]->(block:block) return block.time".format(self.address)

        # Aqui estamos colocando o resultado após a consulta ser rodada no banco
        timeStampIn = self.query(queryIn)
        timeStampOut = self.query(queryOut)

        #Iremos criar uma lista
        timeStampResult = list()

        #Nesta lista iremos colocar o timeStamp obtido através da consulta. Para tratarmos o retorno é necessário utilizar [o que queremos]
        for timeStamp in timeStampIn:
            timeStampResult.append(timeStamp["block.time"])

        for timeStamp in timeStampOut:
            timeStampResult.append(timeStamp["block.time"])

        #Iremos retorna a diferença do maior com o menor, assim teremos a do último dia com a do primeiro dia
        if(getWhat == "AddressLifeTime"):
            # Aqui irá pegar o primeiro dia em que recebeu ou enviou bitcoin, e o último dia em que recebou ou enviou
            largestTimeStamp = max(timeStampResult)
            smallestTimeStamp = min(timeStampResult)
            return largestTimeStamp - smallestTimeStamp;

        #Caso queira dias de atividade iremos retornar o tamanho da lista, que contém todos timestamp
        elif(getWhat == "ActivityDays"):
            # Criando um dicionário para armazenar quantos dias um endereço recebeu ou pagou alguém
            daysResult = {}

            #Percorre todos os TimeStamp obtidos pela query e coloca 1 por 1 em transactionDay
            for transactionDay in timeStampResult:
                #Após colocar 1 a 1 no transaction day ele converte em data no formado "06021998"
                date = datetime.fromtimestamp(transactionDay)
                date = date.strftime('%d%m%Y')

                #Verifica se já existe esta data no dicionário, se não existir ele vai adiciona-lá. E se existir ele vai somar +1 nas transações do dia
                if not date in daysResult:
                    daysResult[date] = {
                        "numberTransactions": 1
                    }
                else:
                    daysResult[date]["numberTransactions"] += 1;

            #Irá retornar o tamanho do dicionário, ou seja, quantos dias diferentes possui no dicionário
            return len(daysResult);

        elif (getWhat == "MaximumNumberDailyTransactions"):
            # Criando um dicionário para armazenar quantos dias um endereço recebeu ou pagou alguém
            daysResult = {}
            # Percorre todos os TimeStamp obtidos pela query e coloca 1 por 1 em transactionDay
            for transactionDay in timeStampResult:
                # Após colocar 1 a 1 no transaction day ele converte em data no formado "06021998"
                date = datetime.fromtimestamp(transactionDay)
                date = date.strftime('%d%m%Y')
                # Verifica se já existe esta data no dicionário, se não existir ele vai adiciona-lá. E se existir ele vai somar +1 nas transações do dia
                if not date in daysResult:
                    daysResult[date] = {
                        "numberTransactions": 1
                    }
                else:
                    daysResult[date]["numberTransactions"] += 1;


            maxDate = max(daysResult, key=lambda day: daysResult[day]["numberTransactions"])
            maxTransaction = daysResult[maxDate]["numberTransactions"]
            # Irá retornar o tamanho do dicionário, ou seja, quantos dias diferentes possui no dicionário
            return maxTransaction;



    #The number of incoming (resp. outgoing) transactions which transfer money to (resp. from) the address.
    #• The ratio between incoming and outgoing transactions to/from the address.
    def getNumberIncomingTransactionsOrRatio(self, getWhat):
        #Declaro a minha query que irei utilizar
        #Aqui eu encontro todas transações aonde ele foi output, ou seja, recebeu dinheiro
        queryTransactionOut = "MATCH (a:address)<-[:locked]-(:output)<-[:out]-(transaction:tx) WHERE a.address='{}' return transaction.txid".format(self.address)
        queryResultOut = self.query(queryTransactionOut)

        # Declaro a minha query que irei utilizar
        # Aqui eu encontro todas transações aonde ele foi input, ou seja, pagou alguém
        queryTransactionIn = "MATCH (a:address)<-[:locked]-(:output)-[:in]->(transaction:tx) WHERE a.address='{}' return transaction.txid".format(self.address)
        queryResultIn = self.query(queryTransactionIn)

        transactionsOut = list()
        for result in queryResultOut:
            if not result['transaction.txid'] in transactionsOut:
                transactionsOut.append(result['transaction.txid'])

        transactionsIn = list()
        for result in queryResultIn:
            if not result['transaction.txid'] in transactionsIn:
                transactionsIn.append(result['transaction.txid'])

        if(getWhat == "NumberIncomingTransactions"):
            return len(transactionsOut)

        elif(getWhat == "Ratio"):
            return len(transactionsOut)/len(transactionsIn)
