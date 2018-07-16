import pandas
import itertools


def search_string(candidates):
    """
    Gera uma expressão regular (regex) a partir de uma lista. a expressão é usada para procurar as ocorrencias
    simultâneas de todos os elementos da lista em uma transação

    Exemplo:
    >> search_string(['carne','frango'])
    '(?=.*carne)(?=.*frango)'

    """
    str = ""
    for item in candidates:
        str += "(?=.*" + item + ")"
    return str

def items_frequencies(item_set,n_transactions,df_transactions):
    """
    Calcula o suporte para cada item da lista de candidatos

    :param item_set: Lista de itemsets candidatos
    :param n_transactions: Número total de transções
    :param df_transactions: Dataframe com todas as transações

    :return Dicionário com os itemsets candidatos e seus respectivos suportes
    """
    d = {}
    for set_member in item_set:
        regex = search_string(set_member)
        count = df_transactions[df_transactions['col'].str.contains(regex)].shape[0]
        freq = count/n_transactions
        d[','.join(set_member)] = freq
    return d

def has_infrequent_subset(candidate, last_frequent_items):
    """
    Verifica se há algum subset do itemset candidato que não é frequente (ou seja, não está na lista anterior)

    :param candidate: itemset candidato
    :param last_frequent_items: lista anterior de itemsets frequentes
    :return: True se existe algum subset que não está na lista anterior e False caso contrário
    """


    # Obter tamanho dos itens da lista anterior pegando o primeiro item como exemplo
    m = len(last_frequent_items[0][0].split(","))
    ## Gerar todos as combinações (subsets) de tamanho m a partir do itemset cadidato
    #### itertools.combinations(S, m) - S: Set original   m: numero de elemtnos do subset
    subsets = set(itertools.combinations(candidate, m))


    for subset in subsets: ## Para cada subset
        subset = [",".join(list(subset))]  # Converter de tupla para lista
        if subset not in last_frequent_items: ## Se subset não estiver na lista anterior
            return True
    return False


def gerar_candidatos(last_frequent_items, df_transactions):
    """
    :param last_frequent_items: Lista anterior de items frequentes
    :param df_transactions: Dataframe com todas as transações

    :return: Dicionário com os itemsets candidatos e seus respectivos suportes
    """

    if len(last_frequent_items) == 0: ##Se a lista de itemsets frequentes anterior for vazia, então iniciar processo
        all_items = []
        for i in range(df_transactions.shape[0]): ## Para cada uma das transações do Dataframe
            list_items = df_transactions['col'].iloc[i].split(",") ##Gerar lista com todos os items da transação
            for item in list_items: ## Inserir todos os elementos na lista all_items
                item = item.strip()
                all_items.append(item)

        item_set = set(all_items) ##Gerar set (remover duplicados) a partir da lista all_items

        C1 = []

        ##C1 terá todos os elementos distintos das tranações
        for item in item_set:
            C1.append([item])

        ## Retornar dicionário com todos os elementos de C1 e seus respectivos suportes
        return items_frequencies(C1, df_transactions.shape[0], df_transactions)

    else: ## Se lista de itemsets anteriores não for vazia
        C = []

        ##Comparar cada elemento da lista anterior com todos os outros elementos
        for frequent_item_1 in last_frequent_items:
            for frequent_item_2 in last_frequent_items:
                ##REALIZAR JOIN
                ## Comparacao entre os indices dos items frequentes (devem ser iguais) menos o ultimo indice
                ## frequent_item_1[0].split(",") transforma frequent_item_1 de string para lista
                first_same = first_are_same(frequent_item_1[0].split(","), frequent_item_2[0].split(","))
                if first_same:
                    if frequent_item_1[-1] < frequent_item_2[-1]:  # Se o ultimo item do primeiro itemset
                                                                   # for menor que o ultimo item do segundo
                        ## Obter ultimo item do frequent_item_2
                        last_item = frequent_item_2[0].split(",")[-1]
                        ## Inserir ultimo item do frequent_item_2 ao final do frequent_item_1
                        candidate = ','.join(frequent_item_1) + "," + last_item
                        ## Remover espaços e converter de string para lista
                        candidate = candidate.strip().split(',')

                        ##verificar se há algum subset não frequente
                        subsets_infrequent = has_infrequent_subset(candidate, last_frequent_items)
                        if (not subsets_infrequent): ## Se não há
                            ## adicionar a lista de cadidatos atual
                            C.append(candidate)

        ## Retornar dicionário com todos os elementos de C e seus respectivos suportes
        return items_frequencies(C, df_transactions.shape[0], df_transactions)


