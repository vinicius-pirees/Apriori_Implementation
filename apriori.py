import pandas
import itertools

def search_string(candidates):
    str = ""
    for item in candidates:
        str += "(?=.*" + item + ")"
    return str

def items_frequencies(item_set,n_transactions,df_transactions):
    d = {}
    for set_member in item_set:
        regex = search_string(set_member)
        count = df_transactions[df_transactions['col'].str.contains(regex)].shape[0]
        freq = count/n_transactions
        d[','.join(set_member)] = freq
    return d

def has_infrequent_subset(candidate, last_frequent_items):
    ##itertools.combinations(S, m) - S: Set original   m: numero de elemtnos do subset

    #problema na lista e no m
    m = len(last_frequent_items[0][0].split(",")) #Obter tamanho dos itens da lista anterior pegando o primeiro item como exemplo
    subsets = set(itertools.combinations(candidate, m))
    for each in subsets:
        each = list(each)  # change tuple into list
        if each not in last_frequent_items:
            return True
    return False


# Recebe ultima lista de items frequentes e as transacoes
# Retorna dataframe com frequencia e items
def gerar_candidatos(last_frequent_items, df_transactions):
    if len(last_frequent_items) == 0:
        all_items = []
        for i in range(df.shape[0]):
            list_items = df['col'].iloc[i].split(",")
            for item in list_items:
                item = item.strip()
                all_items.append(item)

        item_set = set(all_items)

        C1 = []

        for item in item_set:
            C1.append([item])

        return items_frequencies(C1, df_transactions.shape[0], df_transactions)
    else:
        C = []

        for frequent_item_1 in last_frequent_items:
            for frequent_item_2 in last_frequent_items:
                ##REALIZAR JOIN
                ## Comparacao entre os indices dos items frequentes (devem ser iguais) menos o ultimo indice
                first_same = first_are_same(frequent_item_1, frequent_item_2)
                if first_same:
                    # Se o ultimo item do primeiro itemset for menor que o ultimo item do segundo, entao fazemos o join
                    if frequent_item_1[-1] < frequent_item_2[-1]:
                        last_item = frequent_item_2[0].split(",")[-1]
                        candidate = ','.join(frequent_item_1) + "," + last_item
                        candidate = candidate.strip().split(',')

                        ##verificar se todos os subsets sao frequentes
                        subsets_infrequent = has_infrequent_subset(candidate, last_frequent_items)
                        if (not subsets_infrequent):
                            C.append(candidate)

        return items_frequencies(C, df_transactions.shape[0], df_transactions)

## Quando há apenas 1 elemento em cada lista, nao entra no for - retorna sempre True
def first_are_same(list1,list2):
    for i in range (len(list1) - 1):
        if list1[i] != list2[i]:
            return False
    return True

# Recebe lista de candidatos e filtra de acordo com o suporte minimo
# Retorna lista de items frequentes
def frequent_items(C,min_suporte):
    L = []
    min_suporte = 0.2
    for key, value in C.items():
        if value >= min_suporte:
            L.append([key])
    return L


def frequent_itemset(min_suporte, df_transactions):
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

    # retorna todos os items menos o ultimo (pois é uma lista vazia)
    return list_of_lists[1:-1]


data = {'col': ["apple,orange,eggs",
                "apple,eggs",
                "eggs,spoon",
                "snowflakes,orange",
                "apple,orange",
                "spoon,vitamin"]}
df = pandas.DataFrame.from_dict(data)


min_suporte = 0.2

frequent_itemset = frequent_itemset(min_suporte, df)

print(frequent_itemset)















