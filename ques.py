# Write your code here
exchanges = dict()
ans = []
for query in inputs:
    q = query.split()
    print(q)
    if q[0] == 'ADD':
        new_p = q[1]
        new_e = q[2]
        if new_e not in exchanges.keys():
            prods = dict()
            prods[new_p] = [1, 0]
            [new_e] = prods
        else:
            if new_p not in exchanges[new_e].keys():
                id = len(exchanges[new_e].keys())
                exchanges[new_e][new_p] = [id + 1, 0]
        ans.append(exchanges[new_e][new_p][0])
        print(exchanges[new_e][new_p][0])
    elif q[0] == 'QUERY':
        ex = q[1]
        max_prod = -1
        prod = None
        if ex not in exchanges.keys():
            print("")
            break
        l = exchanges[ex]
        for key in l:
            if l[key][1] > max_prod:
                max_prod = l[key][1]
                prod = key
            elif l[key][1] == max_prod:
                if prod is not None and prod > key:
                    prod = key
        ans.append(prod)
        print(prod)

    else:
        trades = q[3]
        pid = q[2]
        ex = q[1]
        if ex in exchanges.keys():
            fe = exchanges[ex]
        else:
            print("")
        finalTrades = 0
        for pair in fe.values():
            if pair[0] == pid:
                pair[1] += trades
                finalTrades = pair[1]
                break
        print(finalTrades)
return ans