def first_are_same(list1,list2):
    """
    Compara todos os elementos das duas listas, menos o ultimo
    Quando há apenas 1 elemento em cada lista, nao entra no for - retorna sempre True

    :param list1: Lista 1
    :param list2: Lista 2

    :return: True se primeiros items sao iguais, False caso contrário

    """
    for i in range (len(list1) - 1):
        if list1[i] != list2[i]:
            return False
    return True


def frequent_items(C,min_suporte):
    """
    Recebe lista de candidatos e filtra de acordo com o suporte minimo

    :param C: Dicionário com os itemsets candidatos e seus respectivos suportes
    :param min_suporte: Suporte minímo para considerar um itemset frequente

    :return: Lista de itemsets frequentes
    """
    L = []
    for key, value in C.items():
        if value >= min_suporte:
            L.append([key])
    return L


def frequent_itemset(min_suporte, df_transactions):
    """

    :param min_suporte: Suporte minímo para considerar um itemset frequente
    :param df_transactions: Dataframe com todas as transações

    :return: Lista com todos os itemsets frequentes
    """

    # Inicializando lista de listas items frequentes
    list_of_lists = [[]]

    # Obtendo primeiros candidatos
    C1 = gerar_candidatos(list_of_lists[-1], df_transactions)
    # Obtendo primeiros items frequentes (L1)
    L1 = frequent_items(C1, min_suporte)
    # Adicionando lista items frequentes a lista principal
    list_of_lists.append(L1)

    # Enquanto ultima lista de items frequentes não estiver vazia
    while (len(list_of_lists[-1]) != 0):
        # Obter lista de candidatos a partir dos item anteriores
        C = gerar_candidatos(list_of_lists[-1], df_transactions)
        L = frequent_items(C, min_suporte)
        list_of_lists.append(L)

    # retorna todos os items menos o primeiro e ultimo (pois sao listas vazias)
    return list_of_lists[1:-1]



def regras(frequent_item_set, df_transactions, min_conf):
    """
    Exibe todas as regras de associação que possuem suporte e confiança mímimas especificadas

    :param frequent_item_set: Lista de itemsets frequentes
    :param df_transactions: Dataframe com todas as transações
    :param min_conf: Confiança miníma para considerar uma regra forte

    """
    ## Para cada itemset na lista de itemsets frequentes
    for frequent_item in frequent_item_set:
        # converter itemset de string para lista
        frequent_item = frequent_item[0].split(",")
        ## Tamanho dos subsets a serem gerados
        len_subsets = len(frequent_item) - 1
        while (len_subsets != 0): ## Enquanto houver substes a serem gerados
            ##Gerar subsets (subconjuntos não vazios) de tamanho len_subsets
            subsets = set(itertools.combinations(frequent_item, len_subsets))

            ## Quantidade de ocorrencias do itemset frequente
            count_f = df_transactions[df_transactions['col'].str.contains(search_string(frequent_item))].shape[0]
            ## Total de transações
            total = df_transactions.shape[0]

            ## Suporte
            support = count_f / total

            ## Para cada subset
            for subset in subsets:
                ## Obter consequente
                consequente = set(frequent_item) - set(subset)
                ## Contar ocorrencias do subset
                count_subset = df_transactions[df_transactions['col'].str.contains(search_string(subset))].shape[0]
                ## Calcular confiança
                confidence = count_f / count_subset

                if confidence > min_conf:
                    print(list(subset), "->", list(consequente), "suporte ", support, "cofianca ", confidence)
            ## Proximo subset tera tamanho = tamanho atual - 1
            len_subsets = len_subsets - 1




def apriori(dataset, min_suporte, min_conf):

    ##Obter lista com todos os itemsets frequentes dado um suporte minímo
    frequent_item_set = frequent_itemset(min_suporte, dataset)
    print("Frequent itemset:")
    print(frequent_item_set, "\n")

    ## Removendo L1 - lista com apenas um item
    itemsets = frequent_item_set[1:]

    ## Gerar lista única de itemsets frequentes
    freq_items = []
    for itemset_list in itemsets:
        for item in itemset_list:
            freq_items.append(item)

    ##Gerar regras com confiança mínimo
    print("Regras:")
    regras(freq_items, dataset, min_conf)

if __name__ == "__main__":

    ##Teste

    data = {'col': ["carne,frango,leite",
                    "carne,frango",
                    "queijo,botas",
                    "carne,frango,queijo",
                    "carne,frango,roupas,queijo,leite",
                    "frango,roupas,leite",
                    "frango,leite,roupas"]}

    df = pandas.DataFrame.from_dict(data)

    ## min_suporte = 0.3 e min_conf = 0.8
    apriori(df, 0.3, 0.8)


