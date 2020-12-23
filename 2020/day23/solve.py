import itertools


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None

    def insert_range_after(self, node_start, node_end):
        node_end.next = self.next
        self.next = node_start

    def remove_range_after(self, range_end):
        self.next = range_end.next
        range_end.next = None

    def get_values(self, n):
        acc = []
        curr = self
        for _ in range(n):
            acc.append(curr.val)
            curr = curr.next
        return acc


def build_linked_list(iterable):
    it = iter(iterable)
    head = Node(next(it))
    table = {head.val: head}

    curr = head
    for el in it:
        table[el] = curr.next = Node(el)
        curr = curr.next
    curr.next = head  # circular list
    return head, table


def step(node, table):
    picked = node.next
    node.remove_range_after(picked.next.next)

    dest = node.val - 1 if node.val - 1 != 0 else len(table)
    while dest in [picked.val, picked.next.val, picked.next.next.val]:
        dest = (dest - 1) % len(table)
        if dest == 0:
            dest = len(table)

    dest_node = table[dest]
    dest_node.insert_range_after(picked, picked.next.next)


def run(cups, table, steps):
    curr_node = cups
    for i in range(steps):
        if i % 100000 == 0:
            print(f'{i + 1}/{steps}')
        step(curr_node, table)
        curr_node = curr_node.next
    return cups


with open('input.txt', 'r') as f:
    data = list(map(int, f.read().strip()))

# part 1
lst, table = build_linked_list(data)
result = run(lst, table, 100)
one_node = table[1]
print(''.join(map(str, one_node.get_values(9)[1:])))

# part 2
new_lst, new_table = build_linked_list(itertools.chain(data, range(max(data) + 1, max(data) + 10**6 - len(data) + 1)))
result = run(new_lst, new_table, 10**7)
one_node = new_table[1]
print(one_node.next.val * one_node.next.next.val)
