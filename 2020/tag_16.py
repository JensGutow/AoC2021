import time
from collections import defaultdict


def read_puzzle(file_name):
    status = "rules"
    rules = {}
    my_ticket = []
    nearby_tickets = []
    with open(file_name) as f:
        for zeile in f:
            if zeile.startswith("\n"):continue
            if status == "rules":
                if zeile.startswith("your ticket"):
                    status = "your ticket"
                else:
                    values = zeile.split(":")
                    name = values[0]
                    rules_ = [list(map(int,rule.split("-"))) for rule in values[1].strip().split(" or ")]
                    rules[name] = rules_
            elif status == "your ticket":
                if zeile.startswith("nearby ticket"):
                   status = "nearby"
                else:
                    my_ticket = list(map(int,zeile.strip().split(",")))
            else:
                nearby_tickets.append(list(map(int,zeile.strip().split(","))))
                pass
    return rules, my_ticket, nearby_tickets


def löse1(rules, nearby_tickets):
    s = 0
    valid_tickets = []
    for ticket in nearby_tickets:
        ticket_status = True
        for nr in ticket:
            check = False
            for rule_terms in rules.values():
                for rule in rule_terms:
                    if rule[0] <= nr and nr <= rule[1]: 
                        check = True
                        break
            if not(check):
                ticket_status = False
                s+=nr
        if ticket_status:
            valid_tickets.append(ticket)    
    return s, valid_tickets


def löse2(rules, nearby_tickets, my_ticket):
    d = {}
    for i in range(len(my_ticket)):
        kandidaten_and = set(rules.keys())
        for nb_ticket in nearby_tickets:
            kandidaten = set()
            nr = nb_ticket[i]
            for rule_name, rule_items in rules.items():
                for rule_item in rule_items:
                    if rule_item[0] <= nr and nr <= rule_item[1]: 
                        check = True
                        kandidaten.add(rule_name)
                        break
            kandidaten_and = kandidaten_and.intersection(kandidaten)
        
        #reduziere kandidaten um die Namen, di in places_valid genau ein Eleemnt haben
        # print("i",i)    
        # print(kandidaten_and)
        d[i] = kandidaten_and

    # komprimiere 
    weiter = True
    while weiter:
        weiter = False
        for i in d:
            if len(d[i])==1:
                name = list(d[i])[0]
                for j in d:
                    if j != i:
                        if name in d[j]:
                            d[j].remove(name)
                            weiter = True
        if not weiter:
            break

    p = 1
    l = [i for i in d if list(d[i])[0].startswith("departure")]
    print(l)
    for i in l:
        p *= my_ticket[i]

    print(p)
    return p

rules, my_ticket,nearby_tickets = read_puzzle("tag_16.txt")
# print(rules)
# print(my_ticket)
#print(nearby_tickets)
s1, valid_tickets = löse1(rules,nearby_tickets)
print(s1)

löse2(rules,valid_tickets,my_ticket)
# print("Task 1")
# start = time.perf_counter()
# print(löse(p,2020), time.perf_counter() - start)
# print("Task 2")
# start = time.perf_counter()
# print(löse(p,30000000), time.perf_counter() - start)