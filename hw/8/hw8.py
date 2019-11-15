import csv
from hw7 import *
from hw6 import *
r = random.randint
seed = random.seed
from collections import defaultdict

def dominates(i, j, goals): # i and j are rows.
    z = 0.00001
    s1, s2, n = z, z, z + len(goals)
    for idx, goal in enumerate(goals):
        if isinstance(goal, Num):
            a, b = i.leaves[idx].mu, j.leaves[idx].mu
            a, b = goal.num_norm(a), goal.num_norm(b)
            s1 -= 10 ** (goal.weight * (a - b) / n)
            s2 -= 10 ** (goal.weight * (b - a) / n)
    return s1/n - s2/n  # i is better if it losses least (i.e. this number under 0)


def distance(c1, c2, goals):
    d, n, p = 0, 0, 2
    for idx, col in enumerate(goals):
        n += 1
        d0 = None
        if isinstance(col, Num):
            d0 = col.dist(c1.leaves[idx].mu, c2.leaves[idx].mu)
        else:
            d0 = col.dist(c1.leaves[idx].mode, c2.leaves[idx].mode)
        d += d0 ** p
    return d ** (1 / p) / n ** (1 / p)

def look_envy_centroid(lines):
    rp_tree = HW7(lines)
    centroids = rp_tree.leaf_nodes
    envy_nodes = defaultdict(list)
    closest_envy_nodes = []
    goals = [rp_tree.table.cols[each-1] for each in rp_tree.table.goals]
    for c1 in centroids:
        for c2 in centroids:
            if dominates(c1, c2, goals) > 0:
                envy_nodes[c1].append(c2)
    for c1 in envy_nodes.keys():
        min_dist, most_envy = float('inf'), None
        for c2 in envy_nodes[c1]:
            dist = distance(c1, c2, goals)
            if dist < min_dist:
                min_dist = dist
                most_envy = c2
        closest_envy_nodes.append((c1, most_envy))
    for idx, val in enumerate(closest_envy_nodes):
        tbl = Table()
        cols = [col.col_name for col in val[0].table.cols]
        cols.append('!$new_class')
        tbl.read_lines(idx, cols)
        for each in val[0].table.rows:
            cells = each.cells
            cells.append(0)
            # print(cells)
            tbl.read_lines(1, cells)
        for each in val[1].table.rows:
            cells = each.cells
            cells.append(1)
            # print(cells)
            tbl.read_lines(1, cells)
        try:
            result = tree(tbl)
            # print(result)
            print("TREE FOR ONE OF THE CLUSTERS and its ENVY CLUSTER")
            show(result[0])
            print("-----------------------------------------------------------")
        except:
            pass

def show(tree, level=0):
    # print(tree,'\n' , isinstance(tree, list))
    for _ in range(level):
        print("| ", end=" ")
    print("{0} = {1}...{2}".format(tree['text'], tree['low'], tree['high']), end=" ")
    if not isinstance(tree['childs'], list):
        print("{0} ({1})".format(tree['childs']['val'], tree['childs']['n']))
    else:
        for each in tree['childs']:
            print("")
            show(each, level + 1)


if __name__ == '__main__':
    hw = "auto1.csv"
    file = ""
    with open(hw, 'r') as lines:
        reader = csv.reader(lines, delimiter=' ', quotechar='|')
        for row in reader:
            file += ','.join(row)
            file += '\n'
    lines = fromString(file)
    look_envy_centroid(lines)